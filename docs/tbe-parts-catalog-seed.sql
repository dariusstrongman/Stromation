-- TBE parts catalog seed — pulls existing 89 parts from WF4 hardcoded list,
-- adds tier classification, adds missing QSR/Commercial-tier parts.
-- Run AFTER tbe-schema-spec-system.sql.
-- Idempotent via ON CONFLICT DO NOTHING on (manufacturer, model).

-- Unique constraint to support upsert (parts identified by mfr+model)
ALTER TABLE tbe_parts_catalog
  DROP CONSTRAINT IF EXISTS tbe_parts_catalog_mfr_model_key;
ALTER TABLE tbe_parts_catalog
  ADD CONSTRAINT tbe_parts_catalog_mfr_model_key UNIQUE (manufacturer, model);

BEGIN;

-- ===== CABLE / STRUCTURED CABLING (tier=all — used universally) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Panduit','PUP6AHD04BU-G','cable','cat6a_blue','Panduit Cat 6A Vari-MaTriX HD 23 AWG Blue (1000ft)','box',1414.27,'all',true,'wf4_legacy'),
('Panduit','PUP6AHD04GR-G','cable','cat6a_green','Panduit Cat 6A Vari-MaTriX HD 23 AWG Green (1000ft)','box',1414.27,'all',false,'wf4_legacy'),
('Panduit','PUP6AHD04VL-G','cable','cat6a_violet','Panduit Cat 6A Vari-MaTriX HD 23 AWG Violet (1000ft) - cameras','box',1414.27,'all',false,'wf4_legacy'),
('Panduit','PUP6AHD04IG-G','cable','cat6a_grey','Panduit Cat 6A Vari-MaTriX HD 23 AWG Grey (1000ft)','box',1414.27,'all',false,'wf4_legacy'),
('CommScope','SYSTIMAX-2071E-BU','cable','cat6a_blue','CommScope SYSTIMAX 2071E Cat 6A Blue (1000ft)','box',1325.00,'all',false,'msrp_estimate'),
('Belden','6302UE','cable','access_control','Belden 18-4C STR BC LSPVC, JKT BLACK CMP 75C (1000ft)','box',600.00,'all',true,'wf4_legacy'),
('Belden','5320UE-FA','cable','fire_alarm','Belden 16-2C Shielded Fire Alarm Cable FPLR (1000ft)','box',450.00,'all',false,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== JACKS (tier=all) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Panduit','CJ6X88TGBU','jack','cat6a_blue','Panduit Mini-Com Cat 6A UTP Jack, Blue','ea',19.86,'all',true,'wf4_legacy'),
('Panduit','CJ6X88TGGR','jack','cat6a_green','Panduit Mini-Com TX6A 10Gig UTP Jack, Green','ea',19.80,'all',false,'wf4_legacy'),
('Panduit','CJ6X88TGVL','jack','cat6a_violet','Panduit Mini-Com Cat6A Jack, Violet','ea',19.86,'all',false,'wf4_legacy'),
('Panduit','CJ6X88TGIG','jack','cat6a_grey','Panduit Mini-Com Cat 6A UTP Jack, Grey','ea',21.29,'all',false,'wf4_legacy'),
('CommScope','MGS400-262','jack','cat6a','CommScope MGS400-262 Mod Jack Cat 6A','ea',22.50,'all',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== FACEPLATES (tier=all) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Panduit','CFPL2SY','faceplate','2_port_steel','Panduit Stainless Steel Faceplate, 2-Port','ea',15.20,'all',true,'wf4_legacy'),
('Panduit','CBX2WH-AY','faceplate','2_port_surface','Panduit Mini-Com 2-Port Surface Mount Box, White','ea',7.33,'all',false,'wf4_legacy'),
('Panduit','CBX1WH-AY','faceplate','1_port_surface','Panduit Mini-Com 1-Port Surface Mount Box, White','ea',4.16,'all',false,'wf4_legacy'),
('Generic','FP-3PORT','faceplate','3_port','Faceplate, 3-Port, White','ea',3.66,'all',false,'wf4_legacy'),
('Generic','FP-FLOOR-2P','faceplate','floor_box','Floor Box Faceplate, 2-Port','ea',45.00,'all',false,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== PATCH CORDS (tier=all) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Generic','UTP28CH8BU','patch_cord','cat6a_8ft_blue','Cat 6A SD 8ft Blue','ea',37.94,'all',true,'wf4_legacy'),
('Generic','UTP28CH2BU','patch_cord','cat6a_2ft_blue','Cat 6A SD 2ft Blue','ea',29.35,'all',false,'wf4_legacy'),
('Generic','UTP28CH8GR','patch_cord','cat6a_8ft_green','Cat 6A SD 8ft Green','ea',37.94,'all',false,'wf4_legacy'),
('Generic','UTP28CH2GR','patch_cord','cat6a_2ft_green','Cat 6A SD 2ft Green','ea',29.35,'all',false,'wf4_legacy'),
('Generic','UTP28CH8VL','patch_cord','cat6a_8ft_violet','Cat 6A SD 8ft Violet','ea',37.94,'all',false,'wf4_legacy'),
('Generic','UTP28CH2VL','patch_cord','cat6a_2ft_violet','Cat 6A SD 2ft Violet','ea',29.35,'all',false,'wf4_legacy'),
('Generic','UTP28CH8GI','patch_cord','cat6a_8ft_grey','Cat 6A SD 8ft Grey','ea',37.94,'all',false,'wf4_legacy'),
('Generic','UTP28CH2GI','patch_cord','cat6a_2ft_grey','Cat 6A SD 2ft Grey','ea',29.35,'all',false,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== PATCH PANELS / CABLE MANAGEMENT =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Panduit','CPPL48WBLY','patch_panel','48_port','Panduit 48 Port Modular Snap-In Patch Panel','ea',98.30,'commercial',true,'wf4_legacy'),
('Panduit','CPPL48WBLY','patch_panel','48_port','Panduit 48 Port Modular Snap-In Patch Panel','ea',98.30,'enterprise',true,'wf4_legacy'),
('Panduit','CPPL24WBLY','patch_panel','24_port','Panduit 24 Port Modular Snap-In Patch Panel','ea',60.00,'qsr',true,'msrp_estimate'),
('Panduit','SRB19BLY','strain_relief','19in','Panduit Strain Relief Bar, 2" Deep, Black','ea',26.34,'all',true,'wf4_legacy'),
('Evolution','35441-702','cable_manager','horiz_2u','Evolution Horizontal Cable Manager, 19" Wide, 2RMU','ea',130.27,'commercial',true,'wf4_legacy'),
('Evolution','35441-702','cable_manager','horiz_2u','Evolution Horizontal Cable Manager, 19" Wide, 2RMU','ea',130.27,'enterprise',true,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== VIDEO SURVEILLANCE — Enterprise (i-PRO existing) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('i-PRO','WV-X25500-V3LN','camera_fixed','5mp_dome','i-PRO 5MP Outdoor Network Dome Camera with 2.9-9mm Lens','ea',1730.18,'enterprise',true,'wf4_legacy'),
('i-PRO','WV-S8573L','camera_ptz','25mp_multi','i-PRO 3x4K Outdoor Multi-Directional IP Camera AI','ea',2999.94,'enterprise',true,'wf4_legacy'),
('i-PRO','NVR-R-2-64TB-V8','nvr','enterprise','i-PRO NX Series High-Secured Network Video Recorder','ea',26400.00,'enterprise',true,'wf4_legacy'),
('i-PRO','IPSVC-UL','camera_license','single','i-PRO Single Camera License for Video Insight 7','ea',238.80,'enterprise',true,'wf4_legacy'),
('i-PRO','WV-QWL500-W','camera_mount','wall_white','i-PRO Wall Mount Bracket','ea',89.12,'enterprise',true,'wf4_legacy'),
('i-PRO','WV-QWL501-W','camera_mount','wall_white_alt','i-PRO Wall Mount Bracket (White)','ea',82.80,'enterprise',false,'wf4_legacy'),
('i-PRO','WV-QSR503-W','camera_mount','rec','i-PRO Mount Bracket (White)','ea',73.20,'enterprise',false,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== VIDEO SURVEILLANCE — Commercial / QSR (NEW additions) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Avigilon','HD-NVR-PREM-6TB','nvr','commercial','Avigilon HD NVR Premium 6TB Storage','ea',5000.00,'commercial',true,'msrp_estimate'),
('Avigilon','H6A-DO1-IR','camera_fixed','4mp_dome','Avigilon H6A 4MP IP Dome Camera with IR','ea',850.00,'commercial',true,'msrp_estimate'),
('Avigilon','H4-MT-CMNT','camera_mount','wall','Avigilon Wall Mount Bracket','ea',95.00,'commercial',true,'msrp_estimate'),
('Hikvision','DS-7608NXI-K2','nvr','qsr_8ch','Hikvision 8-Channel NVR, 2-bay, no HDD','ea',800.00,'qsr',true,'msrp_estimate'),
('Hikvision','DS-2CD2143G2-IS','camera_fixed','4mp_dome_qsr','Hikvision 4MP IP Dome Camera (QSR-grade)','ea',180.00,'qsr',true,'msrp_estimate'),
('Hikvision','DS-1273ZJ-130','camera_mount','wall_qsr','Hikvision Wall Mount Bracket (QSR)','ea',45.00,'qsr',true,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== ACCESS CONTROL =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
-- COSEC (Commercial)
('Matrix COSEC','ACM100','access_license','100_user','COSEC CENTRA Access Control - 100 User License','ea',492.00,'commercial',false,'wf4_legacy'),
('Matrix COSEC','PLT100','access_license','platform_users','COSEC CENTRA Platform Users - 10 User License','ea',360.00,'commercial',false,'wf4_legacy'),
('Hirsch Electronics','AEB8','access_expansion','8_input','Hirsch AEB8 8 Input Alarm Expansion Circuit Board','ea',102.00,'commercial',false,'wf4_legacy'),
-- HID Signo (all tiers - common reader)
('HID','Plus 6005','card_reader','prox','HID Proximity ProxPoint Plus 6005 Card Reader','ea',257.63,'all',false,'wf4_legacy'),
('HID','40KNKS','card_reader','signo_keypad','HID Signo 40K Wall Mount Keypad Reader','ea',394.94,'all',true,'wf4_legacy'),
-- Avigilon Unity (Enterprise)
('Avigilon','AC-MER-CONT','access_controller','unity_lp','Avigilon Unity LP Series Intelligent Controller','ea',1627.08,'enterprise',true,'wf4_legacy'),
('Avigilon','AC-MER-CON-MR','access_controller','2_reader','Avigilon 2-Reader Interface Module','ea',895.33,'enterprise',true,'wf4_legacy'),
('Avigilon','UA-SW-LIC','access_software','unity7_20door','Unity Access 7 Base Package License, 20-Doors','ea',4065.60,'enterprise',true,'wf4_legacy'),
('Avigilon','UA7-HYPER-V','access_software','virtual','Unity Access 7 Virtual Hyper-V Appliance License','ea',217.80,'enterprise',true,'wf4_legacy'),
-- Door hardware (all tiers)
('Bosch','ISN-CSD70-W','door_contact','recessed_magnetic','Bosch ISN-CSD70 3/4" Recessed Magnetic Contact','ea',33.16,'all',true,'wf4_legacy'),
('Honeywell','269R','hold_up_switch','dpdt','Honeywell 269R Hold-Up Switch, DPDT, Stainless Steel','ea',28.79,'all',false,'wf4_legacy'),
('Altronix','PS-ALTRONIX','power_supply','door','Altronix Power Supply for Doors','ea',720.00,'all',true,'wf4_legacy'),
-- Misc bucket
('Generic','MISC-AC','access_misc','misc','Miscellaneous Access Control Materials','lot',2400.00,'commercial',true,'wf4_legacy'),
('Generic','MISC-AC','access_misc','misc','Miscellaneous Access Control Materials','lot',2400.00,'enterprise',true,'wf4_legacy'),
('Generic','MISC-AC-QSR','access_misc','misc_qsr','Miscellaneous Access Control Materials (QSR)','lot',600.00,'qsr',true,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== INTRUSION (Bosch series) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Bosch','B9512G','intrusion_panel','main','Bosch B9512G Control Panel','ea',1043.65,'all',true,'wf4_legacy'),
('Bosch','B208','intrusion_expansion','8_input','Bosch B208 Expansion Module SDI2 8-Input','ea',160.24,'all',false,'wf4_legacy'),
('Bosch','B8103','intrusion_enclosure','universal','Bosch B8103 Universal Enclosure White','ea',131.77,'all',false,'wf4_legacy'),
('Bosch','D137','intrusion_bracket','accessory','Bosch D137 Mounting Bracket for Enclosure','ea',18.10,'all',false,'wf4_legacy'),
('Bosch','D9002-5','intrusion_plate','mounting','Bosch D9002-5 Mounting Plate 6-Loc 3-Hole','ea',50.50,'all',false,'wf4_legacy'),
('Bosch','D110','intrusion_tamper','enclosure','Bosch D110 Tamper Switch','ea',10.63,'all',false,'wf4_legacy'),
('Bosch','D122','intrusion_battery_harness','dual','Bosch D122 Dual Battery Harness','ea',19.79,'all',false,'wf4_legacy'),
('Bosch','D126','intrusion_battery','12v_7ah','Bosch D126 Battery 12V 7AH','ea',52.92,'all',false,'wf4_legacy'),
('Bosch','D1640','intrusion_transformer','16v_40va','Bosch D1640 Transformer 16V 40VA','ea',23.09,'all',false,'wf4_legacy'),
('Bosch','B426','intrusion_comm','ethernet','Bosch B426 Ethernet Communication Module','ea',377.40,'all',false,'wf4_legacy'),
('Bosch','B44-V2','intrusion_comm','cellular_lte','Bosch B44-V2 Conettix Plug-In Cell Module VZW LTE','ea',445.91,'all',false,'wf4_legacy'),
('Bosch','DS9370','motion_detector','tritech_50ft','Bosch DS9370 TriTech Motion Detector 50FT','ea',102.47,'all',true,'wf4_legacy'),
('Bosch','B920','intrusion_keypad','alpha_2line','Bosch B920 2-Line Alphanumeric Keypad SDI2','ea',204.00,'all',true,'wf4_legacy'),
('Honeywell','945T-WH','door_contact','mini_surface','Honeywell 945T-WH Mini Surface Mount Contact','ea',8.70,'all',true,'wf4_legacy'),
('Alarm Controls','TS-2','panic_button','generic','Alarm Controls TS-2 Panic Button','ea',150.00,'all',false,'wf4_legacy'),
('Generic','MISC-INT','intrusion_misc','misc','Miscellaneous Intrusion Materials','lot',3500.00,'all',true,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== AUDIO VISUAL / PAGING (all tiers) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Generic','SP-CEIL-70V','speaker','ceiling_70v','Ceiling Speaker, 70V, 8" with Backcan','ea',300.00,'all',true,'wf4_legacy'),
('Generic','SP-WALL-70V','speaker','wall_70v','Wall Baffle Speaker, 70V','ea',275.00,'all',false,'wf4_legacy'),
('Generic','AMP-240W','paging_amp','4zone_240w','Paging Amplifier, 240W, 4-Zone','ea',1200.00,'all',true,'wf4_legacy'),
('Generic','IC-STATION','intercom','flush','Intercom Station, Flush Mount','ea',800.00,'all',true,'wf4_legacy'),
('Generic','AV-DISPLAY','display','mount_cabling','Display/TV Mount and Cabling','ea',650.00,'all',true,'wf4_legacy'),
('Generic','AV-CONF','av_package','conference_room','Conference Room AV Package','ea',5000.00,'all',false,'wf4_legacy'),
('Generic','SP-WIRE','speaker_wire','14_2_plenum','14/2 Speaker Wire Plenum (1000ft)','box',350.00,'all',true,'wf4_legacy'),
('Generic','MISC-AV','av_misc','misc','Miscellaneous AV Materials','lot',1200.00,'all',true,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== NETWORK INFRASTRUCTURE (tiered) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
-- Racks tiered
('Generic','RACK-42U','rack','42u_floor','42U Equipment Rack with Cable Management','ea',2800.00,'enterprise',true,'wf4_legacy'),
('Chatsworth','RACK-18U','rack','18u_wall','Chatsworth Fixed Wall Mount Rack 19" 18U','ea',1180.90,'commercial',true,'wf4_legacy'),
('Generic','RACK-12U-WALL','rack','12u_wall_qsr','12U Wall Mount Rack (QSR-grade)','ea',400.00,'qsr',true,'msrp_estimate'),
-- PDUs all tiers
('Generic','RACK-PDU','pdu','20a_120v','Rack PDU, 20A, 120V','ea',450.00,'all',true,'wf4_legacy'),
-- Shelves
('Generic','RACK-SHELF','rack_shelf','19in_vented','Rack Shelf, 19" Vented','ea',85.00,'all',true,'wf4_legacy'),
-- Grounding tiered
('Generic','RACK-GROUND','grounding_kit','enterprise','Grounding Kit (busbar, conductor, clamps) - Enterprise','ea',6000.00,'enterprise',true,'wf4_legacy'),
('Panduit','GRND-COMM-KIT','grounding_kit','commercial','Panduit Grounding Kit - Commercial','ea',1500.00,'commercial',true,'msrp_estimate'),
('Generic','GRND-QSR-BAR','grounding_kit','qsr_basic','Basic Grounding Bar + Conductor (QSR)','ea',300.00,'qsr',true,'msrp_estimate'),
-- Labels all tiers (smaller for QSR but same line item)
('Generic','LABEL-KIT','labeling','machine_print','Labeling Kit (machine-printed labels)','ea',600.00,'commercial',true,'wf4_legacy'),
('Generic','LABEL-KIT','labeling','machine_print','Labeling Kit (machine-printed labels)','ea',600.00,'enterprise',true,'wf4_legacy'),
('Generic','LABEL-KIT-QSR','labeling','basic','Basic Labeling Kit (QSR)','ea',150.00,'qsr',true,'msrp_estimate'),
-- Backboards
('Generic','BACKBOARD','backboard','4x8_fire','4x8 Plywood Backboard, Fire-Rated','ea',250.00,'qsr',true,'wf4_legacy'),
('Generic','BACKBOARD','backboard','4x8_fire','4x8 Plywood Backboard, Fire-Rated','ea',250.00,'commercial',true,'wf4_legacy'),
-- UPS by tier
('APC','SMT1500','ups','1500va_tower','APC SmartUPS 1500VA Tower (QSR)','ea',300.00,'qsr',true,'msrp_estimate'),
('APC','SMT3000RM','ups','3000va_rack','APC SmartUPS 3000VA Rackmount (Commercial)','ea',1100.00,'commercial',true,'msrp_estimate'),
('APC','SMX3000RM2UC','ups','3000va_extended','APC SmartUPS 3000VA RackMount Extended Runtime (Enterprise)','ea',1900.00,'enterprise',true,'msrp_estimate'),
-- Misc rack
('Generic','MISC-RACK','rack_misc','misc','Miscellaneous Rack/MDF Materials','lot',800.00,'all',true,'wf4_legacy')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== FIRE ALARM (DISABLED — Antonio doesn't bid this scope) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, is_active, source, notes) VALUES
('Bosch','FPA-1000','fire_alarm_panel','main','Bosch FPA-1000 Fire Alarm Control Panel','ea',4500.00,'all',false,false,'wf4_legacy','Fire alarm out of scope per Antonio'),
('Bosch','FAP-440-T','smoke_detector','photoelectric','Bosch FAP-440 Photoelectric Smoke Detector','ea',225.00,'all',false,false,'wf4_legacy','Out of scope'),
('Bosch','FCS-320-TH','heat_detector','generic','Bosch FCS-320-TH Heat Detector','ea',185.00,'all',false,false,'wf4_legacy','Out of scope'),
('Generic','HN-S-R','horn_strobe','wall_red','Horn/Strobe Wall Mount Red','ea',325.00,'all',false,false,'wf4_legacy','Out of scope'),
('Generic','HN-S-C','horn_strobe','ceiling_red','Horn/Strobe Ceiling Mount Red','ea',345.00,'all',false,false,'wf4_legacy','Out of scope')
ON CONFLICT (manufacturer, model) DO NOTHING;

COMMIT;

-- Verify
SELECT category, tier, COUNT(*) AS parts_count, SUM(CASE WHEN is_default_for_tier THEN 1 ELSE 0 END) AS defaults
FROM tbe_parts_catalog
WHERE is_active
GROUP BY category, tier
ORDER BY category, tier;

SELECT 'Total active parts:' AS metric, COUNT(*)::text AS value FROM tbe_parts_catalog WHERE is_active
UNION ALL
SELECT 'Tier coverage (qsr defaults)', COUNT(DISTINCT category)::text FROM tbe_parts_catalog WHERE is_active AND tier='qsr' AND is_default_for_tier
UNION ALL
SELECT 'Tier coverage (commercial defaults)', COUNT(DISTINCT category)::text FROM tbe_parts_catalog WHERE is_active AND tier='commercial' AND is_default_for_tier
UNION ALL
SELECT 'Tier coverage (enterprise defaults)', COUNT(DISTINCT category)::text FROM tbe_parts_catalog WHERE is_active AND tier='enterprise' AND is_default_for_tier;
