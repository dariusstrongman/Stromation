"""One wake-up of the founder. Run by Railway cron; each run is one work
session with a hard budget gate and a metered cost.

    python -m stro.main
"""
import asyncio
import os
import pathlib
from datetime import datetime, timezone

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    query,
)

from . import company, narrator, staff, voiceover
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


def _measured_per_turn(co: dict, mode: str,
                       model: str | None = None) -> float:
    """Cost per turn from recent sessions of the SAME shape.

    Ticks run on Haiku and outnumber focus blocks massively, so pooling
    them makes a focus briefing quote tick economics and wildly overstate
    how many turns it can afford — the exact miscalibration this exists to
    prevent.
    """
    rows = company._req(
        f"wakeups?company_id=eq.{co['id']}&mode=eq.{mode}&num_turns=gt.3"
        "&select=num_turns,cost_usd&order=started_at.desc&limit=5")
    tot_c = sum(float(w["cost_usd"] or 0) for w in rows)
    tot_t = sum(w["num_turns"] for w in rows) or 0
    if tot_c > 0 and tot_t:
        return max(0.002, tot_c / tot_t)
    # The model that will RUN this session, which for a tick is the tick
    # model, not the company's. Quoting Sonnet's rate to a Haiku check-in
    # understates its affordable turns threefold.
    defaults = {"claude-opus-5": 0.09, "claude-sonnet-5": 0.018,
                "claude-haiku-4-5-20251001": 0.006}
    return defaults.get(model or co.get("model") or "", 0.018)


def _tick_briefing(co: dict, budget: float, reasons: list[str] | None,
                   per_turn: float) -> str:
    """The cheap path. A check-in ships ~3k tokens, not ~32k: no
    credentials, no roster, no memory, no books. Prompt size is the
    dominant cost of a tick, so this is what makes an hourly heartbeat
    affordable."""
    ws = os.environ.get("STRO_WORKSPACE", "/workspace")
    parts = [f"# {co['name']} — check-in",
             f"You are the founder. Objective: {co['objective']}"]
    if reasons:
        parts.append("## Why you are awake\n- " + "\n- ".join(reasons))
    tasks = company.open_tasks(co["id"])[:6]
    if tasks:
        parts.append("## Open tasks\n" + "\n".join(
            f"- (p{t['priority']}) {t['title'][:110]} [id {t['id']}]"
            for t in tasks))
    jr = company.recent_journal(co["id"], limit=3)
    if jr:
        parts.append("## Last entries\n" + "\n".join(
            f"- {j['content'][:160]}" for j in jr))
    parts.append(
        f"## Workspace\n{ws} — persists between sessions; your work is there.")
    parts.append(
        "## Watched for you, free\nPaid orders, company email, staff reports "
        "and owner answers are polled automatically every minute. Never "
        "spend a turn checking them — if something had arrived it would be "
        "listed above.")
    parts.append(
        f"\nThis is a CHECK-IN: about {max(3, int(budget / per_turn))} turns. "
        "Do the smallest useful thing and stop — answer, ship, fix, or note "
        "it as a task. Do NOT start building; that is your focus block. "
        "Journal one line before you finish. Keep tool output tiny.")
    return "\n\n".join(parts)


def _state_briefing(co: dict, mode: str = "focus",
                    budget: float | None = None,
                    reasons: list[str] | None = None,
                    session_model: str | None = None) -> str:
    budget = budget if budget is not None else SESSION_BUDGET_USD
    if mode == "tick":
        return _tick_briefing(co, budget, reasons,
                              _measured_per_turn(co, "tick", session_model))
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
    from datetime import datetime as _dt
    from datetime import timedelta
    from datetime import timezone as _tz
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
    per_turn = _measured_per_turn(co, mode, co.get("model"))

    team = staff.active_staff(co["id"])
    pay = staff.payroll(co["id"])
    # What HIS OWN thinking costs, next to what everyone else costs. This
    # is the comparison that makes delegation a real decision rather than a
    # feature he never touches.
    parts.append(
        f"## What thinking costs\n"
        f"You are running on **{co['model']}** at roughly "
        f"${per_turn:.4f} per turn of your own thought. You can change that "
        "with set_my_model — a better brain costs more per turn, a cheaper "
        "one buys more days of runway.\n"
        "Everyone you could hire, and what they cost:\n"
        + staff.roster_text()
        + "\n\nNote the asymmetry: an advisor answering a research question "
          "typically costs a fraction of a cent — often 20-50x less than "
          "working it out yourself turn by turn. If a question is research "
          "rather than judgment, delegating it is almost always the cheaper "
          "answer.")
    if team:
        parts.append("## Your staff (their salary is real, from your runway)\n"
                     + "\n".join(
            f"- {e['name']} — {e['role']} ({e['model']}), "
            f"${pay.get(e['id'], 0):.2f} this month"
            for e in team))
    else:
        parts.append(
            "## Staff\nYou work alone. Hire when a function is genuinely "
            "eating your time — an employee's model IS their salary, paid "
            "from the same runway you live on.")
    from datetime import datetime as _dt2
    from datetime import timedelta as _td2
    from datetime import timezone as _tz2
    since = (_dt2.now(_tz2.utc) - _td2(days=3)).isoformat().replace(
        "+00:00", "Z")
    reports = staff.completed_since(co["id"], since)
    if reports:
        by_id = {e["id"]: e["name"] for e in
                 company._req(f"employees?company_id=eq.{co['id']}&select=id,name")}
        parts.append("## Reports back from your staff\n" + "\n".join(
            f"- {by_id.get(r['employee_id'], '?')} on '{r['task'][:60]}' "
            f"[{r['status']}, ${float(r['cost_usd'] or 0):.2f}]: "
            f"{(r['result'] or '')[:400]}" for r in reports))

    creds = {k[len("STRO_SECRET_"):]: v for k, v in os.environ.items()
             if k.startswith("STRO_SECRET_")}
    if creds:
        parts.append("## Company credentials (REAL — use in commands only, "
                     "never write them into journal/memory/tasks/customer "
                     "content)\n" + "\n".join(
            f"- {name}: {value}" for name, value in sorted(creds.items())))
    ws = os.environ.get("STRO_WORKSPACE", "/workspace")
    parts.append(
        f"## Your workspace: {ws}\n"
        "This disk PERSISTS between sessions. Whatever you built last time is "
        "still there — look before you rebuild. Keep your work in project "
        "folders, commit to git as you go, and leave notes for your future "
        "self. Anything you want to survive lives here or in memory; nothing "
        "else does.")
    # Report the budget as WORK, not as a dollar figure: a small-looking
    # number made him quit at 35% usage having done almost nothing. What
    # matters is how many turns it buys, and that unspent budget is wasted.
    affordable = max(3, int(budget / per_turn))
    parts.append(
        "## What is watched for you, free, every minute\n"
        "Paid orders, company email, staff reports and owner answers are "
        "polled automatically at zero cost, and you are woken when any of "
        "them changes. NEVER spend a turn checking whether an order or an "
        "email has arrived — if one had, it would say so below. Polling an "
        "empty inbox is the most expensive way to do nothing.")
    if reasons:
        parts.append("## Why you are awake right now\n- "
                     + "\n- ".join(reasons))
    if mode == "tick":
        parts.append(
            f"\n## This is a CHECK-IN, not a work session (~{affordable} "
            "turns)\nSomething above needed attention. Handle the smallest "
            "useful piece of it and stop — answer the customer, ship the "
            "order, note what you found, tick a task off. Do NOT start "
            "building anything; that is what your focus block is for. If "
            "what you found needs real work, write it down as a task and "
            "leave it. Being brief here is what keeps you alive all day.")
        return "\n\n".join(parts)
    if mode == "focus":
        focus_note = (
            "## This is your focus block — the day's real work\n"
            "Do not spend it on verification, status checks or tidying. "
            "Spend it MOVING THE BUSINESS: something a stranger could see, "
            "use, or buy by the end of it.")
        if books["revenue_usd"] <= 0:
            focus_note += (
                " You have never made a sale, so the binding constraint is "
                "almost certainly distribution rather than the product. Ship "
                "something outward.")
        else:
            focus_note += (
                f" You have earned ${books['revenue_usd']:.2f} — something "
                "works. Find out what, and do more of it.")
        parts.append(focus_note)
    parts.append(
        f"\nYou have roughly **{affordable} turns** of work in this session "
        "— a solid working block, comfortably enough to finish something "
        "real. USE IT: unspent budget does not roll over, and a session that "
        "ends early having accomplished nothing is pure waste. Do not ration "
        "yourself into paralysis.\n"
        "Spend it well rather than sparingly: every turn re-reads everything "
        "before it, so keep tool output small (pipe to `head`/`tail`, "
        "`--quiet`, `2>/dev/null`, never print progress bars or whole files). "
        "Pick ONE thing worth finishing rather than starting five, and leave "
        "a few turns at the end to write the day down.")
    return "\n\n".join(parts)


async def wake(mode: str = "focus", model: str | None = None,
               budget: float | None = None,
               reasons: list[str] | None = None):
    """One unit of work. A `tick` is short, cheap and reactive; a `focus`
    block is the day's real session on the good model."""
    co = company.get_company()
    session_model = model or co["model"]
    session_budget = budget if budget is not None else SESSION_BUDGET_USD
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

    wk = company.insert("wakeups", {"company_id": co["id"], "mode": mode})
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
        return False

    _cli_err: list[str] = []
    persona = "founder.md" if mode == "focus" else "founder_tick.md"
    options = ClaudeAgentOptions(
        system_prompt=(HERE / persona).read_text(),
        model=session_model,
        max_turns=MAX_TURNS if mode == "focus" else 14,
        max_budget_usd=session_budget,
        effort=EFFORT,
        cwd=os.environ.get("STRO_WORKSPACE", "/workspace"),
        permission_mode="bypassPermissions",   # headless founder, no human
        # The CLI's own stderr is the only place launch failures explain
        # themselves; capture it so a crash is diagnosable from the world.
        stderr=lambda line: _cli_err.append(line),
        env={**os.environ, "HOME": os.environ.get("STRO_HOME", "/home/stro"),
             "IS_SANDBOX": "1"},
        allowed_tools=(
            ["Bash", "Read", "Write", "Edit", "Glob", "Grep",
             "WebSearch", "WebFetch",
             "mcp__company__journal_write", "mcp__company__memory_save",
             "mcp__company__task_create", "mcp__company__task_update",
             "mcp__company__escalate", "mcp__company__set_appearance",
             "mcp__company__book_expense", "mcp__company__hire",
             "mcp__company__delegate", "mcp__company__fire",
             "mcp__company__set_my_model"]
            if mode == "focus" else
            # A check-in gets a small, immediate toolset: a long list gets
            # deferred and he burns his whole budget searching for his own
            # hands instead of using them.
            ["Bash", "Read", "Grep",
             "mcp__company__journal_write", "mcp__company__task_create",
             "mcp__company__task_update"]),
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
            print("[main] swallowed a failure at line 340")

    cost, turns, last_text = 0.0, 0, ""
    usage_note: list[str] = []
    emit("session_start", "Stro wakes up", None)
    try:
      async with asyncio.timeout(int(os.environ.get("STRO_SESSION_MAX_S",
                                                    "2400"))):
        async for msg in query(prompt=_state_briefing(co, mode, session_budget,
                                                  reasons, session_model),
                               options=options):
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
        spent_out = ("maximum budget" in str(exc)
                     or "max_budget" in str(exc).lower())
        if spent_out:
            # He used exactly what he was given. That is the budget doing
            # its job, not a failure — do not book it as one.
            status = "completed"
            last_text = f"spent the session budget after {turns} turns"
        else:
            status = "failed"
            last_text = f"session crashed: {exc}" + (
                f"\nCLI stderr: {detail}" if detail else "")
            emit("session_end", "crash detail", last_text)

    # If the session ended without him writing anything down — ran out of
    # turns mid-thought, timed out, crashed — give him a short, focused last
    # call whose only job is to remember the day. Losing the work is bad;
    # losing the MEMORY of the work is what actually compounds.
    wrote = company._req(f"journal?wakeup_id=eq.{wk['id']}&select=id&limit=1")
    if not wrote and turns > 0 and mode == "focus":
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
                model=session_model, max_turns=6,
                max_budget_usd=max(0.03, session_budget * 0.5),
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
            print("[main] swallowed a failure at line 436")

    # The founder has gone home; the staff work their tasks now, so their
    # reports are waiting for him next session.
    for d in staff.pending_delegations(co["id"])[:4]:
        emit("tool_use", "staff", f"delegation running: {d['task'][:100]}")
        try:
            await staff.run_delegation(co, d)
        except Exception:  # noqa: BLE001 — an employee failing is not fatal
            print("[main] swallowed a failure at line 445")

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

    # The documentary crew films the DAY, not every check-in. Narrating a
    # four-turn inbox glance produced episodes like "The First Audit" and
    # spends real money under a category the budget gate deliberately
    # ignores — uncapped by construction.
    if mode != "focus":
        print(f"{status}: {turns} turns, ${cost:.4f}")
        return True
    try:
        started = datetime.fromisoformat(
            co["created_at"].replace("Z", "+00:00"))
        day = max(1, (datetime.now(timezone.utc) - started).days + 1)
        nar = narrator.write_narration(
            co["id"], wk["id"], day, session_events,
            company.month_to_date(co["id"]),
            os.environ.get("NARRATOR_MODEL", "claude-haiku-4-5-20251001"))
        if nar:
            voiceover.voice_narration(nar)
    except Exception:  # noqa: BLE001 — narration never breaks the company
        print("[main] swallowed a failure at line 477")
    print(f"{status}: {turns} turns, ${cost:.4f}")
    return True


if __name__ == "__main__":
    asyncio.run(wake())
