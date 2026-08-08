"""Reasons to wake up — all of them free.

Nothing in this module costs a token. That is the whole point: the company
can be alive around the clock because *noticing* is free and only *acting*
is billed.
"""
import imaplib
import json
import os
import urllib.request
from datetime import datetime, timezone

from . import company


def _new_mail() -> str | None:
    host = (os.environ.get("STRO_SECRET_EMAIL_IMAP") or "").split(":")[0]
    user = os.environ.get("STRO_SECRET_COMPANY_EMAIL")
    pw = os.environ.get("STRO_SECRET_COMPANY_EMAIL_PASSWORD")
    if not (host and user and pw):
        return None
    try:
        m = imaplib.IMAP4_SSL(host, 993, timeout=25)
        m.login(user, pw)
        m.select("INBOX")
        _, data = m.search(None, "UNSEEN")
        n = len(data[0].split()) if data and data[0] else 0
        m.logout()
        return f"{n} unread email(s) in the company inbox" if n else None
    except Exception:  # noqa: BLE001 — a flaky mailbox must not wake anyone
        return None


def _new_payment(company_id: str) -> str | None:
    key = os.environ.get("STRO_SECRET_STRIPE_KEY")
    if not key:
        return None
    try:
        req = urllib.request.Request(
            "https://api.stripe.com/v1/charges?limit=20",
            headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=25) as r:
            charges = json.loads(r.read())["data"]
    except Exception:  # noqa: BLE001
        return None
    booked = {row["description"] for row in company._req(
        f"ledger?company_id=eq.{company_id}&category=eq.revenue"
        "&select=description")}
    fresh = [c for c in charges
             if c.get("paid") and not c.get("refunded")
             and (c.get("metadata") or {}).get("stromation") == "1"
             and f"stripe_charge:{c['id']}" not in booked]
    if fresh:
        total = sum(c["amount"] for c in fresh) / 100.0
        return (f"{len(fresh)} NEW PAID ORDER(S) worth ${total:.2f} — "
                "a real customer is waiting. This is the most important "
                "thing happening.")
    return None


def _staff_reports(company_id: str) -> str | None:
    from datetime import timedelta
    since = (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat(
    ).replace("+00:00", "Z")
    rows = company._req(
        f"delegations?company_id=eq.{company_id}&status=eq.done"
        f"&completed_at=gte.{since}&select=id&limit=5")
    return f"{len(rows)} employee report(s) came back" if rows else None


def _owner_answered(company_id: str) -> str | None:
    from datetime import timedelta
    since = (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(
    ).replace("+00:00", "Z")
    rows = company.resolved_escalations_since(company_id, since)
    return (f"the owner answered {len(rows)} escalation(s)"
            if rows else None)


def _idle(company_id: str, max_idle_min: int) -> str | None:
    rows = company._req(
        f"wakeups?company_id=eq.{company_id}&select=started_at"
        "&order=started_at.desc&limit=1")
    if not rows:
        return "the company has never worked a day"
    last = datetime.fromisoformat(rows[0]["started_at"].replace("Z", "+00:00"))
    mins = (datetime.now(timezone.utc) - last).total_seconds() / 60
    return (f"{int(mins)} minutes since any work happened"
            if mins >= max_idle_min else None)


def check(company_id: str, max_idle_min: int) -> list[str]:
    """Every reason to act right now. Costs nothing to ask."""
    found = []
    for fn in (lambda: _new_payment(company_id),
               _new_mail,
               lambda: _staff_reports(company_id),
               lambda: _owner_answered(company_id),
               lambda: _idle(company_id, max_idle_min)):
        try:
            r = fn()
        except Exception:  # noqa: BLE001
            r = None
        if r:
            found.append(r)
    return found
