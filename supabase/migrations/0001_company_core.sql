-- Stromation company core: the world one AI founder lives in.
-- Everything Stro is, knows, owes, and has decided lives in these tables.

-- The company itself: exactly one row per company. v0 has one company.
create table company (
  id uuid primary key default gen_random_uuid(),
  name text not null default 'Unnamed Company',
  objective text not null,
  budget_monthly_usd numeric(10,2) not null,
  model text not null default 'claude-sonnet-5',
  created_at timestamptz not null default now()
);

-- Every wake-up is one unit of founder work with a metered cost.
create table wakeups (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  status text not null default 'running'
    check (status in ('running','completed','failed','budget_blocked')),
  cost_usd numeric(10,4),
  num_turns int,
  summary text
);

-- The founder's journal: the narrative the owner reads. Append-only.
create table journal (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  wakeup_id uuid references wakeups(id),
  ts timestamptz not null default now(),
  entry_type text not null default 'note'
    check (entry_type in ('note','decision','learning','milestone','problem')),
  content text not null
);

-- Institutional memory: durable knowledge, one fact/policy/insight per row.
-- Unlike the journal (what happened), memory is what the company KNOWS.
create table memory (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  slug text not null,
  kind text not null default 'knowledge'
    check (kind in ('knowledge','strategy','customer','product','policy')),
  content text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (company_id, slug)
);

-- Work: what the founder has decided to do, is doing, has done.
create table tasks (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  title text not null,
  why text,
  status text not null default 'open'
    check (status in ('open','in_progress','done','dropped')),
  priority int not null default 3 check (priority between 1 and 5),
  result text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- The books. Every dollar in or out, including every thought (inference).
create table ledger (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  wakeup_id uuid references wakeups(id),
  ts timestamptz not null default now(),
  category text not null
    check (category in ('inference','infrastructure','tools','revenue','other')),
  description text not null,
  amount_usd numeric(10,4) not null  -- negative = expense, positive = revenue
);

-- Actions beyond the founder's authority wait here for the owner.
create table escalations (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  wakeup_id uuid references wakeups(id),
  ts timestamptz not null default now(),
  action text not null,
  reason text not null,
  status text not null default 'pending'
    check (status in ('pending','approved','denied')),
  resolution text,
  resolved_at timestamptz
);

create index on journal (company_id, ts desc);
create index on ledger (company_id, ts desc);
create index on tasks (company_id, status);
create index on escalations (company_id, status);
