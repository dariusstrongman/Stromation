-- Employees become real colleagues with real salaries.
-- An employee's "salary" IS the cost of running their model — hiring
-- someone genuinely increases the company's burn, and firing them
-- genuinely reduces it. Payroll is not a simulation.

alter table employees add column if not exists model text;
alter table employees add column if not exists hired_reason text;
alter table employees add column if not exists departed_at timestamptz;
alter table employees add column if not exists departed_reason text;

-- Work handed to an employee. Asynchronous, like real delegation: the
-- founder asks, the employee works after he finishes, the answer is
-- waiting for him next session.
create table delegations (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  employee_id uuid not null references employees(id),
  task text not null,
  context text,
  status text not null default 'pending'
    check (status in ('pending','done','failed')),
  result text,
  cost_usd numeric(10,4),
  created_at timestamptz not null default now(),
  completed_at timestamptz
);
create index on delegations (company_id, status);

-- Payroll is per-person, so the founder can see who earns their keep.
alter table ledger add column if not exists employee_id uuid references employees(id);
alter table ledger drop constraint if exists ledger_category_check;
alter table ledger add constraint ledger_category_check
  check (category in ('inference','infrastructure','tools','revenue',
                      'media','salary','other'));

-- Employees keep their own memory, so a colleague remembers last week.
alter table journal add column if not exists employee_id uuid references employees(id);
alter table memory add column if not exists employee_id uuid references employees(id);

alter table delegations enable row level security;
create policy "observatory read" on delegations for select using (true);
alter publication supabase_realtime add table delegations;
