-- TBE: spec extraction + parts catalog (production-grade parts system)
-- Safe, idempotent, no destructive operations.
-- Run in Supabase SQL Editor.

BEGIN;

-- 1. New columns on tbe_bids for spec extraction + tiering
ALTER TABLE tbe_bids
  ADD COLUMN IF NOT EXISTS spec_data JSONB,
  ADD COLUMN IF NOT EXISTS project_tier TEXT,
  ADD COLUMN IF NOT EXISTS spec_extracted_at TIMESTAMPTZ;

-- 2. Source attribution on each line item (so we can show why each part was chosen)
ALTER TABLE tbe_bid_items
  ADD COLUMN IF NOT EXISTS source TEXT;

-- 3. Parts catalog — single source of truth for parts + pricing
CREATE TABLE IF NOT EXISTS tbe_parts_catalog (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  manufacturer TEXT NOT NULL,
  model TEXT NOT NULL,
  category TEXT NOT NULL,           -- 'cable','jack','camera_fixed','nvr','rack','grounding_kit', etc.
  sub_category TEXT,
  description TEXT,
  unit TEXT NOT NULL DEFAULT 'ea',  -- ea, ft, hr, box
  unit_price NUMERIC,
  msrp NUMERIC,
  vendor_cost NUMERIC,
  markup_pct NUMERIC,
  tier TEXT NOT NULL DEFAULT 'all', -- qsr, commercial, enterprise, all
  is_default_for_tier BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  notes TEXT,
  source TEXT,                      -- where price came from
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT tier_valid CHECK (tier IN ('qsr','commercial','enterprise','all'))
);

CREATE INDEX IF NOT EXISTS idx_parts_category_tier ON tbe_parts_catalog(category, tier) WHERE is_active;
CREATE INDEX IF NOT EXISTS idx_parts_mfr_model ON tbe_parts_catalog(manufacturer, model) WHERE is_active;
CREATE INDEX IF NOT EXISTS idx_parts_default ON tbe_parts_catalog(category, tier, is_default_for_tier) WHERE is_default_for_tier AND is_active;

-- RLS so the dashboard can read; service role can write (for n8n)
ALTER TABLE tbe_parts_catalog ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS parts_catalog_anon_read ON tbe_parts_catalog;
CREATE POLICY parts_catalog_anon_read ON tbe_parts_catalog FOR SELECT TO anon USING (true);

DROP POLICY IF EXISTS parts_catalog_anon_write ON tbe_parts_catalog;
CREATE POLICY parts_catalog_anon_write ON tbe_parts_catalog FOR UPDATE TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS parts_catalog_anon_insert ON tbe_parts_catalog;
CREATE POLICY parts_catalog_anon_insert ON tbe_parts_catalog FOR INSERT TO anon WITH CHECK (true);

DROP POLICY IF EXISTS parts_catalog_anon_delete ON tbe_parts_catalog;
CREATE POLICY parts_catalog_anon_delete ON tbe_parts_catalog FOR DELETE TO anon USING (true);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION tbe_parts_catalog_touch_updated()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tbe_parts_catalog_updated_at ON tbe_parts_catalog;
CREATE TRIGGER tbe_parts_catalog_updated_at
  BEFORE UPDATE ON tbe_parts_catalog
  FOR EACH ROW EXECUTE FUNCTION tbe_parts_catalog_touch_updated();

COMMIT;

-- Verify
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('tbe_bids','tbe_bid_items','tbe_parts_catalog')
  AND column_name IN ('spec_data','project_tier','spec_extracted_at','source','manufacturer','model','tier')
ORDER BY table_name, column_name;
