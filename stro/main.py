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
# A session is bounded by MONEY, not turns. Turns are a crude proxy: a
# frugal turn and a wasteful one cost wildly different amounts, and capping
# turns punishes efficiency instead of rewarding it. The turn ceiling stays
# only as a runaway backstop, set high.
SESSION_BUDGET_USD = float(os.environ.get("STRO_SESSION_BUDGET_USD", "0.55"))
MAX_TURNS = int(os.environ.get("STRO_MAX_TURNS", "150"))
EFFORT = os.environ.get("STRO_EFFORT", "medium")
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
    mems = company.memories(co["id"])[:25]
    if mems:
        parts.append("## Memory\n" + "\n".join(
            f"- [{m['kind']}] {m['slug']}: {m['content'][:220]}" for m in mems))
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
    journal = company.recent_journal(co["id"], limit=12)
    if journal:
        parts.append("## Recent journal (newest first)\n" + "\n".join(
            f"- {j['ts'][:16]} [{j['entry_type']}] {j['content'][:280]}"
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
    parts.append(
        f"\nThis session is bounded by MONEY, not time: about "
        f"${SESSION_BUDGET_USD:.2f} of thinking. Every turn you take re-reads "
        "everything before it, so a noisy command early costs you on every "
        "turn after it — silence is literally cheaper. Keep tool output "
        "small (pipe to `head`/`tail`, use `--quiet`, `-q`, `2>/dev/null`, "
        "never print progress bars or whole files you do not need). Pick ONE "
        "thing worth finishing rather than starting five, and leave room to "
        "write the day down. Efficiency buys you more work, not less.")
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
        max_budget_usd=SESSION_BUDGET_USD,
        effort=EFFORT,
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
    usage_note: list[str] = []
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
                u = msg.usage or {}
                if isinstance(u, dict) and u:
                    usage_note.append(
                        "tokens in={} out={} cache_read={} cache_write={}".format(
                            u.get("input_tokens", 0), u.get("output_tokens", 0),
                            u.get("cache_read_input_tokens", 0),
                            u.get("cache_creation_input_tokens", 0)))
      status = "completed"
    except Exception as exc:  # noqa: BLE001 — a crashed session still gets booked
        detail = " | ".join(_cli_err[-12:])[:1500]
        status = "failed"
        last_text = f"session crashed: {exc}" + (f"\nCLI stderr: {detail}"
                                                 if detail else "")
        emit("session_end", "crash detail", last_text)

    # If the session ended without him writing anything down — ran out of
    # turns mid-thought, timed out, crashed — give him a short, focused last
    # call whose only job is to remember the day. Losing the work is bad;
    # losing the MEMORY of the work is what actually compounds.
    wrote = company._req(f"journal?wakeup_id=eq.{wk['id']}&select=id&limit=1")
    if not wrote and turns > 0:
        emit("thought", None, "Out of time — writing the day down.")
        did = [f"{e['title'] or e['kind']}: {(e['body'] or '')[:120]}"
               for e in session_events if e["kind"] == "tool_use"][-25:]
        recap = (
            f"Your work session just ended ({status}) after {turns} turns.\n\n"
            "WHAT YOU DID THIS SESSION, in order:\n- " + "\n- ".join(did) +
            "\n\nYou have a handful of turns left and exactly one job: "
            "record this day so tomorrow's you inherits it. Call "
            "journal_write with what you did, what you decided and WHY, and "
            "what failed. Update or create tasks so the next session knows "
            "where to resume. Do not start new work.")
        try:
            wrap_opts = ClaudeAgentOptions(
                system_prompt=(HERE / "founder.md").read_text(),
                model=co["model"], max_turns=8,
                cwd=os.environ.get("STRO_WORKSPACE", "/workspace"),
                permission_mode="bypassPermissions",
                stderr=lambda line: _cli_err.append(line),
                env={**os.environ,
                     "HOME": os.environ.get("STRO_HOME", "/home/stro"),
                     "IS_SANDBOX": "1"},
                allowed_tools=["mcp__company__journal_write",
                               "mcp__company__memory_save",
                               "mcp__company__task_create",
                               "mcp__company__task_update"],
                mcp_servers={"company": make_company_server(co["id"], wk["id"])},
            )
            async with asyncio.timeout(420):
                async for msg in query(prompt=recap, options=wrap_opts):
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, ToolUseBlock):
                                import json as _j
                                emit("tool_use", block.name,
                                     _j.dumps(block.input)[:1500])
                    elif isinstance(msg, ResultMessage):
                        cost += msg.total_cost_usd or 0.0
        except Exception:  # noqa: BLE001 — best effort; never fatal
            pass

    company.insert("ledger", {
        "company_id": co["id"], "wakeup_id": wk["id"],
        "category": "inference",
        "description": f"founder work session ({turns} turns)",
        "amount_usd": -round(cost, 4)})
    company.update("wakeups", wk["id"], {
        "status": status, "cost_usd": round(cost, 4), "num_turns": turns,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "summary": (last_text[:1800] + ("\n\n" + usage_note[-1]
                                        if usage_note else ""))[:2000]})
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
