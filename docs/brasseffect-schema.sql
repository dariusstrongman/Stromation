-- ============================================================
-- THE BRASS EFFECT - Division 27 Auto-Bidder System
-- Run in Supabase SQL Editor after creating the project
-- ============================================================

-- Bids: every project opportunity
CREATE TABLE bids (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_name TEXT NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('sam_gov', 'planhub', 'constructconnect', 'manual', 'referral', 'other')),
    source_url TEXT,

    -- Location
    location TEXT,
    city TEXT,
    state TEXT DEFAULT 'TX',

    -- Project details
    building_type TEXT,
    square_footage INTEGER,
    num_floors INTEGER,
    scope_summary TEXT,
    scope_categories TEXT[],
    division_codes TEXT,

    -- People
    general_contractor TEXT,
    gc_email TEXT,
    gc_phone TEXT,
    architect TEXT,
    project_owner TEXT,

    -- Money
    estimated_value NUMERIC(12,2),
    material_cost NUMERIC(12,2),
    labor_cost NUMERIC(12,2),
    overhead_cost NUMERIC(12,2),
    profit_amount NUMERIC(12,2),
    total_bid NUMERIC(12,2),
    won_amount NUMERIC(12,2),

    -- Pipeline
    status TEXT DEFAULT 'new' CHECK (status IN (
        'new', 'reviewing', 'estimating', 'quote_ready',
        'quote_sent', 'submitted', 'won', 'lost', 'no_bid', 'expired'
    )),
    relevance_score INTEGER CHECK (relevance_score BETWEEN 1 AND 10),
    bid_deadline TIMESTAMPTZ,
    submitted_at TIMESTAMPTZ,
    won_at TIMESTAMPTZ,
    lost_at TIMESTAMPTZ,
    lost_reason TEXT,

    -- Quote
    quote_html TEXT,
    quote_sent_to TEXT,
    quote_sent_at TIMESTAMPTZ,

    -- Meta
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Line items: materials + labor breakdown per bid
CREATE TABLE bid_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    bid_id UUID REFERENCES bids(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    item_name TEXT NOT NULL,
    description TEXT,
    quantity INTEGER DEFAULT 1,
    unit TEXT DEFAULT 'ea',
    unit_price NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    is_labor BOOLEAN DEFAULT false,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Pricing templates: default rates Antonio can adjust
CREATE TABLE pricing_defaults (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    item_key TEXT UNIQUE NOT NULL,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    default_unit_price NUMERIC(10,2) NOT NULL,
    unit TEXT DEFAULT 'ea',
    is_labor BOOLEAN DEFAULT false,
    notes TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Insert DFW market default pricing for Division 27
INSERT INTO pricing_defaults (item_key, item_name, category, default_unit_price, unit, is_labor, notes) VALUES
    -- Structured Cabling
    ('cat6_drop', 'Cat6 Data Drop', 'Structured Cabling', 225.00, 'drop', false, 'Includes cable, termination, testing, labeling'),
    ('cat6a_drop', 'Cat6A Data Drop', 'Structured Cabling', 325.00, 'drop', false, 'Includes cable, termination, testing, labeling'),
    ('fiber_sm_run', 'Single-Mode Fiber Run', 'Structured Cabling', 550.00, 'run', false, 'Includes fiber, termination, testing'),
    ('fiber_mm_run', 'Multi-Mode Fiber Run', 'Structured Cabling', 450.00, 'run', false, 'Includes fiber, termination, testing'),
    ('patch_panel_24', '24-Port Patch Panel', 'Structured Cabling', 185.00, 'ea', false, 'Loaded, labeled, tested'),
    ('patch_panel_48', '48-Port Patch Panel', 'Structured Cabling', 325.00, 'ea', false, 'Loaded, labeled, tested'),
    ('cable_tray_ft', 'Cable Tray/Basket', 'Structured Cabling', 18.00, 'ft', false, 'Installed with supports'),

    -- Network Infrastructure
    ('rack_buildout', 'Equipment Rack Buildout', 'Network Infrastructure', 5500.00, 'ea', false, 'Rack, power, grounding, cable management'),
    ('mdf_buildout', 'MDF/IDF Room Buildout', 'Network Infrastructure', 8500.00, 'ea', false, 'Full room: racks, backboard, power, grounding, labeling'),
    ('wifi_ap', 'WiFi Access Point Install', 'Network Infrastructure', 450.00, 'ea', false, 'AP, mount, cable, config'),

    -- Security / Access Control
    ('access_door', 'Access Control Door', 'Access Control', 2200.00, 'door', false, 'Reader, controller, lock hardware, wiring'),
    ('access_door_premium', 'Access Control Door (Premium)', 'Access Control', 3500.00, 'door', false, 'Biometric reader, electric strike, full hardware'),
    ('camera_fixed', 'Security Camera (Fixed)', 'Security / CCTV', 850.00, 'ea', false, 'Camera, mount, cable, license'),
    ('camera_ptz', 'Security Camera (PTZ)', 'Security / CCTV', 1800.00, 'ea', false, 'PTZ camera, mount, cable, license'),
    ('nvr', 'Network Video Recorder', 'Security / CCTV', 3500.00, 'ea', false, '32-channel NVR with storage'),

    -- Fire Alarm
    ('fa_pull_station', 'Fire Alarm Pull Station', 'Fire Alarm', 275.00, 'ea', false, 'Device, backbox, wiring'),
    ('fa_smoke_detector', 'Smoke Detector', 'Fire Alarm', 225.00, 'ea', false, 'Detector, base, wiring'),
    ('fa_horn_strobe', 'Horn/Strobe', 'Fire Alarm', 325.00, 'ea', false, 'Device, backbox, wiring'),
    ('fa_panel', 'Fire Alarm Control Panel', 'Fire Alarm', 4500.00, 'ea', false, 'Panel, programming, testing'),

    -- Audio Visual
    ('av_display', 'Display/TV Install', 'Audio Visual', 650.00, 'ea', false, 'Mount, cabling, termination (display not included)'),
    ('av_projector', 'Projector Install', 'Audio Visual', 1200.00, 'ea', false, 'Mount, cabling, screen (projector not included)'),
    ('av_conf_room', 'Conference Room AV Package', 'Audio Visual', 5000.00, 'room', false, 'Display, camera, soundbar, cabling, programming'),
    ('av_speaker', 'Ceiling Speaker', 'Audio Visual', 300.00, 'ea', false, 'Speaker, backcan, cabling'),

    -- Paging / Intercom
    ('paging_speaker', 'Paging Speaker', 'Paging / Intercom', 300.00, 'ea', false, 'Speaker, wiring, zone setup'),
    ('paging_amp', 'Paging Amplifier', 'Paging / Intercom', 1200.00, 'ea', false, 'Amp, zone controller, programming'),
    ('intercom_station', 'Intercom Station', 'Paging / Intercom', 800.00, 'ea', false, 'Station, wiring, programming'),

    -- Labor Rates
    ('labor_journeyman', 'Journeyman Technician', 'Labor', 45.00, 'hr', true, 'Experienced low-voltage tech'),
    ('labor_apprentice', 'Apprentice Technician', 'Labor', 22.00, 'hr', true, 'Entry-level tech'),
    ('labor_foreman', 'Project Foreman', 'Labor', 55.00, 'hr', true, 'On-site project lead'),
    ('labor_engineer', 'Systems Engineer', 'Labor', 75.00, 'hr', true, 'Design, programming, commissioning'),

    -- Overhead Rates (stored as percentages)
    ('overhead_pct', 'Overhead', 'Rates', 15.00, '%', false, 'Insurance, vehicles, tools, office'),
    ('profit_pct', 'Profit Margin', 'Rates', 15.00, '%', false, 'Target profit margin')
;

-- Activity log: tracks every status change
CREATE TABLE bid_activity (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    bid_id UUID REFERENCES bids(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    old_status TEXT,
    new_status TEXT,
    details TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE bids ENABLE ROW LEVEL SECURITY;
ALTER TABLE bid_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE pricing_defaults ENABLE ROW LEVEL SECURITY;
ALTER TABLE bid_activity ENABLE ROW LEVEL SECURITY;

-- Service role full access (for n8n workflows)
CREATE POLICY "Service role full access" ON bids FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON bid_items FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON pricing_defaults FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON bid_activity FOR ALL USING (true) WITH CHECK (true);

-- Anon read access (for dashboard)
CREATE POLICY "Anon read access" ON bids FOR SELECT USING (true);
CREATE POLICY "Anon read access" ON bid_items FOR SELECT USING (true);
CREATE POLICY "Anon read access" ON pricing_defaults FOR SELECT USING (true);
CREATE POLICY "Anon read access" ON bid_activity FOR SELECT USING (true);

-- Anon write for dashboard updates (status changes, notes, bid amounts)
CREATE POLICY "Anon update bids" ON bids FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "Anon insert activity" ON bid_activity FOR INSERT WITH CHECK (true);
CREATE POLICY "Anon update pricing" ON pricing_defaults FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "Anon insert items" ON bid_items FOR INSERT WITH CHECK (true);
CREATE POLICY "Anon update items" ON bid_items FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "Anon delete items" ON bid_items FOR DELETE USING (true);

-- Indexes
CREATE INDEX idx_bids_status ON bids(status);
CREATE INDEX idx_bids_deadline ON bids(bid_deadline);
CREATE INDEX idx_bids_source ON bids(source);
CREATE INDEX idx_bids_created ON bids(created_at DESC);
CREATE INDEX idx_bid_items_bid ON bid_items(bid_id);
CREATE INDEX idx_bid_activity_bid ON bid_activity(bid_id);
