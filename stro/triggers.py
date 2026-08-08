"""Reasons to wake up — all of them free, and each fires only once.

Nothing here costs a token. That is the point: the company can be alive
around the clock because *noticing* is free and only *acting* is billed.

Every trigger keeps a high-water mark. Without one, a trigger reports the
continued existence of an old thing rather than the arrival of a new one —
and a single unread newsletter would wake the founder every sixty seconds
for the rest of its life.
"""
import imaplib
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

from . import company


def _state(co: dict) -> dict:
    """Returns the SAME dict object held on `co`, deliberately: check()
    mutates it in place and loop.mark_focus_done() then reads the advanced
    marks off `co` before writing. Returning a copy here would silently
    clobber the mail high-water mark."""
    st = co.get("trigger_state")
    if not isinstance(st, dict):
        st = {}
        co["trigger_state"] = st
    return st


def _save(company_id: str, state: dict) -> None:
    company.update("company", company_id, {"trigger_state": state})


def _new_mail(state: dict, company_id: str = "") -> tuple[str | None, dict]:
    """Fires on mail newer than anything seen before — read or not.

    Deliberately does NOT use the \\Seen flag: whether the founder opened
    something is his business, and junk he chooses to ignore must not wake
    him forever.
    """
    host = (os.environ.get("STRO_SECRET_EMAIL_IMAP") or "").split(":")[0]
    user = os.environ.get("STRO_SECRET_COMPANY_EMAIL")
    pw = os.environ.get("STRO_SECRET_COMPANY_EMAIL_PASSWORD")
    if not (host and user and pw):
        return None, state
    try:
        m = imaplib.IMAP4_SSL(host, 993, timeout=25)
        m.login(user, pw)
        m.select("INBOX")
        validity = 0
        try:
            _, vd = m.status("INBOX", "(UIDVALIDITY)")
            raw = vd[0].decode() if vd and vd[0] else ""
            validity = int(raw.split("UIDVALIDITY")[1].strip(" ()\r\n"))
        except Exception:  # noqa: BLE001
            validity = 0
        _, data = m.uid("search", None, "ALL")
        uids = [int(x) for x in (data[0].split() if data and data[0] else [])]
        m.logout()
    except Exception:  # noqa: BLE001 — a flaky mailbox must not wake anyone
        return None, state
    if not uids:
        return None, state
    top = max(uids)
    # A UID only means anything within its UIDVALIDITY generation. If the
    # mailbox is recreated or migrated, UIDs reset to low numbers and a
    # stale high-water mark would silence mail forever — the same bug with
    # the sign flipped. Re-baseline instead of comparing across generations.
    if not validity and not state.get("uidvalidity_warned"):
        # The guard is off and nothing would say so. Record it once.
        state["uidvalidity_warned"] = True
        try:
            company.insert("journal", {
                "company_id": company_id,
                "entry_type": "problem",
                "content": "This mailbox does not report UIDVALIDITY, so the "
                           "mail trigger cannot detect a mailbox reset. If "
                           "mail ever stops waking me, suspect that first."})
        except Exception:  # noqa: BLE001
            pass
    if validity and state.get("mail_uidvalidity") != validity:
        state["mail_uidvalidity"] = validity
        state["mail_uid"] = top
        return None, state
    seen = int(state.get("mail_uid", 0))
    if seen == 0:
        # First run: adopt the current mailbox as the baseline rather than
        # announcing every message that ever arrived.
        state["mail_uid"] = top
        if validity:
            state["mail_uidvalidity"] = validity
        return None, state
    if top > seen:
        n = len([u for u in uids if u > seen])
        state["mail_uid"] = top
        return f"{n} new email(s) in the company inbox", state
    return None, state


def _new_payment(company_id: str) -> str | None:
    """Paid orders are checked against the ledger, which is already the
    high-water mark: anything booked has been handled."""
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


def _staff_reports(company_id: str, state: dict) -> tuple[str | None, dict]:
    rows = company._req(
        f"delegations?company_id=eq.{company_id}&status=in.(done,failed)"
        "&select=id,completed_at&order=completed_at.desc&limit=10")
    if not rows:
        return None, state
    latest = rows[0]["completed_at"]
    if state.get("delegation_at") == latest:
        return None, state
    prev = state.get("delegation_at")
    state["delegation_at"] = latest
    if prev is None:
        return None, state
    n = len([r for r in rows if r["completed_at"] > prev])
    return (f"{n} employee report(s) came back", state)


def _owner_answered(company_id: str, state: dict) -> tuple[str | None, dict]:
    rows = company._req(
        f"escalations?company_id=eq.{company_id}&status=in.(approved,denied)"
        "&select=resolved_at,action&order=resolved_at.desc&limit=10")
    if not rows or not rows[0].get("resolved_at"):
        return None, state
    latest = rows[0]["resolved_at"]
    if state.get("escalation_at") == latest:
        return None, state
    prev = state.get("escalation_at")
    state["escalation_at"] = latest
    if prev is None:
        return None, state
    return ("the owner answered an escalation — act on it", state)


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


def check(co: dict, max_idle_min: int) -> list[str]:
    """Every reason to act right now. Costs nothing to ask.

    High-water marks advance whether or not the resulting session succeeds:
    a trigger that re-fires until it is 'handled' is how you get an
    infinite loop at three in the morning.
    """
    cid = co["id"]
    state = _state(co)
    before = dict(state)
    found: list[str] = []

    try:
        r = _new_payment(cid)
        if r:
            found.append(r)
    except Exception:  # noqa: BLE001
        pass
    for fn in (_new_mail,):
        try:
            r, state = fn(state, cid)
            if r:
                found.append(r)
        except Exception:  # noqa: BLE001
            pass
    for fn in (_staff_reports, _owner_answered):
        try:
            r, state = fn(cid, state)
            if r:
                found.append(r)
        except Exception:  # noqa: BLE001
            pass
    try:
        r = _idle(cid, max_idle_min)
        if r:
            found.append(r)
    except Exception:  # noqa: BLE001
        pass

    if state != before:
        try:
            _save(cid, state)
        except Exception:  # noqa: BLE001
            pass
    return found
