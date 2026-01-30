# Changelog

## 2025-01-30 - Workflow Replacement Studio Rebrand

### Overview
Transformed the site from a generic "AI automation agency" into a **Workflow Replacement Studio** with clear positioning, honest marketing, and a defined sales process centered on the $299 Automation Audit.

---

### Positioning Changes

**Before:** Generic AI automation services with placeholder pricing and fake testimonials
**After:** Custom workflow automation studio that replaces specific manual processes

- New tagline: "Replace Busywork With Systems"
- Core message: We build systems that replace manual steps in your workflow
- Primary CTA changed from "Free Consultation" to "$299 Automation Audit"
- Audit fee credited toward build if client proceeds

---

### Content Integrity Fixes

Removed all placeholder and unsubstantiated content:
- ❌ Phone number placeholders (123-456-7890)
- ❌ Generic [Name] and [Company] placeholders
- ❌ "X years of experience" claims
- ❌ Fake testimonials with made-up client names
- ❌ Unverifiable stats ("300+ automations deployed")

Replaced with:
- ✅ Real founder name (Darius Stroman)
- ✅ Real company name (Stromation)
- ✅ "Example Engagement" labels for anonymized case studies
- ✅ "Typical Outcomes" instead of guaranteed results

---

### Page-by-Page Changes

#### index.html (Homepage)
- New hero: "Replace Busywork With Systems"
- Added "What We Replace" section with 6 common workflow examples
- Added "How It Works" 4-step process
- Added "Is This Right for You?" fit/not-fit section
- Updated all CTAs to point to Audit

#### services.html
- Changed from tool-based to **system-based categories**:
  - Intake & Lead Handling
  - Ops & Admin Workflow Replacement
  - Customer Support & Knowledge Assistants
  - Reporting & Visibility
- Replaced package pricing with **implementation ranges**: $1,000–$2,500 / $2,500–$6,000 / $6,000–$15,000+
- Added **support retainer tiers**: Monitor ($149/mo), Maintain ($299/mo), Optimize ($499/mo)
- Added "What You Get" section: Documentation, Training, Monitoring

#### case-studies.html → Example Engagements
- Renamed to "Example Engagements"
- All case studies now clearly labeled as examples
- New format: Problem → Workflow Map → Automation Built → Typical Outcomes → Stack
- 5 anonymized examples across different industries

#### industries.html → Common Workflows
- Nav link changed from "Industries" to "Workflows"
- Added workflow matrix table (workflow × industry type)
- Simplified to 4 industry cards with common pain points

#### about.html
- Replaced placeholders with real info (Darius Stroman, Stromation)
- Removed years-of-experience claims
- Added philosophy: "Replace steps, not jobs"
- Updated 5-step process: Audit → Scope → Build → Deploy → Support

#### contact.html
- Hero changed to "Request Your Automation Audit"
- Added lead qualification filters (Best Fit / Not the Right Fit)
- Enhanced form with:
  - Tools checklist (Google Workspace, Slack, HubSpot, etc.)
  - Workflow description textarea
  - Volume and desired outcome fields
  - Budget range dropdown
  - Timeline dropdown

#### audit.html (NEW)
- Dedicated landing page for the $299 Automation Audit
- Explains what the audit is and what's included
- 4 deliverables: Workflow Map, Prioritized Opportunities, System Architecture, Build Scope & Quote
- Clear next steps process

---

### Navigation Updates
- "Industries" → "Workflows"
- "Case Studies" → "Examples"
- Added "Get the $299 Audit" as primary nav CTA
- Removed phone numbers from footer

---

### CSS Additions (styles.css)
Added ~250 lines of new styles for:
- `.fit-badge` - Best fit/not fit indicators
- `.replace-grid` - What we replace cards
- `.process-grid` - How it works steps
- `.fit-grid` - Fit/not fit two-column layout
- `.pricing-range-grid` - Implementation pricing tiers
- `.support-grid` - Support retainer cards
- `.workflow-table` - Industry/workflow matrix
- `.typical-outcomes` - Outcome list styling
- `.filter-box` - Lead qualification boxes
- `.philosophy-box` - Philosophy callout
- `.checkbox-group` - Form tool selection
- `.form-row` - Two-column form fields

---

### Why These Changes

1. **Honesty over hype** - Removed fake testimonials and unverifiable claims that undermine trust
2. **Clear positioning** - "Workflow replacement" is specific and understandable vs generic "AI automation"
3. **Qualified leads** - Fit/not-fit sections and detailed intake form filter out bad-fit inquiries
4. **Real pricing signals** - Implementation ranges set expectations; $299 Audit ensures serious inquiries only
5. **Credibility through specificity** - Example engagements with actual workflow details are more believable than vague success claims

---

## 2026-01-30 - Pricing Visibility & Broadening Update

### Overview
Made pricing easier to find and broadened examples beyond CRM to clearly fit many workflow types (ops/admin, data entry, support, reporting).

---

### Changes

#### C1: Pricing Nav Link
- Added "Pricing" nav link on all 7 pages
- Links directly to `services.html#pricing`
- Position: after "Services" in nav order

#### C2: Services Pricing Section Upgrade
- Renamed section to "Pricing (Starting Ranges)"
- Added audit credit note box above tiers
- Added "Starting Range" badges to each tier
- Broadened examples to include:
  - Spreadsheet/database updates (not just CRM)
  - Data entry replacement with validation
  - Recurring reporting automation
  - AI document extraction (invoices/forms)
  - AI-generated summaries for tickets/calls
  - Role-based routing + audit trails

#### C3: Homepage Pricing Preview
- Added new "Pricing at a Glance" section on index.html
- Shows 3 tier price ranges in compact cards
- Includes $299 audit credit note
- "See Pricing Details" button links to services.html#pricing

#### C4: CRM Overemphasis Reduction
- Reduced "CRM" mentions from 6 to 4
- industries.html: Changed "CRM entry" → "database entry"
- industries.html: Changed "intake → CRM → task" → "intake → database/spreadsheet → task"
- services.html: Changed "CRM entry" → "database/CRM entry"
- Remaining CRM mentions are in case-studies where specific to the example

#### C5: Pricing CSS
Added new styles:
- `.pricing-audit-note` - Highlighted note box
- `.pricing-badge` - "Starting Range" label
- `.pricing-disclaimer` - Bottom reliability note
- `.pricing-preview-grid` / `.pricing-preview-card` - Homepage pricing cards

---

### Acceptance Tests Passed
| Test | Result |
|------|--------|
| "Pricing" nav link on all pages | 7/7 |
| Homepage "Pricing at a Glance" section | Present |
| services.html has `id="pricing"` section | Present |
| CRM not dominant example | Reduced from 6→4 |
| Pricing values unchanged | $1k-$2.5k, $2.5k-$6k, $6k-$15k+, $299 |

---

## 2026-01-30 - Production Ready Patches

### Overview
Made the site production-ready with working form submission, legal pages, and SEO files.

---

### Changes

#### P1: Formspree Endpoint
- Set real Formspree endpoint: `https://formspree.io/f/mkobkvwl`
- Contact form now submits to working endpoint

#### P2: Privacy Policy Page
- Created `privacy.html` with standard privacy policy content
- Covers: data collection, usage, third-party services, cookies, data retention, user rights, security, children's privacy
- Uses site's existing header/footer template
- Includes canonical and OG tags

#### P3: Terms of Service Page
- Created `terms.html` with standard terms content
- Covers: scope of services, audit terms, client responsibilities, payment, refunds, IP, liability, acceptable use, confidentiality, termination
- Uses site's existing header/footer template
- Includes canonical and OG tags

#### P4: Footer Legal Links
- Added Privacy and Terms links to footer on all 9 pages
- New `.footer-legal` CSS styling

#### P5: robots.txt
- Created `robots.txt` at site root
- Allows all crawlers, references sitemap

#### P6: sitemap.xml
- Created `sitemap.xml` at site root
- Includes all 9 pages with lastmod dates

#### P7: Legal Page SEO
- Both new pages include: title, meta description, canonical link, OG tags

---

### Files Created
- `privacy.html`
- `terms.html`
- `robots.txt`
- `sitemap.xml`

### Files Modified
- `script.js` - Formspree endpoint
- `styles.css` - Legal content + footer-legal CSS
- All 7 existing HTML pages - Footer legal links

---

### Acceptance Tests Passed
| Test | Result |
|------|--------|
| Formspree endpoint set | `mkobkvwl` |
| privacy.html exists | Yes |
| terms.html exists | Yes |
| Footer legal links on all pages | 9/9 |
| robots.txt exists | Yes |
| sitemap.xml exists | Yes |
| New pages have SEO tags | Yes |
