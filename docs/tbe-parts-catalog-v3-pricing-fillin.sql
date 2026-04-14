-- TBE catalog v3: fill in market-estimate pricing for placeholder spec items
-- These are parts that appeared in real audit specs but didn't have catalog matches.
-- Prices are conservative best-knowledge market estimates as of 2026-04 — Antonio
-- should refine with his actual distributor pricing (mark source='antonio_quote').
-- Run after v2.

BEGIN;

INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
-- From Jimmy John's audit
('Middle Atlantic','TW12','cable_manager','wire_trough_12in','Middle Atlantic TW12 12-inch wire trough/cable management','ea',125.00,'all',false,'market_estimate_2026_04'),
('Signature Systems','N/A','pos_terminal','qsr_workstation_bundle','Signature Systems POS workstation bundle (terminal + cash drawer + receipt printer + cabling, per station)','ea',2850.00,'qsr',false,'market_estimate_2026_04'),
('Middle Atlantic','UTR1','rack_shelf','utility_shelf_1u','Middle Atlantic UTR1 1U utility rack shelf','ea',85.00,'all',false,'market_estimate_2026_04'),
-- Common phone handset that gets spec'd alongside Mitel base
('Mitel','5320e','phone_handset','ip_handset_8line','Mitel 5320e IP phone handset','ea',195.00,'all',false,'market_estimate_2026_04'),
-- Drive-thru hardware
('HME','speaker post','intercom','drive_thru_post','HME drive-thru speaker post (mounting + speaker assembly)','ea',1850.00,'qsr',false,'market_estimate_2026_04'),
-- Atlas variant
('Atlas Sound','FAP62T-W','speaker','ceiling_70v_qsr_white','Atlas Sound FAP62T-W 6.5in ceiling speaker 70V white','ea',95.00,'qsr',false,'market_estimate_2026_04'),
-- Camera mount variants
('Avigilon','H4-MT-CRNR1','camera_mount','corner_mount','Avigilon H4-MT-CRNR1 corner mount adapter','ea',135.00,'all',false,'market_estimate_2026_04')
ON CONFLICT (manufacturer, model) DO NOTHING;

COMMIT;

SELECT manufacturer, model, unit_price, source FROM tbe_parts_catalog WHERE source = 'market_estimate_2026_04' ORDER BY manufacturer;
