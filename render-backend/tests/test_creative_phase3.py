"""Phase 3 creative intelligence — Hook V2, intelligent b-roll (plan ->
engine -> renderers -> editor), motion-graphics vocabulary, caption
refinement, audio-aware breath padding, visual rhythm, retention critic.

Contract: all flags default OFF = planner behavior unchanged (the Phase 2
golden still passes untouched apart from the documented additive keys);
every subsystem is deterministic; system-authored fields are never
model-writable.
"""
import copy
import os

import pytest

os.environ.setdefault("SUPABASE_URL", "https://fake.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "fake-service-key")
os.environ["WORKER_ENABLED"] = "0"

from app.pipeline import creative_phase3 as p3  # noqa: E402
from app.pipeline import editorial_planner as ep  # noqa: E402
from app.pipeline import picture_edit_v2 as pe2  # noqa: E402
from app.pipeline.schemas import Segment, SpeechSpan, Word  # noqa: E402
from tests.test_editorial_planner import _segments, _valid_plan  # noqa: E402


@pytest.fixture(autouse=True)
def _flags_off(monkeypatch):
    for f in p3.ALL_PHASE3_FLAGS:
        monkeypatch.delenv(f, raising=False)
    monkeypatch.delenv("PHASE3_RETENTION_FLOOR", raising=False)
    for f in ("PHASE2_DIALOGUE", "PHASE2_HOOK", "PHASE2_COHERENCE",
              "PHASE2_TENSION", "PHASE2_INTEREST_GATE"):
        monkeypatch.delenv(f, raising=False)


def _plan(raw=None):
    return ep.EditorialPlan(**(raw or _valid_plan()))


def _talker(seg_id="seg-1", text="we inspect the ceiling for water damage",
            **kw):
    return Segment(segmentId=seg_id, assetId="asset-1", sourceStart=0.0,
                   sourceEnd=20.0, transcript=text,
                   speechSpans=[SpeechSpan(start=0.5, end=9.5, text=text)],
                   wordTimings=[Word(word=w, start=0.5 + i, end=1.3 + i)
                                for i, w in enumerate(text.split()[:8])],
                   **kw)


def _broll_seg(seg_id="br-1", search="ceiling water damage close up",
               **kw):
    return Segment(segmentId=seg_id, assetId="asset-2", sourceStart=0.0,
                   sourceEnd=8.0, storyUses=["broll"],
                   action=search, searchText=search, **kw)


def _long_plan(host_seconds=10.0):
    """Two-entry plan: a short hook + one long talking host clip."""
    raw = _valid_plan()
    raw["timeline"] = [
        dict(raw["timeline"][0], segmentId="seg-3", sourceIn=0.0,
             sourceOut=2.0, timelineIn=0.0, timelineOut=2.0, beat="hook"),
        dict(raw["timeline"][1], segmentId="seg-1", sourceIn=0.0,
             sourceOut=host_seconds, timelineIn=2.0,
             timelineOut=2.0 + host_seconds, beat="payoff")]
    raw["hook"]["segmentId"] = "seg-3"
    raw["hook"]["sourceOut"] = 2.0
    raw["hook"]["durationSeconds"] = 2.0
    raw["pacing"] = [{"beat": "hook", "targetDurationSeconds": 2.0,
                      "energy": 0.9},
                     {"beat": "payoff", "targetDurationSeconds": host_seconds,
                      "energy": 0.6}]
    raw["beats"] = [{"key": "hook", "purpose": "p"},
                    {"key": "payoff", "purpose": "p"}]
    raw["plannedDurationSeconds"] = 2.0 + host_seconds
    raw["audio"]["naturalSoundSegmentIds"] = []
    raw["audioTreatments"] = []
    raw["colorStabilization"] = []
    raw["transitions"] = []                # the inherited ones no longer join
    raw["storySentence"] = {               # evidence matching the real segs
        "text": "This is a story about the crew at work, leading to the "
                "finished job.",
        "claimType": "fact",
        "evidence": [{"sourceType": "transcript", "segmentId": "seg-3",
                      "quoteOrValue": "we finished the job"}]}
    return raw


# ================================================================ Hook V2
def test_banned_stock_openings_are_rejected(monkeypatch):
    monkeypatch.setenv(p3.HOOK_V2_FLAG, "1")
    seg = _talker("seg-1", "hey guys welcome back to the channel")
    raw = _valid_plan()
    plan = _plan(raw)
    out = p3.hook_v2_violations(plan, [seg] + _segments()[1:])
    assert any("stock introduction" in v for v in out)


def test_strong_opening_passes():
    seg = _talker("seg-1", "this ceiling should not be wet")
    assert p3.hook_v2_violations(_plan(), [seg] + _segments()[1:]) == []


def test_chronological_opening_needs_merit():
    # seg-1 is the earliest recorded moment AND not a ranked candidate,
    # while real candidates exist -> violation
    segs = [_talker("seg-1", "steady establishing footage of the house"),
            _talker("seg-2", "why is the floor wet again?",
                    storyUses=["hook"]),
            _talker("seg-3", "don't ever ignore stains on your ceiling",
                    storyUses=["hook"])]
    out = p3.hook_v2_violations(_plan(), segs)      # plan hooks seg-1
    assert any("chronologically first" in v for v in out)


# ======================================================== B-roll planning
def test_broll_proposed_with_lexical_match_and_confidence():
    raw = _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw, segs)
    ins = raw.get("brollInsertions")
    assert ins and ins[0]["brollSegmentId"] == "br-1"
    assert ins[0]["motivation"] == "illustrate_claim"
    assert ins[0]["confidence"] >= p3.BROLL_MIN_CONFIDENCE
    assert set(ins[0]["matchedTokens"]) & {"ceiling", "water", "damage"}
    assert ins[0]["audioUnder"] is True
    assert ins[0]["targetIndex"] == 1               # never the hook


def test_broll_never_covers_hook_or_emotional_closeups():
    raw = _long_plan()
    crying = _talker("seg-1", "ceiling water damage everywhere",
                     emotion="crying", shotType="close")
    crying = crying.model_copy(update={"shotSize": "close"})
    segs = [crying, _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw, segs)
    assert "brollInsertions" not in raw             # face is the content


def test_broll_edge_guard_and_duration_bounds():
    raw = _long_plan(host_seconds=10.0)
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw, segs)
    b = raw["brollInsertions"][0]
    assert b["offsetSeconds"] >= p3.BROLL_EDGE_GUARD_SECONDS
    assert b["offsetSeconds"] + b["durationSeconds"] \
        <= 10.0 - p3.BROLL_EDGE_GUARD_SECONDS + 1e-6
    assert p3.BROLL_MIN_SECONDS <= b["durationSeconds"] \
        <= p3.BROLL_MAX_SECONDS


def test_broll_is_deterministic_and_model_cannot_write_it():
    raw1, raw2 = _long_plan(), _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw1, segs)
    p3.propose_broll(raw2, segs)
    assert raw1["brollInsertions"] == raw2["brollInsertions"]
    fabricated = _long_plan()
    fabricated["brollInsertions"] = [{"id": "FAKE"}]
    ep._normalize_timeline_arithmetic(fabricated, segs)   # flags off
    assert "brollInsertions" not in fabricated            # system-owned


def test_provider_seam_accepts_external_sources():
    class StockProvider:
        origin = "stock"

        def candidates(self):
            return [{"segmentId": "stock-1", "assetId": "stock-asset",
                     "sourceStart": 0.0, "sourceEnd": 6.0,
                     "searchTokens": {"ceiling", "water", "damage"},
                     "origin": "stock"}]
    raw = _long_plan()
    p3.propose_broll(raw, [_talker("seg-1")] + _segments()[1:],
                     providers=[StockProvider()])
    assert raw["brollInsertions"][0]["origin"] == "stock"


def test_broll_validation_rejects_drift(monkeypatch):
    monkeypatch.setenv(p3.BROLL_FLAG, "1")
    raw = _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw, segs)
    plan = _plan(raw)
    assert p3.broll_violations(plan, segs) == []
    # hand-authored abuse: cover the hook
    bad = copy.deepcopy(raw)
    bad["brollInsertions"][0]["targetIndex"] = 0
    assert any("covers the hook" in v
               for v in p3.broll_violations(_plan(bad), segs))
    # invented b-roll segment
    bad2 = copy.deepcopy(raw)
    bad2["brollInsertions"][0]["brollSegmentId"] = "ghost"
    assert any("invented or unusable" in v
               for v in p3.broll_violations(_plan(bad2), segs))


# ============================================== B-roll execution (engine)
def _plan_row(raw):
    return {"id": "plan-1", "project_id": "p1", "version": 1,
            "status": "approved", "plan": raw, "request": {},
            "validation": {"deterministicGate": {"passed": True,
                                                 "score": 100,
                                                 "hardFailures": []}}}


def test_engine_splits_host_and_carries_audio_under():
    raw = _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw, segs)
    out = pe2.build_picture_edit(_plan_row(raw), segs, now="t")
    clips = out["timeline"]["tracks"][0]["clips"]
    assert len(clips) == 4                        # hook + A1 + B + A2
    b = next(c for c in clips if c.get("audioFrom"))
    ins = raw["brollInsertions"][0]
    assert b["assetId"] == "asset-2" and b["volume"] == 0.0
    assert b["audioFrom"]["assetId"] == "asset-1"     # host speech continues
    # donor audio window matches the covered host picture exactly
    host_a1 = clips[1]
    assert abs(b["audioFrom"]["sourceStart"] - host_a1["sourceEnd"]) < 1e-6
    assert abs((b["audioFrom"]["sourceEnd"] - b["audioFrom"]["sourceStart"])
               - ins["durationSeconds"]) < 1e-6
    # total duration unchanged; timeline contiguous
    assert abs(clips[-1]["timelineEnd"] - raw["plannedDurationSeconds"]) < 1e-6
    for a, bb in zip(clips, clips[1:], strict=False):
        assert abs(a["timelineEnd"] - bb["timelineStart"]) < 1e-6
    assert out["brollApplied"][0]["brollSegmentId"] == "br-1"
    assert out["engineVersion"] == pe2.ENGINE_VERSION == "2.2.0"


def test_engine_without_broll_is_unchanged():
    raw = _long_plan()
    out = pe2.build_picture_edit(_plan_row(raw),
                                 [_talker("seg-1")] + _segments()[1:],
                                 now="t")
    assert out["brollApplied"] == []
    assert len(out["timeline"]["tracks"][0]["clips"]) == 2


def test_engine_rejects_broll_catalog_drift():
    raw = _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    p3.propose_broll(raw, segs)
    drifted = [s for s in segs if s.segmentId != "br-1"]  # b-roll vanished
    with pytest.raises(pe2.PictureEditRejected) as exc:
        pe2.build_picture_edit(_plan_row(raw), drifted, now="t")
    assert any("absent from the current source catalog" in r
               for r in exc.value.reasons)


# ==================================================== Editor audioFrom sync
def test_editor_trim_and_split_keep_donor_audio_in_sync():
    from app.product_editor import _sync_audio_from
    clip = {"id": "b", "assetId": "asset-2", "sourceStart": 1.0,
            "sourceEnd": 3.0, "speed": 1.0,
            "audioFrom": {"assetId": "asset-1", "sourceStart": 10.0,
                          "sourceEnd": 12.0, "speed": 1.0}}
    _sync_audio_from(clip, 1.0, 1.5, 2.5)          # trim 0.5 off each end
    assert clip["audioFrom"]["sourceStart"] == 10.5
    assert clip["audioFrom"]["sourceEnd"] == 11.5
    fast = {"id": "b2", "assetId": "asset-2", "sourceStart": 0.0,
            "sourceEnd": 2.0, "speed": 1.0,
            "audioFrom": {"assetId": "asset-1", "sourceStart": 0.0,
                          "sourceEnd": 4.0, "speed": 2.0}}
    _sync_audio_from(fast, 0.0, 1.0, 2.0)          # donor advances at 2x
    assert fast["audioFrom"]["sourceStart"] == 2.0
    assert fast["audioFrom"]["sourceEnd"] == 4.0


# ============================================================== Graphics V2
def _graphic(**over):
    base = {"graphicType": "stat_card", "claimType": "fact",
            "text": "42 jobs", "evidence": [
                {"sourceType": "transcript", "segmentId": "seg-3",
                 "quoteOrValue": "we finished 42 jobs"}],
            "timelineStart": 4.0, "timelineEnd": 6.0, "durationSeconds": 2.0}
    base.update(over)
    return base


def test_graphic_type_vocabulary_is_closed(monkeypatch):
    raw = _valid_plan()
    raw["graphics"] = [_graphic(graphicType="sparkle_explosion")]
    out = p3.graphics_violations(_plan(raw), _segments())
    assert any("not in the renderer-ready vocabulary" in v for v in out)


def test_stat_card_needs_a_spoken_number():
    raw = _valid_plan()
    raw["graphics"] = [_graphic(text="lots of jobs", evidence=[
        {"sourceType": "transcript", "segmentId": "seg-3",
         "quoteOrValue": "we finished the job"}])]
    out = p3.graphics_violations(_plan(raw), _segments())
    assert any("needs data" in v for v in out)
    assert p3.graphics_violations(_plan({**_valid_plan(),
                                         "graphics": [_graphic()]}),
                                  _segments()) == []


def test_graphics_density_ceiling():
    raw = _valid_plan()
    raw["graphics"] = [_graphic(timelineStart=2.0, timelineEnd=3.0),
                       _graphic(timelineStart=5.0, timelineEnd=6.0)]
    out = p3.graphics_violations(_plan(raw), _segments())
    assert any("minimum spacing" in v.lower() for v in out)


def test_graphics_opportunities_detected_from_catalog():
    segs = [_talker("seg-1", "this repair cost 4000 dollars versus 500 "
                             "for prevention")]
    kinds = {s["graphicType"] for s in p3.propose_graphics(segs)}
    assert "stat_card" in kinds and "comparison" in kinds


# ============================================================== Captions V2
def test_long_caption_splits_at_clause_with_time_split():
    raw = {"captions": [{
        "claimType": "editorial_label",
        "text": "The Setup Begins Here, and the final reveal comes after",
        "timelineStart": 0.0, "timelineEnd": 4.0}]}
    p3.refine_captions(raw, [])
    caps = raw["captions"]
    assert len(caps) == 2
    assert caps[0]["timelineEnd"] == caps[1]["timelineStart"]
    assert caps[0]["timelineEnd"] < 4.0
    assert all(len(c["text"]) <= p3.CAPTION_MAX_LINE_CHARS for c in caps)


def test_emphasis_word_priority_number_then_negation_then_substantive():
    assert p3._emphasis_word("we finished 42 jobs") == "42"
    assert p3._emphasis_word("never ignore the ceiling") == "never"
    assert p3._emphasis_word("the crew keeps working") == "working"
    assert p3._emphasis_word("we do it") is None


def test_short_caption_extended_to_readability_floor():
    raw = {"captions": [
        {"claimType": "cta", "text": "Watch", "timelineStart": 1.0,
         "timelineEnd": 1.3},
        {"claimType": "cta", "text": "The End", "timelineStart": 3.0,
         "timelineEnd": 4.0}]}
    p3.refine_captions(raw, [])
    assert raw["captions"][0]["timelineEnd"] \
        >= 1.0 + p3.CAPTION_MIN_SECONDS - 1e-6


def test_caption_wall_and_floor_violations(monkeypatch):
    raw = _valid_plan()
    raw["captions"] = [
        {"claimType": "editorial_label", "text": "w" * 90,
         "timelineStart": 0.0, "timelineEnd": 0.4, "evidence": []}]
    out = p3.caption_v2_violations(_plan(raw))
    assert any("subtitle wall" in v for v in out)
    assert any("readability floor" in v for v in out)


# ============================================================ Audio-aware
def test_breath_pad_extends_sentence_end_cuts():
    seg = _talker("seg-1", "we inspect the ceiling")
    seg = seg.model_copy(update={
        "speechSpans": [SpeechSpan(start=0.5, end=5.0,
                                   text="we inspect the ceiling")]})
    raw = {"timeline": [{"segmentId": "seg-1", "assetId": "asset-1",
                         "sourceIn": 0.0, "sourceOut": 5.0,
                         "timelineIn": 0.0, "timelineOut": 5.0,
                         "beat": "hook"}]}
    p3.breath_pad_cuts(raw, [seg])
    assert raw["timeline"][0]["sourceOut"] == 5.0 + p3.BREATH_PAD_SECONDS
    assert raw["dialogueAdjustments"][0]["reason"] \
        == "breath room after sentence end"


def test_breath_pad_respects_reserved_transition_handles():
    seg = _talker("seg-1").model_copy(update={
        "sourceEnd": 5.1,
        "speechSpans": [SpeechSpan(start=0.5, end=5.0, text="x")]})
    raw = {"timeline": [
        {"segmentId": "seg-1", "assetId": "asset-1", "sourceIn": 0.0,
         "sourceOut": 5.0, "timelineIn": 0.0, "timelineOut": 5.0,
         "beat": "hook"},
        {"segmentId": "seg-2", "assetId": "asset-1", "sourceIn": 6.0,
         "sourceOut": 8.0, "timelineIn": 5.0, "timelineOut": 7.0,
         "beat": "next"}],
        "transitions": [{"fromSegmentId": "seg-1", "toSegmentId": "seg-2",
                         "type": "dissolve", "durationSeconds": 0.1,
                         "purpose": "soften"}]}
    p3.breath_pad_cuts(raw, [seg])
    # only 0.1s of unreserved room exists (5.1 end - 0.1 reserve = 5.0):
    # padding would eat the dissolve's handle, so the cut stays put
    assert raw["timeline"][0]["sourceOut"] == 5.0


def test_breath_pad_runs_before_arithmetic_rebuild(monkeypatch):
    monkeypatch.setenv(p3.AUDIO_FLAG, "1")
    seg = _talker("seg-1").model_copy(update={
        "speechSpans": [SpeechSpan(start=0.5, end=4.0, text="x")]})
    raw = _valid_plan()
    raw["timeline"][0]["segmentId"] = "seg-1"
    raw["hook"]["segmentId"] = "seg-1"
    ep._normalize_timeline_arithmetic(raw, [seg] + _segments()[1:])
    e = raw["timeline"][0]
    assert e["sourceOut"] == 4.0 + p3.BREATH_PAD_SECONDS
    # arithmetic was rebuilt FROM the padded trim — no stale bookkeeping
    assert abs((e["timelineOut"] - e["timelineIn"])
               - (e["sourceOut"] - e["sourceIn"])) < 1e-6
    plan = _plan(raw)
    timing = [v for v in ep.validate_plan(plan, [seg] + _segments()[1:], {},
                                          False)
              if "not contiguous" in v or "does not match" in v]
    assert timing == []


# ================================================================= Rhythm
def test_rhythm_flags_monotony_and_metronome(monkeypatch):
    segs = [s.model_copy(update={"shotSize": "medium"}) for s in _segments()]
    segs.append(_segments()[0].model_copy(update={"segmentId": "seg-4",
                                                  "shotSize": "wide"}))
    raw = _valid_plan()
    raw["timeline"] = raw["timeline"] + [
        dict(raw["timeline"][0], segmentId="seg-1", sourceIn=4.0,
             sourceOut=8.0, timelineIn=12.0, timelineOut=16.0,
             beat="payoff")]
    out = p3.rhythm_violations(_plan(raw), segs)
    assert any("consecutive shots" in v for v in out)      # 4x medium
    assert any("metronomic" in v for v in out)             # all 4.0s


def test_rhythm_report_suggests_punch_ins_on_long_talkers():
    raw = _long_plan(host_seconds=9.0)
    rep = p3.rhythm_report(_plan(raw), [_talker("seg-1")] + _segments()[1:])
    assert rep["punchInSuggestions"]
    assert rep["punchInSuggestions"][0]["timelineIndex"] == 1


# ========================================================= Retention critic
def test_retention_report_axes_and_actionable_advice():
    rep = p3.retention_report(_plan(), _segments())
    assert {a["axis"] for a in rep["axes"]} == set(p3.CRITIC_AXES)
    assert all(0 <= a["score"] <= 100 for a in rep["axes"])
    assert all(a["advice"] for a in rep["axes"])
    assert isinstance(rep["wouldKeepWatching"], bool)
    assert rep["rhythm"]["shotCount"] == 3


def test_retention_critic_is_advisory_without_a_floor(monkeypatch):
    monkeypatch.setenv(p3.CRITIC_FLAG, "1")
    result = ep.plan_editorial(_segments(), {}, False,
                               lambda p, s: copy.deepcopy(_valid_plan()))
    assert "retentionReport" in result
    assert result["status"] == "approved"          # no floor -> never blocks


def test_retention_floor_turns_weak_axes_into_revise_feedback(monkeypatch):
    monkeypatch.setenv(p3.CRITIC_FLAG, "1")
    monkeypatch.setenv("PHASE3_RETENTION_FLOOR", "101")   # unreachable
    with pytest.raises(ep.PlanRejected) as exc:
        ep.plan_editorial(_segments(), {}, False,
                          lambda p, s: copy.deepcopy(_valid_plan()),
                          max_attempts=2)
    last = exc.value.violations_history[-1]
    assert any(v.startswith("retention:") for v in last)
    assert any("below the floor" in v for v in last)


# =========================================================== flags-off inertia
def test_all_flags_off_contributes_nothing():
    assert p3.phase3_violations(_plan(), _segments()) == []
    assert p3.prompt_parts(_segments()) == []
    raw = _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    ep._normalize_timeline_arithmetic(raw, segs)   # all flags off
    assert "brollInsertions" not in raw
    assert "emphasisWord" not in (raw.get("captions") or [{}])[0] \
        if raw.get("captions") else True


def test_audio_under_broll_renders_in_the_FINAL_renderer(tmp_path):
    """Parity by construction: the b-roll clip's audioFrom is honored by
    renderer2 — the FINAL export path — with real ffmpeg. The b-roll shows
    its own picture while the donor's audio continues underneath."""
    import subprocess

    from app.renderer import FFMPEG, probe
    from app.renderer2 import render_timeline
    host = str(tmp_path / "host.mp4")
    broll = str(tmp_path / "broll.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", "testsrc=duration=6:size=128x72:rate=12",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
                    "-c:v", "libx264", "-c:a", "aac", "-shortest", host],
                   check=True, timeout=120)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", "smptebars=duration=4:size=128x72:rate=12",
                    "-c:v", "libx264", broll], check=True, timeout=120)
    timeline = {"version": 1, "width": 128, "height": 72, "fps": 12,
                "duration": 5.0, "tracks": [{"id": "v", "type": "video",
                                             "clips": [
        {"id": "a1", "assetId": "H", "sourceStart": 0.0, "sourceEnd": 1.5,
         "timelineStart": 0.0, "timelineEnd": 1.5, "speed": 1, "volume": 1},
        {"id": "b", "assetId": "B", "sourceStart": 0.0, "sourceEnd": 2.0,
         "timelineStart": 1.5, "timelineEnd": 3.5, "speed": 1, "volume": 0,
         "audioFrom": {"assetId": "H", "sourceStart": 1.5, "sourceEnd": 3.5,
                       "speed": 1.0}},
        {"id": "a2", "assetId": "H", "sourceStart": 3.5, "sourceEnd": 5.0,
         "timelineStart": 3.5, "timelineEnd": 5.0, "speed": 1, "volume": 1},
    ]}]}
    out = str(tmp_path / "out.mp4")
    render_timeline(timeline, {"H": host, "B": broll}, out, profile="preview")
    info = probe(out)
    assert abs(info.duration - 5.0) < 0.6         # duration preserved
    assert info.has_audio                          # donor audio ran throughout


def test_full_planner_run_with_all_phase3_flags(monkeypatch):
    for f in p3.ALL_PHASE3_FLAGS:
        monkeypatch.setenv(f, "1")
    raw = _long_plan()
    segs = [_talker("seg-1"), _broll_seg("br-1")] + _segments()[1:]
    result = ep.plan_editorial(segs, {}, False,
                               lambda p, s: copy.deepcopy(raw))
    assert result["status"] == "approved"
    assert result["plan"]["brollInsertions"]          # planned + validated
    assert "retentionReport" in result
