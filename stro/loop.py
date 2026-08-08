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
FOCUS_HOUR_UTC = int(os.environ.get("STRO_FOCUS_HOUR_UTC", "13"))
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


def focus_done_today(co: dict) -> bool:
    st = co.get("trigger_state") or {}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return st.get("focus_date") == today


def mark_focus_done(co: dict) -> None:
    """Recorded BEFORE the block runs. A focus session that crashes must not
    retry every minute for the rest of the hour."""
    st = dict(co.get("trigger_state") or {})
    st["focus_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    company.update("company", co["id"], {"trigger_state": st})


def _park(co: dict, reasons: list[str], why: str) -> None:
    """A trigger fires once. If the session it triggered never ran, the
    signal is gone — so write it down where the founder will find it."""
    try:
        company.insert("tasks", {
            "company_id": co["id"], "priority": 2,
            "title": f"Missed signal: {'; '.join(reasons)[:120]}",
            "why": f"The loop could not run a session for this ({why[:160]}). "
                   "It will not be raised again automatically."})
    except Exception:  # noqa: BLE001
        pass


async def run() -> None:
    print("stro is awake; the office does not close")
    while True:
        try:
            co = company.get_company()
            budget_left = allowance(co)

            # Broke for now: stay alive, stay quiet, cost nothing.
            if budget_left < 0.02:
                await asyncio.sleep(600)
                continue

            now = datetime.now(timezone.utc)
            is_focus = (now.hour == FOCUS_HOUR_UTC
                        and not focus_done_today(co))
            reasons = triggers.check(co, MAX_IDLE_MIN)

            if is_focus:
                mark_focus_done(co)
                # The day's real work: the good model, the full budget.
                await wake(mode="focus",
                           model=co["model"],
                           budget=min(FOCUS_BUDGET, budget_left),
                           reasons=["today's focus block"] + reasons)
            elif reasons:
                try:
                    await wake(mode="tick",
                               model=TICK_MODEL,
                               budget=min(TICK_BUDGET, budget_left),
                               reasons=reasons)
                except Exception as exc:  # noqa: BLE001
                    # The marks already advanced, so this signal will never
                    # fire again. Park it where he will see it instead of
                    # losing it — without re-arming the trigger.
                    _park(co, reasons, str(exc))
                    raise
            # nothing to do: the free path, and by far the most common one
        except Exception as exc:  # noqa: BLE001 — the company outlives its bugs
            print(f"loop error (continuing): {exc}")
        await asyncio.sleep(CHECK_EVERY_S)


if __name__ == "__main__":
    asyncio.run(run())
