-- TBE parts catalog: add real-world brands surfaced by drawing audits.
-- Pulled from actual project specs (Jimmy John's prototype + general QSR/commercial knowledge).
-- Run after tbe-parts-catalog-seed.sql. Idempotent.

BEGIN;

-- ===== NETWORK SWITCHES (Dell — most common in QSR/retail) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Dell','PowerConnect 3524','network_switch','24_port_managed','Dell PowerConnect 3524 24-port managed L2 switch','ea',650.00,'qsr',true,'spec_jimmy_johns'),
('Dell','N3024','network_switch','24_port_managed','Dell N3024 24-port managed L2 switch','ea',850.00,'commercial',true,'msrp_estimate'),
('Dell','N3048','network_switch','48_port_managed','Dell N3048 48-port managed L2 switch','ea',1500.00,'commercial',false,'msrp_estimate'),
('Dell','N1524','network_switch','24_port_smart','Dell N1524 24-port smart-managed switch','ea',500.00,'qsr',false,'msrp_estimate'),
('Cisco','C1000-24P','network_switch','24_port_poe','Cisco Catalyst 1000 24-port PoE+','ea',1200.00,'enterprise',true,'msrp_estimate'),
('Cisco','C1000-48P','network_switch','48_port_poe','Cisco Catalyst 1000 48-port PoE+','ea',2200.00,'enterprise',false,'msrp_estimate'),
('Aruba','2530-24G-PoEP','network_switch','24_port_poe_aruba','Aruba 2530-24G PoE+ switch','ea',1100.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== ROUTERS =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Netopia','4686XL','router','dsl_business','Netopia 4686XL business router (legacy QSR)','ea',300.00,'qsr',true,'spec_jimmy_johns'),
('Cisco','ISR 1100','router','small_business','Cisco ISR 1100 small business router','ea',900.00,'commercial',true,'msrp_estimate'),
('Cisco','ASR 1001-X','router','enterprise','Cisco ASR 1001-X enterprise router','ea',5500.00,'enterprise',true,'msrp_estimate'),
('Meraki','MX67','router','sd_wan_qsr','Cisco Meraki MX67 SD-WAN appliance','ea',650.00,'qsr',false,'msrp_estimate'),
('Meraki','MX95','router','sd_wan_comm','Cisco Meraki MX95 SD-WAN appliance','ea',2400.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== RACK CABINETS (Middle Atlantic — actual brand from audit) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Middle Atlantic','EWR-12-17','rack','12u_wall_qsr','Middle Atlantic EWR-12-17 12U wall-mount rack (17in deep)','ea',520.00,'qsr',true,'spec_jimmy_johns'),
('Middle Atlantic','EWR-18-17','rack','18u_wall','Middle Atlantic EWR-18-17 18U wall-mount rack','ea',780.00,'commercial',true,'spec_jimmy_johns'),
('Middle Atlantic','MRK-3231','rack','42u_floor_mid','Middle Atlantic MRK-3231 42U floor rack','ea',2100.00,'enterprise',false,'msrp_estimate'),
('Middle Atlantic','BGR-4536','rack','45u_open_frame','Middle Atlantic BGR-4536 45U open-frame relay rack','ea',1400.00,'enterprise',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== RACK PDUS (Middle Atlantic) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Middle Atlantic','PD-915RV-R','rack_pdu','9_outlet_rackmount','Middle Atlantic PD-915RV-R 9-outlet rackmount PDU w/ surge','ea',285.00,'qsr',true,'spec_jimmy_johns'),
('Middle Atlantic','PD-NRP6-RN','rack_pdu','6_outlet_rackmount','Middle Atlantic PD-NRP6-RN 6-outlet rackmount PDU','ea',195.00,'qsr',false,'msrp_estimate'),
('Middle Atlantic','PD-815R','rack_pdu','8_outlet_rackmount','Middle Atlantic PD-815R 8-outlet rackmount PDU','ea',225.00,'commercial',true,'msrp_estimate'),
('Tripp Lite','PDU3MV6L2120','rack_pdu','3phase_30a','Tripp Lite 3-phase 30A rack PDU','ea',1100.00,'enterprise',true,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== PHONE SYSTEMS (Mitel + others) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Mitel','MiVoice Office 250','phone_system','small_office','Mitel MiVoice Office 250 phone system base','ea',2400.00,'qsr',true,'spec_jimmy_johns'),
('Mitel','6863i','phone_handset','sip_handset','Mitel 6863i SIP handset','ea',180.00,'qsr',true,'msrp_estimate'),
('Mitel','MiVoice Business','phone_system','enterprise','Mitel MiVoice Business enterprise phone system','ea',8500.00,'enterprise',true,'msrp_estimate'),
('RingCentral','MVP Cloud','phone_system','cloud_pbx','RingCentral MVP Cloud PBX (per seat/mo)','ea',35.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== AUDIO/PAGING (Atlas Sound + Bose — common brands) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Atlas Sound','TSD-PA40G','paging_amp','40w_4zone_qsr','Atlas Sound TSD-PA40G 40W 4-zone paging amp (QSR)','ea',650.00,'qsr',true,'msrp_estimate'),
('Atlas Sound','PA-1001','paging_amp','100w_commercial','Atlas Sound PA-1001 100W commercial paging amp','ea',950.00,'commercial',true,'msrp_estimate'),
('Atlas Sound','TSD-PA240G','paging_amp','240w_zoned','Atlas Sound TSD-PA240G 240W zoned amp','ea',1450.00,'enterprise',false,'msrp_estimate'),
('Atlas Sound','FAP62T','speaker','ceiling_70v_qsr','Atlas Sound FAP62T 6.5in ceiling speaker 70V (QSR-grade)','ea',95.00,'qsr',true,'msrp_estimate'),
('Atlas Sound','FAP82T','speaker','ceiling_70v_8in','Atlas Sound FAP82T 8in ceiling speaker 70V','ea',135.00,'commercial',true,'msrp_estimate'),
('Bose','FreeSpace DS 16F','speaker','ceiling_premium','Bose FreeSpace DS 16F ceiling speaker','ea',285.00,'enterprise',true,'msrp_estimate'),
('JBL','Control 26C','speaker','ceiling_commercial','JBL Control 26C ceiling speaker','ea',195.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== DRIVE-THRU INTERCOMS =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('HME','EOS HD','intercom','drive_thru_qsr','HME EOS HD Drive-Thru audio system (full kit)','ea',8500.00,'qsr',true,'msrp_estimate'),
('3M','XT-1','intercom','drive_thru_basic','3M XT-1 Drive-Thru system (basic)','ea',5500.00,'qsr',false,'msrp_estimate'),
('PAR Technology','EverServ Drive-Thru','intercom','qsr_pos_integrated','PAR EverServ Drive-Thru audio (POS-integrated)','ea',9500.00,'qsr',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== PATCH PANELS — additional sizes =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Panduit','CFAPPBL1','patch_panel','24_port_blank','Panduit CFAPPBL1 24-port modular patch panel (blank)','ea',75.00,'qsr',false,'spec_jimmy_johns'),
('Panduit','DP24688TGV','patch_panel','24_port_loaded','Panduit DP24688TGV 24-port loaded Cat 6A','ea',285.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== POS EQUIPMENT (Signature Systems + common) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Signature Systems','PDX Component Box','pos_equipment','qsr_network_box','Signature Systems PDX network component box (preconfig QSR)','ea',1850.00,'qsr',false,'spec_jimmy_johns'),
('Toast','Flex Terminal','pos_terminal','restaurant','Toast Flex POS terminal','ea',850.00,'qsr',false,'msrp_estimate'),
('Square','Register','pos_terminal','retail','Square Register POS terminal','ea',799.00,'qsr',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== HIKVISION CAMERA VARIANTS (more sizes) =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('Hikvision','DS-7616NXI-K2','nvr','qsr_16ch','Hikvision DS-7616NXI-K2 16-channel NVR (larger QSR)','ea',1100.00,'qsr',false,'msrp_estimate'),
('Hikvision','DS-7732NXI-I4','nvr','commercial_32ch','Hikvision DS-7732NXI-I4 32-channel NVR','ea',1850.00,'commercial',false,'msrp_estimate'),
('Hikvision','DS-2CD2T46G2-2I','camera_fixed','4mp_bullet_outdoor','Hikvision DS-2CD2T46G2-2I 4MP outdoor bullet camera','ea',220.00,'qsr',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

-- ===== UPS additions =====
INSERT INTO tbe_parts_catalog (manufacturer, model, category, sub_category, description, unit, unit_price, tier, is_default_for_tier, source) VALUES
('CyberPower','OR1500LCDRT2U','ups','1500va_rack_2u','CyberPower OR1500LCDRT2U 1500VA rackmount UPS','ea',420.00,'commercial',false,'msrp_estimate'),
('Eaton','5PX 1500VA','ups','1500va_eaton','Eaton 5PX 1500VA rackmount UPS','ea',780.00,'commercial',false,'msrp_estimate')
ON CONFLICT (manufacturer, model) DO NOTHING;

COMMIT;

-- Verify
SELECT category, COUNT(*) FILTER (WHERE is_active) AS active, COUNT(*) FILTER (WHERE source LIKE 'spec_%') AS from_real_specs
FROM tbe_parts_catalog
GROUP BY category
ORDER BY active DESC;
