# v0 — Stro's spine

One AI founder, working unattended on a heartbeat, with real books and
hard governance rails. No org chart, no office UI — those are later layers
on top of real events.

```
Railway cron ──▶ python -m stro.main          (one wake-up per run)
                    │
                    ├─ budget gate            burn ≥ 95% of cap → blocked + escalation
                    ├─ state briefing         journal + memory + tasks + books
                    ├─ agent session          Claude Agent SDK, founder.md persona
                    │     └─ company tools    journal / memory / tasks / escalate
                    └─ bookkeeping            wakeup row + inference cost → ledger
Supabase = the company                        (fresh project, shared with nothing)
```

## Files

- `stro/founder.md` — Stro's identity. The most load-bearing file in the repo.
- `stro/main.py` — one wake-up: gate → brief → work → book the cost.
- `stro/company.py` — Supabase state access.
- `stro/tools.py` — the only mutations Stro can make, all attributed to a wakeup.
- `supabase/migrations/0001_company_core.sql` — the world schema.

## Owner setup (once)

1. **Supabase**: new project → SQL editor → run `0001_company_core.sql`, then seed:
   ```sql
   insert into company (name, objective, budget_monthly_usd, model) values
     ('Company One',
      'Build a sustainable business. Choose what to build yourself.',
      50.00, 'claude-sonnet-5');
   ```
2. **Anthropic**: create a fresh API key used by nothing else.
3. **Railway**: new project → deploy this repo (Dockerfile) → set env vars
   from `stro/.env.example` → give the service a **cron schedule** instead of
   an always-on start:
   `0 6,13,20 * * *` (three sessions/day) fits a $50/mo cap with headroom.
4. Read `journal` (newest first) whenever you want to see your company.
   Answer `escalations` by setting `status` to `approved`/`denied` with a
   `resolution` — Stro sees the answer at his next wake-up.

## Deliberate v0 limits

- Workspace disk is ephemeral: durable knowledge must go through
  memory/journal (founder.md says so). A git workspace repo is v1.
- Resolved escalations reach Stro via the state briefing, not push.
- One company, one founder. Hiring requires the employee runtime — v1+.
- The observatory is `select * from journal order by ts desc` until the
  loop has proven itself. UI before substance is how this project fails.

## First milestone

Owner closes the laptop for 48 hours → returns to a coherent journal of
research, decisions and real work toward a product, and an accurate bill.
Then: raise the heartbeat rate, add the workspace repo, and let revenue
have somewhere to arrive.
