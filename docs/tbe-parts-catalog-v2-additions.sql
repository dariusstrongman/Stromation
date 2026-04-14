-- TBE catalog v2: additional parts surfaced by Jimmy John's audit + production-readiness gaps
-- Run in Supabase SQL Editor. Idempotent.

BEGIN;

-- ===== CABLE COLOR VARIANTS (so spec-driven color swaps work) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Panduit','PUP6AHD04OR-G','cable','cat6a_orange','Panduit Cat 6A Vari-MaTriX HD 23 AWG Orange (1000ft)','box',1414.27,'all',false,'msrp_estimate'),
('Panduit','PUP6AHD04YL-G','cable','cat6a_yellow','Panduit Cat 6A Vari-MaTriX HD 23 AWG Yellow (1000ft)','box',1414.27,'all',false,'msrp_estimate'),
('Panduit','PUP6AHD04WH-G','cable','cat6a_white','Panduit Cat 6A Vari-MaTriX HD 23 AWG White (1000ft)','box',1414.27,'all',false,'msrp_estimate'),
('Panduit','PUP6AHD04BK-G','cable','cat6a_black','Panduit Cat 6A Vari-MaTriX HD 23 AWG Black (1000ft)','box',1414.27,'all',false,'msrp_estimate'),
('Panduit','PUP6AHD04RD-G','cable','cat6a_red','Panduit Cat 6A Vari-MaTriX HD 23 AWG Red (1000ft)','box',1414.27,'all',false,'msrp_estimate'),
-- Matching jack colors
('Panduit','CJ6X88TGOR','jack','cat6a_orange','Panduit Mini-Com Cat 6A UTP Jack, Orange','ea',19.86,'all',false,'msrp_estimate'),
('Panduit','CJ6X88TGYL','jack','cat6a_yellow','Panduit Mini-Com Cat 6A UTP Jack, Yellow','ea',19.86,'all',false,'msrp_estimate'),
('Panduit','CJ6X88TGWH','jack','cat6a_white','Panduit Mini-Com Cat 6A UTP Jack, White','ea',19.86,'all',false,'msrp_estimate'),
('Panduit','CJ6X88TGBK','jack','cat6a_black','Panduit Mini-Com Cat 6A UTP Jack, Black','ea',19.86,'all',false,'msrp_estimate'),
('Panduit','CJ6X88TGRD','jack','cat6a_red','Panduit Mini-Com Cat 6A UTP Jack, Red','ea',19.86,'all',false,'msrp_estimate'),
-- Patch cords by color
('Generic','UTP28CH8OR','patch_cord','cat6a_8ft_orange','Cat 6A SD 8ft Orange','ea',37.94,'all',false,'msrp_estimate'),
('Generic','UTP28CH2OR','patch_cord','cat6a_2ft_orange','Cat 6A SD 2ft Orange','ea',29.35,'all',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== SPEAKERS — additional brands surfaced by Jimmy John's spec =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Definitive','AW6500BK','speaker','outdoor_qsr','Definitive Technology AW6500BK 6.5in outdoor speaker','ea',195.00,'qsr',false,'spec_jimmy_johns'),
('Definitive','UEL-A','speaker','indoor_premium','Definitive Technology UEL-A in-ceiling speaker','ea',225.00,'commercial',false,'msrp_estimate'),
('Polk Audio','RC85i','speaker','ceiling_qsr_alt','Polk Audio RC85i 8in ceiling speaker','ea',125.00,'qsr',false,'msrp_estimate'),
('Atlas Sound','AP-S15T','speaker','strategy_paging','Atlas Sound AP-S15T 15W paging speaker','ea',85.00,'qsr',false,'msrp_estimate'),
('Crown','PA-160','speaker','industrial','Crown PA-160 industrial paging speaker','ea',155.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== PAGING AMPLIFIERS — additional brands =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Yamaha','RS700','paging_amp','rack_qsr','Yamaha RS700 rackmount mixer/amplifier','ea',850.00,'qsr',false,'spec_jimmy_johns'),
('Yamaha','PA2120','paging_amp','120w','Yamaha PA2120 120W paging amplifier','ea',650.00,'qsr',false,'msrp_estimate'),
('Crown','CDi 1000','paging_amp','1000w_pro','Crown CDi 1000 dual-channel amplifier','ea',1100.00,'commercial',false,'msrp_estimate'),
('Atlas Sound','AAT100','paging_amp','100w_zone','Atlas Sound AAT100 100W zone amp','ea',680.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== VOLUME CONTROLS =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Niles','SSVC-4','volume_control','4_zone_qsr','Niles SSVC-4 4-zone speaker volume control','ea',285.00,'qsr',false,'spec_jimmy_johns'),
('Atlas Sound','AT-100','volume_control','100w_inline','Atlas Sound AT-100 100W inline volume control','ea',95.00,'qsr',false,'msrp_estimate'),
('Lutron','HWI-RP-15A','volume_control','rack_mount','Lutron HWI-RP-15A rack-mount audio control','ea',195.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== DISPLAYS / DIGITAL SIGNAGE =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Samsung','QM55C','display','55in_commercial','Samsung QM55C 55in commercial display 4K','ea',1450.00,'commercial',true,'msrp_estimate'),
('Samsung','QM43R','display','43in_qsr','Samsung QM43R 43in commercial display (QSR menu board)','ea',850.00,'qsr',true,'msrp_estimate'),
('LG','55UH5N-E','display','55in_commercial_lg','LG 55UH5N-E 55in commercial display','ea',1350.00,'commercial',false,'msrp_estimate'),
('Chief','LSAU','display_mount','articulating_qsr','Chief LSAU articulating wall mount (32-65in)','ea',285.00,'qsr',true,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== INTERCOMS — additional drive-thru and door =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Aiphone','GT-DMB-N','intercom','door_video','Aiphone GT-DMB-N video door intercom','ea',1250.00,'commercial',true,'msrp_estimate'),
('Aiphone','LE-D','intercom','door_audio','Aiphone LE-D audio-only door intercom','ea',285.00,'qsr',true,'msrp_estimate'),
('Doorking','1812','intercom','telephone_entry','Doorking 1812 telephone entry system','ea',1850.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== POS HANDHELD / KITCHEN DISPLAY =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Toast','Handheld 2','pos_handheld','tabletside','Toast Handheld 2 server tablet','ea',650.00,'qsr',false,'msrp_estimate'),
('Toast','KDS Display','pos_kds','kitchen_display','Toast Kitchen Display Screen','ea',1250.00,'qsr',false,'msrp_estimate'),
('Square','Terminal','pos_handheld','square_terminal','Square Terminal handheld','ea',299.00,'qsr',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== UPS — fill out tier coverage =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('APC','BR1500MS2','ups','1500va_battery_qsr','APC BR1500MS2 1500VA battery backup','ea',285.00,'qsr',false,'msrp_estimate'),
('CyberPower','CP1500AVRLCD','ups','1500va_avr','CyberPower CP1500AVRLCD 1500VA AVR LCD','ea',225.00,'qsr',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== CAMERA MOUNTS — additional brands =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Avigilon','H4-MT-PEND1','camera_mount','pendant_commercial','Avigilon H4-MT-PEND1 pendant mount','ea',125.00,'commercial',false,'msrp_estimate'),
('Hikvision','DS-1281ZJ-DM26','camera_mount','indoor_qsr','Hikvision DS-1281ZJ-DM26 indoor mount','ea',55.00,'qsr',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== POS COMPONENT BOXES — additional vendors =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Signature Systems, Inc','POS System','pos_terminal','signature_pos','Signature Systems POS terminal (full system)','ea',2850.00,'qsr',false,'spec_jimmy_johns')
ON CONFLICT (manufacturer, model) DO NOTHING;

COMMIT;

SELECT manufacturer, COUNT(*) FROM tbe_parts_catalog WHERE source LIKE 'spec_%' OR manufacturer IN ('Definitive','Yamaha','Niles','Aiphone','Samsung','LG','Chief','Toast','Doorking','Polk Audio','Crown','Lutron') GROUP BY manufacturer ORDER BY 1;
