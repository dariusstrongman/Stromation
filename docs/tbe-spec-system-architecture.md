# TBE Spec System — Production Architecture

Built 2026-04-14. Replaces hardcoded parts database with a 3-layer system: **spec extraction → tier defaults → user catalog**.

## Goals

- Quotes use the actual parts named in project specs (not generic placeholders that get the bid disqualified).
- For projects without specs (small QSRs), use project-size tiering instead of enterprise-grade defaults.
- Antonio can edit pricing per part with his real distributor cost.
- Every line item carries a `source` field so we can audit where each price came from.

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│ Pipeline (existing)                                                │
│  PlanHub email → WF1 Bid Alert → WF2 File Downloader              │
│   ↓                                                                │
│  Page classification → Claude vision counts → device counts        │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│ NEW: WF8 Spec Extractor (manual trigger via dashboard)             │
│  Dashboard "Upload Spec PDF" button                                │
│   → POST /webhook/tbe-extract-specs {bid_id, pdf_base64}           │
│   → Claude Sonnet reads PDF natively (no OCR/PyMuPDF needed)       │
│   → Extracts manufacturer + model per device category              │
│   → Stores in tbe_bids.spec_data JSONB                             │
│  Cost: ~$0.50-3 per spec PDF                                       │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│ WF4 Auto Bidder (refactored)                                       │
│  1. projectTier(sqFt, building_type, name) → qsr/commercial/ent    │
│  2. Read bid.spec_data (if present)                                │
│  3. expandSystems(counts, vendors, {tier, specData}) →             │
│     - Spec'd manufacturer/model takes precedence                   │
│     - Else tier defaults from PARTS catalog                        │
│  4. Each line item carries _source attribution                     │
│  5. Save with project_tier + per-item source to Supabase           │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│ Dashboard                                                          │
│  Bid card: tier badge (QSR green / Commercial blue / Ent purple)   │
│             spec badge (count of spec'd categories)                │
│             pipeline stepper now 8 phases (added Specs)            │
│  Modal: "Specifications Extracted" table — mfr, model, section     │
│         Line items table now shows Source column with color codes  │
│         "Upload Spec PDF" button + "Re-upload" if already extracted│
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│ admin-parts.html — Antonio's catalog UI                            │
│  /admin-parts.html (Kyomi123 protected)                            │
│  Table of all parts: mfr, model, category, tier, price, default,  │
│   active. Inline edit with auto-save. Add new / disable / delete.  │
│  Filters: search, category, tier, active state.                    │
└────────────────────────────────────────────────────────────────────┘
```

## Project tiers (when no spec available)

| Tier | Trigger | NVR | Camera | Rack | Grounding | UPS |
|---|---|---|---|---|---|---|
| QSR | sqft<5K • restaurant/QSR/fastfood/coffeeshop | Hikvision DS-7608NXI-K2 ($800) | Hikvision DS-2CD2143G2-IS ($180) | 12U wall ($400) | Basic bar ($300) | 1500VA tower ($300) |
| Commercial | sqft 5K-30K • office/retail/warehouse | Avigilon HD-NVR-PREM-6TB ($5K) | Avigilon H6A-DO1-IR ($850) | 18U wall ($1.2K) | Panduit kit ($1.5K) | 3000VA rackmount ($1.1K) |
| Enterprise | sqft >30K • school/hospital/government/airport | i-PRO NVR-R-2-64TB-V8 ($26K) | i-PRO WV-X25500-V3LN ($1.7K) | 42U + PDU ($2.8K) | Hospital-grade ($6K) | 3000VA extended ($1.9K) |

Conservative default: **commercial** (over-engineering kills bids more than under-engineering).

## Cable quantity fix (separate from tiering)

Previous logic: `cableBoxes = ceil(drops / 6.5)` → 56 drops × 50ft = 2,800ft estimate but billed 9 boxes (9000ft). Way over.

New: `cableBoxes = max(1, ceil(drops / 16) + buffer)` → 56 drops → 4 boxes. Each box = 1000ft, avg drop = 60ft, so 16 drops/box is realistic with light buffer.

## spec_data JSONB shape

```json
{
  "spec_pdf": "Project Manual Vol 2.pdf",
  "sections_found": ["27 11 00", "27 13 00", "28 13 00", "28 23 00"],
  "device_specs": {
    "cat6a_drops": {
      "manufacturer": "CommScope",
      "model": "SYSTIMAX 2071E",
      "alternates": ["Panduit"],
      "spec_section": "27 13 00",
      "spec_page": 162,
      "color": "blue",
      "qty_rule": "as shown on plans",
      "notes": "plenum-rated, 25-year warranty required"
    },
    "fixed_cameras": { "manufacturer": "Avigilon", "model": "H6A-DO1-IR", ... },
    ...
  },
  "general_requirements": {
    "warranty": "25 years",
    "labor_class": "BICSI Tech II",
    "testing": "permanent link certification per cable",
    "cable_jacket": "plenum"
  },
  "summary": "1-2 sentence description",
  "extracted_at": "2026-04-14T...",
  "tokens_used": {"input": 12345, "output": 678},
  "estimated_cost_usd": 0.04
}
```

## Workflows

| ID | Name | Webhook | Purpose |
|---|---|---|---|
| uTiy5gtBbhoL2wjo | TBE WF4 - Auto Bidder Engine | /tbe-bid | Builds quote (now tier-aware + spec-aware) |
| 3IjbS6wWZIxQSj9a | TBE WF5 - Quote Sender | /tbe-send-quote | Sends PDF email |
| ZcSsnPOZGN4IxXiM | TBE WF6 - Gemini Verifier | /tbe-verify | Critic on counts |
| 09NUezjKeX1RFjDK | TBE WF7 - Claude Arbitrator | /tbe-arbitrate | Reconciles Claude vs Gemini |
| RfasyaaxB9IHDzVo | TBE WF8 - Spec Extractor | /tbe-extract-specs | Reads spec PDF → spec_data |

## Schema additions

- `tbe_bids.spec_data` JSONB
- `tbe_bids.project_tier` TEXT (qsr/commercial/enterprise)
- `tbe_bids.spec_extracted_at` TIMESTAMPTZ
- `tbe_bid_items.source` TEXT (e.g. "spec:27 13 00 page 162", "tier:qsr (Hikvision NVR)", "manual_override")
- `tbe_parts_catalog` — new table, anon RW (Antonio editable from dashboard)

## What's deferred to next iteration

- **Phase 3 — full vendor pricing**: Antonio uploads his distributor quote sheets, system uses his actual cost + markup instead of MSRP. Catalog now supports `vendor_cost` + `markup_pct` columns; need import UI.
- **Spec-driven price lookup**: WF4 currently swaps part numbers based on TIER; spec_data is captured + displayed but doesn't yet drive part swaps automatically (the catalog lookup-by-mfr-model bridge isn't wired). Phase 2 work.
- **Auto-trigger spec extraction**: currently manual via dashboard upload. Once stable, integrate into pipeline script on EC2 to fire automatically when spec PDFs are detected.
- **Spec extractor cost guard**: large spec books (>200 pages) could cost $5+. Add a confirm with cost estimate before firing.
- **Multi-PDF spec books**: spec usually spans Vol 1 + Vol 2 + Vol 3. Currently one upload at a time — should accept multiple files and merge.

## Files

- `docs/tbe-schema-spec-system.sql` — schema migration (run first)
- `docs/tbe-parts-catalog-seed.sql` — 89 parts + tier alternates (run second)
- `admin-bids.html` — main bid tracker (tier badges, spec phase, upload, source attribution)
- `admin-parts.html` — Antonio's catalog editor
- WF4/WF8 — published via n8n API, code lives on n8n.myaibuffet.com
