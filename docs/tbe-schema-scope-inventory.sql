-- TBE: scope_inventory column on tbe_bids
-- Tells downstream stages what sheet categories actually exist in the bid set,
-- so tier minimums / Gemini / Arbitrator don't invent out-of-scope devices.
-- Idempotent.

BEGIN;

ALTER TABLE tbe_bids
  ADD COLUMN IF NOT EXISTS scope_inventory JSONB DEFAULT NULL;

COMMENT ON COLUMN tbe_bids.scope_inventory IS
  'Set by WF2 pipeline at end of Pass 1. Shape: {has_telecom_sheets, has_security_sheets, has_fire_alarm_sheets, has_av_sheets, has_access_control_sheets, lv_sheet_count, lv_sheet_ids:[], cover_sheet_flags:{}}';

-- Backfill existing bids with empty inventory so downstream code can safely
-- check `.has_X === true` without null handling.
UPDATE tbe_bids
SET scope_inventory = jsonb_build_object(
  'has_telecom_sheets', false,
  'has_security_sheets', false,
  'has_fire_alarm_sheets', false,
  'has_av_sheets', false,
  'has_access_control_sheets', false,
  'lv_sheet_count', 0,
  'lv_sheet_ids', jsonb_build_array(),
  'cover_sheet_flags', jsonb_build_object(),
  'backfilled', true
)
WHERE scope_inventory IS NULL;

COMMIT;

SELECT COUNT(*) AS bids_with_inventory FROM tbe_bids WHERE scope_inventory IS NOT NULL;
