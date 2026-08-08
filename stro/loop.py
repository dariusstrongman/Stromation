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
from .main import BUDGET_HEADROOM, wake

CHECK_EVERY_S = int(os.environ.get("STRO_CHECK_EVERY_S", "60"))
MAX_IDLE_MIN = int(os.environ.get("STRO_MAX_IDLE_MIN", "25"))
# Office hours, UTC. Routine work concentrates here so the same budget buys
# a much denser heartbeat — and so the owner is awake for most of it. The
# company still LIVES around the clock: money on the table always rings
# through. Set STRO_WORK_HOURS_UTC="" for genuine 24/7.
_WH = os.environ.get("STRO_WORK_HOURS_UTC", "14-22")
WORK_START, WORK_END = (int(x) for x in _WH.split("-")) if "-" in _WH else (0, 24)
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
    except Exception as exc:  # noqa: BLE001
        print(f"[loop] could not park signal: {exc!r}")


def _report_broken(co: dict, streak: int, why: str) -> None:
    """A company meant to run forever must be able to say when it cannot.

    Escalates ONCE per outage: the owner learns something is wrong without
    being buried, and the founder's own escalation queue is not spammed.
    """
    # Re-read rather than trusting `co`: the caller passes the last company
    # row that loaded successfully, which under backoff can be half an hour
    # stale. Writing that snapshot back wholesale would revert any trigger
    # mark advanced since.
    try:
        co = company.get_company()
    except Exception as exc:  # noqa: BLE001 — if this fails, so will the rest
        print(f"[loop] could not re-read company to report outage: {exc!r}")
        return
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


def publish_hours(co: dict) -> None:
    """Put the working hours where the world can read them.

    index.html draws a home and an office based on these hours and claims
    what it shows is true. It cannot be true if the page hardcodes one set
    and the loop enforces another, so the loop publishes and the page
    reads. Written only when it changes.
    """
    st = dict(co.get("trigger_state") or {})
    hours = {"start": WORK_START, "end": WORK_END, "focus": FOCUS_HOURS}
    if st.get("work_hours") == hours:
        return
    st["work_hours"] = hours
    try:
        company.update("company", co["id"], {"trigger_state": st})
        co["trigger_state"] = st
    except Exception as exc:  # noqa: BLE001 — cosmetic; never blocks work
        print(f"[loop] could not publish work hours: {exc!r}")


async def run() -> None:
    print("stro is awake; the office does not close")
    streak, last_err, last_co = 0, "", None
    while True:
        try:
            co = company.get_company()
            publish_hours(co)
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
            open_for_business = WORK_START <= now.hour < WORK_END
            is_focus = (now.hour in FOCUS_HOURS
                        and not focus_done_this_slot(co, now.hour))

            # Out of hours the founder is off the clock, but the business is
            # not closed: a paid customer is waiting on something they have
            # already bought, and that outranks office hours. Everything
            # else keeps until morning.
            #
            # Which triggers we ASK is the whole point. Every mark-keeping
            # trigger fires exactly once, so asking one while refusing to
            # act on it destroys the signal: mail arriving at 3am would
            # advance the high-water mark, be filtered out as non-urgent,
            # and never be raised again — while the check-in persona tells
            # him never to look, because he would have been told. Out of
            # hours we therefore consult ONLY the payment trigger, which
            # holds no mark (it compares against the ledger and re-fires
            # until the money is booked). Mail and the rest are simply not
            # asked, so they are still waiting in the morning.
            if not open_for_business and not is_focus:
                reasons = triggers.check_urgent_only(co)
                if not reasons:
                    await asyncio.sleep(CHECK_EVERY_S)
                    continue
            else:
                reasons = triggers.check(co, MAX_IDLE_MIN)

            # A session may overshoot its target by BUDGET_HEADROOM to land
            # itself, so the target handed out has to leave room for that
            # inside what the day actually has left. Without the divide,
            # the last session of the day spends 35% more than the governor
            # said was available.
            spendable = budget_left / BUDGET_HEADROOM

            if is_focus:
                mark_focus_done(co, now.hour)
                # The day's real work: the good model, the full budget.
                await wake(mode="focus",
                           model=co["model"],
                           budget=min(FOCUS_BUDGET, spendable),
                           reasons=["today's focus block"] + reasons)
            elif reasons:
                try:
                    ran = await wake(mode="tick",
                                     model=TICK_MODEL,
                                     budget=min(TICK_BUDGET, spendable),
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
