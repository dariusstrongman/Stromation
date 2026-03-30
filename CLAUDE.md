# Stromation

## Project Overview
- **stromation.com** -- Workflow Replacement Studio owned by Darius Stroman
- Static HTML/CSS/JS site hosted on GitHub Pages
- Repo: github.com/dariusstrongman/Stromation
- Domain: www.stromation.com (CNAME)
- Twitter/X: @stromationhq
- Email: support@stromation.com
- Darius personal email: dariusstroman@gmail.com

## Tech Stack
- Pure vanilla HTML, CSS, JS -- no frameworks, no build tools, no bundlers
- Google Fonts (Inter, weights 400-800)
- Google Analytics (G-B6Z6XV02RT)
- Forms submit to n8n webhook (stromation-form), NOT Formspree
- Chat widget (chat.js) connects to n8n webhook at n8n.myaibuffet.com
- Schema.org structured data (ProfessionalService) on index.html
- FAQ schema (FAQPage) on services.html and audit.html
- RSS feed (feed.xml) for blog syndication
- OG and Twitter meta tags on all pages
- Supabase (iadzcnzgbtuigyodeqas.supabase.co) for lead/business CRM
- Google Places API for local business discovery
- Remotion project at C:/Users/Darius/Desktop/stromation-video for video generation

## CSS Custom Properties
Defined in `:root` in styles.css:
- `--primary: #2563EB` / `--primary-dark: #1D4ED8` / `--primary-light: #3B82F6`
- `--secondary: #0EA5E9`
- `--bg-white: #FFFFFF` / `--bg-light: #F8FAFC` / `--bg-subtle: #F1F5F9`
- `--text-primary: #1E293B` / `--text-secondary: #64748B` / `--text-muted: #94A3B8`
- `--success: #10B981` / `--border: #E2E8F0`
- Font: `--font-heading` and `--font-body` both use Inter

## Site Structure

### Root Pages
| File | Purpose |
|------|---------|
| index.html | Homepage -- hero, showcase video, services overview, how-it-works, stats, testimonial, FAQ |
| services.html | Detailed service offerings and pricing tiers (FAQ schema) |
| industries.html | Industry-specific automation use cases |
| case-studies.html | Client case studies with results |
| about.html | About Darius, company story, headshot |
| contact.html | Contact form (n8n webhook) + info |
| audit.html | Free automation audit request form (FAQ schema) |
| blog.html | Blog index with card grid |
| checklist.html | Lead magnet -- free automation readiness checklist with email capture |
| privacy.html | Privacy policy |
| terms.html | Terms of service |
| 404.html | Custom 404 error page |

### Blog Posts (blog/) -- 16 posts
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

New blog posts are auto-generated weekly by WF25 (Sunday 6AM CT).

### Other Key Files
| File | Purpose |
|------|---------|
| styles.css | Single global stylesheet |
| script.js | Main JS -- mobile menu, scroll animations, parallax, forms, FAQ accordion |
| chat.js | Chat widget connecting to n8n webhook (loaded deferred on all pages) |
| stromation-showcase.mp4 | 48s showcase video on homepage (Remotion + OpenAI TTS + music) |
| feed.xml | RSS feed for blog posts |
| sitemap.xml | XML sitemap for search engines |
| robots.txt | Robots directives |
| voicemail.xml | TwiML -- redirects callers to text instead (Google Neural2-J voice) |
| CNAME | GitHub Pages custom domain |
| .nojekyll | Disables Jekyll processing |

### Image Assets
- `img/` -- SVG illustrations for services, case studies, steps, chat icon
- `logos/` -- Full brand kit: icon, logo, dark/light variants in SVG + PNG (512px to 4096px). The correct logo is `logos/logo.svg` and `logos/logo.png`
- Root: logo.svg (nav icon), logo-icon.svg, logo-white.svg, logo.png, banner-1500x500.png, profile-pic-400x400.png, favicon.ico

## Blog Workflow
When creating a new blog post:
1. Create HTML file in `blog/` matching the structure of an existing post
2. Add a card to `blog.html` in the blog grid section
3. Add a `<url>` entry to `sitemap.xml` with `<priority>0.7</priority>`
4. Add an `<item>` to `feed.xml` (newest first)
5. Use existing CSS classes from styles.css -- no inline styles needed
6. Blog posts use relative paths: `../logo.svg`, `../styles.css`, `../blog.html`
7. Include Google Analytics snippet, OG/Twitter meta tags, and canonical URL
8. Commit message format: `blog: Post Title Here`

WF25 (Auto Blog Publisher) handles this automatically every Sunday.

## n8n Workflows (n8n.myaibuffet.com) -- 16 active, 1 off

### Lead Capture & Communication
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 11 | SMS Handler | Webhook | AI text replies + emails leads to Gmail |
| 12 | Website Chatbot | Webhook | GPT acts as Darius on stromation.com (casual voice, fixVoice post-processing) |
| 22 | Website Form Handler | Webhook | Audit/contact/checklist forms → Supabase + email to Gmail |

### Outbound & Outreach
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 18 | Local Business Finder | Daily 7AM CT | Google Places API → finds DFW businesses → Supabase |
| 19 | Cold Email Outreach | Daily 9AM CT | 3-email sequence to new leads (Darius voice, fixVoice) |
| 20 | Outreach Reply Handler | IMAP trigger | AI conversation with replies, extracts phone/tools/pain → Supabase |
| 23 | Lead Nurture Drip | Daily 10AM CT | 3-email drip for website leads (seq 50/51/52) |

### Reddit (u/dev_darius -- karma currently low, building up)
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 13 | Reddit Community Bot | **OFF** | Posts to subreddits -- disabled until karma recovers |
| 14 | Reddit Comment Bot | 2x daily (12PM/5PM CT) | Comments on relevant automation posts |
| 15 | Reddit Reply Handler | Every 4 hours | Responds to replies on our comments |
| 17 | Reddit Karma Builder | Daily 9AM CT | Casual comments on safe subreddits (AskReddit, todayilearned, LifeProTips, etc.) max 2 comments/run |
| 21 | Reddit Lead Digest | Daily 6PM CT | Scans Reddit for high-intent posts, emails digest to Gmail |

### Content & Reporting
| ID | Name | Schedule | Description |
|----|------|----------|-------------|
| 24 | Weekly Pipeline Digest | Monday 8AM CT | Pipeline stats + hot leads email to Gmail |
| 25 | Auto Blog Publisher | Sunday 6AM CT | GPT generates blog post → commits to GitHub → updates blog.html + sitemap + RSS |

### Client Management (webhook-triggered)
| ID | Name | Webhook | Description |
|----|------|---------|-------------|
| 26 | Review Request | /webhook/stromation-review-request | Sends Google review request email to client |
| 27 | Invoice Generator | /webhook/stromation-invoice | Generates HTML invoice, sends to client, CCs Gmail |
| 28 | Client Onboarding | /webhook/stromation-onboard | Welcome email + intake link, updates Supabase status to 'won' |

### Deleted Workflows
- 00 (Error Handler) -- was sending SMS alerts, wasted credits
- 10 (Voicemail Handler) -- replaced by text redirect
- 16 (Lead Alert) -- replaced by WF21 (Reddit Lead Digest) via email

### Webhook URLs
| Webhook | Purpose |
|---------|---------|
| /webhook/stromation-form | Website forms (audit, contact, checklist) |
| /webhook/stromation-chat | Website chatbot |
| /webhook/stromation-sms | Inbound SMS from Twilio |
| /webhook/stromation-review-request | Trigger review request email |
| /webhook/stromation-invoice | Generate and send invoice |
| /webhook/stromation-onboard | Client onboarding sequence |

### Key n8n Details
- Reddit account: u/dev_darius (refresh token with read/submit/identity/history/vote scope)
- All email sends use SMTP credential "SMTP - Stromation (leads@)" from leads@stromation.com
- n8n API requires `X-N8N-API-KEY` header
- All Code nodes use `this.helpers.httpRequest()` (NOT fetch, NOT require)
- `Buffer.from()` works in n8n but `btoa()` is safer
- `require('crypto')` is BLOCKED in n8n sandbox
- All GPT-generated text runs through `fixVoice()` post-processor (strips apostrophes from contractions, removes semicolons/exclamation marks/em dashes)

## Supabase (iadzcnzgbtuigyodeqas.supabase.co)

### Tables
| Table | Purpose |
|-------|---------|
| businesses | Lead/prospect CRM -- name, email, phone, type, city, outreach_status, pain points, tools, deal_value |
| outreach_log | Email history -- business_id, email_num, subject, body, sent_at, status |
| reddit_leads | Reddit lead posts scored by GPT |
| projects | Client projects -- business_id, name, status (proposed/approved/in_progress/delivered/completed), tier, amount, retainer_amount, timeline, dates |
| invoices | Invoice tracking -- business_id, project_id, invoice_num, amount, status (draft/sent/paid/overdue/cancelled), stripe fields, due/paid dates |
| proposals | Proposals/contracts -- business_id, project_title, tier, amount, retainer, timeline, status (sent/viewed/approved/declined/expired) |

### Outreach Status Values (check constraint enforced)
- `new` -- just added (from website form or business finder)
- `in_campaign` -- cold email sequence in progress
- `replied` -- lead replied to outreach (also used for qualified leads)
- `won` -- signed client (set by WF28 onboarding)
- `lost` -- deal lost
- `not_interested` -- declined
- `sequence_complete` -- finished 3-email sequence, no reply
- `unsubscribed` -- requested removal
- `bounced` -- email bounced

INVALID values (will cause 400 error): `qualified`, `client`, `audit_requested`

### Email Sequence Numbers
- 1-3: Cold outreach emails (WF19)
- 50-52: Nurture drip emails (WF23)
- 100+: Conversational replies (WF20)

## Darius Voice (for all AI-generated emails and chat)
All outbound communication matches Darius's actual writing style:
- Normal capitalization (first word of sentences, proper nouns, I)
- NEVER use apostrophes in contractions (dont, cant, Im, youre, Ill, thats, whats, doesnt)
- No exclamation marks, semicolons, or em dashes
- Short sentences, fragments ok, casual (gonna, kinda, prob, tbh)
- Never say: "I noticed", "I help", "I specialize", "dive deeper", "I hear you", "reach out", "touch base", "leverage", "streamline", "absolutely", "great question"
- Sound like a real person, not a salesperson or AI
- fixVoice() post-processor strips smart quotes, apostrophes, semicolons, and exclamation marks from all GPT output

## Key Patterns
- All pages share the same nav and footer HTML structure
- Nav CTA button: "Get a Free Audit" links to audit.html
- Logo in nav: workflow node icon (logo.svg) + "Stromation" text span
- Blog posts reference `../logo.svg` and `../blog.html` (relative paths from blog/)
- Footer includes stromation-icon.svg from `logos/` folder
- All pages include `chat.js` with `defer` attribute
- Forms post to n8n webhook stromation-form (NOT Formspree)
- Homepage has embedded showcase video (stromation-showcase.mp4)

## Phone/SMS
- Number: (855) 932-0493
- Calls: short message redirecting caller to text instead (voicemail.xml, Google Neural2-J voice). No recording/transcription.
- Texts: AI-classified via GPT, auto-reply sent, lead emailed to dariusstroman@gmail.com
- All lead capture happens via text, website forms, or cold email replies

## Pricing (current)
| Tier | Price |
|------|-------|
| Automation Audit | Free |
| Simple Automation | $1,000 -- $2,500 |
| AI-Assisted Automation | $2,500 -- $6,000 |
| End-to-End Automation | $6,000 -- $15,000+ |
| Retainer (Monitor) | $99/month |
| Retainer (Maintain) | $149/month |
| Retainer (Optimize) | $499/month |

## Custom Commands (.claude/commands/)
| Command | Description |
|---------|-------------|
| /brand-update | Apply a brand update across the entire site |
| /case-study | Create a new case study |
| /check-links | Check for broken internal links across all pages |
| /deploy | Deploy to GitHub Pages |
| /n8n-form | Create/update n8n workflow for form submissions |
| /n8n-lead | Design n8n lead handling/follow-up automation |
| /n8n-workflow | Design or troubleshoot an n8n workflow |
| /new-blog | Create a new blog post |
| /new-page | Create a new page for the site |
| /performance | Audit site for performance issues |
| /preview | Start local HTTP server (python -m http.server 8000) |
| /seo-check | Audit SEO across all pages |
| /sitemap | Update sitemap.xml |
| /update-footer | Update footer across all pages |
| /update-nav | Update nav bar across all pages |

## Custom Subagents (.claude/agents/)
| Agent | Purpose |
|-------|---------|
| blog-reviewer | Reviews blog posts for SEO, formatting, and site consistency |
| site-validator | Validates entire site for broken links, missing elements |
| n8n-reviewer | Reviews n8n workflow JSON for bugs, syntax, and best practices |

## Video (Remotion Project)
- Location: C:/Users/Darius/Desktop/stromation-video
- Render: `cd stromation-video && npx remotion render StromationShowcase out/stromation-showcase.mp4`
- 48 seconds, 1920x1080, 30fps
- Voice: OpenAI TTS HD "echo" voice, segmented per scene for precise sync
- Music: Kevin MacLeod "Inspired" (CC BY 4.0)
- Logo outro: SVG draw-on animation matching exact logo from logos/logo.svg
- Copy output to Stromation/stromation-showcase.mp4 after rendering

## Don'ts
- Don't add frameworks or build tools -- this is intentionally vanilla HTML/CSS/JS
- Don't change pricing without explicit request from Darius
- Don't use Formspree -- all forms go to n8n webhook stromation-form
- Don't use SMS for notifications -- use n8n email node (leads@stromation.com)
- Don't use `fetch()` in n8n Code nodes -- use `this.helpers.httpRequest()`
- Don't use `require('crypto')` in n8n -- its blocked in the sandbox
- Don't commit .env files or API keys
- Don't use inline styles -- use existing CSS classes in styles.css
- Don't break relative paths in blog posts (they use ../ prefix)
- Don't re-enable WF13 (Reddit Community Bot) until karma is 50+
- Don't modify voicemail.xml without explicit request
