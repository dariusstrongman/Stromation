# Stromation

## Project Overview
- **stromation.com** -- Workflow Replacement Studio owned by Darius Stroman
- Static HTML/CSS/JS site hosted on GitHub Pages (public repo)
- Repo: github.com/dariusstrongman/Stromation
- Domain: www.stromation.com (CNAME)
- Twitter/X: @stromationhq
- Business email: darius@stromation.com (SMTP credential: "admin")
- Contact email: contact@stromation.com (used sitewide)
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
- Cal.com booking: https://cal.com/darius-stroman-byeng8/30min (embedded on audit.html and thank-you.html)
- Anthropic API (Claude Sonnet 4.6) for blueprint PDF analysis
- html2pdf.app API for quote PDF generation
- PlanHub REST API (api.planhub.com/api/v1/) for project details, file lists, downloads (auth token captured from browser)

## Site Structure

### Root Pages (31 pages)
| File | Purpose |
|------|---------|
| index.html | Homepage -- hero, showcase video (lazy loaded), services, how-it-works, stats, testimonial |
| services.html | 5 service categories + 4 pricing tiers + retainers (FAQ schema) |
| industries.html | Industries hub -- 8 cards linking to dedicated landing pages |
| case-studies.html | Client case studies with results |
| about.html | About Darius, company story |
| contact.html | Contact form (n8n webhook) |
| audit.html | Free audit form (FAQ schema) + Cal.com booking embed |
| blog.html | Blog index with card grid |
| faq.html | Standalone FAQ page (accordion UI, FAQPage schema) |
| checklist.html | Lead magnet -- automation readiness checklist with email capture |
| roi-calculator.html | Interactive ROI calculator with live math + email capture |
| thank-you.html | Post-form confirmation + Cal.com booking (noindex) |
| dental.html | Ad landing page for dental practices |
| home-services.html | Ad landing page for home service businesses |
| agencies.html | Ad landing page for marketing agencies |
| real-estate.html | Ad landing page for real estate |
| accounting.html | Ad landing page for accounting firms |
| legal.html | Ad landing page for law firms |
| fitness.html | Ad landing page for gyms/fitness |
| restaurants.html | Ad landing page for restaurants |
| admin-invoice.html | Admin: send invoices (password protected: Kyomi123, noindex) |
| admin-proposal.html | Admin: send proposals (password protected: Kyomi123, noindex) |
| admin-dashboard.html | Admin: live CRM dashboard from Supabase (password protected: Kyomi123, noindex) |
| admin-retainer.html | Admin: set up Stripe subscription retainer billing (password protected: Kyomi123, noindex) |
| admin-bids.html | Admin: TBE bid tracker dashboard (password protected: Kyomi123, noindex) |
| admin-coldcall.html | Admin: cold call script dashboard (password protected: Kyomi123, noindex) |
| project-status.html | Client project status page (noindex, UUID-based auth) |
| privacy.html | Privacy policy |
| terms.html | Terms of service |
| 404.html | Custom 404 error page |

### Blog Posts (blog/) -- 46 posts
Auto-generated weekly by WF25 (Sunday 6AM CT). All posts have reading time badges, breadcrumbs, internal cross-links, and 3 related posts.

### Other Key Files
| File | Purpose |
|------|---------|
| styles.css | Single global stylesheet |
| script.js | Main JS -- mobile menu, scroll animations, parallax, forms, FAQ accordion |
| chat.js | Chat widget connecting to n8n webhook (deferred on all pages) |
| feed.xml | RSS feed (46 items) |
| sitemap.xml | XML sitemap (46 blog entries) |
| robots.txt | Robots directives |
| voicemail.xml | TwiML -- redirects callers to text (Google Neural2-J voice) |
| CNAME | GitHub Pages custom domain |

### docs/ (internal business documents)
| File | Purpose |
|------|---------|
| sales-playbook.md | Discovery questions, objection handlers, closing scripts |
| service-agreement.md | SOW/contract template for client projects |
| brasseffect-schema.sql | TBE Supabase schema (5 tables, 32+ pricing defaults) |
| linkedin-profile.md | Optimized LinkedIn profile copy |
| linkedin-posts.md | 4 weekly LinkedIn posts |
| twitter-content-30days.md | 30 days of tweets for @stromationhq |
| supabase-schema.sql | SQL for projects/invoices/proposals tables |

### workflow-templates/
| File | Purpose |
|------|---------|
| missed-call-textback.json | Missed Call Text-Back system (Twilio) |
| missed-call-setup-guide.md | Deployment guide |
| README.md | Template index |

## n8n Workflows (n8n.stromation.com)

### TBE (The Brass Effect) Workflows -- Active
| n8n ID | Name | Trigger | Description |
|--------|------|---------|-------------|
| 6OXGUtj6mQlWSsEQ | WF1 - Bid Alert Parser | **OFF** | Checks bids@ for PlanHub emails, extracts project data, triggers pipeline |
| CJlS0xgvY4oHtQsy | WF2 - File Downloader | Webhook | PlanHub API download + pipeline v17.4 (scope_brief grounding, Gemini batch classify, Claude vision) |
| MCioEt93wGOlbd7d | WF3 - Blueprint Analyzer | Webhook | Claude Sonnet 4.6 vision -- extract_legend, extract_schedule, count_devices modes |
| uTiy5gtBbhoL2wjo | WF4 - Auto Bidder Engine | Webhook | Pricing engine with Wavenet/Panduit vendor profiles, autopilot chain (heuristic → Gemini → send) |
| 3IjbS6wWZIxQSj9a | WF5 - Quote Sender | Webhook | PDF via html2pdf.app, emails to Darius (test mode). CC darius@stromation.com |
| ZcSsnPOZGN4IxXiM | WF6 - Gemini Verifier | Webhook | Gemini 2.5-flash-lite critic, size-aware rules, returns verdict/confidence/issues |
| 09NUezjKeX1RFjDK | WF7 - Claude Arbitrator | Webhook | Auto-rejects Gemini suggestions for out-of-scope categories |
| RfasyaaxB9IHDzVo | WF8 - Spec Extractor | Webhook | Reads spec pages for vendor requirements |
| 0W9zvozyYwNhuwwS | WF9 - Drawing Audit | Webhook | Manual PDF upload path with keyed_notes_inventory |
| Xi7gyvl3tzMqaknK | SAM.gov Bid Finder | Daily 6AM CT | Division 27 opportunities from SAM.gov |
| VYQEc5i1Ae2usxN3 | Deadline Reminders | Daily 8AM CT | Upcoming deadline summary email |
| P8pO5V6vewkRAPFa | Auto-Expire | Daily 1AM CT | Marks past-deadline bids as expired |
| DUk2xWWZNeLoirfU | Gap Reconcile | Hourly :15 | 11 gap rules + auto-junk zombies + auto-rescan + auto-promote via Gemini |
| JHAP2Qj7zrPyAiUK | Disk Cleanup | Daily 3:30AM CT | Purges /tmp caches, leaked work dirs, old n8n executions |
| H788XzpQwRzXHy96 | BidEngine Chatbot | Webhook | Chat widget on bidengine.stromation.com |

### Stromation Workflows -- Active
| n8n ID | Name | Trigger | Description |
|--------|------|---------|-------------|
| SFbGasyyu7kfcaYn | 11 - SMS Handler | Webhook | AI text replies + emails leads to Gmail |
| hAGWEpTGAA8kktw2 | 12 - Website Chatbot | Webhook | GPT as Darius, fixVoice post-processing |
| KO405axX2qcNthyz | 14 - Reddit Comment Bot | 2x daily | Comments on relevant automation posts |
| sG4yXO59P9LWnhI6 | 21 - Reddit Lead Digest | Daily 6PM CT | Scans Reddit for high-intent posts |
| moCdSoa37fI4ufR8 | 22 - Website Form Handler | Webhook | Forms → Supabase businesses table + email to Gmail |
| IOcuiuEuSkK8nljj | 25 - Auto Blog Publisher | Sunday 6AM CT | GPT → blog post → GitHub commit → updates blog.html + sitemap + RSS |
| IoqOSKMxtFHDVY3i | 26 - Review Request | Webhook | Review request email |
| h9EG9Q3KRc1gpvqK | 27 - Invoice Generator | Webhook | Invoice + Stripe Pay Now link |
| eqV9tBqHVKRF1eED | 28 - Client Onboarding | Webhook | Welcome email + intake link |
| pFhjuOD8LxbbxLpw | 30 - Proposal Generator | Webhook | Branded proposal email |
| qkG5JXc3N12zFol1 | 31 - Client Weekly Update | Friday 4PM CT | Active project status emails |
| LqK02yBF41kLbqBg | 32 - Post-Delivery Sequence | Daily 11AM CT | Day 1 review, Day 7 referral, Day 30 case study |
| yOx8M0wQtnSoAOaM | 33 - Retainer Billing | Webhook | Stripe subscription checkout |

### Stromation Workflows -- OFF
| n8n ID | Name | Reason |
|--------|------|--------|
| 6ifZIIHeEfDyIixL | 13 - Reddit Community Bot | Disabled until karma 50+ |
| UGRobtNd5Hx5ogmB | 15 - Reddit Reply Handler | OFF |
| poONkDtBrIXeafIX | 17 - Reddit Karma Builder | OFF |
| U2lfXN8F2szI6v67 | 18 - Local Business Finder | KILLED -- cold outreach abandoned |
| m8TJKxwBj6h1OPUp | 19 - Cold Email Outreach | KILLED -- 0 replies from 245 emails |
| LQI7ojFU2GOaqMHo | 20 - Outreach Reply Handler | KILLED -- no outreach to handle |
| L22SHb3s7blq3fXR | 23 - Lead Nurture Drip | KILLED -- part of outreach system |
| QkUSrPM055wfnsKL | 24 - Weekly Pipeline Digest | OFF |

### SMTP Credentials
| Credential | Email | Used By |
|------------|-------|---------|
| admin | darius@stromation.com | WF27, WF30, WF31, WF32, all TBE workflows |
| SMTP - Stromation (leads@) | leads@stromation.com | WF11, WF21, WF22, WF25, WF26 |

### Critical n8n Rules
- Use `this.helpers.httpRequest()` -- NOT fetch(), NOT require()
- emailSend v2.1: use `text` or `html` param -- NOT `message` (silently ignored = blank emails)
- Always set `options: { appendAttribution: false }` on email nodes
- fromEmail MUST match SMTP credential user (or 553 rejection)
- bids@stromation.com is NOT a valid SMTP sender -- gets 553 rejected. Use darius@stromation.com
- Don't use `Buffer.from()` in n8n Code nodes -- use pure JS base64 helpers
- n8n API PUT only updates draft -- must publish from UI. Workaround: deactivate/reactivate via API
- n8n API key at /home/darius/Documents/mcp/n8n_api_key.txt (expires periodically)

## Supabase

### Keys
- Anon (frontend-safe): sb_publishable_8qa-nssfdtEkCz-42wOSWQ_2P7S4Zj7
- Service (server-only): REDACTED_USE_N8N_CREDENTIALS

### Tables
| Table | Purpose |
|-------|---------|
| businesses | Website lead CRM (source=website from WF22). Cold outreach data wiped 2026-04-20 |
| outreach_log | Email history -- wiped 2026-04-20 (cold outreach abandoned) |
| reddit_leads | Reddit posts scored by GPT |
| projects | Client projects (WF28 onboarding) |
| invoices | Invoice tracking (WF27) |
| proposals | Proposals/contracts (WF30) |
| tbe_bids | TBE bid opportunities + pipeline tracking |
| tbe_bid_items | TBE line items per bid (materials + labor) |
| tbe_pricing_defaults | TBE default rates (32 items, DFW market) |
| tbe_bid_activity | TBE status change audit log |
| tbe_saved_searches | TBE keyword/filter monitoring |
| tbe_bid_skiplist | Junked bids -- prevents WF1 from re-creating |

## TBE Auto-Bidder -- Current Architecture (Pipeline v17.4)

### Antonio's Scope (Division 27 ONLY)
- Structured cabling (Cat5E Wavenet default, Cat6A only when spec requires)
- Cameras -- install only (hang + cable, owner furnishes hardware/NVR/licenses)
- Audio visual (speakers, displays, paging)
- Intercom / drive-thru (HME EOS HD)
- Network infrastructure (rack, patch panels, cable management)
- **NOT in scope**: access control, intrusion, fire alarm, SCADA, POS terminals, UPS/PDU/switch (owner/IT scope)

### Default Vendor: Wavenet (QSR/commercial)
- Cat5E cable $246/box, jacks $1.39, faceplates $0.85, patch cords $1.92
- 6U wall mount rack $293 (≤24 drops), 12U+ for larger jobs
- Panduit Cat6A only for enterprise tier or when spec explicitly requires
- Freight: $130 QSR, $500 commercial, $1,200 enterprise
- PM hours: 4 small, 8 medium, scaled 18% large
- Labor: $85/hr field, $105/hr PM

### Pipeline Flow
1. **Intake** (WF1): PlanHub email → extract project ID → create bid row
2. **Download** (WF2): PlanHub API → download PDFs → split pages → classify (Gemini batch, free)
3. **Legend** (WF3): extract symbol legend → build scope_brief (~500 tokens)
4. **Count** (WF3): Claude vision on DRAWING pages only, grounded by scope_brief
5. **Crosscheck**: Gemini free second-opinion per page, caps overcounts
6. **Quote** (WF4): pricing engine → line items → Supabase
7. **Verify** (WF6): Gemini critic with size-aware rules
8. **Autopilot**: if Gemini=looks_right ≥90% AND heuristics pass → auto-send via WF5
9. **Review**: else → pending_review with specific banner

### Bid Statuses
`new, awaiting_blueprints, analyzing, pending_review, reviewing, estimating, quote_ready, quote_sent, submitted, won, lost, no_bid, expired`

### Cost Per Bid
- Small commercial (10-15 pages): ~$0.50
- Medium renovation (50 pages): ~$2.40
- Large school (4000+ pages): ~$1.95 (Gemini batch classify saves on large sets)
- Hard cap: $3/bid

### Open TBE Items
- [ ] Gemini free tier RPD cap (20/day) -- enable billing at aistudio.google.com for free $300 credit
- [ ] WF5 toEmail in test mode (dariusstroman@gmail.com) -- flip to antonio@tbeit.com for production
- [ ] WF1 Bid Alert Parser currently OFF -- re-enable when PlanHub token refreshed
- [ ] Move WF3 hardcoded Anthropic key to n8n credentials
- [ ] Add page_evidence JSONB column to tbe_bids
- [ ] PlanHub auth token refresh (re-capture from browser DevTools)
- [ ] Anthropic Batch API for non-urgent bids (50% discount)

## Darius Voice
- Normal capitalization, no apostrophes in contractions (dont, cant, Im, youre)
- No exclamation marks, semicolons, em dashes
- Short sentences, casual (gonna, kinda, prob, tbh)
- Never say AI phrases ("I noticed", "dive deeper", "leverage", "streamline", etc.)
- fixVoice() post-processor on all GPT output

## Phone/SMS
- Number: (855) 932-0493
- Calls → text redirect (voicemail.xml)
- Texts → AI reply + lead emailed to Gmail

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

## Don'ts
- **NEVER delete Supabase data without showing Darius every record first and getting explicit confirmation.**
- **NEVER commit API keys, JWTs, bearer tokens, or service-role secrets to ANY tracked file.** Reference values by where they live (n8n credential name, env var, dashboard) instead of pasting.
- Don't add frameworks or build tools
- Don't change pricing without explicit request
- Don't use Formspree -- all forms → n8n webhook
- Don't re-enable cold email outreach (WF18/19/20/23) -- abandoned, 0% reply rate, burns sender reputation
- Don't put Supabase service key in frontend code (use anon key)
- Don't modify voicemail.xml without explicit request
- Don't mention Make or Zapier on the site -- Stromation only uses n8n
- Nav says "Industries" not "Workflows"

## Bot Protection (added 2026-04-20)
- All 4 forms (contact, audit, checklist, ROI) have honeypot field + 3-second time gate
- WF22 server-side honeypot check returns empty array (kills email for bots)
- Chat widget: 6 msgs/min rate limit + 30 msgs/session cap
- Phone/SMS: Twilio transport layer handles abuse

## Blog
- 46 posts (auto-generated weekly by WF25, Sunday 6AM CT)
- Blog page paginated: 9 posts per page with prev/next
- Reading times calculated from actual word count (not hardcoded)
- WF25 calculates reading time for new posts automatically

## Known Issues
- Reddit karma still at -1 (WF13 off until 50+)
- Google Ads + Facebook Pixel not set up yet
- LinkedIn/Twitter content not yet posted (docs ready in docs/)
- Industry landing pages (dental, home-services, etc.) have no inline forms, only link to audit.html
