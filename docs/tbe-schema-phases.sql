-- TBE phased pipeline: adds pipeline_phases JSONB column
-- Safe to re-run. No data mutation. Run in Supabase SQL Editor.

BEGIN;

-- 1. Add pipeline_phases column (tracks per-phase state for dashboard stepper)
ALTER TABLE tbe_bids
  ADD COLUMN IF NOT EXISTS pipeline_phases JSONB DEFAULT '{}'::jsonb;

-- 2. Backfill empty phases on existing bids so dashboard stepper renders something
UPDATE tbe_bids
SET pipeline_phases = jsonb_build_object(
  'download',       jsonb_build_object('status', CASE WHEN estimate_method IN ('blueprint_claude','blueprint_gemini','blueprint_gpt') THEN 'complete' ELSE 'not_started' END),
  'classify',       jsonb_build_object('status', CASE WHEN page_classification IS NOT NULL THEN 'complete' ELSE 'not_started' END),
  'claude_counts',  jsonb_build_object('status', CASE WHEN device_analysis IS NOT NULL THEN 'complete' ELSE 'not_started' END),
  'gemini_verify',  jsonb_build_object('status', 'not_started'),
  'quote_built',    jsonb_build_object('status', CASE WHEN quote_html IS NOT NULL AND length(quote_html) > 100 THEN 'complete' ELSE 'not_started' END),
  'pending_review', jsonb_build_object('status', CASE WHEN status = 'pending_review' THEN 'in_progress' WHEN status IN ('quote_ready','quote_sent','submitted','won','lost') THEN 'complete' ELSE 'not_started' END),
  'sent',           jsonb_build_object('status', CASE WHEN status IN ('quote_sent','submitted','won','lost') THEN 'complete' ELSE 'not_started' END)
)
WHERE pipeline_phases = '{}'::jsonb OR pipeline_phases IS NULL;

COMMIT;

-- Verify
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'tbe_bids' AND column_name = 'pipeline_phases';

SELECT id, project_name, status,
  pipeline_phases->'download'->>'status' AS download,
  pipeline_phases->'classify'->>'status' AS classify,
  pipeline_phases->'claude_counts'->>'status' AS claude,
  pipeline_phases->'gemini_verify'->>'status' AS gemini,
  pipeline_phases->'quote_built'->>'status' AS quote_built,
  pipeline_phases->'pending_review'->>'status' AS pending,
  pipeline_phases->'sent'->>'status' AS sent
FROM tbe_bids
ORDER BY updated_at DESC
LIMIT 5;
