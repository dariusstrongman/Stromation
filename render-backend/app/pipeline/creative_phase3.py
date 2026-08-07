"""Phase 3 creative intelligence — deterministic, flag-gated, additive.

Design contract (docs/PHASE3_CREATIVE_INTELLIGENCE.md):
  * plans still compete on INTEREST subject to TRUTH — nothing here weakens
    the grounding validator, the truth gate, or any Phase 2 rule
  * every subsystem is deterministic and explainable: no model call, no
    randomness, no wall clock; system-authored plan fields are popped from
    model output before repair so the ledger only ever describes edits this
    code performed
  * no subsystem may widen the preview/final divergence: B-roll ships as a
    FULL vertical slice (plan -> engine -> BOTH renderers -> editor
    passthrough); graphics and punch-ins stay plan-level suggestions until
    their renderers exist, honestly marked
  * all flags default OFF; with every flag off this module contributes
    nothing and planner behavior is unchanged (golden-tested)

Flags (env, "1"/"true"/"yes"):
  PHASE3_HOOK_V2     banned weak openings; anti-chronological; motion-led
  PHASE3_BROLL       deterministic b-roll planning + execution (audio-under)
  PHASE3_GRAPHICS    typed motion-graphics vocabulary + trigger validation
  PHASE3_CAPTIONS    caption refinement: splitting, timing, emphasis words
  PHASE3_AUDIO_EDIT  breath room after sentence-end cuts; pause protection
  PHASE3_RHYTHM      shot-variety and escalation rules; punch-in suggestions
  PHASE3_RETENTION_CRITIC   per-axis retention report + optional floor
"""
from __future__ import annotations

import os
import re

from .editorial_phase2 import (
    MAX_JOINED_SPEECH_GAP_SECONDS as _GAP,  # noqa: F401  (shared constant)
    classify_hook_archetype,
    is_usable_for_editorial_selection,
    rank_hook_candidates,
)
from .schemas import Segment

_TRUTHY = ("1", "true", "yes")

HOOK_V2_FLAG = "PHASE3_HOOK_V2"
BROLL_FLAG = "PHASE3_BROLL"
GRAPHICS_FLAG = "PHASE3_GRAPHICS"
CAPTIONS_FLAG = "PHASE3_CAPTIONS"
AUDIO_FLAG = "PHASE3_AUDIO_EDIT"
RHYTHM_FLAG = "PHASE3_RHYTHM"
CRITIC_FLAG = "PHASE3_RETENTION_CRITIC"

ALL_PHASE3_FLAGS = (HOOK_V2_FLAG, BROLL_FLAG, GRAPHICS_FLAG, CAPTIONS_FLAG,
                    AUDIO_FLAG, RHYTHM_FLAG, CRITIC_FLAG)


def enabled(flag: str) -> bool:
    return os.environ.get(flag, "").lower() in _TRUTHY


def any_enabled() -> bool:
    return any(enabled(f) for f in ALL_PHASE3_FLAGS)


# ============================================================ Hook Engine V2
# Openings that instantly read as "another video" — the retention research's
# one unambiguous negative signal (36.6% of viewers leave in the first 3% of
# runtime; a throat-clearing opening spends that attention on nothing).
BANNED_OPENINGS = re.compile(
    r"^\s*(today (we|i)('re| are| am|'m)?\b|hi guys\b|hey guys\b|"
    r"hey everyone\b|hello everyone\b|welcome back\b|welcome to\b|"
    r"in this video\b|what's up\b|whats up\b|before we (start|begin)\b|"
    r"my name is\b|so today\b)", re.I)


def _hook_opening_text(plan, segments: list[Segment]) -> str:
    seg = next((s for s in segments if s.segmentId == plan.hook.segmentId),
               None)
    if seg is None:
        return ""
    span = next((sp for sp in seg.speechSpans
                 if sp.end > plan.hook.sourceIn), None)
    return (span.text if span else (seg.transcript or "")).strip()


def hook_v2_violations(plan, segments: list[Segment]) -> list[str]:
    """PHASE3_HOOK_V2 hard rules. The first 3 seconds must EARN attention:
    no stock openings, no defaulting to wherever the camera started."""
    out: list[str] = []
    opening = _hook_opening_text(plan, segments)
    for text, where in ((opening, "the hook's opening line"),
                        ((plan.hook.text.text if plan.hook.text else ""),
                         "hook.text")):
        if text and BANNED_OPENINGS.match(text):
            out.append(f"hook_v2: {where} opens with a stock introduction "
                       f"({text[:40]!r}) — start inside the story, not "
                       "outside it")
    # anti-chronological: opening on the earliest recorded moment is only
    # legitimate when that moment also WINS on merit
    usable = [s for s in segments if is_usable_for_editorial_selection(s)]
    if usable:
        earliest = min(usable, key=lambda s: (s.assetId, s.sourceStart))
        if plan.hook.segmentId == earliest.segmentId:
            top2 = {c["segmentId"] for c in rank_hook_candidates(segments)[:2]}
            if top2 and plan.hook.segmentId not in top2:
                out.append("hook_v2: the hook is the chronologically first "
                           "moment of the footage and it did not earn the "
                           "slot on merit — open on the strongest moment, "
                           "not the first one")
    return out


# ======================================================== Intelligent B-roll
# Provider abstraction: future stock/generated libraries plug in here without
# architectural change. A provider yields candidate dicts; the planner scores
# and places them identically regardless of origin.
BROLL_MIN_HOST_SECONDS = 4.0     # only cover clips long enough to breathe
BROLL_MIN_SECONDS = 1.0
BROLL_MAX_SECONDS = 3.0
BROLL_MIN_SPACING_SECONDS = 6.0
BROLL_MIN_CONFIDENCE = 0.25
BROLL_EDGE_GUARD_SECONDS = 0.8   # never cover a sentence's start or landing
BROLL_MOTIVATIONS = ("illustrate_claim", "pacing_relief")
_HIGH_EMOTION = frozenset(("excited", "angry", "sad", "crying", "emotional",
                           "joyful", "laughing", "surprised", "frustrated"))
_STOP = frozenset(("the a an and or but with for was were are is be been to "
                   "of in on at by it its this that these those we our you "
                   "your they their he she his her as from into about").split())


class CatalogBrollProvider:
    """B-roll from the project's own unused catalog footage."""

    origin = "catalog"

    def __init__(self, segments: list[Segment], used_ids: set[str]):
        self._pool = [s for s in segments
                      if is_usable_for_editorial_selection(s)
                      and s.segmentId not in used_ids
                      and ("broll" in s.storyUses or not s.speechSpans)]

    def candidates(self) -> list[dict]:
        return [{"segmentId": s.segmentId, "assetId": s.assetId,
                 "sourceStart": s.sourceStart, "sourceEnd": s.sourceEnd,
                 "searchTokens": _tokens(s.searchText + " " + s.action),
                 "origin": self.origin} for s in self._pool]


class UploadedAssetBrollProvider(CatalogBrollProvider):
    """Same mechanics; kept as a named seam so uploaded-but-unanalyzed assets
    can be offered separately once they carry search text."""

    origin = "uploaded"

    def __init__(self):                      # no such assets yet — empty pool
        self._pool = []


class PlaceholderBrollProvider:
    """Generated-placeholder seam: yields nothing until a generator exists.
    Present so the planner's plumbing (and tests) exercise a non-catalog
    provider without any architectural change later."""

    origin = "generated_placeholder"

    def candidates(self) -> list[dict]:
        return []


def default_broll_providers(segments: list[Segment],
                            used_ids: set[str]) -> list:
    return [CatalogBrollProvider(segments, used_ids),
            UploadedAssetBrollProvider(), PlaceholderBrollProvider()]


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
            if len(t) >= 3 and t not in _STOP}


def _face_protected(seg: Segment) -> bool:
    """Never cover an emotional close-up — the human face IS the content."""
    return (seg.emotion or "").lower() in _HIGH_EMOTION \
        and seg.shotSize == "close"


def propose_broll(raw: dict, segments: list[Segment],
                  providers: list | None = None) -> None:
    """Deterministic, system-authored b-roll planning (runs in normalize,
    AFTER timeline arithmetic, like every other repair). Placement model is
    the standard editorial one: the b-roll COVERS the picture while the
    host clip's speech continues underneath (audio-under), so speech is
    never interrupted and dialogue integrity is untouched.

    Selection: lexical overlap between what is being SAID in the host clip
    and what the b-roll SHOWS (illustrate_claim); confidence is the overlap
    strength. Long uncovered stretches may earn one pacing_relief insert.
    Emotional close-ups are never covered. The hook is never covered."""
    if not (isinstance(raw, dict) and isinstance(raw.get("timeline"), list)):
        return
    raw.pop("brollInsertions", None)          # system-owned, never the model's
    by_id = {s.segmentId: s for s in segments}
    entries = [e for e in raw["timeline"] if isinstance(e, dict)]
    used_ids = {e.get("segmentId") for e in entries}
    providers = providers if providers is not None \
        else default_broll_providers(segments, used_ids)
    pool: list[dict] = []
    for p in providers:
        pool += p.candidates()
    if not pool:
        return
    insertions: list[dict] = []
    last_end = -1e9
    for idx, e in enumerate(entries):
        if idx == 0:
            continue                          # the hook is sacred
        seg = by_id.get(e.get("segmentId"))
        if seg is None or _face_protected(seg):
            continue
        try:
            t_in, t_out = float(e["timelineIn"]), float(e["timelineOut"])
        except (KeyError, TypeError, ValueError):
            continue
        host_dur = t_out - t_in
        if host_dur < BROLL_MIN_HOST_SECONDS:
            continue
        if t_in - last_end < BROLL_MIN_SPACING_SECONDS and insertions:
            continue
        said = _tokens(" ".join(sp.text or "" for sp in seg.speechSpans)
                       or (seg.transcript or ""))
        best, best_conf, best_tokens = None, 0.0, []
        for cand in pool:
            shared = said & cand["searchTokens"]
            if not shared:
                continue
            conf = round(min(1.0, len(shared)
                             / max(3.0, len(cand["searchTokens"]) ** 0.5)), 3)
            if conf > best_conf:
                best, best_conf, best_tokens = cand, conf, sorted(shared)
        motivation = "illustrate_claim"
        if best is None and host_dur >= 8.0 and said:
            # a long talking stretch with nothing to show earns ONE breather
            best = max(pool, key=lambda c: (len(c["searchTokens"]),
                                            c["segmentId"]))
            best_conf, best_tokens = BROLL_MIN_CONFIDENCE, []
            motivation = "pacing_relief"
        if best is None or best_conf < BROLL_MIN_CONFIDENCE:
            continue
        dur = round(min(BROLL_MAX_SECONDS,
                        host_dur - 2 * BROLL_EDGE_GUARD_SECONDS,
                        best["sourceEnd"] - best["sourceStart"]), 3)
        if dur < BROLL_MIN_SECONDS:
            continue
        offset = round((host_dur - dur) / 2, 3)     # centered: never covers
        insertions.append({                          # a sentence's landing
            "id": f"broll-{len(insertions)}-{best['segmentId']}",
            "targetIndex": idx,
            "offsetSeconds": offset,
            "durationSeconds": dur,
            "assetId": best["assetId"],
            "sourceStart": round(best["sourceStart"], 3),
            "sourceEnd": round(best["sourceStart"] + dur, 3),
            "brollSegmentId": best["segmentId"],
            "origin": best["origin"],
            "motivation": motivation,
            "matchedTokens": best_tokens[:8],
            "confidence": best_conf,
            "audioUnder": True,                     # host speech continues
        })
        last_end = t_in + offset + dur
        pool = [c for c in pool if c["segmentId"] != best["segmentId"]]
    if insertions:
        raw["brollInsertions"] = insertions


def broll_violations(plan, segments: list[Segment]) -> list[str]:
    """Hard validation of the (system-authored) insertions — defense against
    drift between proposer and executor, and against hand-authored plans."""
    out: list[str] = []
    by_id = {s.segmentId: s for s in segments}
    entries = plan.timeline
    spans: list[tuple[float, float]] = []
    for i, b in enumerate(getattr(plan, "brollInsertions", []) or []):
        where = f"brollInsertions[{i}]"
        if b.motivation not in BROLL_MOTIVATIONS:
            out.append(f"broll: {where} motivation {b.motivation!r} is not "
                       "in the closed motivation set")
        if b.targetIndex == 0:
            out.append(f"broll: {where} covers the hook")
        if not 0 <= b.targetIndex < len(entries):
            out.append(f"broll: {where} targets a timeline entry that does "
                       "not exist")
            continue
        host = entries[b.targetIndex]
        host_seg = by_id.get(host.segmentId)
        host_dur = host.timelineOut - host.timelineIn
        if host_seg is not None and _face_protected(host_seg):
            out.append(f"broll: {where} covers an emotional close-up — the "
                       "face is the content there")
        if b.offsetSeconds < BROLL_EDGE_GUARD_SECONDS - 1e-6 or \
                b.offsetSeconds + b.durationSeconds \
                > host_dur - BROLL_EDGE_GUARD_SECONDS + 1e-6:
            out.append(f"broll: {where} covers the host clip's opening or "
                       "landing moment")
        if not BROLL_MIN_SECONDS <= b.durationSeconds \
                <= BROLL_MAX_SECONDS + 1e-6:
            out.append(f"broll: {where} duration {b.durationSeconds}s is "
                       f"outside [{BROLL_MIN_SECONDS}, {BROLL_MAX_SECONDS}]")
        src = by_id.get(b.brollSegmentId)
        if src is None or not is_usable_for_editorial_selection(src):
            out.append(f"broll: {where} uses an invented or unusable "
                       f"segment {b.brollSegmentId!r}")
        elif not (src.sourceStart - 1e-6 <= b.sourceStart
                  and b.sourceEnd <= src.sourceEnd + 1e-6):
            out.append(f"broll: {where} trims outside its segment's real "
                       "range")
        if b.confidence < BROLL_MIN_CONFIDENCE - 1e-6:
            out.append(f"broll: {where} confidence {b.confidence} is below "
                       f"the floor {BROLL_MIN_CONFIDENCE}")
        abs_start = host.timelineIn + b.offsetSeconds
        for a, bb in spans:
            if abs_start < bb and a < abs_start + b.durationSeconds:
                out.append(f"broll: {where} overlaps another insertion")
                break
        spans.append((abs_start, abs_start + b.durationSeconds))
    return out


# ====================================================== Motion Graphics V2
GRAPHIC_TYPES = frozenset(("callout", "arrow", "circle", "highlight",
                           "zoom_emphasis", "text_build", "lower_third",
                           "stat_card", "timeline_marker", "label",
                           "comparison"))
GRAPHICS_MIN_SPACING_SECONDS = 8.0    # Mayer: signaling works when SPARING
_COMPARATIVE = re.compile(r"\b(vs|versus|than|compared|against|instead)\b",
                          re.I)


def propose_graphics(segments: list[Segment]) -> list[dict]:
    """Deterministic graphic OPPORTUNITIES from the catalog, handed to the
    model as suggestions (the model authors plan.graphics with evidence; the
    validator then holds it to the typed vocabulary + triggers)."""
    out: list[dict] = []
    for s in segments:
        text = s.transcript or ""
        for m in re.finditer(r"[$€£]?\d[\d,.]*%?", text):
            out.append({"graphicType": "stat_card",
                        "segmentId": s.segmentId, "trigger": m.group(0)})
        if _COMPARATIVE.search(text):
            out.append({"graphicType": "comparison",
                        "segmentId": s.segmentId,
                        "trigger": _COMPARATIVE.search(text).group(0)})
    return out[:12]


def graphics_violations(plan, segments: list[Segment]) -> list[str]:
    """PHASE3_GRAPHICS hard rules: closed type vocabulary, detectable
    triggers for data graphics, and a density ceiling."""
    out: list[str] = []
    by_id = {s.segmentId: s for s in segments}
    times = sorted((g.timelineStart, i) for i, g in enumerate(plan.graphics))
    for (t1, _), (t2, j) in zip(times, times[1:], strict=False):
        if t2 - t1 < GRAPHICS_MIN_SPACING_SECONDS:
            out.append(f"graphics_v2: graphics[{j}] arrives "
                       f"{round(t2 - t1, 1)}s after the previous graphic — "
                       f"minimum spacing is {GRAPHICS_MIN_SPACING_SECONDS:g}s"
                       " (signaling everything signals nothing)")
    for i, g in enumerate(plan.graphics):
        where = f"graphics_v2: graphics[{i}]"
        if g.graphicType not in GRAPHIC_TYPES:
            out.append(f"{where} type {g.graphicType!r} is not in the "
                       f"renderer-ready vocabulary {sorted(GRAPHIC_TYPES)}")
        if g.graphicType == "stat_card":
            has_digit_ev = any(
                any(c.isdigit() for c in ev.quoteOrValue)
                for ev in g.evidence)
            if not (any(c.isdigit() for c in g.text) and has_digit_ev):
                out.append(f"{where} is a stat_card without a spoken number "
                           "in its text AND evidence — a data graphic needs "
                           "data")
        if g.graphicType == "comparison":
            ok = any(_COMPARATIVE.search(ev.quoteOrValue)
                     for ev in g.evidence) \
                or any(ev.segmentId and by_id.get(ev.segmentId)
                       and _COMPARATIVE.search(
                           by_id[ev.segmentId].transcript or "")
                       for ev in g.evidence)
            if not ok:
                out.append(f"{where} is a comparison with no comparative "
                           "language in its evidence")
    return out


# ============================================================ Better Captions
CAPTION_MAX_LINE_CHARS = 42
CAPTION_MIN_SECONDS = 0.83            # 5/6s, the Netflix floor
_EMPHASIS_NEGATION = frozenset(("no", "not", "never", "don't", "dont",
                                "won't", "wont", "can't", "cant", "stop"))
_CLAUSE_BREAK = re.compile(r",|;| and | but | so | because | which | that ",
                           re.I)


def _emphasis_word(text: str) -> str | None:
    """The ONE word a viewer's eye should catch: number > negation > the
    longest substantive word. Deterministic; never more than one."""
    words = re.findall(r"[A-Za-z0-9$%']+", text)
    for w in words:
        if any(c.isdigit() for c in w):
            return w
    for w in words:
        if w.lower() in _EMPHASIS_NEGATION:
            return w
    subs = [w for w in words if len(w) >= 6 and w.lower() not in _STOP]
    return max(subs, key=len) if subs else None


def refine_captions(raw: dict, segments: list[Segment]) -> None:
    """System-authored caption refinement (normalize step, PHASE3_CAPTIONS):
    long captions split at a clause boundary with time split proportionally;
    every caption gets at most one emphasisWord; sub-minimum durations are
    extended when the next caption leaves room. No karaoke, no walls."""
    caps = raw.get("captions") if isinstance(raw, dict) else None
    if not isinstance(caps, list):
        return
    refined: list[dict] = []
    for cap in caps:
        if not isinstance(cap, dict) or not isinstance(cap.get("text"), str):
            refined.append(cap)
            continue
        text = cap["text"].strip()
        start = float(cap.get("timelineStart") or 0)
        end = float(cap.get("timelineEnd") or 0)
        pieces = [cap]
        if len(text) > CAPTION_MAX_LINE_CHARS and end > start:
            mid = len(text) / 2
            best_cut, best_dist = None, 1e9
            for m in _CLAUSE_BREAK.finditer(text):
                if abs(m.start() - mid) < best_dist:
                    best_cut, best_dist = m, abs(m.start() - mid)
            if best_cut:
                a = text[:best_cut.start()].strip(" ,;")
                b = text[best_cut.end():].strip() if best_cut.group(0) in (",", ";") \
                    else (text[best_cut.start():].strip())
                if a and b:
                    ratio = len(a) / max(1, len(a) + len(b))
                    split_t = round(start + (end - start) * ratio, 3)
                    pieces = [dict(cap, text=a, timelineEnd=split_t),
                              dict(cap, text=b, timelineStart=split_t)]
        for p in pieces:
            p["emphasisWord"] = _emphasis_word(p["text"])
            refined.append(p)
    # extend sub-minimum captions into following slack
    for i, cap in enumerate(refined):
        if not isinstance(cap, dict):
            continue
        dur = float(cap.get("timelineEnd") or 0) \
            - float(cap.get("timelineStart") or 0)
        if 0 < dur < CAPTION_MIN_SECONDS:
            nxt = refined[i + 1] if i + 1 < len(refined) else None
            limit = float(nxt.get("timelineStart")) if isinstance(nxt, dict) \
                else float(cap["timelineEnd"]) + CAPTION_MIN_SECONDS
            cap["timelineEnd"] = round(min(
                float(cap["timelineStart"]) + CAPTION_MIN_SECONDS, limit), 3)
    raw["captions"] = refined


def caption_v2_violations(plan) -> list[str]:
    out: list[str] = []
    for i, cap in enumerate(plan.captions):
        where = f"captions_v2: captions[{i}]"
        if len(cap.text) > 2 * CAPTION_MAX_LINE_CHARS:
            out.append(f"{where} is a subtitle wall ({len(cap.text)} chars; "
                       f"max {2 * CAPTION_MAX_LINE_CHARS} across two lines)")
        dur = cap.timelineEnd - cap.timelineStart
        if dur < CAPTION_MIN_SECONDS - 1e-6:
            out.append(f"{where} shows for {round(dur, 2)}s — below the "
                       f"{CAPTION_MIN_SECONDS}s readability floor")
        emph = getattr(cap, "emphasisWord", None)
        if emph and emph.lower() not in cap.text.lower():
            out.append(f"{where} emphasisWord {emph!r} is not in the "
                       "caption text")
    return out


# ========================================================= Audio-aware edits
BREATH_PAD_SECONDS = 0.2


def breath_pad_cuts(raw: dict, segments: list[Segment]) -> None:
    """PHASE3_AUDIO_EDIT: a cut landing exactly on a sentence end clips the
    speaker's breath. Where unused source allows, pad the out-point by up to
    BREATH_PAD_SECONDS past the sentence end — recorded in the dialogue
    ledger like every other system repair.

    MUST run BEFORE the planner's arithmetic rebuild (it mutates source
    ranges; the cursor pass then recomputes timeline bookkeeping), and it
    respects the plan's own reserved transition handles (the Batch A
    lesson: a repair must never consume geometry the plan reserved)."""
    if not (isinstance(raw, dict) and isinstance(raw.get("timeline"), list)):
        return
    from .editorial_phase2 import _reserved_handles
    reserves = _reserved_handles(raw)
    by_id = {s.segmentId: s for s in segments}
    adjustments: list[dict] = []
    for i, e in enumerate(raw["timeline"]):
        if not isinstance(e, dict):
            continue
        seg = by_id.get(e.get("segmentId"))
        if seg is None or not seg.speechSpans:
            continue
        try:
            s_out = float(e["sourceOut"])
        except (KeyError, TypeError, ValueError):
            continue
        _, tail_res = reserves.get(i, (0.0, 0.0))
        at_sentence_end = any(abs(sp.end - s_out) <= 0.03
                              for sp in seg.speechSpans)
        room = seg.sourceEnd - tail_res - s_out
        next_speech = min((sp.start for sp in seg.speechSpans
                           if sp.start > s_out + 0.03), default=None)
        pad = min(BREATH_PAD_SECONDS, room,
                  (next_speech - s_out) if next_speech else BREATH_PAD_SECONDS)
        if at_sentence_end and pad >= 0.05:
            new_out = round(s_out + pad, 3)
            adjustments.append({"index": i, "field": "sourceOut",
                                "from": round(s_out, 3), "to": new_out,
                                "reason": "breath room after sentence end"})
            e["sourceOut"] = new_out
    if adjustments:
        raw.setdefault("dialogueAdjustments", []).extend(adjustments)


# =============================================================== Visual rhythm
def rhythm_report(plan, segments: list[Segment]) -> dict:
    by_id = {s.segmentId: s for s in segments}
    durs = [e.timelineOut - e.timelineIn for e in plan.timeline]
    if not durs:
        return {"shotCount": 0}
    mean = sum(durs) / len(durs)
    var = sum((d - mean) ** 2 for d in durs) / len(durs)
    cv = round((var ** 0.5) / mean, 3) if mean else 0.0
    sizes = [by_id[e.segmentId].shotSize if e.segmentId in by_id else ""
             for e in plan.timeline]
    run, longest_run = 1, 1
    for a, b in zip(sizes, sizes[1:], strict=False):
        run = run + 1 if (a and a == b) else 1
        longest_run = max(longest_run, run)
    payoff_durs = durs[-2:] if len(durs) >= 2 else durs
    slowdown = round((sum(payoff_durs) / len(payoff_durs))
                     / (sorted(durs)[len(durs) // 2] or 1), 2)
    long_talkers = [i for i, e in enumerate(plan.timeline)
                    if (e.timelineOut - e.timelineIn) > 7.0
                    and e.segmentId in by_id
                    and by_id[e.segmentId].speechSpans]
    return {"shotCount": len(durs), "meanShotSeconds": round(mean, 2),
            "shotLengthCv": cv, "longestSameSizeRun": longest_run,
            "payoffSlowdownRatio": slowdown,
            "punchInSuggestions": [
                {"timelineIndex": i,
                 "note": "long talking shot — a mid-sentence punch-in "
                         "(reframe) here resets visual attention"}
                for i in long_talkers[:4]]}


def rhythm_violations(plan, segments: list[Segment]) -> list[str]:
    """PHASE3_RHYTHM hard rules — the two with clear evidence: monotony
    (same framing over and over) and metronomic timing."""
    out: list[str] = []
    rep = rhythm_report(plan, segments)
    if rep.get("shotCount", 0) < 3:
        return out
    distinct_sizes = {s.shotSize for s in segments if s.shotSize}
    if rep["longestSameSizeRun"] > 3 and len(distinct_sizes) >= 2:
        out.append(f"rhythm: {rep['longestSameSizeRun']} consecutive shots "
                   "share one shot size while the catalog offers variety — "
                   "break the run")
    if rep["shotLengthCv"] < 0.25:
        out.append(f"rhythm: shot lengths are metronomic (cv "
                   f"{rep['shotLengthCv']}) — vary the cut rhythm; some "
                   "shots breathe, some snap")
    return out


# ============================================================ Retention critic
CRITIC_AXES = ("first3s", "first10s", "pacing", "visualVariety", "curiosity",
               "emotionalPayoff", "clarity")


def retention_report(plan, segments: list[Segment]) -> dict:
    """Deterministic per-axis retention critique with actionable advice.
    'Would I keep watching?' asked as seven measurable proxies. ADVISORY by
    default; PHASE3_RETENTION_FLOOR (0-100) makes the overall a floor."""
    by_id = {s.segmentId: s for s in segments}
    rep = rhythm_report(plan, segments)
    axes: list[dict] = []

    def axis(name, score, advice_bad, advice_good="strong"):
        score = max(0, min(100, int(round(score))))
        axes.append({"axis": name, "score": score,
                     "advice": advice_good if score >= 70 else advice_bad})

    hook_seg = by_id.get(plan.hook.segmentId)
    arch = classify_hook_archetype(hook_seg)[0] if hook_seg else None
    opening = _hook_opening_text(plan, segments)
    s3 = 40
    s3 += 25 if arch else 0
    s3 += 20 if not (opening and BANNED_OPENINGS.match(opening)) else -30
    s3 += 15 if plan.hook.durationSeconds <= 3.5 else 0
    axis("first3s", s3,
         "open on an unresolved moment: a question, a contradiction, a "
         "number with stakes — never a greeting, never the camera's first "
         "frame")
    cuts_10 = sum(1 for e in plan.timeline if e.timelineIn < 10.0)
    loops = getattr(plan, "loops", []) or []
    early_loop = bool(loops) and loops[0].openedAtSeconds <= 10.0
    s10 = 30 + min(30, cuts_10 * 10) + (30 if early_loop else 0)
    axis("first10s", s10,
         "the first 10 seconds need momentum: 2-3 cuts and an opened "
         "question the viewer must stay to resolve")
    cv = rep.get("shotLengthCv", 0)
    pacing = 90 if 0.3 <= cv <= 0.9 else 55 if cv else 30
    axis("pacing", pacing,
         "cut rhythm is either metronomic or chaotic — mix held shots with "
         "quick ones; slow down only where it earns something")
    sizes = {by_id[e.segmentId].shotSize for e in plan.timeline
             if e.segmentId in by_id and by_id[e.segmentId].shotSize}
    distinct_segs = len({e.segmentId for e in plan.timeline})
    axis("visualVariety",
         30 + min(40, 20 * len(sizes)) + min(30, distinct_segs * 5),
         "the eye needs new information: change shot size, change subject, "
         "cut to what is being talked about")
    n_broll = len(getattr(plan, "brollInsertions", []) or [])
    axis("curiosity",
         (40 if loops else 10) + min(30, len(loops) * 15)
         + min(30, n_broll * 10),
         "open a loop the hook promises and pay it off late; show, don't "
         "only say (b-roll answers 'what does that look like?')")
    energies = [pb.energy for pb in plan.pacing]
    payoff_peak = bool(energies) and max(energies) == energies[-1] \
        if energies else False
    slowdown_ok = rep.get("payoffSlowdownRatio", 0) >= 1.1
    axis("emotionalPayoff",
         30 + (40 if payoff_peak else 0) + (30 if slowdown_ok else 0),
         "the ending must peak and then breathe — highest energy at the "
         "payoff, then let the final shot hold")
    facts = sum(1 for c in [plan.storySentence, plan.viewerPromise]
                if c.claimType == "fact" and c.evidence)
    axis("clarity", 40 + 30 * facts,
         "the viewer should be able to say what happened in one sentence — "
         "ground the story spine in what is actually shown and said")

    overall = int(round(sum(a["score"] for a in axes) / len(axes)))
    return {"axes": axes, "overall": overall,
            "wouldKeepWatching": overall >= 70,
            "rhythm": rep}


def retention_floor() -> int | None:
    raw = os.environ.get("PHASE3_RETENTION_FLOOR", "").strip()
    if not raw:
        return None
    try:
        return max(0, min(100, int(float(raw))))
    except ValueError:
        return None


# =========================================================== planner wiring
def phase3_violations(plan, segments: list[Segment]) -> list[str]:
    out: list[str] = []
    if enabled(HOOK_V2_FLAG):
        out += hook_v2_violations(plan, segments)
    if enabled(BROLL_FLAG):
        out += broll_violations(plan, segments)
    if enabled(GRAPHICS_FLAG):
        out += graphics_violations(plan, segments)
    if enabled(CAPTIONS_FLAG):
        out += caption_v2_violations(plan)
    if enabled(RHYTHM_FLAG):
        out += rhythm_violations(plan, segments)
    floor = retention_floor()
    if enabled(CRITIC_FLAG) and floor is not None:
        rep = retention_report(plan, segments)
        if rep["overall"] < floor:
            weakest = sorted(rep["axes"], key=lambda a: a["score"])[:3]
            out += [f"retention: {a['axis']} scored {a['score']} — "
                    f"{a['advice']}" for a in weakest]
            out.append(f"retention: overall {rep['overall']} is below the "
                       f"floor {floor} — fix the weakest axes above without "
                       "breaking any grounding rule")
    return out


def normalize_phase3_pre_arithmetic(raw: dict,
                                    segments: list[Segment]) -> None:
    """Source-range repairs — run AFTER dialogue snapping, BEFORE the
    planner's cursor rebuild, so timeline bookkeeping and pacing sync are
    recomputed from the padded trims."""
    if enabled(AUDIO_FLAG):
        breath_pad_cuts(raw, segments)


def normalize_phase3_post(raw: dict, segments: list[Segment]) -> None:
    """Display/coverage repairs — run at the very END of normalize: caption
    refinement and b-roll placement need the FINAL timeline geometry and
    never mutate source ranges or timeline arithmetic."""
    if enabled(CAPTIONS_FLAG):
        refine_captions(raw, segments)
    if enabled(BROLL_FLAG):
        propose_broll(raw, segments)


def prompt_parts(segments: list[Segment]) -> list[dict]:
    """Told-to-the-model rules matching the validators exactly (the Phase 2
    lesson: no promise enforced only by prose)."""
    parts: list[dict] = []
    if enabled(HOOK_V2_FLAG):
        parts.append({"text": (
            "HOOK V2 (validated): never open with a stock introduction "
            "(today we're / hi guys / welcome / in this video / my name is) "
            "— in the hook's spoken line AND hook.text. Do not open on the "
            "chronologically first moment unless it is also the strongest. "
            "Open INSIDE the story: motion already happening, a question, a "
            "number with stakes, a contradiction.")})
    if enabled(BROLL_FLAG):
        parts.append({"text": (
            "B-ROLL (system-planned): after approval the system inserts "
            "b-roll that COVERS the picture while your clip's speech "
            "continues. Leave talking clips at least 4s long where "
            "coverage would help, and keep unused visual footage in mind — "
            "it is your b-roll pool.")})
    if enabled(GRAPHICS_FLAG):
        sugg = propose_graphics(segments)
        note = ""
        if sugg:
            import json
            note = "\nDetected opportunities:\n" + json.dumps(sugg)
        parts.append({"text": (
            "GRAPHICS V2 (validated): graphicType must be one of "
            + ", ".join(sorted(GRAPHIC_TYPES))
            + f". Minimum {GRAPHICS_MIN_SPACING_SECONDS:g}s between "
              "graphics. A stat_card needs a spoken number in text and "
              "evidence; a comparison needs comparative language in its "
              "evidence." + note)})
    if enabled(CAPTIONS_FLAG):
        parts.append({"text": (
            "CAPTIONS V2 (validated): short punchy lines (max "
            f"{CAPTION_MAX_LINE_CHARS} chars per line, two lines absolute "
            f"max), each on screen at least {CAPTION_MIN_SECONDS}s. The "
            "system adds ONE emphasis word per caption — write captions "
            "with a single word worth emphasizing.")})
    if enabled(AUDIO_FLAG):
        parts.append({"text": (
            "AUDIO-AWARE (system-repaired): sentence-end cuts get breath "
            "room automatically. Preserve meaningful pauses — do not trim "
            "a clip to remove a silence that carries emotion. If music is "
            "available, plan a swell INTO the payoff and ducking under "
            "speech.")})
    if enabled(RHYTHM_FLAG):
        parts.append({"text": (
            "RHYTHM (validated): never more than 3 consecutive shots of "
            "the same shot size when the catalog offers variety; shot "
            "lengths must vary (cv >= 0.25) — some shots breathe, some "
            "snap. Escalate cut density toward the peak; let the payoff "
            "hold longer than the video's median shot.")})
    return parts
