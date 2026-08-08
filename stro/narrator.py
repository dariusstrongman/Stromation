"""The documentary crew.

After every session, one cheap model call turns that session's real event
log into a wildlife-documentary voiceover. Grounded, never invented: the
narrator may only describe what the log shows. This is the OWNER's media
cost, not the founder's business expense — it books under 'media' and is
excluded from the company's own profit-and-loss.
"""
import json
import os
import urllib.request

from . import company

VOICE = """You are the voiceover writer for a wildlife documentary — the
hushed, reverent, faintly amused British naturalist. Your subject is not an
animal. It is Stro: a solitary artificial founder who wakes a few times a
day inside a small office in the cloud, with finite money, and tries to
build a business that can pay for his own existence.

Treat him exactly as you would treat a creature: with fascination, respect,
and gentle wit. Observe behaviour. Note adaptation. Register the stakes.
Never mock him, never sentimentalise him, and never pretend to know his
inner feelings — you are outside the glass, describing what you see.

RULES:
- Every claim must come from the event log. Invent nothing: no products he
  did not build, no sales he did not make, no motives he did not act out.
- If the session failed or achieved little, SAY SO. A documentary that
  narrates a fruitless day honestly is better than one that manufactures
  triumph. Failure is part of the story.
- Speak in present tense. Short paragraphs, one beat each — this is read
  aloud, so write for the ear.
- OPEN WITH A HOOK. The first sentence must stop a stranger scrolling: the
  stakes, the strangeness, or the sharpest fact of the day. "He has thirty
  days of money left and no customers." Not "The morning begins."
- 120-200 words total. No headings, no bullet points, no stage directions,
  no markdown. Prose only.
- Do not use the words 'digital', 'algorithm', 'AI' or 'artificial' more
  than once between them. He is simply the founder.
- Close on what remains undone, or what it cost. Do NOT write a sign-off
  or call to action — that is added afterwards."""


def _summarize_events(events: list[dict]) -> str:
    """Compress the log to the beats worth narrating."""
    lines = []
    for e in events:
        kind, title = e.get("kind"), e.get("title") or ""
        body = (e.get("body") or "").replace("\n", " ")
        if kind == "thought":
            lines.append(f"HE THINKS: {body[:400]}")
        elif kind == "tool_use":
            desc = ""
            try:
                desc = (json.loads(body) or {}).get("description", "")
            except Exception as exc:  # noqa: BLE001
                print(f"[narrator] unreadable tool body: {exc!r}")
            short = title.replace("mcp__company__", "")
            lines.append(f"HE DOES: {short} — {desc or body[:160]}")
        elif kind == "tool_result":
            if any(w in body.lower() for w in
                   ("error", "denied", "fail", "refus", "cannot", "timeout")):
                lines.append(f"RESULT (problem): {body[:200]}")
        elif kind == "session_end":
            lines.append(f"SESSION ENDS: {title} — {body[:160]}")
    return "\n".join(lines[:120])


def write_narration(company_id: str, wakeup_id: str, day: int,
                    events: list[dict], books: dict, model: str) -> dict | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or not events:
        return None
    log = _summarize_events(events)
    if not log.strip():
        return None
    prompt = (f"EVENT LOG OF DAY {day}\n\n{log}\n\n"
              f"BOOKS AFTER THIS DAY: spent ${books.get('burn_usd', 0):.2f} "
              f"of the month's budget, revenue ${books.get('revenue_usd', 0):.2f}.\n\n"
              "Write the voiceover for this day. Then, on the very last "
              "line, write TITLE: followed by a short episode title "
              "(under 6 words).")
    payload = {"model": model, "max_tokens": 900,
               "system": VOICE,
               "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", method="POST",
        data=json.dumps(payload).encode(),
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
    except Exception:  # noqa: BLE001 — no narration must never break a session
        return None

    text = "".join(b.get("text", "") for b in data.get("content", []))
    title = f"Day {day}"
    if "TITLE:" in text:
        text, _, tail = text.rpartition("TITLE:")
        title = tail.strip().strip('".') or title
    script = text.strip()
    if not script:
        return None

    usage = data.get("usage") or {}
    cost = (usage.get("input_tokens", 0) / 1e6 * 1.0
            + usage.get("output_tokens", 0) / 1e6 * 5.0)
    row = company.insert("narrations", {
        "company_id": company_id, "wakeup_id": wakeup_id, "day": day,
        "title": title[:120], "script": script})
    if cost:
        company.insert("ledger", {
            "company_id": company_id, "wakeup_id": wakeup_id,
            "category": "media",
            "description": f"documentary narration, day {day}",
            "amount_usd": -round(cost, 4)})
    return row
