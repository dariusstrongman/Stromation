"""The company that never closes.

A process that does not exit. Most of what it does is free: every minute it
asks whether anything is worth doing — new mail, a paid order, a report
back from staff, an answer from the owner, or simply too long since
anything happened. Only when the answer is yes does it spend money.

The spend is paced by a governor so the month cannot be burned in a week,
and the day has a shape: cheap ticks keep the lights on, and once a day a
longer focus block gets the good model for real work. That is closer to how
a person works than three scheduled bursts, and it costs the same.

    python -m stro.loop
"""
import asyncio
import os
from datetime import datetime, timedelta, timezone

from . import company, triggers
from .main import wake

CHECK_EVERY_S = int(os.environ.get("STRO_CHECK_EVERY_S", "60"))
MAX_IDLE_MIN = int(os.environ.get("STRO_MAX_IDLE_MIN", "25"))
# More than one real work session a day, because check-ins deliberately
# cannot build anything — the focus blocks are the only time the business
# actually moves.
FOCUS_HOURS = [int(h) for h in
               os.environ.get("STRO_FOCUS_HOUR_UTC", "13").split(",") if h.strip()]
TICK_MODEL = os.environ.get("STRO_TICK_MODEL", "claude-haiku-4-5-20251001")
TICK_BUDGET = float(os.environ.get("STRO_TICK_BUDGET_USD", "0.06"))
FOCUS_BUDGET = float(os.environ.get("STRO_FOCUS_BUDGET_USD", "0.55"))


def _month_bounds() -> tuple[datetime, int]:
    now = datetime.now(timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    nxt = (start + timedelta(days=32)).replace(day=1)
    return now, max(1, int((nxt - start).days))


def allowance(co: dict) -> float:
    """What may still be spent today without endangering the month.

    Unspent days accrue: a quiet week leaves room for a busy one, which is
    how a real budget behaves. Never lets one day eat more than a fifth of
    the monthly cap.
    """
    now, days_in_month = _month_bounds()
    cap = float(co["budget_monthly_usd"])
    spent = company.month_to_date(co["id"])["burn_usd"]
    day_of_month = now.day
    earned = cap * (day_of_month / days_in_month)
    remaining_today = max(0.0, earned - spent)
    return min(remaining_today, cap / 5)


def focus_done_this_slot(co: dict, hour: int) -> bool:
    st = co.get("trigger_state") or {}
    slot = datetime.now(timezone.utc).strftime("%Y-%m-%d") + f"H{hour}"
    return st.get("focus_slot") == slot


def mark_focus_done(co: dict, hour: int) -> None:
    """Recorded BEFORE the block runs. A focus session that crashes must not
    retry every minute for the rest of the hour."""
    st = dict(co.get("trigger_state") or {})
    st["focus_slot"] = datetime.now(timezone.utc).strftime("%Y-%m-%d") + f"H{hour}"
    company.update("company", co["id"], {"trigger_state": st})


def _park(co: dict, reasons: list[str], why: str) -> None:
    """A trigger fires once. If the session it triggered never ran, the
    signal is gone — so write it down where the founder will find it.

    Two things this must not do. It must never park the idle clock: wake()
    writes its row before doing anything, so idle re-fires every cycle even
    when sessions fail, and parking it would file ~57 identical tasks a day.
    And it must not duplicate — parked tasks flow into every briefing, so a
    persistent failure would inflate the prompt it is trying to protect.
    """
    real = [r for r in reasons if "since any work happened" not in r
            and "never worked a day" not in r]
    if not real:
        return
    title = f"Missed signal: {'; '.join(real)[:110]}"
    try:
        dupes = company._req(
            f"tasks?company_id=eq.{co['id']}&status=in.(open,in_progress)"
            "&select=id,title")
        if any(t["title"] == title for t in dupes):
            return
        company.insert("tasks", {
            "company_id": co["id"], "priority": 2, "title": title,
            "why": f"The loop could not run a session for this ({why[:160]}). "
                   "It will not be raised again automatically."})
    except Exception:  # noqa: BLE001
        print("[loop] swallowed a failure at line 93")


def _report_broken(co: dict, streak: int, why: str) -> None:
    """A company meant to run forever must be able to say when it cannot.

    Escalates ONCE per outage: the owner learns something is wrong without
    being buried, and the founder's own escalation queue is not spammed.
    """
    st = dict(co.get("trigger_state") or {})
    if st.get("outage_reported"):
        return
    st["outage_reported"] = True
    try:
        company.update("company", co["id"], {"trigger_state": st})
        company.insert("escalations", {
            "company_id": co["id"],
            "action": f"The company has been unable to work for {streak} "
                      "consecutive cycles",
            "reason": f"Last error: {why[:400]}. Nothing will run until this "
                      "is fixed. This is reported once per outage."})
    except Exception as exc:  # noqa: BLE001
        print(f"[loop] could not report outage: {exc!r}")


def _report_recovered(co: dict) -> None:
    st = dict(co.get("trigger_state") or {})
    if not st.get("outage_reported"):
        return
    st["outage_reported"] = False
    try:
        company.update("company", co["id"], {"trigger_state": st})
    except Exception as exc:  # noqa: BLE001
        print(f"[loop] could not clear outage flag: {exc!r}")


async def run() -> None:
    print("stro is awake; the office does not close")
    streak, last_err, last_co = 0, "", None
    while True:
        try:
            co = company.get_company()
            budget_left = allowance(co)

            # Out of money for now: stay alive, stay quiet, cost nothing.
            # This is a normal end-of-month state, not a failure — the
            # allowance refills as the calendar advances.
            if budget_left < 0.02:
                if streak:
                    _report_recovered(co)
                streak, last_co = 0, co
                await asyncio.sleep(600)
                continue

            now = datetime.now(timezone.utc)
            is_focus = (now.hour in FOCUS_HOURS
                        and not focus_done_this_slot(co, now.hour))
            reasons = triggers.check(co, MAX_IDLE_MIN)

            if is_focus:
                mark_focus_done(co, now.hour)
                # The day's real work: the good model, the full budget.
                await wake(mode="focus",
                           model=co["model"],
                           budget=min(FOCUS_BUDGET, budget_left),
                           reasons=["today's focus block"] + reasons)
            elif reasons:
                try:
                    ran = await wake(mode="tick",
                                     model=TICK_MODEL,
                                     budget=min(TICK_BUDGET, budget_left),
                                     reasons=reasons)
                    if not ran:
                        # Budget-blocked: wake() returns rather than raising,
                        # and month-end blocking is routine, so this is the
                        # likelier way to lose a signal than a crash.
                        _park(co, reasons, "monthly budget exhausted")
                except Exception as exc:
                    _park(co, reasons, str(exc))
                    raise
            # nothing to do: the free path, and by far the most common one
            if streak:
                print(f"[loop] recovered after {streak} failed cycles")
                _report_recovered(co)
            streak, last_co = 0, co
        except Exception as exc:  # noqa: BLE001 — the company outlives its bugs
            streak += 1
            last_err = f"{exc!r}"
            print(f"[loop] error #{streak} (continuing): {last_err}")
            # Ten consecutive failures is not a blip. Tell the owner, once.
            if streak == 10 and last_co:
                _report_broken(last_co, streak, last_err)

        # Back off when the world is broken rather than hammering a dead
        # dependency every minute for days.
        delay = CHECK_EVERY_S
        if streak:
            delay = min(CHECK_EVERY_S * (2 ** min(streak, 5)), 1800)
        await asyncio.sleep(delay)


if __name__ == "__main__":
    asyncio.run(run())
