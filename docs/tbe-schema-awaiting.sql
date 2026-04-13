-- Add 'awaiting_blueprints' status for bids triaged but missing plans.
-- Safe, idempotent, no data mutation.

BEGIN;

-- Drop and re-add the status check constraint with the new value
DO $$
DECLARE c RECORD;
BEGIN
  FOR c IN
    SELECT conname FROM pg_constraint
    WHERE conrelid = 'tbe_bids'::regclass
      AND contype = 'c'
      AND pg_get_constraintdef(oid) ILIKE '%status%IN%'
  LOOP
    EXECUTE format('ALTER TABLE tbe_bids DROP CONSTRAINT %I', c.conname);
  END LOOP;
END $$;

ALTER TABLE tbe_bids
  ADD CONSTRAINT tbe_bids_status_check CHECK (status IN (
    'new',
    'awaiting_blueprints',
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

-- Verify
SELECT pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'tbe_bids'::regclass AND conname = 'tbe_bids_status_check';
