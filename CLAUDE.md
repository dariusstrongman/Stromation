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

## Site Structure

### Root Pages (20 pages)
| File | Purpose |
|------|---------|
| index.html | Homepage -- hero, showcase video (lazy loaded), services, how-it-works, stats, testimonial |
| services.html | Service offerings + pricing tiers (FAQ schema) |
| industries.html | Industry-specific automation use cases |
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
| admin-invoice.html | Admin: send invoices (password protected: Kyomi123, noindex) |
| admin-proposal.html | Admin: send proposals (password protected: Kyomi123, noindex) |
| admin-dashboard.html | Admin: live CRM dashboard from Supabase (password protected: Kyomi123, noindex) |
| privacy.html | Privacy policy |
| terms.html | Terms of service |
| 404.html | Custom 404 error page |

### Blog Posts (blog/) -- 18 posts
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

## n8n Workflows (n8n.myaibuffet.com) -- 20 total (18 active, 1 OFF, 1 template)

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

### Client Management (webhook-triggered)
| ID | Name | Webhook | Description |
|----|------|---------|-------------|
| 26 | Review Request | /webhook/stromation-review-request | Review request email. Validates: requires client_email. |
| 27 | Invoice Generator | /webhook/stromation-invoice | Professional invoice + Stripe Pay Now link. Validates: requires email, positive amount. From darius@. |
| 28 | Client Onboarding | /webhook/stromation-onboard | Welcome email + intake link, status → 'won'. Validates: requires email + name. |
| 30 | Proposal Generator | /webhook/stromation-proposal | Branded proposal email. Validates: requires email, amount, project_title. From darius@. |

### Operations
| ID | Name | Description |
|----|------|-------------|
| 29 | Error Alert | Emails dariusstroman@gmail.com on ANY workflow failure. Wired to all via errorWorkflow. |

### SMTP/IMAP Credentials
| Credential | Email | Used By |
|------------|-------|---------|
| SMTP - Stromation (leads@) | leads@stromation.com | WF11, WF21, WF22, WF23, WF24, WF25, WF26, WF29 |
| admin | darius@stromation.com | WF27 (invoices), WF30 (proposals) |
| SMTP - Outreach(Chase) | chase@stromation.com | WF19 (cold email outreach) |
| IMAP - Outreach(chase) | chase@stromation.com | WF20 (watches inbox for replies) |

**Chase is the outreach persona.** Cold emails go from chase@stromation.com. When a lead gets hot, Chase hands off to Darius. outreach@stromation.com was deleted -- do not reference it.

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
| Simple | $1,000 -- $2,500 |
| AI-Assisted | $2,500 -- $6,000 |
| End-to-End | $6,000 -- $15,000+ |
| Monitor Retainer | $99/month |
| Maintain Retainer | $149/month |
| Optimize Retainer | $499/month |

## Admin Pages
All password protected with `Kyomi123` (sessionStorage, once per session):
- stromation.com/admin-invoice.html -- send invoices
- stromation.com/admin-proposal.html -- send proposals
- stromation.com/admin-dashboard.html -- live CRM dashboard (uses Supabase anon key)

## Performance Optimizations Applied
- Showcase video: preload=none + loading=lazy (saves 3.5MB initial load)
- Cal.com iframes: loading=lazy
- CSS/font preload hints on index.html
- Reading time badges on all 18 blog posts
- Breadcrumbs + BreadcrumbList schema on all main pages + blog posts
- Internal cross-linking between blog posts (33 links)
- FAQ link in footer on all pages

## Don'ts
- **NEVER delete Supabase data without showing Darius every record first and getting explicit confirmation.** Real data was lost because records were assumed to be test data. Always ask before ANY delete operation. Never use `id=not.is.null` without approval.
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
- Don't modify voicemail.xml without explicit request

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
