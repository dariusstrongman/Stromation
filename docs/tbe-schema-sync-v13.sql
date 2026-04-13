-- TBE schema sync for pipeline v13
-- Run in Supabase SQL Editor. Safe to re-run. No data mutation.
--
-- Confirmed already in prod (no action needed):
--   device_analysis JSONB, page_classification JSONB, estimate_method TEXT
--
-- Missing from prod (this file adds them):
--   1. pipeline_version column (v13 writes this; currently silently dropped)
--   2. 'analyzing' + 'pending_review' in status CHECK constraint

-- STEP 0 (optional) — run this FIRST on its own to see current status constraints.
-- If you see a constraint name other than 'tbe_bids_status_check', tell me before running the rest.
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'tbe_bids'::regclass
  AND contype = 'c'
  AND pg_get_constraintdef(oid) ILIKE '%status%';

-- ============================================================
-- Migration (wrapped in transaction — all or nothing)
-- ============================================================
BEGIN;

-- 1. Add pipeline_version column
ALTER TABLE tbe_bids
  ADD COLUMN IF NOT EXISTS pipeline_version TEXT;

-- 2. Drop ANY existing CHECK constraint on status (handles unknown auto-generated names)
DO $$
DECLARE
  c RECORD;
BEGIN
  FOR c IN
    SELECT conname
    FROM pg_constraint
    WHERE conrelid = 'tbe_bids'::regclass
      AND contype = 'c'
      AND pg_get_constraintdef(oid) ILIKE '%status%IN%'
  LOOP
    EXECUTE format('ALTER TABLE tbe_bids DROP CONSTRAINT %I', c.conname);
  END LOOP;
END $$;

-- 3. Add new CHECK constraint with analyzing + pending_review
ALTER TABLE tbe_bids
  ADD CONSTRAINT tbe_bids_status_check CHECK (status IN (
    'new',
    'analyzing',
    'pending_review',
    'reviewing',
    'estimating',
    'quote_ready',
    'quote_sent',
    'submitted',
    'won',
    'lost',
    'no_bid',
    'expired'
  ));

COMMIT;

-- ============================================================
-- Verify (run after commit)
-- ============================================================
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'tbe_bids'::regclass
  AND conname = 'tbe_bids_status_check';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'tbe_bids'
  AND column_name IN ('pipeline_version', 'device_analysis', 'page_classification', 'estimate_method')
ORDER BY column_name;
