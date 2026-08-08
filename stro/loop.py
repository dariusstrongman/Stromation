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


def spent_today(company_id: str) -> float:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
    rows = company._req(
        f"ledger?company_id=eq.{company_id}&ts=gte.{day}"
        "&select=category,amount_usd")
    return round(sum(-float(r["amount_usd"]) for r in rows
                     if float(r["amount_usd"]) < 0
                     and r["category"] in ("inference", "salary")), 4)


def focus_done_today(company_id: str) -> bool:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
    rows = company._req(
        f"wakeups?company_id=eq.{company_id}&started_at=gte.{day}"
        "&num_turns=gt.8&select=id&limit=1")
    return bool(rows)


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
                        and not focus_done_today(co["id"]))
            reasons = triggers.check(co["id"], MAX_IDLE_MIN)

            if is_focus:
                # The day's real work: the good model, the full budget.
                await wake(mode="focus",
                           model=co["model"],
                           budget=min(FOCUS_BUDGET, budget_left),
                           reasons=["today's focus block"] + reasons)
            elif reasons:
                await wake(mode="tick",
                           model=TICK_MODEL,
                           budget=min(TICK_BUDGET, budget_left),
                           reasons=reasons)
            # nothing to do: the free path, and by far the most common one
        except Exception as exc:  # noqa: BLE001 — the company outlives its bugs
            print(f"loop error (continuing): {exc}")
        await asyncio.sleep(CHECK_EVERY_S)


if __name__ == "__main__":
    asyncio.run(run())
