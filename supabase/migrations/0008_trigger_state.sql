-- Triggers must fire on NEW things, not on the continued existence of old
-- ones. Without a high-water mark, one unread newsletter wakes the founder
-- every sixty seconds forever.
alter table company add column if not exists trigger_state jsonb not null default '{}'::jsonb;
