# Stromation — Main Branch Architecture

> **Living document for engineers (human and AI).** Describes exactly what is on
> `main` right now — not plans, not feature branches. Update this file after every
> major merge. Last synchronized: **2026-08-05, main = `39c1c3c`**
> ("fix(planner): caption 90-char limit on the wire").
>
> Audience: a senior engineer (or an AI session) who has never seen this repo and
> needs to make a correct change today. Nothing here is customer documentation.

---

## High Level Architecture

Stromation is an AI-first video product: a customer uploads raw phone footage and
gets back a finished, professionally-cut video. One repo holds three deployables:

| Piece | Tech | Hosting | URL |
|---|---|---|---|
| Marketing site | static HTML (repo root) | GitHub Pages | stromation.com |
| Customer app | React + Vite SPA (`app/`) | Vercel (auto-deploy on push to main) | app.stromation.com |
| Render backend | FastAPI + FFmpeg (`render-backend/`) | Railway (auto-deploy on push to main) | api.stromation.com |
| Database/Auth/Storage | Supabase project "Stromation" (`iadzcnzgbtuigyodeqas`) | Supabase cloud | — |

**Merging to `main` deploys immediately** (Railway + Vercel both track main).
Therefore: apply Supabase migrations BEFORE merging backend code that needs them.
Safe order: migrations → backend deploy → frontend deploy → smoke test.

### The production pipeline

```
Upload (browser → S3 multipart, presigned; legacy assets in Supabase Storage)
  ↓
Analysis  (pipeline_jobs kind=analysis)
  probe → proxy → scenes → mechanical → audio → transcript → semantic → motion → catalog
  produces: asset_analysis artifacts + canonical `segments` catalog
  ↓
Editorial Planner  (kind=editorial_plan — ONLY when PICTURE_EDIT_ENGINE_V2_ENABLED)
  Gemini writes an evidence-grounded EditorialPlan; a deterministic validator +
  scoring gate approves/rejects it; approved plans land in `editorial_plans`
  ↓
Picture Edit Engine  (kind=autoedit)
  V2 (flag on): pure-deterministic build_picture_edit() compiles the approved plan
    against the segment catalog into a timeline; picture_render_v2 renders a preview
  V1/legacy (flag off): planner/selector/critic/revision loop (autoedit.py)
  ↓
Bridge  (autoedit_bridge.py, runs inside the autoedit job)
  wraps the picture edit in the audiovisual ancestry chain:
  preproduction_run → picture_edit_run → bridged candidate_run (+ preview upload)
  ↓
Product Editor  (editor_documents + editor_operations)
  the customer-facing immutable editing document; tracks: picture / captions /
  music / sfx / graphics; all changes are versioned OperationBatches
  ↓
Final Render  (kind=final_render with params.editor_document_id)
  handle_product_editor_render compiles the document → FFmpeg → export upload
  ↓
Export / Download
  private object in `exports` (Supabase) or S3 (EXPORT_STORAGE_PROVIDER=s3),
  served to the owner via short-lived signed URLs
```

**What each stage actually does**

- **Upload** — browser calls `/projects/{id}/raw-uploads/initiate` → backend mints
  presigned S3 multipart part-URLs (`sign-parts`) → browser PUTs parts directly to
  S3 → `complete` finishes the multipart → `finalize` validates (ffprobe, size,
  ownership) and creates the `media_assets` row **server-side** (service role only;
  clients cannot forge storage provenance). Legacy path: direct Supabase Storage
  upload to `raw-footage` (existing rows keep `storage_provider='supabase'`).
- **Analysis** — resumable, stage-based (`pipeline/runner.py`). Every stage writes
  an inspectable `asset_analysis` artifact; completed stages are skipped on re-run.
  Ends by merging everything into versioned `Segment` records (the "catalog") —
  the single source of truth about what footage exists. **No stage ever invents
  footage.**
- **Editorial Planner** — a separate structured *planning* stage (no FFmpeg, no
  rendering). Produces a strict-JSON `EditorialPlan`: ordered story sections with
  per-clip evidence references into the catalog, requested durations, transitions
  (closed enum), and grounded text. Validated deterministically; scored by
  `deterministic_gate()` (rules sum to 100, approval threshold 80, hard failures
  cannot be overridden by the model's self-assessment). Bounded 3-attempt revise
  loop. Honest `insufficient_footage` rejection with computed-achievable data.
- **Picture Edit Engine V2** — `build_picture_edit(plan_row, segments, now=)` is a
  **pure function**: same plan + same catalog → identical timeline and identical
  `deterministicHash`. No LLM. Executable transitions render via xfade; anything
  the renderer can't do yet is recorded in `pending_renderer_support` — never
  silently substituted.
- **Bridge** — gives the V2 (or legacy) picture edit a real ancestry so the
  Product Editor and all downstream audio/graphics stages can attach to it.
  Deterministic ids (`uuid5`) keyed by **project + timeline**, so re-runs reuse
  instead of duplicate, and different timelines' candidates coexist.
- **Product Editor** — the ONLY editing surface customers touch. Documents are
  immutable-versioned; every change is an `OperationBatch` appended to
  `editor_operations`. The customer editor speaks only this API (see
  `app/src/pages/Editor.jsx` header comment).
- **Final render / export** — `final_render` jobs carrying `editor_document_id`
  compile the current document version to FFmpeg and upload a private export;
  the project moves to `completed` only after a successful final render.

---

## Backend

Root: `render-backend/` (Python ≥3.12, FastAPI, FFmpeg required on PATH).
Entry: `app/main.py` (uvicorn). Startup: `app/config.py.validate()` fails fast.

### Directory map

```
render-backend/
├── Dockerfile                  # deployment image (Railway builds this)
├── requirements.txt
├── ruff.toml                   # lint config (CI-enforced)
├── pricing.json                # per-stage cost ESTIMATES for telemetry
├── app/
│   ├── main.py                 # ALL HTTP endpoints (~3200 lines), auth, rate limits
│   ├── config.py               # startup env validation
│   ├── jobs.py                 # pipeline_jobs worker: claim/run/retry/cancel + all job handlers
│   ├── supa.py                 # Supabase REST/Storage/Auth helpers (service role)
│   ├── s3store.py              # S3 abstraction: presigned multipart, GET urls, lazy boto3
│   ├── raw_uploads.py          # multipart upload session logic (initiate…finalize)
│   ├── media_store.py          # provider-agnostic source download w/ ancestry re-validation
│   ├── autoedit_bridge.py      # picture-edit → candidate ancestry bridge (deterministic ids)
│   ├── product_editor.py       # editor document/operation/version domain logic
│   ├── timeline.py             # timeline JSON contract validation
│   ├── timeline_ops.py         # constrained op set applied to timelines
│   ├── renderer.py             # v1 single-clip renderer (legacy /render is 410 Gone)
│   ├── renderer2.py            # multi-clip renderer: speed/volume/title/captions/music/fades
│   ├── mediaprobe.py           # bounded ffprobe wrapper
│   ├── human_ceiling.py        # human-editor benchmark sessions (operator tooling)
│   ├── logging_util.py         # structured log_event()
│   ├── audio_library/          # licensed-music ingestion/providers/store (Freesound etc.)
│   └── pipeline/
│       ├── runner.py           # analysis orchestrator (local + cloud modes)
│       ├── schemas.py          # pydantic models incl. Segment
│       ├── media.py, scenes.py, mechanical.py, motion.py, transcribe.py, semantic.py
│       ├── catalog.py          # merge stage → segments table
│       ├── editorial_planner.py# Editorial Planner (plan_editorial, validate_plan, gate)
│       ├── picture_edit_v2.py  # deterministic V2 engine (ENGINE_VERSION, hashes)
│       ├── picture_render_v2.py# additive FFmpeg preview renderer for V2 (xfade chain)
│       ├── gemini_common.py    # generate_json(): schema-degradation ladder, error surfacing
│       ├── autoedit.py         # LEGACY orchestrator: plan→select→preview→critic→revise
│       ├── planner.py, selector.py, validator.py, critic.py, revision.py, conversational.py
│       ├── preferences.py      # rules-based weight adjustment from corrections (±0.05 cap)
│       ├── coverage.py, capture_quality.py
│       ├── preproduction.py, picture_editor.py, music_supervisor.py, audio_rendering.py,
│       │   composition.py, creative_director.py, editorial_intelligence.py, story_editor.py,
│       │   visual_finishing.py   # operator-only audiovisual stages (milestones 0008–0013)
│       ├── telemetry.py        # stage_metrics recording w/ retry queue
│       └── templates/fitness_v1.json
├── scripts/                    # live verification, NOT unit tests
│   ├── apply_migrations.py     # idempotent migration applier (checks project name first)
│   ├── e2e_pipeline.py, e2e_operator_flow.py, test_db_integrity.py
│   ├── check_coverage.py       # per-module coverage gates (CI)
│   └── project_one_*.py        # first-real-project readiness harness
└── tests/                      # pytest suite (fake_supa in-memory Supabase semantics)
```

### How jobs work (`pipeline_jobs`)

One DB-backed worker thread (started at FastAPI startup when `WORKER_ENABLED`
is truthy) polls `pipeline_jobs` every `JOB_POLL_INTERVAL_S` (default 3 s):

1. **Enqueue** (`jobs.enqueue_job`) — inserts `status='queued'`. Idempotency: an
   active (queued/processing) job of the same kind for the same project is
   returned instead of duplicated. Per-user cap `MAX_ACTIVE_JOBS_PER_USER`
   (default 4) raises `ConcurrencyLimit`.
2. **Claim** — optimistic `PATCH … WHERE id=eq.X AND status=eq.queued` to
   `processing`; a lost race simply finds no row. Oldest-first.
3. **Run** — handler dispatched from `HANDLERS`; each job gets a temp dir
   (cleaned in `finally`), a `JobContext` (heartbeats, cancellation checkpoints,
   telemetry), and structured `JOB-START`/`JOB-END` logs.
4. **Stale recovery** — a `processing` job with no heartbeat for
   `JOB_STALE_AFTER_S` (default 900 s) is requeued (attempt-capped).
5. **Failure** — `status='failed'` + error recorded. Project status moves via
   `FAIL_STATUS` **only for kinds listed there** — `editorial_plan` is
   deliberately absent so a failed optional planning stage never wrecks the
   project state machine.
6. **Cancellation** — `queued → cancelled` immediately; `processing →
   cancel_requested → cancelled` at the next checkpoint (between stages, between
   assets, and mid-FFmpeg via subprocess termination + partial-output deletion).
   An in-flight Gemini/Whisper HTTP call is not interruptible; cancellation lands
   when it returns.

**Job state machine:** `queued → processing → completed | failed | cancelled`,
plus `processing → cancel_requested → cancelled` and stale `processing → queued`.

**Kinds and handlers** (`jobs.HANDLERS`):

| kind | handler | project status on failure |
|---|---|---|
| `analysis` | `handle_analysis` | `analysis_failed` |
| `autoedit` | `handle_autoedit` (routes to `handle_autoedit_v2` when flag on) | `analysis_failed` |
| `revision` | `handle_revision` | `analysis_failed` |
| `final_render` | `handle_final_render` (→ `handle_product_editor_render` when `params.editor_document_id`) | `render_failed` |
| `editorial_plan` | `handle_editorial_plan` | — (never moves project status) |

**Customer-journey chaining** (in `jobs.py`):

- Analysis completion calls `_maybe_enqueue_customer_autoedit(project)`:
  - a bridged candidate already exists → do nothing (idempotent);
  - **flag ON** → `_maybe_enqueue_customer_editorial_plan(project)`: if an
    APPROVED plan already exists but no candidate (mid-journey failure), skip
    straight to `autoedit` pinned to that exact plan id+version; else enqueue
    `editorial_plan` with constraints derived from the project (name → brief,
    `aspect_ratio`, `target_platform`);
  - **flag OFF** → enqueue legacy `autoedit` (`source=customer_journey`).
- `editorial_plan` completion (customer-journey source) chains into `autoedit`.
- `POST /projects/{id}/request-edit` — customer retry/resume of this chain.
- `POST /projects/{id}/recut` — re-cut with optional new `aspectRatio`
  (16:9 / 9:16 / 1:1). Reuses the catalog; with the flag on it re-PLANS (plans
  are shape-aware) and never enqueues a bare autoedit.

### HTTP surface (`app/main.py`)

Auth: user JWT verified against GoTrue, then **explicit ownership-chain checks**
(`_owned_project` — deleted-aware). Operator endpoints additionally require an
`operators` table row; every sensitive operator action is audited
(**audit-before-action**: a CONFIRMED `operator_audit` row is written first, or
the action aborts 503). Rate limiting per user+action. Responses are stripped by
`_public_*` helpers so internal fields never leak to customers.

Key endpoint groups (see the file for the full list):

- Health: `GET /healthz`, `/readyz`, `/readyz/s3`, `/readyz/s3/canary`
- Customer journey: `request-analysis`, `request-edit`, `recut`,
  `editorial-plan` (POST/GET), `workspace`, `DELETE /projects/{id}` (soft delete)
- Raw uploads (S3 multipart): `raw-uploads/initiate | sign-parts | complete |
  finalize | abort`
- Product Editor: `editor/start`, `GET editor/{doc}`, `editor/{doc}/operations`,
  `editor/revisions/propose`, `editor/render`, `editor/renders/{job}/retry|sign`
- Signing: `projects/{id}/sign`, `assets/{id}/sign`,
  `candidates/{id}/preview-url`
- Jobs: `GET /jobs/{id}`, `retry`, `cancel`
- Operator-only pipeline stages: `analyze`, `generate-draft`, `revise`,
  `render-final`, `timeline-ops`, `preproduction`, `picture-edit`, `music-sound`,
  `licensed-music/upload`, `audio-render`, `visual-finishing`,
  `editorial-intelligence`, `coverage`, `evaluation`, `segments/{id}/flag`,
  `human-ceiling/*`
- Legacy: `POST /render` returns **410 Gone**.

---

## Frontend (`app/` — React + Vite SPA)

Supabase Auth (email+password) with session restore; PostgREST reads under RLS
using the publishable key only. The service-role key must never appear in `app/`
(`scripts/check-secrets.mjs` + gitleaks enforce this in CI).

Routes (`App.jsx`):

| Route | Page | Purpose |
|---|---|---|
| `/login`, `/reset-password` | Login / ResetPassword | auth |
| `/` | Dashboard | project list; "hero" project with rename/delete; version history named by cut shape |
| `/project/new` | NewProject | creation wizard: name, "Where will this live?" (platform), "vibe" — persisted to `projects.target_platform/vibe`, mapped to `aspect_ratio` (migration 0025) |
| `/project/:id` | Project | upload + processing + results hub (the main page) |
| `/project/:id/editor/:documentId` | Editor | the Product Editor timeline UI |
| `/operator` | Operator | operator console (server-side gated) |

**Customer journey through the UI:**

1. **Create** — NewProject wizard writes name/platform/vibe; `aspect_ratio`
   decides the rendered frame for every downstream stage.
2. **Upload** — `lib/s3upload.js` `MultipartUpload`: validate file → initiate →
   presigned part PUTs with progress/retry → complete → finalize. Errors are
   typed (`UploadError`).
3. **Processing** — Project page renders a live pipeline stage list mapped to
   real `asset_analysis.kind` values (probe → … → catalog) plus project status
   labels (`STATUS_LABEL`: `analyzing` = "Examining your clips",
   `draft_ready` = "Your edit is ready.", etc.). No fake progress.
4. **Edit** — the finished draft opens in the Editor: track lanes (picture /
   captions / music / sfx / graphics), zoom, snap, selection; all mutations are
   OperationBatches, autosaved (800 ms debounce) through
   `POST /editor/{doc}/operations`; undo/redo is history-rebased on version
   conflicts (`lib/editor.js` `rebaseHistory`).
5. **Preview** — short-lived signed candidate preview URLs
   (`POST /candidates/{id}/preview-url`).
6. **Export** — `POST /editor/render` enqueues the final render. In the UI a
   customer export is exactly: `pipeline_jobs.kind === 'final_render'` with
   `params.editor_document_id` (`isExportJob` in Project.jsx). Download uses
   `editor/renders/{job}/sign`.
7. **Re-cut** — a completed project can be re-cut at a new shape (confirm dialog
   explains what a re-cut does); kept versions are named by the shape they were
   cut at.

An `ErrorBoundary` wraps routes so one broken screen can't blank the whole app.

---

## AI Systems

### Analysis stages
- **Scene analysis** — PySceneDetect ContentDetector (`scenes.py`) → shot
  boundaries; `mechanical.py` adds deterministic per-scene measurements (blur,
  exposure/clipping, black/frozen frames, motion energy, shake, perceptual-hash
  duplicate groups). No LLMs in mechanical.
- **Transcription** — `TranscriptionProvider` → OpenAI Whisper API with word
  timestamps (`transcribe.py`). Degrades gracefully when `OPENAI_API_KEY` unset.
- **Semantic** — `VideoUnderstandingProvider` → Gemini via Files API with strict
  `responseSchema`, pydantic-validated (`semantic.py`). Files are deleted in
  `finally` (fallback: Google's ~48 h auto-expiry).
- **Motion** — dense OpenCV frame-diff sampling (~12 fps): intensity, peaks,
  stationary ranges.
- **Catalog** — merges all of the above into versioned `Segment` records; the
  planner and engines consume ONLY this catalog.

### Editorial Planner (`pipeline/editorial_planner.py`)
- `plan_editorial(segments, constraints, music_available, generate, max_attempts=3)`
  — Gemini (`EDITORIAL_PLANNER_MODEL`, via `gemini_common.generate_json`; the
  `generate` callable is injected for tests).
- **Grounding**: every factual claim is a `GroundedText` with `EvidenceRef`s
  pointing at real segments/transcript spans. Editorial labels must come from a
  strictly-closed neutral-label vocabulary (`_NEUTRAL_LABEL_WORDS`, fail-closed —
  unknown words are rejected, never pooled from the catalog).
- **Policies**: `parse_creative_policies()` turns tone/style words into a
  structured, enforceable profile; unparseable directives are either hard
  rejections or, with `toneAdvisoryOnly`, warned advisories
  (`unresolvedToneDirectives`).
- **Transitions**: closed `TransitionType` Literal enum; exactly one transition
  per boundary.
- **Gate**: `deterministic_gate()` — weighted rules summing to 100, approval
  threshold 80 (`APPROVAL_THRESHOLD`); hard failures are unoverridable by
  `modelSelfAssessment`. Violation messages are prefixed (`policy:`,
  `execution:`, `shortfall:`) and map to gate rules.
- **Honesty**: when footage can't satisfy the brief, the planner returns
  `insufficient_footage` with computed achievable duration and structured
  `MissingFootage` — it does not pad or invent.
- **Wire hardening** (top of main): Gemini schema-degradation ladder for
  "too many states" rejections (prune the options subtree first, carry the full
  contract in the prompt on pruned rungs), deep repetitive sections generated in
  a strict second call, on-the-wire enforcement of option key presence,
  self-assessment score bounds, and caption length (≤90 chars).

### Picture Edit Engine V2 (`pipeline/picture_edit_v2.py`)
- `ENGINE_VERSION = "2.1.0"` — **bump on ANY payload change** (the version is
  bound into `deterministicHash`; silent payload drift would poison idempotent
  reuse). `SCHEMA_VERSION = 1`.
- `catalog_hash(segments)` binds the output to the exact catalog it was built
  from; idempotency key = (project, plan version, engine version, catalog hash).
- Deterministic pacing metrics including measured `actualEnergy`
  (0.6·duration-weighted motionIntensity + 0.4·min(1, shotDensity/2)) and
  `energyDeviation` vs the plan's target.
- Executable transitions: `hard_cut`, `dissolve`, `dip_to_black`, `dip_to_white`
  (xfade consumes real source handles). Everything else (speed ramps, advanced
  transitions, zoom crops) → `pending_renderer_support`, never silently replaced.
- Rejections raise `PictureEditRejected(reasons)` — honest failure, no fallback.
- `picture_render_v2.py` renders the preview: aspect-preserving dims (long edge
  640, even), exact fps strings ("29.97" — no truncation), per-clip tail-handle
  extension so xfade never shortens the timeline, audio hard-concat.

### Bridge (`autoedit_bridge.py`)
Deterministic ancestry ids: `uuid5(_BRIDGE_NS, f"{project}:{timeline}:preproduction|picture")`;
`bridged_picture_id()` / `find_bridged_candidate()` bind candidate reuse to the
**timeline**, not the project (migration 0023's partial unique index enforces one
bridged candidate per picture_edit_run). Batch + preview keys are also
per-timeline. Cleanup is persist-or-reopen: untracked cleanup outcomes raise;
double failures log `CLEANUP-PERSIST-FAILED` and re-raise. The V2 reuse path
repairs a missing candidate by re-rendering + re-bridging (`bridgeRepaired`).

### Critic / revision (legacy path)
Gemini watches the actual preview against the brief (fixed question set,
timestamped `revisionRequests`, schema-validated). The revision agent converts
requests into constrained timeline ops; loop capped by `AUTOEDIT_MAX_REVISIONS`
(default 2). Known quirk: `overallScore` can contradict the boolean answers —
treat the requests, not the score, as signal.

### Product Editor (`product_editor.py`)
Immutable versioned documents; constrained operation vocabulary; server-side
validation of every batch; `sourceAssetIds` must be UUIDs. Renders are enqueued
as `final_render` jobs carrying `editor_document_id`.

### Providers
- **Gemini** (`GEMINI_API_KEY`) — semantic video understanding, planner, critic,
  conversational edits. Model overrides: `GEMINI_VIDEO_MODEL`,
  `GEMINI_CRITIC_MODEL`, `GEMINI_NL_MODEL`, `EDITORIAL_PLANNER_MODEL`.
- **OpenAI** (`OPENAI_API_KEY`) — Whisper transcription.
- Both optional: stages degrade or skip, they never fake results.

---

## Database (Supabase `iadzcnzgbtuigyodeqas`)

Migrations: `supabase/migrations/0001 … 0025` — applied idempotently by
`scripts/apply_migrations.py`, or individually via the Supabase Management API.
CI replays the full chain on PostgreSQL 16 plus re-application of
0012/0013/0014/0016/0019/0021 and ~10 integrity SQL suites (`.github/ci/*.sql`).

### Tables (by migration)

| Migration | Tables | Purpose |
|---|---|---|
| 0001 | `profiles`, `projects`, `media_assets`, `timelines`, `render_jobs` | core: users, projects, uploads, versioned timelines, v1 render jobs |
| 0002 | (storage policies) | path-scoped policies for `raw-footage` / `exports` buckets |
| 0003 | `asset_analysis`, `segments` | per-stage analysis artifacts + canonical footage catalog (FTS) |
| 0004 | `edit_runs`, `user_corrections` | autoedit run records (blueprint incl. V2 `deterministicHash`) + preference signals |
| 0005 | `project_status_events`, `operators`, `operator_audit`, `pipeline_jobs`, `draft_evaluations`, `stage_metrics` | hardening: status log (trigger), operator gate + audit, job queue, evaluation, telemetry |
| 0006 | — | cancellation states on jobs |
| 0007 | `human_edit_sessions`, `human_edit_timing_events`, `timeline_scorecards` | human-ceiling benchmark |
| 0008–0012 | `preproduction_runs`, `picture_edit_runs`, `music_sound_runs`, `licensed_music_assets`, `audio_mix_runs`, `graphics_runs`, `caption_runs`, `color_runs` | audiovisual stage records (operator pipeline) |
| 0013 | `candidate_runs`, `critic_runs`, `publishability_reports`, `tournament_runs` | editorial intelligence: candidates + judging |
| 0014–0015 | `editor_documents`, `editor_operations`, `editor_render_requests`, `editor_revision_proposals`, `editor_audit_events` | Product Editor |
| 0016 | — | `generation_kind='bridged'` candidate support (CHECK + trigger: no audio/graphics lineage, autoedit preview prefix) |
| 0017–0021 | `pending_storage_cleanup` (0020) | project soft delete (`deleted_at`), deletion-state protection, **complete** soft-delete-aware child RLS (30 tables), tracked storage cleanup |
| 0022 | `editorial_plans` | versioned plans + RLS + `pipeline_jobs.kind` widened with `editorial_plan` |
| 0023 | — | partial unique index `candidate_runs_bridged_per_picture_idx` (one bridged candidate per picture run/timeline) |
| 0024 | `raw_upload_sessions` | S3 multipart sessions; `media_assets` gains `storage_provider/bucket/key/etag`; media_assets writes become **service-role only** |
| 0025 | — | `projects.aspect_ratio` (16:9/9:16/1:1, default 16:9) + `target_platform` + `vibe` |

### Relationships & ancestry

- Ownership chain: `auth.users → projects → {media_assets, timelines,
  pipeline_jobs, edit_runs, …}` — enforced by RLS **and** relational-ownership
  triggers (migration 0005): child rows must match their project's owner.
- **Candidate ancestry** (audiovisual chain):
  `preproduction_runs → picture_edit_runs → candidate_runs`, with optional
  `audio_mix_run_id` / graphics / caption / color lineage columns. DB triggers
  enforce that a bridged candidate's `picture_edit_run` descends from the SAME
  `preproduction_run` the candidate points at (exact ancestry, not just same
  project), carries no audio/graphics lineage, and stores its preview under the
  `autoedit/` prefix. One bridged candidate per picture run (0023).
- **Timeline ancestry**: `timelines` are versioned per project; lineage
  `autonomous_revised` rows must be immutable. V2 timelines link back through
  `edit_runs.timeline_v2_id`; the bridge derives all ids from
  (project, timeline), so candidate reuse is timeline-bound.

### RLS
Everything customer-reachable is owner-scoped (`user_id = auth.uid()`) and
**soft-delete aware**: children of a deleted project disappear from customer
reads (0019/0021, `project_not_deleted()` predicate). Operators get read
policies via the `operators` table. `media_assets` INSERT/UPDATE is service-role
only (0024). The service role bypasses RLS but the backend still does explicit
ownership checks before every action.

---

## Current Production Behavior

### When a customer uploads footage (flag OFF — today's default)
1. SPA initiates S3 multipart; parts go browser→S3; `finalize` creates the
   `media_assets` row after server-side validation.
2. Customer (or upload completion flow) triggers analysis → `analysis` job →
   full stage chain → `segments` catalog; project `analyzing`.
3. Analysis completion auto-enqueues legacy `autoedit`
   (`source=customer_journey`): plan → select → preview render → validate →
   critic → up to 2 revision passes → timeline; the bridge wraps it into a
   bridged `candidate_run` with a preview in storage; project `draft_ready`.
4. The draft opens in the Product Editor (an `editor_document` bound to the
   candidate).

### When V2 is enabled (`PICTURE_EDIT_ENGINE_V2_ENABLED=true`)
Same steps 1–2, then:
3. Analysis completion enqueues `editorial_plan` instead. Constraints come from
   the project (name → brief, aspect_ratio, target_platform). The planner writes
   an approved `editorial_plans` row (or fails without touching project status;
   `request-edit` retries).
4. Plan approval chains into `autoedit`, which routes to `handle_autoedit_v2`:
   requires the approved plan (**no legacy fallback**), builds the deterministic
   V2 timeline, renders the preview via `picture_render_v2`, bridges a candidate
   (timeline-bound reuse; missing-candidate repair re-renders + re-bridges).
   Idempotent per `deterministicHash` — repeat runs reuse.
5. Re-cut re-plans at the new shape (plans are shape-aware).

### During export
`POST /projects/{id}/editor/render` → `final_render` job with
`editor_document_id` → `handle_product_editor_render` compiles the document
version to an FFmpeg graph (renderer2 primitives) → uploads the export
(Supabase `exports` bucket, or S3 when `EXPORT_STORAGE_PROVIDER=s3`) → project
`completed` → SPA polls the job row (no timers) → download via
`editor/renders/{job}/sign` (short-lived signed URL). Failures land in
`render_failed` with a visible reason + retry.

---

## Environment Variables (render backend)

**Required** (startup fails without): `SUPABASE_URL`,
`SUPABASE_SERVICE_ROLE_KEY`. FFmpeg + ffprobe must be on PATH.

| Variable | Purpose | Default |
|---|---|---|
| `GEMINI_API_KEY` | semantic/planner/critic/NL (optional — stages degrade) | unset |
| `OPENAI_API_KEY` | Whisper transcription (optional) | unset |
| `PICTURE_EDIT_ENGINE_V2_ENABLED` | THE V2 journey flag (`1/true/yes`) | off |
| `EDITORIAL_PLANNER_MODEL` | planner model override | gemini default in code |
| `GEMINI_VIDEO_MODEL` / `GEMINI_CRITIC_MODEL` / `GEMINI_NL_MODEL` | per-role model overrides | code defaults |
| `AUTOEDIT_MAX_REVISIONS` | legacy critic/revision loop cap | 2 |
| `WORKER_ENABLED` | start the job worker thread | enabled |
| `WORKER_CONCURRENCY` | concurrent jobs | 1 |
| `JOB_POLL_INTERVAL_S` / `JOB_STALE_AFTER_S` | worker poll / stale requeue | 3 / 900 |
| `MAX_ACTIVE_JOBS_PER_USER` | per-user active-job cap | 4 |
| `ALLOWED_ORIGINS` | CORS | — |
| `RENDER_TIMEOUT_S` | FFmpeg render timeout | code default |
| `FFMPEG_BIN` / `FFPROBE_BIN` | binary overrides | ffmpeg/ffprobe |
| `TITLE_FONT_FILE` | drawtext font | code default |
| `MAX_UPLOAD_BYTES` / `MAX_BODY_BYTES` | upload/body caps | code defaults |
| `MAX_CONCURRENT_PROBES`, `PROBE_TIMEOUT_S`, `PROBE_SIZE_BYTES`, `PROBE_ANALYZE_DURATION_US`, `PROBE_RW_TIMEOUT_US` | bounded ffprobe | code defaults |
| `OPERATOR_RATE_LIMIT_PER_MIN` | operator endpoint rate limit | code default |
| `AWS_S3_BUCKET`, `AWS_REGION`, `AWS_S3_ENDPOINT_URL` | S3 raw-footage store (S3 disabled when bucket unset) | unset |
| `S3_PART_URL_EXPIRE_S` / `S3_GET_URL_EXPIRE_S` | presigned URL TTLs | 3600 / 3600 |
| `S3_SSE_ALGORITHM` | server-side encryption | AES256 |
| `RAW_UPLOAD_PART_SIZE` / `RAW_UPLOAD_TTL_S` | multipart tuning | code defaults |
| `EXPORT_STORAGE_PROVIDER` | `supabase` or `s3` for exports | `supabase` |
| `PRICING_FILE` | telemetry cost estimates | `pricing.json` |
| `AUDIO_LIBRARY_ROOT`, `FREESOUND_API_KEY`, `FREESOUND_OAUTH_TOKEN`, `FREESOUND_TERMS_REVIEWED_AT`, `FREESOUND_COMMERCIAL_API_APPROVAL_REFERENCE` | licensed-music ingestion | unset |
| `HUMAN_EDIT_IDLE_GAP_CAP_SECONDS`, `HUMAN_OPERATION_INDEX_RETRIES` | human-ceiling tooling | code defaults |

Frontend env (`app/.env`, browser-safe only): Supabase URL + publishable key,
`RENDER_API` base URL. Never the service-role key (CI-enforced).

## Feature Flags

| Flag | Default | When enabled |
|---|---|---|
| `PICTURE_EDIT_ENGINE_V2_ENABLED` | **off** | The entire customer edit journey switches: analysis chains to the Editorial Planner; autoedit REQUIRES an approved plan and runs the deterministic V2 engine; re-cut re-plans. No legacy fallback on failure — failures are honest and retryable via `request-edit`. |
| `EXPORT_STORAGE_PROVIDER=s3` | `supabase` | Final exports are written to S3 instead of the Supabase `exports` bucket; signing switches to presigned S3 GETs. |
| `WORKER_ENABLED=0` | worker on | API serves requests but processes no jobs (multi-instance topologies: exactly one worker). |
| S3 raw uploads (`AWS_S3_BUCKET` set) | unset = legacy Supabase uploads | `/raw-uploads/*` endpoints become operational; new assets get `storage_provider='s3'`. Existing Supabase-stored assets keep working (media_store re-validates provenance either way). |

## Storage

| Location | Contents | Access |
|---|---|---|
| Supabase bucket `raw-footage` (private) | legacy customer uploads: `users/{uid}/projects/{pid}/raw/{asset_id}/{filename}` | path-scoped RLS (segment 2 must equal `auth.uid()`); insert/select/delete own |
| S3 bucket (`AWS_S3_BUCKET`) | multipart raw uploads: `users/{uid}/projects/{pid}/raw-footage/{asset_id}/{safe_filename}` | browser touches S3 ONLY via short-lived presigned URLs; keys built server-side; SSE on |
| Supabase bucket `exports` (private) | rendered previews + final exports (incl. bridged candidate previews under `…/autoedit/`) | only the service role writes; owners get signed-URL reads (+ delete own) |
| S3 (when `EXPORT_STORAGE_PROVIDER=s3`) | final exports | presigned GETs |
| `asset_analysis` table | analysis artifacts (JSON), proxies/thumbnails referenced from storage | RLS |
| `pending_storage_cleanup` table | tracked deletions that must be retried/drained | service role |

## Current Limitations

- **V2 flag is OFF in production** — the merged planner+engine journey is dormant
  until the Railway variable is set. Pre-enable checklist: real-DB bridge-retry
  exercise, representative 9:16/16:9/1:1 renders, 29.97/59.94 fps ffprobe
  verification on production-like footage.
- **Renderer gaps** — speed ramps, advanced transitions (whip/push/slide/zoom/
  match_cut/masked_reveal/audio_led_cut), and zoom crops are honest
  `pending_renderer_support` entries, not rendered effects. renderer2 supports
  concat/speed/volume/title/captions/music-duck/fades; xfade transitions live in
  picture_render_v2 only.
- **Audio pipeline not in the customer journey** — music/sound, audio mix,
  graphics, captions, color are operator-only stages (0008–0013 tables); bridged
  candidates deliberately carry no audio lineage.
- **Single-worker concurrency** — `WORKER_CONCURRENCY=1` default; in-process
  worker thread. Fine for current scale; a queue/worker split is needed before
  real concurrency.
- **AI limitations** — Gemini critic scores can contradict their own boolean
  answers (treat requests as signal); Gemini structured-output "too many states"
  rejections require the degradation ladder in `gemini_common`; transcription/
  semantic quality unvalidated on noisy real-world footage at scale.
- **Cancellation** cannot interrupt an in-flight LLM HTTP call.
- **Storage deletes** are best-effort with `pending_storage_cleanup` tracking;
  a manual drain may be needed after repeated failures.
- **Uploads** — no resumability across sessions for legacy Supabase uploads;
  S3 multipart covers the large-file path (up to 2 GB).
- **Preference learning** is rules-based (±0.05 weight caps) — deliberately no
  fine-tuning until enough approved projects exist.

## Recent Major Milestones (chronological, all merged)

1. **Real video pipeline** (2026-07-31) — real auth/upload/timeline/FFmpeg
   render slice replacing all simulated pages; analysis pipeline (probe→catalog).
2. **Editing engine + hardening** (2026-08-01) — legacy autoedit loop (planner/
   selector/critic/revision), operator console, `pipeline_jobs` worker,
   audit-before-action, cancellation, telemetry, coverage gates.
3. **Audiovisual stage records** (0008–0013) — preproduction/picture/music/
   audio/graphics/caption/color runs + candidates/critics/tournaments.
4. **Product Editor** (0014–0015) — immutable versioned customer editing
   documents + operations + renders.
5. **Bridged candidates** (0016) — legacy autoedit output wrapped into the
   candidate ancestry so the Product Editor has one spine.
6. **Soft delete + child RLS + storage cleanup** (0017–0021).
7. **Repair/audit round** (PR #4, 2026-08-04) — deleted-aware ownership,
   version-bound export revalidation, exact bridged ancestry in PostgreSQL,
   cleanup persist-or-reopen, conflict-safe editor undo/redo.
8. **Editorial Planner v1** (PR #5, 0022) — evidence-grounded, deterministically
   gated planning stage; five Codex audit rounds.
9. **Picture Edit Engine V2** (PR #6, 0023) — deterministic plan→timeline
   compiler, honest execution semantics, timeline-bound ancestry + idempotency;
   four Codex audit rounds. ENGINE_VERSION 2.1.0.
10. **S3 multipart raw uploads** (0024) — direct browser→S3 up to 2 GB,
    service-role-only media_assets provenance.
11. **V2 customer journey** (PR #7, 0025) — planner+V2 wired into the customer
    flow behind the flag; aspect-ratio-aware projects; re-cut; request-edit
    resume; dashboard/editor UX fixes; Gemini schema-degradation ladder and
    planner wire-hardening fixes on top.

## Future Roadmap (natural extensions only)

- **Enable V2 in production** (flip the Railway flag after the controlled smoke
  test passes) — the immediate next step.
- **Renderer parity** — implement `pending_renderer_support` items (ramps,
  advanced transitions, zoom crops) in picture_render_v2/renderer2 so the
  planner's full transition vocabulary becomes executable.
- **Audio in the customer journey** — connect music supervision / audio mix /
  captions to the V2 chain (ancestry columns and tables already exist).
- **Worker scale-out** — split API and worker deployables (`WORKER_ENABLED`
  seam already exists); real queue when concurrency demands it.
- **Preference learning v2** — grow from rules-based weight nudges once enough
  `draft_evaluations` + `user_corrections` accumulate.
- **Human-ceiling benchmarking** — use the 0007 tooling to measure AI drafts
  against human editors on real footage.
- **Operator → customer graduation** — expose currently operator-only stages to
  customers as they prove reliable.

---

*Maintenance rule: any PR that changes pipeline behavior, adds a migration, an
endpoint, an env var, or a flag MUST update this file in the same PR.*
