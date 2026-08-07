"""Supabase-backed company state: the world Stro lives in."""
import json
import os
import urllib.request

SB_URL = os.environ["SUPABASE_URL"].rstrip("/")
SB_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]


def _req(path: str, method: str = "GET", body=None):
    req = urllib.request.Request(
        f"{SB_URL}/rest/v1/{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
                 "Content-Type": "application/json",
                 "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode()
        return json.loads(text) if text else None


# Secret values (STRO_SECRET_* envs) are scrubbed from EVERYTHING persisted:
# journal/memory/events are publicly readable by design, so redaction is a
# structural guarantee, not founder discipline.
_SECRETS = [v for k, v in os.environ.items()
            if k.startswith("STRO_SECRET_") and len(v) >= 6]


def _scrub(obj):
    if isinstance(obj, str):
        for sec in _SECRETS:
            obj = obj.replace(sec, "[REDACTED]")
        return obj
    if isinstance(obj, dict):
        return {k: _scrub(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub(v) for v in obj]
    return obj


def get_company() -> dict:
    rows = _req("company?select=*&limit=1")
    if not rows:
        raise SystemExit("No company row — seed one (see README).")
    return rows[0]


def insert(table: str, row: dict) -> dict:
    return _req(table, "POST", _scrub(row))[0]


def update(table: str, row_id: str, patch: dict):
    _req(f"{table}?id=eq.{row_id}", "PATCH", _scrub(patch))


def recent_journal(company_id: str, limit: int = 25) -> list[dict]:
    return _req(f"journal?company_id=eq.{company_id}"
                f"&select=ts,entry_type,content&order=ts.desc&limit={limit}")


def open_tasks(company_id: str) -> list[dict]:
    return _req(f"tasks?company_id=eq.{company_id}"
                "&status=in.(open,in_progress)"
                "&select=id,title,why,status,priority&order=priority")


def memories(company_id: str) -> list[dict]:
    return _req(f"memory?company_id=eq.{company_id}"
                "&select=slug,kind,content&order=updated_at.desc&limit=50")


def pending_escalations(company_id: str) -> list[dict]:
    return _req(f"escalations?company_id=eq.{company_id}&status=eq.pending"
                "&select=action,reason,ts")


def resolved_escalations_since(company_id: str, since_iso: str) -> list[dict]:
    return _req(f"escalations?company_id=eq.{company_id}"
                f"&status=in.(approved,denied)&resolved_at=gte.{since_iso}"
                "&select=action,status,resolution,resolved_at")


def infra_booked_today(company_id: str) -> bool:
    from datetime import datetime, timezone
    day = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
    rows = _req(f"ledger?company_id=eq.{company_id}&category=eq.infrastructure"
                f"&ts=gte.{day}&select=id&limit=1")
    return bool(rows)


def month_to_date(company_id: str) -> dict:
    """Burn and revenue for the current calendar month, in USD."""
    from datetime import datetime, timezone
    # 'Z' not '+00:00': a '+' inside a querystring decodes as a space and
    # PostgREST rejects the mangled timestamp with a 400.
    start = datetime.now(timezone.utc).replace(
        day=1, hour=0, minute=0, second=0,
        microsecond=0).isoformat().replace("+00:00", "Z")
    rows = _req(f"ledger?company_id=eq.{company_id}&ts=gte.{start}"
                "&select=category,amount_usd")
    burn = sum(-float(r["amount_usd"]) for r in rows if float(r["amount_usd"]) < 0)
    revenue = sum(float(r["amount_usd"]) for r in rows if float(r["amount_usd"]) > 0)
    return {"burn_usd": round(burn, 4), "revenue_usd": round(revenue, 4)}


def founder(company_id: str) -> dict | None:
    rows = _req(f"employees?company_id=eq.{company_id}&role=eq.Founder%20%26%20CEO"
                "&select=id,name,sprite,personality&limit=1")
    return rows[0] if rows else None


def sync_stripe_revenue(company_id: str, since_iso: str) -> float:
    """Book ONLY this company's real Stripe revenue, idempotently.

    The Stripe account is shared with the owner's other businesses, so a
    naive balance-transaction sweep books THEIR income as Stro's — which is
    exactly the fabricated economy this project forbids. Two hard filters:
    charges created after the company existed, AND carrying the company's
    own metadata tag. A sale the founder did not tag is not counted; false
    revenue is worse than missing revenue.
    """
    key = os.environ.get("STRO_SECRET_STRIPE_KEY")
    if not key:
        return 0.0
    from datetime import datetime
    start = int(datetime.fromisoformat(
        since_iso.replace("Z", "+00:00")).timestamp())
    req = urllib.request.Request(
        f"https://api.stripe.com/v1/charges?limit=100&created[gte]={start}",
        headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            charges = json.loads(r.read())["data"]
    except Exception:  # noqa: BLE001 — Stripe down != company broken
        return 0.0
    booked = {row["description"] for row in _req(
        f"ledger?company_id=eq.{company_id}&category=eq.revenue"
        "&select=description")}
    new_total = 0.0
    for c in charges:
        tag = f"stripe_charge:{c['id']}"
        meta = c.get("metadata") or {}
        if (tag in booked or not c.get("paid") or c.get("refunded")
                or meta.get("stromation") != "1"):
            continue
        net = c["amount"] / 100.0
        insert("ledger", {"company_id": company_id, "category": "revenue",
                          "description": tag, "amount_usd": round(net, 4)})
        new_total += net
    return round(new_total, 4)
