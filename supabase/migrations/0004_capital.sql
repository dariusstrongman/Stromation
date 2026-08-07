-- Starting capital: the card's total limit, mirrored into the world so the
-- books can show capital remaining. The card issuer enforces the ceiling;
-- this row lets the ledger account for it.
alter table company add column if not exists
  starting_capital_usd numeric(10,2) not null default 0;
update company set starting_capital_usd = 100.00;
