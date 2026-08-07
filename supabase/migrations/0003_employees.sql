-- Employees become first-class beings. v0 has exactly one: the founder.
-- sprite is self-authored pixel art: {"palette": ["#hex", ...],
-- "grid": [[0,2,1,...] x16 rows]} — 0 transparent, N = palette[N-1].
-- The office renders whatever the employee drew. Identity is data.

create table employees (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references company(id),
  name text not null,
  role text not null,
  personality text,
  sprite jsonb,
  status text not null default 'active'
    check (status in ('active','departed')),
  hired_at timestamptz not null default now()
);
create index on employees (company_id, status);

alter table employees enable row level security;
create policy "observatory read" on employees for select using (true);
alter publication supabase_realtime add table employees;

-- The founder exists from day zero; his appearance is his own first choice.
insert into employees (company_id, name, role)
select id, 'Stro', 'Founder & CEO' from company;
