# Stromation

## Project Overview
- **stromation.com** -- Workflow Replacement Studio owned by Darius Stroman
- Static HTML/CSS/JS site hosted on GitHub Pages
- Repo: github.com/dariusstrongman/Stromation
- Domain: www.stromation.com (CNAME)
- Twitter/X: @stromationhq
- Email: support@stromation.com

## Tech Stack
- Pure vanilla HTML, CSS, JS -- no frameworks, no build tools, no bundlers
- Google Fonts (Inter, weights 400-800)
- Google Analytics (G-B6Z6XV02RT)
- Formspree for contact form (mkobkvwl)
- Chat widget (chat.js) connects to n8n webhook at n8n.myaibuffet.com
- Schema.org structured data (ProfessionalService) on index.html
- FAQ schema (FAQPage) on services.html and audit.html
- RSS feed (feed.xml) for blog syndication
- OG and Twitter meta tags on all pages

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
| index.html | Homepage -- hero (text only, no illustration), services overview, how-it-works, stats, FAQ |
| services.html | Detailed service offerings and pricing tiers |
| industries.html | Industry-specific automation use cases |
| case-studies.html | Client case studies with results |
| about.html | About Darius, company story, headshot |
| contact.html | Contact form (Formspree) + info |
| audit.html | Free automation audit request form |
| blog.html | Blog index with card grid |
| privacy.html | Privacy policy |
| terms.html | Terms of service |
| checklist.html | Lead magnet -- free automation checklist landing page |
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

### Other Key Files
| File | Purpose |
|------|---------|
| styles.css | Single global stylesheet |
| script.js | Main JS -- mobile menu, scroll animations, parallax, forms, FAQ accordion |
| chat.js | Chat widget connecting to n8n webhook (loaded deferred on all pages) |
| feed.xml | RSS feed for blog posts |
| sitemap.xml | XML sitemap for search engines |
| robots.txt | Robots directives |
| voicemail.xml | TwiML voice redirect -- tells callers to text instead (Neural2-J voice) |
| CNAME | GitHub Pages custom domain |
| .nojekyll | Disables Jekyll processing |

### Image Assets
- `img/` -- SVG illustrations for hero, services, case studies, steps, chat icon; darius-headshot.jpg
- `logos/` -- Full brand kit: icon, logo, dark/light variants in SVG + PNG (512px to 4096px)
- Root: logo.svg, logo-icon.svg, logo-white.svg, logo.png, banner-1500x500.png, profile-pic-400x400.png, favicon.ico

## Blog Workflow
When creating a new blog post:
1. Create HTML file in `blog/` matching the structure of an existing post
2. Add a card to `blog.html` in the blog grid section
3. Add a `<url>` entry to `sitemap.xml` with `<priority>0.7</priority>`
4. Use existing CSS classes from styles.css -- no inline styles needed
5. Blog posts use relative paths: `../logo.svg`, `../styles.css`, `../blog.html`
6. Include Google Analytics snippet, OG/Twitter meta tags, and canonical URL
7. Commit message format: `blog: Post Title Here`

## n8n Workflows (n8n.myaibuffet.com) -- 14 active (13 OFF)

### Lead Capture & Communication
| ID | Name | Description |
|----|------|-------------|
| 11 | SMS Handler | AI text replies + emails leads to Gmail |
| 12 | Website Chatbot | GPT acts as Darius on stromation.com |
| 22 | Website Form Handler | Audit/contact/checklist forms → Supabase + email |

### Outbound & Outreach
| ID | Name | Description |
|----|------|-------------|
| 18 | Local Business Finder | Google Places API → Supabase (daily 7AM CT) |
| 19 | Cold Email Outreach | 3-email sequence to new leads (daily 9AM CT) |
| 20 | Outreach Reply Handler | AI conversation with replies, extracts phone/tools/pain |
| 23 | Lead Nurture Drip | 3-email drip for website leads (daily 10AM CT, seq 50/51/52) |

### Reddit (u/dev_darius)
| ID | Name | Description |
|----|------|-------------|
| 13 | Reddit Community Bot | **OFF** -- posts flagged due to low karma |
| 14 | Reddit Comment Bot | Comments on relevant posts (2x daily) |
| 15 | Reddit Reply Handler | Responds to replies (every 4 hours) |
| 17 | Reddit Karma Builder | Casual comments on safe subreddits (daily 9AM CT) |
| 21 | Reddit Lead Digest | Daily 6PM CT digest of high-intent Reddit posts |

### Content & Reporting
| ID | Name | Description |
|----|------|-------------|
| 24 | Weekly Pipeline Digest | Monday 8AM CT stats email to Darius |
| 25 | Auto Blog Publisher | Weekly blog post via GPT → GitHub (Sunday 6AM CT) |

### Client Management (webhook-triggered)
| ID | Name | Description | Webhook |
|----|------|-------------|---------|
| 26 | Review Request | Sends review request email to client | /webhook/stromation-review-request |
| 27 | Invoice Generator | Generates and sends professional invoice | /webhook/stromation-invoice |
| 28 | Client Onboarding | Welcome email + intake questionnaire | /webhook/stromation-onboard |

Deleted: 00 (Error Handler), 10 (Voicemail), 16 (Lead Alert)

- Reddit account: u/dev_darius
- n8n API requires `X-N8N-API-KEY` header
- Form webhook: `https://n8n.myaibuffet.com/webhook/stromation-form`
- All email sends use SMTP credential "SMTP - Stromation (leads@)" from leads@stromation.com

## Key Patterns
- All pages share the same nav and footer HTML structure
- Nav CTA button: "Get a Free Audit" links to audit.html
- Logo in nav: workflow node icon (logo.svg) + "Stromation" text span
- Blog posts reference `../logo.svg` and `../blog.html` (relative paths from blog/)
- Footer includes stromation-icon.svg from `logos/` folder
- All pages include `chat.js` with `defer` attribute
- Forms post to Formspree endpoint or n8n webhook (see script.js constants)
- JS initializes on DOMContentLoaded: mobile menu, header scroll, scroll animations, parallax, steps progress, count-up, smooth scroll, active nav, contact form, newsletter form, FAQ accordion

## Phone/SMS
- Number: (855) 932-0493
- Calls: short message redirecting caller to text instead (voicemail.xml, Neural2-J voice). No recording/transcription.
- Texts: AI-classified via GPT, auto-reply sent, lead emailed to dariusstroman@gmail.com
- Voicemail workflow (10) deleted -- all lead capture happens via text now

## Pricing (current)
| Tier | Price |
|------|-------|
| Automation Audit | Free |
| Simple Automation | $1,000 -- $2,500 |
| AI-Assisted Automation | $2,500 -- $6,000 |
| End-to-End Automation | $6,000 -- $15,000+ |
| Retainer (Starter) | $99/month |
| Retainer (Growth) | $149/month |
| Retainer (Scale) | $499/month |

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

## Don'ts
- Don't add frameworks or build tools -- this is intentionally vanilla HTML/CSS/JS
- Don't change pricing without explicit request from Darius
- Don't use Formspree for new features (use n8n email node instead)
- Don't use SMS for notifications (use n8n email node instead)
- Don't commit .env files or API keys
- Don't use inline styles -- use existing CSS classes in styles.css
- Don't break relative paths in blog posts (they use ../ prefix)
- Don't modify voicemail.xml without explicit request
