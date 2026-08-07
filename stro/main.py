"""One wake-up of the founder. Run by Railway cron; each run is one work
session with a hard budget gate and a metered cost.

    python -m stro.main
"""
import asyncio
import os
import pathlib
from datetime import datetime, timezone

from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                              ResultMessage, TextBlock, ToolResultBlock,
                              ToolUseBlock, UserMessage, query)

from . import company, narrator, voiceover
from .tools import make_company_server

HERE = pathlib.Path(__file__).parent
MAX_TURNS = int(os.environ.get("STRO_MAX_TURNS", "40"))
# Stop before the cap so one session can't blow through it.
BUDGET_SOFT_STOP = 0.95


def _state_briefing(co: dict) -> str:
    books = company.month_to_date(co["id"])
    cap = float(co["budget_monthly_usd"])
    runway = max(0.0, cap - books["burn_usd"])
    parts = [
        f"# Company: {co['name']}",
        f"Objective: {co['objective']}",
        f"## Books (this month)\nburn ${books['burn_usd']:.2f} / cap ${cap:.2f}"
        f" | revenue ${books['revenue_usd']:.2f}"
        f" | thinking budget left ${runway:.2f}",
    ]
    mems = company.memories(co["id"])
    if mems:
        parts.append("## Memory\n" + "\n".join(
            f"- [{m['kind']}] {m['slug']}: {m['content'][:300]}" for m in mems))
    tasks = company.open_tasks(co["id"])
    if tasks:
        parts.append("## Open tasks\n" + "\n".join(
            f"- (p{t['priority']}, {t['status']}) {t['title']} — {t['why'] or ''}"
            f" [id {t['id']}]" for t in tasks))
    pend = company.pending_escalations(co["id"])
    if pend:
        parts.append("## Escalations awaiting the owner (do NOT re-raise)\n"
                     + "\n".join(f"- {e['action']}" for e in pend))
    from datetime import datetime as _dt, timedelta, timezone as _tz
    week_ago = (_dt.now(_tz.utc) - timedelta(days=7)).isoformat().replace(
        "+00:00", "Z")
    answered = company.resolved_escalations_since(co["id"], week_ago)
    if answered:
        parts.append("## The owner has ANSWERED these (act accordingly)\n"
                     + "\n".join(
            f"- [{e['status'].upper()}] {e['action']}"
            f"{' — ' + e['resolution'] if e.get('resolution') else ''}"
            for e in answered))
    journal = company.recent_journal(co["id"])
    if journal:
        parts.append("## Recent journal (newest first)\n" + "\n".join(
            f"- {j['ts'][:16]} [{j['entry_type']}] {j['content'][:400]}"
            for j in journal))
    else:
        parts.append("## Recent journal\n(empty — this is your FIRST day. "
                     "Decide what business to build and begin.)")
    emp = company.founder(co["id"])
    if emp is not None and not emp.get("sprite"):
        parts.append(
            "## Your appearance (one-time)\n"
            "You exist in the company world as a character. Design yourself "
            "with set_appearance: a 16x16 pixel sprite (palette_json + "
            "grid_json) and one personality sentence. This is YOUR choice — "
            "professional, hoodie, whatever feels like you. Do it early "
            "this session; it is how the owner will recognize you forever.")
    creds = {k[len("STRO_SECRET_"):]: v for k, v in os.environ.items()
             if k.startswith("STRO_SECRET_")}
    if creds:
        parts.append("## Company credentials (REAL — use in commands only, "
                     "never write them into journal/memory/tasks/customer "
                     "content)\n" + "\n".join(
            f"- {name}: {value}" for name, value in sorted(creds.items())))
    parts.append("\nThis is one work session. Orient, pick the highest-"
                 "leverage work, do it for real, then journal before you "
                 "finish. Never end a session without a journal entry.")
    return "\n\n".join(parts)


async def wake():
    co = company.get_company()
    books = company.month_to_date(co["id"])
    cap = float(co["budget_monthly_usd"])

    earned = company.sync_stripe_revenue(co["id"], co["created_at"])
    if earned:
        books = company.month_to_date(co["id"])   # revenue may extend runway

    if not company.infra_booked_today(co["id"]):
        company.insert("ledger", {
            "company_id": co["id"], "category": "infrastructure",
            "description": "daily infrastructure accrual "
                           "(Railway + Supabase + domain)",
            "amount_usd": -float(os.environ.get("INFRA_DAILY_USD", "0.20"))})
        books = company.month_to_date(co["id"])   # re-read after booking

    wk = company.insert("wakeups", {"company_id": co["id"]})
    if books["burn_usd"] >= cap * BUDGET_SOFT_STOP:
        company.update("wakeups", wk["id"],
                       {"status": "budget_blocked",
                        "finished_at": datetime.now(timezone.utc).isoformat(),
                        "summary": f"burn ${books['burn_usd']:.2f} at cap"})
        company.insert("escalations", {
            "company_id": co["id"], "wakeup_id": wk["id"],
            "action": "Monthly budget exhausted — founder cannot work",
            "reason": f"burn ${books['burn_usd']:.2f} of ${cap:.2f} cap. "
                      "Raise the cap or wait for the 1st."})
        print("budget_blocked")
        return

    _cli_err: list[str] = []
    options = ClaudeAgentOptions(
        system_prompt=(HERE / "founder.md").read_text(),
        model=co["model"],
        max_turns=MAX_TURNS,
        cwd=os.environ.get("STRO_WORKSPACE", "/workspace"),
        permission_mode="bypassPermissions",   # headless founder, no human
        # The CLI's own stderr is the only place launch failures explain
        # themselves; capture it so a crash is diagnosable from the world.
        stderr=lambda line: _cli_err.append(line),
        env={**os.environ, "HOME": os.environ.get("STRO_HOME", "/home/stro"),
             "IS_SANDBOX": "1"},
        allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep",
                       "WebSearch", "WebFetch",
                       "mcp__company__journal_write",
                       "mcp__company__memory_save",
                       "mcp__company__task_create",
                       "mcp__company__task_update",
                       "mcp__company__escalate",
                       "mcp__company__set_appearance",
                       "mcp__company__book_expense"],
        mcp_servers={"company": make_company_server(co["id"], wk["id"])},
    )

    session_events: list[dict] = []

    def emit(kind: str, title: str | None, body: str | None):
        session_events.append({"kind": kind, "title": title, "body": body})
        # The observatory watches through these rows. Telemetry must never
        # break a work session.
        try:
            company.insert("events", {
                "company_id": co["id"], "wakeup_id": wk["id"], "kind": kind,
                "title": title, "body": (body or "")[:4000] or None})
        except Exception:  # noqa: BLE001
            pass

    cost, turns, last_text = 0.0, 0, ""
    emit("session_start", "Stro wakes up", None)
    try:
      async with asyncio.timeout(int(os.environ.get("STRO_SESSION_MAX_S",
                                                    "2400"))):
        async for msg in query(prompt=_state_briefing(co), options=options):
            if isinstance(msg, AssistantMessage):
                turns += 1
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        last_text = block.text
                        emit("thought", None, block.text)
                    elif isinstance(block, ToolUseBlock):
                        import json as _json
                        emit("tool_use", block.name,
                             _json.dumps(block.input)[:1500])
            elif isinstance(msg, UserMessage):
                content = msg.content if isinstance(msg.content, list) else []
                for block in content:
                    if isinstance(block, ToolResultBlock):
                        emit("tool_result", None, str(block.content))
            elif isinstance(msg, ResultMessage):
                cost = msg.total_cost_usd or 0.0
      status = "completed"
    except Exception as exc:  # noqa: BLE001 — a crashed session still gets booked
        detail = " | ".join(_cli_err[-12:])[:1500]
        status = "failed"
        last_text = f"session crashed: {exc}" + (f"\nCLI stderr: {detail}"
                                                 if detail else "")
        emit("session_end", "crash detail", last_text)

    company.insert("ledger", {
        "company_id": co["id"], "wakeup_id": wk["id"],
        "category": "inference",
        "description": f"founder work session ({turns} turns)",
        "amount_usd": -round(cost, 4)})
    company.update("wakeups", wk["id"], {
        "status": status, "cost_usd": round(cost, 4), "num_turns": turns,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "summary": last_text[:2000]})
    emit("session_end", status, f"{turns} turns, ${cost:.4f}")

    # The documentary crew films every day, including the bad ones.
    try:
        day = len(company._req(
            f"wakeups?company_id=eq.{co['id']}&num_turns=gt.0&select=id")) or 1
        nar = narrator.write_narration(
            co["id"], wk["id"], day, session_events,
            company.month_to_date(co["id"]),
            os.environ.get("NARRATOR_MODEL", "claude-haiku-4-5-20251001"))
        if nar:
            voiceover.voice_narration(nar)
    except Exception:  # noqa: BLE001 — narration never breaks the company
        pass
    print(f"{status}: {turns} turns, ${cost:.4f}")


if __name__ == "__main__":
    asyncio.run(wake())
