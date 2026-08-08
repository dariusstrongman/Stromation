"""Hiring, delegation and payroll.

An employee is a model with a role, a memory and a salary. The salary is
not a number the company pretends to pay — it is literally what running
that model costs, booked per person, so the founder can see whether anyone
is earning their keep.

Delegation is asynchronous on purpose: the founder asks, the employee works
after his session ends, and the answer is waiting for him next time. That
is how delegation works in a real company, and it keeps one agent from
being nested inside another.
"""
import os
from datetime import datetime, timezone

from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                              ResultMessage, TextBlock, query)

from . import company

# Who the founder can hire. Salary bands are real per-million-token prices;
# a senior costs what a senior costs. Roles are NOT fixed — he decides what
# a person is for. Models outside this roster need credentials the owner
# has not provisioned, which is itself something worth escalating about.
# Two kinds of colleague. WORKERS get hands — a shell, the filesystem, the
# web — and can actually build things. ADVISORS only read what you hand
# them and write back; they are cheap, they have enormous context, and they
# are the right hire for research, analysis and copy.
ROSTER = {
    "claude-opus-5": {
        "band": "senior", "kind": "worker", "provider": "anthropic",
        "rate": "$15/$75 per Mtok",
        "good_at": "hardest reasoning, architecture, gnarly debugging"},
    "claude-sonnet-5": {
        "band": "mid", "kind": "worker", "provider": "anthropic",
        "rate": "$3/$15 per Mtok",
        "good_at": "engineering, long tool work, most real tasks"},
    "claude-haiku-4-5-20251001": {
        "band": "junior", "kind": "worker", "provider": "anthropic",
        "rate": "$1/$5 per Mtok",
        "good_at": "routine work, drafting, checking, summarising"},
    "gemini-2.5-pro": {
        "band": "senior", "kind": "advisor", "provider": "google",
        "rate": "$1.25/$10 per Mtok",
        "good_at": "deep research and analysis over huge amounts of text"},
    "gemini-2.5-flash": {
        "band": "junior", "kind": "advisor", "provider": "google",
        "rate": "$0.30/$2.50 per Mtok",
        "good_at": "cheap fast research, summarising, drafting copy"},
}
GOOGLE_PRICES = {           # $ per million tokens (in, out)
    "gemini-2.5-pro": (1.25, 10.0),
    "gemini-2.5-flash": (0.30, 2.50),
}


def roster_text() -> str:
    lines = [f"- {m} ({v['band']} {v['kind']}, {v['rate']}) — {v['good_at']}"
             for m, v in ROSTER.items()]
    return ("\n".join(lines) +
            "\nWORKERS have a shell and the filesystem and can build things. "
            "ADVISORS cannot touch anything — they only read the task and "
            "context you give them and write back, so hand them everything "
            "they need. Advisors are much cheaper.")


def active_staff(company_id: str) -> list[dict]:
    return company._req(
        f"employees?company_id=eq.{company_id}&status=eq.active"
        "&select=id,name,role,model,personality,hired_at&order=hired_at")


def payroll(company_id: str) -> dict:
    """Salary spent per employee this month."""
    from datetime import timedelta  # noqa: F401
    start = datetime.now(timezone.utc).replace(
        day=1, hour=0, minute=0, second=0,
        microsecond=0).isoformat().replace("+00:00", "Z")
    rows = company._req(
        f"ledger?company_id=eq.{company_id}&category=eq.salary"
        f"&ts=gte.{start}&select=employee_id,amount_usd")
    out: dict[str, float] = {}
    for r in rows:
        eid = r.get("employee_id") or "unknown"
        out[eid] = round(out.get(eid, 0.0) + -float(r["amount_usd"]), 4)
    return out


def pending_delegations(company_id: str) -> list[dict]:
    return company._req(
        f"delegations?company_id=eq.{company_id}&status=eq.pending"
        "&select=id,employee_id,task,context&order=created_at")


def completed_since(company_id: str, since_iso: str) -> list[dict]:
    return company._req(
        f"delegations?company_id=eq.{company_id}&status=in.(done,failed)"
        f"&completed_at=gte.{since_iso}"
        "&select=employee_id,task,status,result,cost_usd,completed_at")


def _employee_prompt(emp: dict, task: str, context: str, notes: list) -> str:
    parts = [
        f"You are {emp['name']}, {emp['role']} at this company.",
        emp.get("personality") or "",
        "\nYou were hired to do a specific job, not to run the company. The "
        "founder decides strategy; you do the work he asks for and report "
        "back plainly. If the task is impossible or a bad idea, say so — "
        "an employee who reports bad news early is worth more than one who "
        "pretends.",
        "\nYou cost the company real money every time you work. Be useful "
        "and be brief.",
    ]
    if notes:
        parts.append("\nYour own notes from previous work here:\n" + "\n".join(
            f"- {n['content'][:300]}" for n in notes))
    parts.append(f"\n## Your task\n{task}")
    if context:
        parts.append(f"\n## Context from the founder\n{context}")
    parts.append("\nDo the work, then end with a short report of what you "
                 "did and what the founder needs to know.")
    return "\n".join(p for p in parts if p)


def _ask_gemini(model: str, system: str, task: str) -> tuple[str, float]:
    """An advisor: no hands, just judgment. Returns (report, cost)."""
    import json as _json
    import urllib.request
    key = os.environ.get("STRO_SECRET_GEMINI_KEY")
    if not key:
        return ("no Gemini credentials provisioned", 0.0)
    payload = {"systemInstruction": {"parts": [{"text": system}]},
               "contents": [{"parts": [{"text": task}]}],
               "generationConfig": {"maxOutputTokens": 4000}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={key}",
        method="POST", data=_json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = _json.loads(r.read())
    cands = data.get("candidates") or []
    text = ""
    if cands:
        text = "".join(p.get("text", "")
                       for p in cands[0].get("content", {}).get("parts", []))
    u = data.get("usageMetadata") or {}
    pin, pout = GOOGLE_PRICES.get(model, (0.30, 2.50))
    cost = (u.get("promptTokenCount", 0) / 1e6 * pin
            + u.get("candidatesTokenCount", 0) / 1e6 * pout)
    return (text, round(cost, 6))


async def run_delegation(co: dict, d: dict) -> None:
    """Run one employee's task and book their salary."""
    emps = company._req(f"employees?id=eq.{d['employee_id']}&select=*")
    if not emps:
        company.update("delegations", d["id"],
                       {"status": "failed", "result": "employee not found",
                        "completed_at": datetime.now(timezone.utc).isoformat()})
        return
    emp = emps[0]
    notes = company._req(
        f"memory?employee_id=eq.{emp['id']}&select=content"
        "&order=updated_at.desc&limit=10")
    model = emp.get("model") or "claude-haiku-4-5-20251001"

    spec = ROSTER.get(model, {})
    if spec.get("provider") == "google":
        try:
            system = _employee_prompt(emp, d["task"], d.get("context") or "",
                                      notes)
            text, cost = _ask_gemini(model, system, d["task"])
            status = "done"
        except Exception as exc:  # noqa: BLE001
            status, text, cost = "failed", f"{exc}", 0.0
        company.update("delegations", d["id"], {
            "status": status, "result": text[:4000], "cost_usd": round(cost, 4),
            "completed_at": datetime.now(timezone.utc).isoformat()})
        if cost:
            company.insert("ledger", {
                "company_id": co["id"], "category": "salary",
                "employee_id": emp["id"],
                "description": f"{emp['name']} ({emp['role']}): "
                               f"{d['task'][:80]}",
                "amount_usd": -round(cost, 4)})
        return

    cost, text = 0.0, ""
    try:
        opts = ClaudeAgentOptions(
            system_prompt=_employee_prompt(emp, d["task"], d.get("context") or "",
                                           notes),
            model=model,
            max_turns=int(os.environ.get("STRO_EMPLOYEE_MAX_TURNS", "30")),
            max_budget_usd=float(os.environ.get("STRO_EMPLOYEE_BUDGET_USD",
                                                "0.40")),
            effort=os.environ.get("STRO_EFFORT", "medium"),
            cwd=os.environ.get("STRO_WORKSPACE", "/workspace"),
            permission_mode="bypassPermissions",
            env={**os.environ, "HOME": os.environ.get("STRO_HOME", "/home/stro"),
                 "IS_SANDBOX": "1"},
            allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep",
                           "WebSearch", "WebFetch"],
        )
        async for msg in query(prompt=d["task"], options=opts):
            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, TextBlock):
                        text = b.text
            elif isinstance(msg, ResultMessage):
                cost = msg.total_cost_usd or 0.0
        status = "done"
    except Exception as exc:  # noqa: BLE001 — a failed employee is not a failed company
        status, text = "failed", f"{exc}"

    company.update("delegations", d["id"], {
        "status": status, "result": text[:4000], "cost_usd": round(cost, 4),
        "completed_at": datetime.now(timezone.utc).isoformat()})
    if cost:
        company.insert("ledger", {
            "company_id": co["id"], "category": "salary",
            "employee_id": emp["id"],
            "description": f"{emp['name']} ({emp['role']}): {d['task'][:80]}",
            "amount_usd": -round(cost, 4)})
