-- Sessions have shapes, and their economics differ by an order of
-- magnitude. Without recording which, cost-per-turn estimates pool cheap
-- ticks with expensive focus blocks and mislead both.
alter table wakeups add column if not exists mode text;
