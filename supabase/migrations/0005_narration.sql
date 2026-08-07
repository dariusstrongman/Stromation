-- The documentary track. One narration per session, generated automatically
-- when the session ends. Grounded in that session's real events — the
-- observatory's rule holds here too: nothing narrated that did not happen.
create table narrations (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  wakeup_id uuid not null references wakeups(id) unique,
  day int,
  title text,
  script text not null,          -- full voiceover, paragraph per beat
  created_at timestamptz not null default now()
);
alter table narrations enable row level security;
create policy "observatory read" on narrations for select using (true);
alter publication supabase_realtime add table narrations;

-- The owner's documentary is not the founder's business expense.
alter table ledger drop constraint if exists ledger_category_check;
alter table ledger add constraint ledger_category_check
  check (category in ('inference','infrastructure','tools','revenue',
                      'media','other'));
