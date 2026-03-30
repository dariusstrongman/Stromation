-- Stromation Schema Expansion
-- Run this in the Supabase SQL Editor at:
-- https://supabase.com/dashboard/project/iadzcnzgbtuigyodeqas/sql
--
-- Creates: projects, invoices, proposals tables
-- Date: 2026-03-29

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    business_id UUID REFERENCES businesses(id),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'proposed' CHECK (status IN ('proposed', 'approved', 'in_progress', 'delivered', 'completed')),
    tier TEXT CHECK (tier IN ('simple', 'ai_assisted', 'end_to_end')),
    amount NUMERIC(10,2),
    retainer_amount NUMERIC(10,2),
    timeline TEXT,
    start_date DATE,
    delivered_date DATE,
    completed_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    business_id UUID REFERENCES businesses(id),
    project_id UUID REFERENCES projects(id),
    invoice_num TEXT NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    status TEXT DEFAULT 'sent' CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')),
    due_date DATE,
    paid_date DATE,
    stripe_payment_id TEXT,
    stripe_payment_url TEXT,
    notes TEXT,
    sent_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Contracts/Proposals table
CREATE TABLE IF NOT EXISTS proposals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    business_id UUID REFERENCES businesses(id),
    project_title TEXT NOT NULL,
    description TEXT,
    tier TEXT,
    amount NUMERIC(10,2),
    retainer TEXT,
    timeline TEXT,
    status TEXT DEFAULT 'sent' CHECK (status IN ('sent', 'viewed', 'approved', 'declined', 'expired')),
    approved_at TIMESTAMPTZ,
    sent_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable Row Level Security (match existing tables)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE proposals ENABLE ROW LEVEL SECURITY;

-- Allow service_role full access (for n8n workflows)
CREATE POLICY "Service role full access" ON projects FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON invoices FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON proposals FOR ALL USING (true) WITH CHECK (true);

-- Indexes for common queries
CREATE INDEX idx_projects_business_id ON projects(business_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_invoices_business_id ON invoices(business_id);
CREATE INDEX idx_invoices_project_id ON invoices(project_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_proposals_business_id ON proposals(business_id);
CREATE INDEX idx_proposals_status ON proposals(status);
