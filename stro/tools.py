"""Stro's company tools — the only way state changes, so every change is
attributable to a wake-up and visible to the owner."""
from claude_agent_sdk import create_sdk_mcp_server, tool

from . import company


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

    return create_sdk_mcp_server(
        name="company", version="0.1.0",
        tools=[journal_write, memory_save, task_create, task_update, escalate])
