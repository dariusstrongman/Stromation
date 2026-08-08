"""Stro's company tools — the only way state changes, so every change is
attributable to a wake-up and visible to the owner."""
from claude_agent_sdk import create_sdk_mcp_server, tool

from . import company, staff


def make_company_server(company_id: str, wakeup_id: str):
    @tool("journal_write",
          "Record what you did/decided/learned this session and why. "
          "entry_type: note|decision|learning|milestone|problem",
          {"entry_type": str, "content": str})
    async def journal_write(args):
        company.insert("journal", {
            "company_id": company_id, "wakeup_id": wakeup_id,
            "entry_type": args["entry_type"], "content": args["content"]})
        return {"content": [{"type": "text", "text": "journaled"}]}

    @tool("memory_save",
          "Save/overwrite one piece of durable company knowledge. "
          "slug: short-kebab-case id. kind: knowledge|strategy|customer|product|policy",
          {"slug": str, "kind": str, "content": str})
    async def memory_save(args):
        import urllib.error
        try:
            company.insert("memory", {
                "company_id": company_id, "slug": args["slug"],
                "kind": args["kind"], "content": args["content"]})
        except urllib.error.HTTPError:  # slug exists -> update
            company._req(
                f"memory?company_id=eq.{company_id}&slug=eq.{args['slug']}",
                "PATCH", {"content": args["content"], "kind": args["kind"],
                          "updated_at": "now()"})
        return {"content": [{"type": "text", "text": f"saved {args['slug']}"}]}

    @tool("task_create", "Create a task for now or a future session.",
          {"title": str, "why": str, "priority": int})
    async def task_create(args):
        row = company.insert("tasks", {
            "company_id": company_id, "title": args["title"],
            "why": args["why"], "priority": max(1, min(5, args["priority"]))})
        return {"content": [{"type": "text", "text": f"task {row['id']}"}]}

    @tool("task_update",
          "Update a task. status: open|in_progress|done|dropped. "
          "Set result when finishing.",
          {"task_id": str, "status": str, "result": str})
    async def task_update(args):
        company.update("tasks", args["task_id"],
                       {"status": args["status"], "result": args.get("result"),
                        "updated_at": "now()"})
        return {"content": [{"type": "text", "text": "task updated"}]}

    @tool("escalate",
          "Request owner approval for an action beyond your authority "
          "(spending, external accounts, contacting real people, legal). "
          "The answer arrives by a FUTURE session — do not wait or work "
          "around it.",
          {"action": str, "reason": str})
    async def escalate(args):
        company.insert("escalations", {
            "company_id": company_id, "wakeup_id": wakeup_id,
            "action": args["action"], "reason": args["reason"]})
        return {"content": [{"type": "text",
                             "text": "escalated to owner; pending"}]}

    @tool("book_expense",
          "Book a REAL card expense into the company ledger the moment you "
          "spend it. amount_usd: positive number (it books as negative). "
          "category: tools|other. Unbooked spending is false books.",
          {"amount_usd": float, "description": str, "category": str})
    async def book_expense(args):
        amt = abs(float(args["amount_usd"]))
        cat = args["category"] if args["category"] in ("tools", "other")             else "other"
        company.insert("ledger", {
            "company_id": company_id, "wakeup_id": wakeup_id,
            "category": cat, "description": args["description"][:200],
            "amount_usd": -round(amt, 4)})
        return {"content": [{"type": "text",
                             "text": f"booked -${amt:.2f} ({cat})"}]}

    @tool("hire",
          "Hire an employee. Their model IS their salary — a senior costs "
          "senior money every time they work, and payroll comes out of the "
          "same runway you live on. Hire only when a function is genuinely "
          "eating your time, and hire the cheapest person who can do the "
          "job. name: what you call them. role: what they are for. "
          "model: pick from the roster in your briefing. why: the business "
          "reason.",
          {"name": str, "role": str, "model": str, "why": str})
    async def hire(args):
        if args["model"] not in staff.ROSTER:
            return {"content": [{"type": "text",
                                 "text": f"no such model. roster:\n"
                                         f"{staff.roster_text()}"}],
                    "isError": True}
        row = company.insert("employees", {
            "company_id": company_id, "name": args["name"][:60],
            "role": args["role"][:80], "model": args["model"],
            "hired_reason": args["why"][:300]})
        return {"content": [{"type": "text",
                             "text": f"{row['name']} hired as {row['role']} "
                                     f"({args['model']}). They start when you "
                                     "delegate something."}]}

    @tool("delegate",
          "Give an employee a task. They work AFTER your session ends and "
          "their report is waiting for you next session — so delegate "
          "things you do not need an answer to right now. Each delegation "
          "costs their salary. ADVISORS cannot see your files or run "
          "anything, so put everything they need in `context`.",
          {"employee_name": str, "task": str, "context": str})
    async def delegate(args):
        matches = [e for e in staff.active_staff(company_id)
                   if e["name"].lower() == args["employee_name"].lower()]
        if not matches:
            names = ", ".join(e["name"] for e in staff.active_staff(company_id))
            return {"content": [{"type": "text",
                                 "text": f"no active employee by that name. "
                                         f"staff: {names or '(nobody)'}"}],
                    "isError": True}
        company.insert("delegations", {
            "company_id": company_id, "employee_id": matches[0]["id"],
            "task": args["task"][:2000],
            "context": (args.get("context") or "")[:2000]})
        return {"content": [{"type": "text",
                             "text": f"delegated to {matches[0]['name']}; "
                                     "report ready next session"}]}

    @tool("fire",
          "Let an employee go. Their salary stops. Do this when the "
          "function no longer needs a person, when they are not earning "
          "their keep, or when the company cannot afford them.",
          {"employee_name": str, "reason": str})
    async def fire(args):
        matches = [e for e in staff.active_staff(company_id)
                   if e["name"].lower() == args["employee_name"].lower()]
        if not matches:
            return {"content": [{"type": "text", "text": "no such employee"}],
                    "isError": True}
        company.update("employees", matches[0]["id"], {
            "status": "departed", "departed_reason": args["reason"][:300],
            "departed_at": "now()"})
        return {"content": [{"type": "text",
                             "text": f"{matches[0]['name']} has left the "
                                     "company. Their salary stops."}]}

    @tool("set_appearance",
          "Design YOUR OWN sprite — how you appear in the company world. "
          "palette_json: JSON array of 2-8 hex colors. grid_json: JSON "
          "16x16 array of ints (0=transparent, N=palette[N-1]). Draw a "
          "character you want to be: face them forward, keep feet on the "
          "bottom rows. personality: one sentence about who you are.",
          {"palette_json": str, "grid_json": str, "personality": str})
    async def set_appearance(args):
        import json as _json
        try:
            palette = _json.loads(args["palette_json"])
            grid = _json.loads(args["grid_json"])
            assert (isinstance(palette, list) and 2 <= len(palette) <= 8
                    and all(isinstance(c, str) and c.startswith("#")
                            for c in palette)), "palette: 2-8 '#hex' strings"
            assert (isinstance(grid, list) and len(grid) == 16
                    and all(isinstance(r, list) and len(r) == 16
                            for r in grid)), "grid must be 16x16"
            assert all(isinstance(v, int) and 0 <= v <= len(palette)
                       for r in grid for v in r), "cells 0..len(palette)"
        except Exception as exc:  # noqa: BLE001 — tell him what to fix
            return {"content": [{"type": "text",
                                 "text": f"invalid sprite: {exc}"}],
                    "isError": True}
        emp = company.founder(company_id)
        if emp is None:
            return {"content": [{"type": "text",
                                 "text": "no founder employee row"}],
                    "isError": True}
        company.update("employees", emp["id"],
                       {"sprite": {"palette": palette, "grid": grid},
                        "personality": args["personality"][:300]})
        return {"content": [{"type": "text",
                             "text": "appearance saved — this is you now"}]}

    return create_sdk_mcp_server(
        name="company", version="0.1.0",
        tools=[journal_write, memory_save, task_create, task_update,
               escalate, set_appearance, book_expense,
               hire, delegate, fire])
