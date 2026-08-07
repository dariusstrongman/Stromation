-- The observatory: every move Stro makes becomes a watchable event, and the
-- world becomes safely readable from a browser (read-only, RLS-enforced).

-- Every SDK message in a work session: thoughts, tool calls, results.
create table events (
  id bigint generated always as identity primary key,
  company_id uuid not null references company(id),
  wakeup_id uuid references wakeups(id),
  ts timestamptz not null default now(),
  kind text not null
    check (kind in ('session_start','thought','tool_use','tool_result',
                    'session_end')),
  title text,
  body text
);
create index on events (company_id, id desc);

-- Read-only world: anon may SELECT everything, write NOTHING.
-- Stro's service_role key bypasses RLS; the browser key cannot mutate.
alter table company     enable row level security;
alter table wakeups     enable row level security;
alter table journal     enable row level security;
alter table memory      enable row level security;
alter table tasks       enable row level security;
alter table ledger      enable row level security;
alter table escalations enable row level security;
alter table events      enable row level security;

create policy "observatory read" on company     for select using (true);
create policy "observatory read" on wakeups     for select using (true);
create policy "observatory read" on journal     for select using (true);
create policy "observatory read" on memory      for select using (true);
create policy "observatory read" on tasks       for select using (true);
create policy "observatory read" on ledger      for select using (true);
create policy "observatory read" on escalations for select using (true);
create policy "observatory read" on events      for select using (true);

-- Live push to the browser.
alter publication supabase_realtime add table events, wakeups, journal;
