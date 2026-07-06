# Stromation — The #1 AI News Source

> The signal in the noise. Daily AI news, tools, and insights for business leaders, operators, and founders.

**Live site:** [stromation.com](https://stromation.com)

---

## About

Stromation is a premium AI media brand covering artificial intelligence news, tool reviews, and practical implementation guides. The mission is simple: help business leaders understand what is happening in AI and what to actually do about it — in 5 minutes a day.

---

## Site Structure

| Page | File | Description |
|---|---|---|
| News Homepage | `index.html` | Main news hub with article grid, trending sidebar, and newsletter subscribe |
| AI Tools Directory | `tools.html` | Curated directory of the best AI tools by category |
| Guides & Tutorials | `guides.html` | Deep-dive implementation guides for operators and founders |
| About | `about.html` | Editorial manifesto and brand story |
| Advertise | `advertise.html` | B2B sponsorship intake and media kit request |
| Privacy Policy | `privacy.html` | Privacy policy |
| Terms of Service | `terms.html` | Terms of service |

---

## Design System

The visual system lives in `styles-news.css` and is built around a dark editorial aesthetic:

- **Background:** Deep black (`#050505`) with panel layers (`#0f0f11`)
- **Accents:** Electric cyan (`#00f0ff`) and mint (`#00ffa3`)
- **Typography:** Inter (display + body), JetBrains Mono (metadata + code)
- **Layout:** 12-column CSS grid, responsive down to mobile

---

## Content Categories

- **Breaking News** — Model releases, funding rounds, regulation
- **Enterprise** — AI in business operations and strategy
- **Open Source** — Community models and open-weight releases
- **Tools** — Reviews and comparisons of AI tools
- **Guides** — Step-by-step tutorials and implementation walkthroughs
- **Regulation** — Policy, compliance, and legal developments

---

## Monetization

1. Newsletter advertising (CPM-based, premium AI audience)
2. Sponsored content and tool reviews
3. AI Tools Directory affiliate placements
4. Paid courses and guides (planned)
5. AI job board (planned)

---

## Tech Stack

Pure static HTML/CSS/JS — no build step required. Hosted on GitHub Pages via the `CNAME` pointing to `stromation.com`. Lead capture and newsletter subscriptions post to an n8n webhook.

---

## Local Development

```bash
git clone https://github.com/dariusstrongman/Stromation.git
cd Stromation
python3 -m http.server 8080
# Open http://localhost:8080
```

---

&copy; 2026 Stromation. All rights reserved.
