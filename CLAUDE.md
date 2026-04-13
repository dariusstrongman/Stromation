# Stromation

## Project Overview
- **stromation.com** -- Workflow Replacement Studio owned by Darius Stroman
- Static HTML/CSS/JS site hosted on GitHub Pages (public repo)
- Repo: github.com/dariusstrongman/Stromation
- Domain: www.stromation.com (CNAME)
- Twitter/X: @stromationhq
- Business email: darius@stromation.com (SMTP credential: "admin")
- Contact email: contact@stromation.com (used sitewide, replaced support@)
- Leads email: leads@stromation.com (SMTP credential: "SMTP - Stromation (leads@)")
- Outreach email: chase@stromation.com (SMTP credential: "SMTP - Outreach(Chase)") -- "Chase" is the sales persona
- Bids email: bids@stromation.com (alias under darius@, for ConstructConnect/PlanHub alerts)
- Antonio email: antonio@tbeit.com (TBE quotes sent here)
- Darius personal email: dariusstroman@gmail.com
- Stripe account: Stromation (live, charges enabled)

## Tech Stack
- Pure vanilla HTML, CSS, JS -- no frameworks, no build tools, no bundlers
- Google Fonts (Inter, weights 400-800)
- Google Analytics (G-B6Z6XV02RT)
- Forms submit to n8n webhook (stromation-form), NOT Formspree
- Chat widget (chat.js) connects to n8n webhook
- Schema.org structured data: ProfessionalService (index), FAQPage (services, audit, faq), Service+LocalBusiness (dental, home-services, agencies), BreadcrumbList (all main pages + blog posts)
- RSS feed (feed.xml) for blog syndication
- OG and Twitter meta tags on all pages
- Supabase (iadzcnzgbtuigyodeqas.supabase.co) for lead/business CRM
- Supabase anon key: sb_publishable_8qa-nssfdtEkCz-42wOSWQ_2P7S4Zj7 (safe for frontend)
- Supabase service key: REDACTED_USE_N8N_CREDENTIALS (server-side only, never in frontend code)
- Google Places API for local business discovery
- Cal.com booking: https://cal.com/darius-stroman-byeng8/30min (embedded on audit.html and thank-you.html)
- Remotion project at C:/Users/Darius/Desktop/stromation-video for video generation
- Anthropic API (Claude Sonnet 4.6) for blueprint PDF analysis (rate limit: queue scans 5 min apart)
- html2pdf.app API for quote PDF generation
- PlanHub REST API (api.planhub.com/api/v1/) for project details, file lists, downloads (auth token captured from browser)

## Site Structure

### Root Pages (28 pages)
| File | Purpose |
|------|---------|
| index.html | Homepage -- hero, showcase video (lazy loaded), services, how-it-works, stats, testimonial |
| services.html | 5 service categories (Intake, Ops, Support, Reporting, Custom Workflows) + 4 pricing tiers + retainers (FAQ schema) |
| industries.html | Industries hub — 8 cards linking to dedicated landing pages (nav says "Industries" not "Workflows") |
| case-studies.html | Client case studies with results |
| about.html | About Darius, company story |
| contact.html | Contact form (n8n webhook) |
| audit.html | Free audit form (FAQ schema) + Cal.com booking embed |
| blog.html | Blog index with card grid |
| faq.html | Standalone FAQ page (17 questions, 5 categories, accordion UI, FAQPage schema) |
| checklist.html | Lead magnet -- automation readiness checklist with email capture |
| roi-calculator.html | Interactive ROI calculator with live math + email capture |
| thank-you.html | Post-form confirmation + Cal.com booking (noindex) |
| dental.html | Ad landing page for dental practices (Service+LocalBusiness schema) |
| home-services.html | Ad landing page for home service businesses (Service+LocalBusiness schema) |
| agencies.html | Ad landing page for marketing agencies (Service+LocalBusiness schema) |
| real-estate.html | Ad landing page for real estate (Service+LocalBusiness schema) |
| accounting.html | Ad landing page for accounting firms (Service+LocalBusiness schema) |
| legal.html | Ad landing page for law firms (Service+LocalBusiness schema) |
| fitness.html | Ad landing page for gyms/fitness (Service+LocalBusiness schema) |
| restaurants.html | Ad landing page for restaurants (Service+LocalBusiness schema) |
| admin-invoice.html | Admin: send invoices (password protected: Kyomi123, noindex) |
| admin-proposal.html | Admin: send proposals (password protected: Kyomi123, noindex) |
| admin-dashboard.html | Admin: live CRM dashboard from Supabase (password protected: Kyomi123, noindex) |
| admin-retainer.html | Admin: set up Stripe subscription retainer billing (password protected: Kyomi123, noindex) |
| admin-bids.html | Admin: TBE bid tracker dashboard -- pipeline board, quote preview, blueprint upload, send to Antonio (password protected: Kyomi123, noindex) |
| admin-coldcall.html | Admin: cold call script dashboard for outreach -- step-by-step prompts, notes, outcome logging (password protected: Kyomi123, noindex) |
| project-status.html | Client project status page (noindex, UUID-based auth, uses anon key) |
| privacy.html | Privacy policy |
| terms.html | Terms of service |
| 404.html | Custom 404 error page |

### Blog Posts (blog/) -- 19 posts
All posts have reading time badges, breadcrumbs, internal cross-links, and 3 related posts.
- 5-signs-business-needs-workflow-automation.html
- automate-lead-follow-up.html
- real-cost-of-manual-work.html
- what-is-an-automation-audit.html
- zapier-vs-make-vs-custom-automations.html
- small-business-automation-save-time.html
- top-5-automation-mistakes-small-businesses.html
- streamlining-client-onboarding-with-automation-tools.html
- maximizing-efficiency-automating-client-follow-up-process.html
- harnessing-ai-for-smarter-workflow-automation.html
- future-of-automation-integrating-ai-business-workflows.html
- transform-your-business-with-no-code-workflow-automation-tools.html
- automate-invoicing-get-paid-faster.html
- automate-appointment-scheduling-reduce-no-shows.html
- automate-google-review-requests.html
- stop-manually-entering-data-between-apps.html
- maximizing-roi-business-process-automation-strategies.html
- benefits-automating-customer-support-workflows.html
- automate-social-media-scheduling-increase-engagement.html

New posts auto-generated weekly by WF25 (Sunday 6AM CT).

### Other Key Files
| File | Purpose |
|------|---------|
| styles.css | Single global stylesheet (includes .breadcrumb CSS) |
| script.js | Main JS -- mobile menu, scroll animations, parallax, forms, FAQ accordion |
| chat.js | Chat widget connecting to n8n webhook (deferred on all pages) |
| stromation-showcase.mp4 | 48s showcase video (lazy loaded on homepage) |
| video-thumbnail.png | Poster image for showcase video |
| feed.xml | RSS feed (18 blog posts) |
| sitemap.xml | XML sitemap for search engines |
| robots.txt | Robots directives |
| voicemail.xml | TwiML -- redirects callers to text (Google Neural2-J voice) |
| CNAME | GitHub Pages custom domain |
| .gitignore | Excludes workflow-backups/ |
| .nojekyll | Disables Jekyll processing |

### docs/ (internal business documents, not served on site)
| File | Purpose |
|------|---------|
| sales-playbook.md | Discovery questions, objection handlers, closing scripts |
| service-agreement.md | SOW/contract template for client projects |
| brasseffect-schema.sql | TBE Supabase schema (5 tables, 32+ pricing defaults, TBE_ prefix) |
| linkedin-profile.md | Optimized LinkedIn profile copy |
| linkedin-posts.md | 4 weekly LinkedIn posts |
| twitter-content-30days.md | 30 days of tweets for @stromationhq |
| supabase-schema.sql | SQL for projects/invoices/proposals tables |

### workflow-templates/ (reusable n8n templates for client deployments)
| File | Purpose |
|------|---------|
| missed-call-textback.json | Missed Call Text-Back system -- Twilio missed call -> instant SMS -> AI reply -> lead logging |
| missed-call-setup-guide.md | Step-by-step deployment guide for the missed call system |
| README.md | Template index and overview |

### Image Assets
- `img/` -- SVG illustrations for services, case studies, steps, Stripe tier images
- `logos/` -- logo.svg, logo.png, stromation-icon.svg, logo-transparent.svg, logo-transparent.png, logo-transparent-white.png
- Root: logo.svg (nav icon), logo-icon.svg (SVG favicon), logo.png, banner-1500x500.png, profile-pic-400x400.png, favicon.ico

## n8n Workflows (n8n.myaibuffet.com) -- 33 total (30 active, 1 OFF, 1 template, 1 deleted)

### TBE (The Brass Effect) Workflows
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| uTiy5gtBbhoL2wjo | TBE - Auto Bidder Engine | Webhook (/tbe-bid) | GPT scope analysis OR blueprint bypass → component expansion with real Panduit/i-Pro/Bosch part numbers → professional quote HTML → Supabase. v2: Watson-format quotes. |
| 3IjbS6wWZIxQSj9a | TBE - Quote Sender | Webhook (/tbe-send-quote) | Generates PDF via html2pdf.app → emails to Darius (test mode) with PDF attachment + notify email. From bids@. |
| Xi7gyvl3tzMqaknK | TBE - SAM.gov Bid Finder | Daily 6AM CT | SAM.gov API (DEMO_KEY) → Division 27 opportunities → auto-bidder. |
| VYQEc5i1Ae2usxN3 | TBE - Deadline Reminders | Daily 8AM CT | Queries active bids with upcoming deadlines, emails summary. Skips expired. From leads@. |
| BittpG8u35xMAuUr | TBE - Weekly Analytics | Monday 8AM CT | Pipeline stats, win rate, revenue summary email. |
| MCioEt93wGOlbd7d | TBE - Blueprint Analyzer | Webhook (/tbe-blueprint) | Accepts PDF upload (multipart binary OR JSON with pdf_base64) → Claude Sonnet 4.6 vision counts Division 27 devices → feeds counts to auto-bidder (skips GPT). |
| 6OXGUtj6mQlWSsEQ | TBE - Bid Alert Parser | Every 30 min | Checks bids@ inbox for PlanHub/ConstructConnect ITB emails → extracts project data → PlanHub ITBs auto-call File Downloader (extracts project ID from email) → plans analyzed → auto-bids. CC/other sources use direct bidder. Filters marketing/API emails. |
| CJlS0xgvY4oHtQsy | TBE - PlanHub File Downloader | Webhook (/tbe-download-plans) | PlanHub REST API → download PDF/ZIP to disk → auto-detect format (magic bytes) → smart Div 27 filter (E/T sheets, electrical, fire alarm, security) → max 3 PDFs to Blueprint Analyzer. Skips civil/structural/arch/mech. Cleanup after. |

### Client Templates (inactive, duplicate per client)
| ID | Name | Description |
|----|------|-------------|
| ADsVwfxGwkXDlinp | TEMPLATE - Missed Call Text-Back | Twilio missed call -> SMS text-back -> AI reply handler -> lead logging. Port client number to your Twilio, deploy in 15 min. |

### Lead Capture & Communication
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 11 | SMS Handler | Webhook | AI text replies + emails leads to Gmail. Validates: skips empty SMS body. |
| 12 | Website Chatbot | Webhook | GPT as Darius, fixVoice post-processing, resists prompt injection |
| 22 | Website Form Handler | Webhook | Forms → Supabase + email. Validates: requires email or phone, checks email format. |

### Outbound & Outreach
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 18 | Local Business Finder | Daily 7AM CT | Google Places API → DFW businesses (15/run, 4 types) → 5-page email scrape → Disify verification → Supabase. No info@ guessing. |
| 19 | Cold Email Outreach | Daily 9AM CT | 3-email sequence from chase@, Chase persona, fixVoice, dedup check. Build Emails → Send Email + Log & Update (parallel). |
| 20 | Outreach Reply Handler | IMAP trigger (chase@) | AI replies as Chase, extracts phone/tools/pain, hot leads handed off to Darius. Updates Supabase. |
| 23 | Lead Nurture Drip | Daily 10AM CT | 3-email drip for website leads (seq 50/51/52) |

### Reddit (u/dev_darius -- karma -1, building up)
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 13 | Reddit Community Bot | **OFF** | Posts to subreddits -- disabled until karma 50+ |
| 14 | Reddit Comment Bot | 2x daily | Comments on relevant automation posts |
| 15 | Reddit Reply Handler | Every 4-8 hours | Responds to replies on our comments |
| 17 | Reddit Karma Builder | Daily 9AM CT | Casual comments on safe subreddits, max 2/run |
| 21 | Reddit Lead Digest | Daily 6PM CT | Scans Reddit for high-intent posts, emails digest |

### Content & Reporting
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 24 | Weekly Pipeline Digest | Monday 8AM CT | Pipeline stats + hot leads email to Gmail |
| 25 | Auto Blog Publisher | Sunday 6AM CT | GPT → blog post → GitHub commit → updates blog.html + sitemap + RSS |

### Client Delivery
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 31 | Client Weekly Update | Friday 4PM CT | Queries active projects, sends branded weekly update email with status link. From darius@. |
| 32 | Post-Delivery Sequence | Daily 11AM CT | Day 1: review request, Day 7: referral ask ($100 off), Day 30: case study questionnaire. Tracks via [SENT:tag] in project notes. From darius@. |

### Client Management (webhook-triggered)
| ID | Name | Webhook | Description |
|----|------|---------|-------------|
| 26 | Review Request | /webhook/stromation-review-request | Review request email. Validates: requires client_email. |
| 27 | Invoice Generator | /webhook/stromation-invoice | Professional invoice + Stripe Pay Now link. Validates: requires email, positive amount. From darius@. |
| 28 | Client Onboarding | /webhook/stromation-onboard | Welcome email + intake link, status → 'won'. Validates: requires email + name. |
| 30 | Proposal Generator | /webhook/stromation-proposal | Branded proposal email. Validates: requires email, amount, project_title. From darius@. |
| 33 | Retainer Billing Setup | /webhook/stromation-retainer | Creates Stripe subscription checkout session, sends payment link email. From darius@. |

### Operations
| ID | Name | Description |
|----|------|-------------|
| 29 | Error Alert | **DELETED** -- was too noisy from IMAP drops. |

### SMTP/IMAP Credentials
| Credential | Email | Used By |
|------------|-------|---------|
| SMTP - Stromation (leads@) | leads@stromation.com | WF11, WF21, WF22, WF23, WF24, WF25, WF26, WF29 |
| admin | darius@stromation.com | WF27 (invoices), WF30 (proposals), WF31 (weekly update), WF32 (post-delivery), all TBE workflows |
| SMTP - Outreach(Chase) | chase@stromation.com | WF19 (cold email outreach) |
| IMAP - Outreach(chase) | chase@stromation.com | WF20 (watches inbox for replies) |

**Chase is the outreach persona.** Cold emails go from chase@stromation.com. When a lead gets hot, Chase hands off to Darius. outreach@stromation.com was deleted -- do not reference it.
**BCC:** All cold emails from WF19 are BCC'd to darius@stromation.com so Darius gets a copy of every outreach.

### Critical n8n Rules
- Use `this.helpers.httpRequest()` -- NOT fetch(), NOT require()
- emailSend v2.1: use `text` or `html` param -- NOT `message` (silently ignored = blank emails)
- Always set `options: { appendAttribution: false }` on email nodes
- fromEmail MUST match SMTP credential user (or 553 rejection)
- Error workflow: WF29 (37Mu8KJyxksGOe8B)
- Valid outreach_status: new, in_campaign, replied, won, lost, not_interested, sequence_complete, unsubscribed, bounced
- INVALID status values (400 error): qualified, client, audit_requested

## Supabase

### Keys
- Anon (frontend-safe): sb_publishable_8qa-nssfdtEkCz-42wOSWQ_2P7S4Zj7
- Service (server-only): REDACTED_USE_N8N_CREDENTIALS

### Tables
| Table | Purpose |
|-------|---------|
| businesses | Lead/prospect CRM |
| outreach_log | Email history (business_id, email_num, subject, body, sent_at, status) |
| reddit_leads | Reddit posts scored by GPT |
| projects | Client projects -- logged by WF28 (onboarding) |
| invoices | Invoice tracking -- logged by WF27 (invoice generator) |
| proposals | Proposals/contracts -- logged by WF30 (proposal generator) |
| TBE_bids | TBE bid opportunities -- pipeline tracking |
| TBE_bid_items | TBE line items per bid (materials + labor) |
| TBE_pricing_defaults | TBE default rates (32 items, DFW market) |
| TBE_bid_activity | TBE status change audit log |
| TBE_saved_searches | TBE keyword/filter monitoring |

### Email Sequence Numbers
- 1-3: Cold outreach (WF19)
- 50-52: Nurture drip (WF23)
- 100+: Conversational replies (WF20)

## Darius Voice
- Normal capitalization, no apostrophes in contractions (dont, cant, Im, youre)
- No exclamation marks, semicolons, em dashes
- Short sentences, casual (gonna, kinda, prob, tbh)
- Never say AI phrases ("I noticed", "dive deeper", "leverage", "streamline", etc.)
- fixVoice() post-processor on all GPT output

## Phone/SMS
- Number: (855) 932-0493
- Calls → text redirect (voicemail.xml). No recording.
- Texts → AI reply + lead emailed to Gmail
- Cold outreach is EMAIL ONLY (SMS outreach is illegal under TCPA)

## Pricing
| Tier | Price |
|------|-------|
| Automation Audit | Free |
| Starter Automation | $500 -- $1,000 |
| Simple | $1,000 -- $2,500 |
| AI-Assisted | $2,500 -- $6,000 |
| End-to-End | $6,000 -- $15,000+ |
| Monitor Retainer | $99/month |
| Maintain Retainer | $149/month |
| Optimize Retainer | $499/month |

## Admin Pages
All password protected with `Kyomi123` (sessionStorage, once per session):
- stromation.com/admin-invoice.html -- send invoices (Stripe Pay Now link)
- stromation.com/admin-proposal.html -- send proposals/quotes
- stromation.com/admin-dashboard.html -- live CRM dashboard (uses Supabase anon key)
- stromation.com/admin-retainer.html -- set up Stripe subscription retainer billing

## Performance Optimizations Applied
- Showcase video: preload=none + loading=lazy (saves 3.5MB initial load)
- Cal.com iframes: loading=lazy
- CSS/font preload hints on index.html
- Reading time badges on all 18 blog posts
- Breadcrumbs + BreadcrumbList schema on all main pages + blog posts
- Internal cross-linking between blog posts (33 links)
- FAQ link in footer on all pages

## Don'ts
- **NEVER delete Supabase data without showing Darius every record first and getting explicit confirmation.** Real leads were lost because records were assumed to be test data. Always ask before ANY delete. Never use `id=not.is.null` without approval.
- Don't add frameworks or build tools
- Don't change pricing without explicit request
- Don't use Formspree -- all forms → n8n webhook
- Don't use SMS for cold outreach (illegal under TCPA)
- Don't use `fetch()` or `require()` in n8n Code nodes
- Don't use `message` param on emailSend v2.1 -- use `text` or `html`
- Don't put Supabase service key in frontend code (use anon key)
- Don't commit API keys to the public repo (GitHub push protection blocks it)
- Don't send emails from address mismatching SMTP credential
- Don't use `qualified`, `client`, or `audit_requested` as outreach_status
- Don't re-enable WF13 until Reddit karma is 50+
- Don't guess info@ emails in WF18 -- only save emails scraped from websites/mailto links
- Don't reference outreach@stromation.com -- it's deleted. Use chase@stromation.com for outreach
- Don't use `Buffer.from()` in n8n Code nodes -- use pure JS base64 helpers
- bids@stromation.com is NOT a valid SMTP alias -- gets 553 rejected. Always use darius@stromation.com with "admin" credential for sending
- leads@stromation.com alias status unconfirmed -- use darius@stromation.com to be safe
- Don't modify voicemail.xml without explicit request
- Don't mention Make or Zapier anywhere on the site — Stromation only uses n8n. Blog post zapier-vs-make-vs-custom-automations.html stays for SEO but all other references removed.
- Nav says "Industries" not "Workflows" — updated sitewide on 2026-03-31

## Pre-Launch Checklist
- [x] Fix all n8n workflows (Buffer.from, type safety, connections) -- done 2026-03-30
- [x] Website audit + fix logos, AI phrases, old emails -- done 2026-03-30
- [x] Enable RLS read access for anon role on businesses + outreach_log -- done 2026-03-31
- [x] Fix admin dashboard (outreach_log.sent_at not created_at) -- done 2026-03-31
- [x] Cold outreach pipeline live (9 businesses emailed) -- done 2026-03-31
- [x] Switch outreach from outreach@ to chase@stromation.com -- done 2026-03-31
- [x] Build missed call text-back template -- done 2026-03-31
- [x] Favicon transparent background -- done 2026-03-31
- [x] Finish Stripe onboarding (dashboard.stripe.com) -- done 2026-03-31
- [x] Run docs/supabase-schema.sql in Supabase SQL editor -- done 2026-03-31
- [x] Wire WF27/WF28/WF30 to log to invoices/projects/proposals tables -- done 2026-03-31
- [x] Set up Google Search Console + submit sitemap -- done 2026-03-31
- [ ] Set up Google Ads account + conversion tag
- [ ] Set up Facebook Business Manager + Pixel
- [ ] Get 3-5 client testimonials
- [ ] Build Reddit karma manually (currently -1)
- [ ] Post LinkedIn content (docs/linkedin-profile.md, docs/linkedin-posts.md)
- [ ] Start posting tweets (docs/twitter-content-30days.md)
- [x] Fix WF25 blog template reference -- done 2026-03-31 (now uses 5-signs post)
- [x] Wire WF27/WF28/WF30 Supabase logging -- done 2026-03-31
- [x] Add honeypot spam filter to all website forms -- done 2026-04-01
- [x] Switch outreach to chase@stromation.com -- done 2026-03-31
- [x] Add comparison table, real examples, guarantee to homepage -- done 2026-04-01
- [x] Add client logos + testimonials (The Brass Effect, ReadyMade Video) -- done 2026-04-01
- [x] Applied for n8n affiliate partner program -- done 2026-04-01
- [x] Cold call dashboard built (admin-coldcall.html) -- done 2026-04-01
- [x] Honeypot spam filter on all forms -- done 2026-04-01
- [x] WF20 IMAP fix (removed from error alerts, watchdog approach) -- done 2026-04-01
- [x] WF29 Error Alert deleted (too noisy from IMAP drops) -- done 2026-04-01
- [x] WF19 cold email prompt rewritten (intro, relevance, proof, CTA) -- done 2026-04-01
- [x] WF18 corporate filter + junk email blocklist expanded -- done 2026-04-01
- [x] WF20 bounce detection added (auto-marks bounced in Supabase) -- done 2026-04-01
- [x] Client logos + testimonials on homepage (Brass Effect, ReadyMade Video) -- done 2026-04-01
- [ ] The Brass Effect Division 27 Auto-Bidder -- IN PROGRESS
  - [x] Supabase schema (TBE_ prefix, 5 tables, 32 pricing defaults) -- done 2026-04-01
  - [x] Auto Bidder Engine workflow (n8n ID: uTiy5gtBbhoL2wjo) -- done 2026-04-01
  - [x] Bid Tracker Dashboard (admin-bids.html) -- done 2026-04-01
  - [x] 5% Stromation commission auto-tracked -- done 2026-04-01
  - [x] Logo, veteran-owned, exclusions, warranty, standards in quote -- done 2026-04-01
  - [x] Quote Sender workflow (n8n ID: 3IjbS6wWZIxQSj9a, sends to antonio@tbeit.com) -- done 2026-04-01
  - [x] SAM.gov Bid Finder (n8n ID: Xi7gyvl3tzMqaknK, daily 6AM CT, DEMO_KEY) -- done 2026-04-01
  - [x] Deadline Reminders (n8n ID: VYQEc5i1Ae2usxN3, daily 8AM CT) -- done 2026-04-01
  - [x] Weekly Analytics (n8n ID: BittpG8u35xMAuUr, Monday 8AM CT) -- done 2026-04-01
  - [x] ConstructConnect saved search setup (Division 27 DFW, 3 counties, 129 projects) -- done 2026-04-01
  - [x] All SMTP credentials swapped to "admin" (old leads@ deleted) -- done 2026-04-01
  - [x] Blank email fix (skip returns empty array, email node doesn't fire) -- done 2026-04-01
  - [x] Quote sends to Antonio (antonio@tbeit.com) not GC. Darius reviews first. -- done 2026-04-01
  - [ ] ConstructConnect email parser (needs Antonio's paid CC alerts to bids@stromation.com)
  - [x] Blueprint/spec PDF upload + Claude Sonnet 4.6 vision (n8n ID: MCioEt93wGOlbd7d) -- done 2026-04-02
  - [x] Auto-bidder v2: component expansion with real vendor part numbers (Panduit, i-Pro, Bosch, HID) -- done 2026-04-02
  - [x] Quote Sender sends PDF attachment via html2pdf.app API -- done 2026-04-02
  - [x] Deadline Reminders fixed (was every minute, now daily 8AM, skips expired) -- done 2026-04-02
  - [x] Dashboard "New Bid from Blueprint" upload UI -- done 2026-04-02
  - [x] Bid Alert Parser (n8n ID: 6OXGUtj6mQlWSsEQ, checks bids@ every 30 min) -- done 2026-04-02
  - [x] PlanHub File Downloader v3: pure API, disk download, smart Div 27 filter, no Puppeteer -- done 2026-04-02
  - [x] PlanHub API reverse-engineered (get-details, get-files, download-all-files) -- done 2026-04-02
  - [x] Full pipeline wired: Parser → File Downloader → Blueprint Analyzer → Auto Bidder -- done 2026-04-02
  - [x] Blueprint Analyzer: retry logic (5x, 60-300s backoff), accepts binary + JSON pdf_base64 -- done 2026-04-02
  - [x] bid_id pass-through chain (PATCH existing bids, not INSERT duplicates) -- done 2026-04-02
  - [x] estimate_method field + dashboard badge (GPT Estimate vs Blueprint Scanned) -- done 2026-04-02
  - [x] Bid Alert Parser: Div 27/28 scope filter, passes bid_id downstream -- done 2026-04-02
  - [x] Smart file filter: E/T sheet priority, skip civil/structural/arch, max 3 PDFs -- done 2026-04-02
  - [x] Supabase cleanup: 13 junk entries removed, city parsing fixed -- done 2026-04-02
  - [x] NODE_FUNCTION_ALLOW_BUILTIN=* added to Docker env -- done 2026-04-02
  - [x] Full audit + fix: 5 workflows, 27 issues found, all critical/high fixed -- done 2026-04-03
  - [x] Quote Sender: PDF encoding fix (responseType), dynamic webhook response, em-dash fix -- done 2026-04-03
  - [x] File Downloader: hyphenated sheet regex, S-prefix fix, addendum/elevator/lighting handling -- done 2026-04-03
  - [x] Auto Bidder: camera cable (violet), fire alarm + AV + rack parts/expansion/narrative, GPT prompt expanded, training labor, firestop fix -- done 2026-04-03
  - [x] Blueprint Analyzer v3: two-pass index approach (reads drawing index → identifies Div 27 sheets → scans those), temperature 0.0, size validation, int coercion, try/catch bidder call -- done 2026-04-03
  - [x] Bid Alert Parser: security keyword fix, intend-to-bid gated, project ID regex widened, missing keywords added -- done 2026-04-03
  - [x] File Downloader v4: persistent cache (/tmp/planhub_cache/), skip re-download, connection retry, PyPDF2 page splitting for large PDFs -- done 2026-04-03
  - [x] Switched Blueprint Analyzer to Claude Sonnet 4.6 (Tier 2: 450K tokens/min, 1K req/min) -- done 2026-04-03
  - [x] Dashboard: 4 estimate badges (GPT Estimate, Analyzed with Claude, Analyzed with Gemini, Analyzed with GPT) -- done 2026-04-03
  - [x] First successful blueprint analysis: Faith Refuge $12,591 (3 access doors from plans) -- done 2026-04-03
  - [x] City of Melissa East WTP quote: $20,945 from local blueprints, Claude-analyzed (4 access doors, 1 rack, 1 fiber) -- done 2026-04-03
  - [x] Quote Sender fromEmail fixed: bids@ rejected (553), switched to darius@stromation.com -- done 2026-04-03
  - [x] Blueprint Analyzer prompt v2: reads legends, estimates from context, excludes fire alarm/SCADA per Antonio -- done 2026-04-03
  - [x] Auto-bidder: project_name protection on PATCH (won't overwrite existing names) -- done 2026-04-03
  - [x] Auto-bidder GPT prompt excludes fire alarm -- done 2026-04-03
  - [x] 4 Claude-analyzed quotes generated: Kleberg $81K, Seagoville $117K, Faith Refuge $54K, Melissa $29K -- done 2026-04-03
  - [x] PyPDF2 installed on n8n Docker for large PDF page splitting -- done 2026-04-03
  - [x] Multi-PDF aggregation: counts combined across all PDFs per bid, ONE auto-bidder call -- done 2026-04-03
  - [x] skip_autobid flag: Blueprint Analyzer returns analysis only when called from File Downloader -- done 2026-04-03
  - [x] Skip already-analyzed bids: Prepare Input checks estimate_method before re-scanning (force_rescan=true to override) -- done 2026-04-03
  - [x] Gemini (free) for index sheet identification, Claude only for device counting -- done 2026-04-03
  - [x] Analysis cache: Claude results cached per PDF file, no duplicate API calls -- done 2026-04-03
  - [x] Skip negative-scoring sheets: only send positive/neutral sheets to Claude -- done 2026-04-03
  - [x] Large PDF splitting: PyPDF2 splits >25MB PDFs into individual pages after ZIP extraction AND from cache -- done 2026-04-03
  - [x] File Downloader auto-syncs PlanHub project details to Supabase (deadline, GC, location, sq ft) -- done 2026-04-03
  - [x] Merged PlanHub project ID handling -- done 2026-04-03
  - [x] 7 Claude-analyzed quotes: Kleberg $81K, Seagoville $117K, Faith Refuge $54K, Melissa $29K, Back Nine $89K, FASST $35K, PT Solutions $8K -- done 2026-04-03
  - [x] Antonio scope confirmed: NO fire alarm, NO SCADA. Only cabling, cameras, access control, AV, network, intrusion -- done 2026-04-03
  - [x] Frisco Medical test bid deleted -- done 2026-04-03
  - [ ] PlanHub auth token refresh (may expire, re-capture from browser DevTools Network tab)
  - [ ] PlanHub official API access (applied, waiting for response)
  - [ ] ConstructConnect email parser (needs Antonio's paid CC alerts to bids@stromation.com)
  - [ ] Antonio to verify pricing defaults match his actual vendor rates
  - [ ] Get Antonio's TX license number for quote template
  - [ ] SAM.gov production API key (DEMO_KEY works but rate limited)
  - [ ] Dashboard inline editing of line item quantities/prices
  - [ ] Anthropic Batch API for non-urgent bids (50% discount)
  - [x] Hertz DFW: 80MB PDF split locally, Claude found 45 drops/6 WAPs/8 cameras/4 AC doors → $103K quote -- done 2026-04-03
  - [x] Bowie HS: confirmed no Division 27 scope (flooring/lighting renovation only), marked no_bid -- done 2026-04-03
  - [x] Blueprint Analyzer: removed auto-bidder call entirely, only returns analysis. Caller handles bid. -- done 2026-04-03
  - [x] PlanHub download pagination: auto-fetches page 1+ when >95 files found -- done 2026-04-03
  - [x] force_rescan flag: clears file cache + analysis cache for re-download -- done 2026-04-03
  - [x] Parts database updated from UTSW Frisco proposal: grounding $6K, labeling $600, Avigilon/HID Signo, wall mount rack, floor faceplates -- done 2026-04-04
  - [x] All 8 Claude quotes re-generated with updated parts -- done 2026-04-04
  - [x] BidEngine landing page created at github.com/dariusstrongman/BidEngine -- done 2026-04-04
  - [x] BidEngine case study added to stromation.com case-studies page -- done 2026-04-04
  - [x] Antonio confirmed: no license number needed on quotes -- done 2026-04-04
  - [ ] Remaining GPT bids: AISD JR High (server issues), Tarzan Jane (no Div 27 content in available files)
  - [ ] Large PDF page selection: prioritize 1-8MB pages (floor plans) over tiny (notes) or huge (combined)
  - [x] Spec scanning via Gemini (free): reads spec TOC, extracts vendor requirements -- done 2026-04-04
  - [x] Vendor auto-selection: CommScope vs Panduit, Avigilon vs COSEC based on spec -- done 2026-04-04
  - [x] CommScope parts profile added (from UTSW Frisco proposal) -- done 2026-04-04
  - [x] Schedule + symbol counting priority in Claude prompt -- done 2026-04-04
  - [x] Verification pass for low/medium confidence results -- done 2026-04-04
  - [x] BidEngine subdomain live at bidengine.stromation.com (GitHub Pages, HTTP 200) -- done 2026-04-05
  - [x] BidEngine Chatbot webhookId fix + fixVoice post-processor (was 404, now live) -- done 2026-04-05
  - [x] WF22 honeypot early return fixed (returns [] for bots, no more blank spam emails) -- done 2026-04-05
  - [x] BidEngine waitlist form error handling (loading/error states) -- done 2026-04-05
  - [x] WF2 File Downloader v6: full pipeline rewrite for large bundled PDFs -- done 2026-04-07
    - pymupdf (fitz) replaces PyPDF2 as primary splitter (handles corrupt PDFs that crash PyPDF2)
    - Local index parsing: find_all_index_pages() + parse_index_locally() extracts Div 27 sheet IDs from drawing index via regex (no Gemini needed)
    - Content-based page matching: matches sheet IDs in page HEADERS (first 200 chars) to avoid matching index pages
    - Text pre-filter with scope keywords for fallback when index approach fails
    - Single execution path: fixed double-run (Merge & Filter triggered twice from two inputs → chained sequentially)
    - Stale extracted dir cleanup, existence checks on all file operations, per-page try/except on corrupt pages
    - WF4 project mismatch protection: blocks PATCH if facility names don't match (filters generic construction words)
    - WF4 audit trail: logs old state to tbe_bid_activity before overwrite
    - Kleberg test: 4014 pages split, 19 Div 27 sheet IDs extracted, 9 sheets analyzed → 135 drops, 14 WAPs, 22 displays, 7 racks → $194K bid
    - Aggregation fixed: SUM across pages (was MAX — undercounted by 50%+)
    - One-pass page scanner: reads ALL 4014 pages once, matches by sheet ID count (1-2 matches = drawing, 5+ = index page)
    - Dashboard auto-refresh: 60s normal, 15s during analysis. "Analysis in Progress" badge shows in real-time
    - Infrastructure: EXECUTIONS_TIMEOUT=1800, nginx proxy_read_timeout=1800, PyPDF2+pymupdf in Dockerfile
  - [x] "Analyzing" pipeline status — WF2 sets status to analyzing at start, dashboard shows pulsing badge + disables Send -- done 2026-04-07
  - [x] Pipeline v7 rewrite: clean two-pass architecture, persistent script at /home/node/.n8n/planhub_pipeline.py -- done 2026-04-08
    - Pass 1: page-by-page scope detection (free, keyword match + index parsing)
    - Pass 2: Claude analysis only on confirmed scope pages (paid, targeted)
    - NEEDS_VISION support for scanned/image pages (Gemini free check)
    - Sheet-ID prioritization in Claude queue (priority over generic keyword matches)
    - Supabase table name fixed (tbe_bids lowercase)
    - Kleberg: 1000 pages scanned, 214 SCOPE, 28 INDEX, 19 sheet IDs extracted
  - [x] Pipeline v8 fixes (2026-04-08):
    - MAX_PAGES: 1000 → 10000 (no page left unscanned)
    - MAX_CLAUDE_PAGES: 15 → 999, MAX_VISION_PAGES: 5 → 50 (no caps on analysis)
    - Sheet ID matching: full 2000 chars (was 300, missed title blocks at bottom)
    - text_preview: 500 → 2000 chars for better sheet ID cross-referencing
    - Split ALL multi-page PDFs (was only >25MB, missed small bundled permit sets)
    - Split cached PDFs too (was skipping split on cache hits)
    - fire alarm moved from NEGATIVE to POSITIVE keywords (was blocking Div 28 scope)
    - Added keywords: fire pull, pull station, horn strobe, visual alarm, smoke detector, data, telephone, nurse call
    - Removed "lighting" from NEGATIVE (overlaps with low voltage)
    - Gemini prompt: removed "Do NOT include fire alarm", added symbol-based detection
    - Gemini fallback: checks ALL NO_SCOPE pages when Pass 2 returns 0 device counts
    - Status reset: always sets quote_ready at end of pipeline (was stuck on analyzing)
    - Disk cleanup: deletes split dir, extracted dir, downloads, and cache after completion
    - updated_at: Auto Bidder now sets timestamp on every bid update
    - Dashboard: analyzing cards have purple glow border, analysis date on badges
    - Dashboard: sort dropdown (bid due date, value, name, newest)
    - Bid Alert Parser: blocks "status update", "new projects bidding" emails
    - Concurrent scans: multiple bids can run simultaneously
    - Back Nine: $90K (12 scope pages analyzed), Hertz: $115K (consistent across rescans)
  - [x] Pipeline v9 reliability fixes (2026-04-09):
    - Global 25-minute deadline: checked before every Claude/Gemini API call, raises DeadlineExceeded
    - MAX_CLAUDE_PAGES: 999 → 50, MAX_VISION_PAGES: 50 → 20 (practical caps)
    - Circuit breaker: 5 consecutive Claude failures = abort Pass 2
    - Title block fix: extract_text_from_page returns first 2000 + last 500 chars (was first 2000 only, missed sheet IDs in bottom title blocks)
    - try/finally in main(): ALWAYS resets bid status to quote_ready on ANY exit (crash, deadline, error)
    - bid_id loaded early (before run_pipeline) so finally block can always reset status
    - 30-minute timeout added to n8n executeCommand node (was unlimited)
    - Removed stray vision_checked increment after Gemini loop
    - Pipeline version tracked in output JSON (pipeline_version, elapsed_seconds fields)
    - Fixed: execution 7771 stuck 12+ hours, Kleberg stuck in "analyzing" since Apr 7
  - [x] Pipeline v10 accuracy fix — schedule-first dedup architecture (2026-04-09):
    - Enhanced page classification: SCHEDULE, FLOOR_PLAN, DETAIL, RISER, LEGEND, DEMOLITION (was just SCOPE)
    - Schedule-first analysis: schedules processed before floor plans, schedule counts = authoritative
    - Smart aggregation replaces blind SUM: schedule MAX, floor plan dedup (T vs ES series), SUM only across floors
    - WF3 Blueprint Analyzer v4: new extract_schedule mode for reading device schedule tables
    - WF3 count_devices prompt updated: anti-dedup fields (is_detail_view, is_demolition, floor_identifier, sheet_series)
    - WF4 Auto Bidder: review_mode flag, pending_review status, saves device_analysis + page_classification to Supabase
    - WF4 accepts reviewed_counts from dashboard for post-review quote generation
    - Dashboard: "Pending Review" tab, editable device counts with source/confidence badges, page classification summary
    - Dashboard: "Generate Quote with These Counts" button for human-reviewed quotes
    - Supabase: device_analysis JSONB, page_classification JSONB columns added to tbe_bids
    - Supabase: pending_review added to status constraint
    - Flow: pipeline → pending_review → Darius reviews counts → Generate Quote → quote_ready → Send to Antonio
    - Skips detail views, riser diagrams, legends, demolition plans (prevents overcounting)
    - T-series + ES-series overlap: security devices use MAX(T,ES) not SUM per floor
    - MAX_CLAUDE_PAGES raised to 100, MAX_VISION_PAGES to 30
    - WF2/WF3/WF4 all published 2026-04-09
    - Kleberg rescan triggered (force_rescan=true, execution 8125) but hit Anthropic API credit limit mid-run
      - Pass 1 (free text classification) likely completed — classified 4000+ pages
      - Pass 2 (Claude vision calls via WF3) exhausted credits before finishing
      - try/finally block reset status from analyzing → quote_ready
      - device_analysis and page_classification remain null (v10 aggregation never completed)
      - Old $194K quote unchanged — WF4 was never called with new counts
  - [x] Pipeline v11 cost fixes (2026-04-09):
    - File dedup by hash before splitting (Project Manual = Specs = same file, saved 1756 duplicate pages)
    - Div 27 schedule filter: only data/security/fire alarm schedules sent to Claude (was ALL schedules)
    - Text density filter: pages >800 chars = spec text → NO_SCOPE (not FLOOR_PLAN)
    - Floor plan Div 27 filter: only keyword-matched floor plans go to Claude
    - MAX_SCHEDULE_PAGES = 20 cap added
    - Kleberg cost reduction: 1066 Claude calls → ~50 estimated ($27 → ~$1.25)
  - [x] Pipeline v12 Phase 1 batch classification (2026-04-09):
    - Replaces keyword matching with Claude Sonnet text-only batch calls
    - 50 page text previews per API call (~$0.01/batch)
    - Claude classifies: DRAWING (send to vision), SCHEDULE, INDEX, or SKIP
    - Hill Elementary: 104 vision calls → estimated ~15 vision calls (85% reduction)
    - Anthropic API key added to pipeline script for direct Claude calls
    - Code pushed and published, needs testing on stable n8n instance
  - [ ] Infrastructure blockers:
    - n8n task runner 60s timeout kills WF3 Claude calls (need N8N_RUNNERS_TASK_TIMEOUT=300)
    - Zombie executions after Docker restart (must Stop All + republish WF2)
    - 480MB ZIP downloads take 10-15 min on EC2
    - Anthropic credits at $0 (need refill at console.anthropic.com)
  - [x] Phase 2 agent pipeline ATTEMPTED, ABANDONED (2026-04-09):
    - Built Claude agent with 4 tools: list_pages, read_page_text, analyze_page_vision, submit_counts
    - Tested on Hill Elementary (project 543586) — 4 runs total
    - Agent DID work: classified pages, read schedules, made intelligent vision calls
    - Bug discovered: agent sent flat device counts but WF4 expects nested systems format
    - Fixed the bug, verified with direct WF4 test (pending_review + device_analysis saved correctly)
    - FATAL PROBLEM: each conversation turn sends GROWING message history
      - Turn 1: ~1K input tokens
      - Turn 15: 50K+ input tokens (all prior tool results accumulate in context)
      - Hill Elementary cost: ~$5 per run (estimated $0.50, actual was 10x)
    - Abandoned in favor of v12 fixed pipeline (see below)
  - [x] Pipeline v12 (REBUILT, REPLACES AGENT) (2026-04-10):
    - Fixed pipeline with batch classification, NOT agent-based
    - dedup_files_by_hash before splitting (saves duplicate Project Manual/Specs)
    - Text density filter: pages >800 chars + >50% alphabetic = NO_SCOPE (spec text)
    - batch_classify_pages: Claude text-only, 50 pages per API call (~$0.01/batch)
    - Classification: DRAWING / SCHEDULE / INDEX / SKIP
    - Only DRAWING pages get vision analysis
    - MAX_SCHEDULE_PAGES = 20 cap
    - submit_to_autobidder sends nested systems format (fixes the agent bug at pipeline level)
    - Still has v10 smart aggregation (schedule-first, T/ES dedup, device_analysis)
    - WF2 pushed (draft) 2026-04-10 — needs publish to go live
  - [x] Cost comparison (per Hill Elementary-sized project ~300 pages):
    - **Original v1-v9 (blind SUM, 999 Claude calls)**: ~$27+ per project
    - **v10 (50-100 Claude calls, smart aggregation)**: ~$1.50-3 per project
    - **Agent pipeline (abandoned)**: ~$5 per project (growing context)
    - **v12 fixed pipeline (current)**: ~$0.30-0.50 per project
      - Batch classify: ~$0.01-0.05 (6 batches x $0.01)
      - Vision calls: ~10-15 pages x $0.03-0.05 = $0.30-0.75
      - Total predictable, no runaway cost from growing context
  - [ ] Workflow backups saved to ~/Desktop/tbe-workflow-backups-2026-04-09/
      - Lesson: always check Anthropic credit balance before triggering large rescans
  - [x] Pipeline v13 (2026-04-10) - WORKING END-TO-END, A/B TESTED:
    - **v12 bug**: shipped with MAX_CLAUDE_PAGES=999 (old v10 values), caused ~$10/bid
    - **Cost guard**: MAX_CLAUDE_PAGES=50, MAX_VISION_PAGES=20, MAX_COST_USD=$3
    - **Running cost tracking**: logs $X.XX per call, hard stops at $3 mid-run
    - **Pre-flight estimate**: trims page queue if projected cost > $3
    - **Fixed stray `vision_checked += 1`** bug outside Gemini loop
    - **Text density filter fix**: was over-filtering drawings as spec text
      - Was: runs before keyword check, 800 chars, 50% alpha, killed 27/28 Jimmy Johns pages
      - Now: runs AFTER keyword/prefix check, 2000 chars, 60% alpha, only if NO Div 27 signals
    - **extract_counts_from_result rewrite**: handles nested Claude format
      - WF3 returns `{systems: {structured_cabling: {cat6a_drops: 64}}}`
      - Old code did `int(dict)` → silently failed, returned {}
      - New code walks nested dicts, extracts both flat and `{total: N}` shapes
      - Skips `is_detail_view: true` and `is_demolition: true` pages
      - Added all WF3 field names: cat6a_drops, fixed_cameras, access_control_doors, etc.
    - **submit_to_autobidder fixes**:
      - estimate_method: "Analyzed with Claude" → "blueprint_claude" (valid enum)
      - Removed `source: "pipeline_v13"` (not in tbe_bids_source_check constraint)
      - Moved to `pipeline_version` field instead
      - WF4 defaults source to 'manual' which is valid
    - **Jimmy John's A/B test results (project 543380, 1 PDF, 28 pages):**
      - Before: text density killed all pages → $0, no analysis
      - After: 20 pages analyzed, $1.00 actual cost
      - Device counts: 56 cat6a_drops, 6 cameras, 7 racks, 10 speakers, 2 WAPs, 2 intercoms, 2 displays, 1 access door
      - Old quote: $62,498 (GPT estimate)
      - New quote: **$39,819 (blueprint_claude)** - more realistic for single QSR
      - Quote number: TBE-2026-0410-0K2Z
    - Pipeline pushed and tested live via API (no UI publish needed once webhook is active)
  - [ ] Anthropic Batch API for non-urgent bids (50% discount)
  - [ ] Re-run Kleberg with v10 once credits refill to verify dedup accuracy
  - [x] Pipeline v14 (2026-04-13) - PHASED PIPELINE + GEMINI CRITIC + AUTOPILOT:
    - **WF4 Auto Bidder fully rewritten:** GPT-estimate path removed (was 84 lines, ~3.5KB saved). OPENAI_KEY constant deleted. Bids without `body.systems` now mark `status=awaiting_blueprints` + set `download` phase to `failed` instead of erroring out.
    - **Gemini critic added:** Gemini 2.5-flash-lite (free tier) reviews Claude's device counts after quote built. Returns `{verdict, confidence, issues, suggestions}`. Verdict drives autopilot routing.
    - **Autopilot logic:** if Gemini=`looks_right` AND heuristic sanity passes → auto-POST to WF5 Quote Sender → status=`quote_sent`. Else → park in `pending_review` with banner. If WF5 fails → `quote_ready` with error in notes.
    - **Heuristic sanity check stays:** floor/ceiling ($500/$2.5M BLOCK), drops/racks ratio, cameras vs drops, drop density, labor %. Layered with Gemini.
    - **Phased pipeline tracking:** new `pipeline_phases` JSONB column on tbe_bids tracks 7 phases (download, classify, claude_counts, gemini_verify, quote_built, pending_review, sent). Each phase has `{status, updated_at, detail}`. WF4 writes all of these on completion.
    - **Dashboard stepper:** horizontal 7-dot progress bar on each bid card (compact) + detailed stepper in modal with phase detail text + Verify block showing Gemini verdict/confidence/issues. Colors: green=complete, yellow=in_progress (pulsing), red=failed, gray=not_started.
    - **Re-scan Blueprints button:** added to dashboard for `pending_review`/`quote_ready` bids. Auto-extracts PlanHub project ID from `source_url` or prompts. POSTs to WF2 with `force_rescan: true`. Sets status=`analyzing` immediately so glow appears.
    - **WF5 Quote Sender:** flipped toEmail to antonio@tbeit.com via API for autopilot test, then reverted back to dariusstroman@gmail.com (still in test mode). CC=darius@stromation.com always. Added autopilot warnings block to email body — Gemini flags render inline before sending.
    - **Schema migrations applied to prod (3 SQL files):**
      - `docs/tbe-schema-sync-v13.sql`: pipeline_version column, status constraint expanded with analyzing + pending_review
      - `docs/tbe-schema-phases.sql`: pipeline_phases JSONB column + backfill for existing 30+ bids
      - `docs/tbe-schema-awaiting.sql`: status constraint expanded with awaiting_blueprints
    - **Status constraint final:** `new, awaiting_blueprints, analyzing, pending_review, reviewing, estimating, quote_ready, quote_sent, submitted, won, lost, no_bid, expired`
    - **Dashboard status badges:** `Ready for Analysis` (dashed cyan) for awaiting_blueprints. Status dropdown in modal expanded to all 13 values (was 10). Expired bids visually muted.
    - **Cleanup:** 7 past-deadline bids manually marked `expired` via API PATCH (JV Entry Door, South Euless Park, Seagoville Prek-8th, DISD West Dallas JR High, DISD Resource Center STEM, Org 372, ORG 318). All have activity log entries.
    - **Gemini API key in WF4:** `AIzaSyC-yTfvwZlrWluomtWe9JPK39-TSO7dPVg` (only `gemini-2.5-flash-lite` accessible on this key's free tier; 2.0-flash and 2.5-pro return quota errors).
    - **Self-test confirmed working:** Jimmy John's counts (56 drops, 6 cameras, 7 racks) → Gemini verdict `clearly_wrong` 95% confidence, flagged "7 MDF rooms for a Jimmy John's is extremely high" + suggested {rack_mdf_rooms: 1, cat6a_drops: 20, fixed_cameras: 4}. Would correctly park in pending_review.
  - [ ] Anthropic Batch API for non-urgent bids (50% discount)
  - [ ] Re-run Kleberg with v10 once credits refill to verify dedup accuracy
  - [ ] Multi-tenant auth for BidEngine SaaS (Supabase auth, per-customer dashboards)
  - [ ] NOTE: Always use Gemini (free) for testing pipeline changes before Claude
  - [ ] NOTE: n8n API PUT only updates draft — must publish from UI for production webhooks. Workaround: deactivate/reactivate via API forces reload of latest version.
  - [ ] NOTE: n8n API key at /home/darius/Documents/mcp/n8n_api_key.txt expires periodically — regen at n8n.myaibuffet.com → Settings → n8n API → Create API Key
  - [ ] NOTE: WF5 toEmail is in test mode (dariusstroman@gmail.com). To go fully zero-touch: flip to antonio@tbeit.com. Currently autopilot quotes land in Darius's Gmail with CC, then Darius forwards to Antonio.
