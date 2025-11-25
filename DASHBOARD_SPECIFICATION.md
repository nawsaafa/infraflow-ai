# InfraFlow AI - Dashboard Specification
## Comprehensive Design & Development Guide

**Version:** 1.0
**Date:** 2025-11-25
**Status:** Production Ready

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [User Personas & Needs](#user-personas--needs)
3. [Information Architecture](#information-architecture)
4. [Core Features & Modules](#core-features--modules)
5. [UI/UX Design System](#uiux-design-system)
6. [Technical Stack & Integration](#technical-stack--integration)
7. [Database Schema & API Endpoints](#database-schema--api-endpoints)
8. [Development Phases](#development-phases)
9. [Success Metrics](#success-metrics)

---

## Executive Summary

### Project Overview

**InfraFlow AI** is an AI-powered infrastructure finance intelligence platform designed for Development Finance Institutions (DFIs) and project developers. It accelerates due diligence, automates compliance checking, and enables data-driven investment decisions.

### Key Value Propositions

- **70% faster due diligence** - AI-powered document analysis reduces 3-week reviews to 2-3 days
- **Zero missed risks** - Automated red flag detection and multi-framework compliance checking
- **$65K-128K savings per deal** - Eliminate manual processes and reduce credit losses by 20-40%
- **Instant project intelligence** - Semantic search across 24+ verified infrastructure projects

### Target Users

1. **DFI Investment Officers** - Quick project assessment, compliance checking, deal flow management
2. **Project Developers** - Find financing, understand requirements, track submissions
3. **Risk Analysts** - Comprehensive risk assessment, red flag detection, portfolio monitoring
4. **Executive Decision Makers** - Portfolio overview, KPI tracking, investment committee prep

### Platform Capabilities

✅ **Currently Available (Day 1)**
- 24 verified infrastructure projects ($110B+ investment value)
- Supabase cloud database (10 tables, production-ready)
- Pinecone semantic search (24 vector embeddings)
- 18 countries, 17 DFI partners, 5 compliance frameworks

🚀 **To Build (Dashboard)**
- Project discovery and filtering
- AI document analysis
- Financial modeling tools
- Compliance checker
- Risk assessment dashboard
- Investment memo generator

---

## User Personas & Needs

### Persona 1: Sarah - DFI Investment Officer

**Profile:**
- Age: 32-45, MBA + 8-12 years experience
- Works at bilateral DFI (CDC, FMO, Proparco)
- Manages 15-20 active projects, reviews 50+ deals/year
- Tech-savvy, uses Bloomberg Terminal, Excel, Salesforce

**Pain Points:**
1. **Manual document review** - Spends 2-3 weeks per deal reading 500+ page documents
2. **Compliance complexity** - Must check against EBRD ESP, IFC PS, EU Taxonomy simultaneously
3. **Risk assessment** - Misses subtle red flags in financial models and contracts
4. **Information scatter** - Data across email, SharePoint, deal room, CRM

**Key Needs:**
- 📊 **Deal Pipeline Dashboard** - See all deals at a glance with status, next actions, deadlines
- 🔍 **Smart Search** - Find similar projects by sector, country, DFI, financial metrics
- ⚡ **Quick Screening** - Accept/reject decision in <30 min with AI summary
- ✅ **Compliance Checker** - Automated gap analysis against all frameworks
- 📈 **Financial Analysis** - Instant DCF, IRR, NPV, DSCR with sensitivity analysis
- 🚩 **Red Flag Detection** - AI highlights risks, inconsistencies, missing data
- 📝 **Investment Memo Draft** - AI generates first draft from uploaded documents

**User Journey:**
```
1. Morning: Open dashboard → See 5 new deals in pipeline
2. Click deal → AI shows 2-page summary + risk score
3. Review compliance → See gaps in ESG documentation
4. Run financial model → Test 3 scenarios
5. Flag for IC → AI drafts investment memo
6. IC meeting → Present with confidence
```

**Success Metrics:**
- Time to screen: 3 weeks → 2-3 days (70% reduction)
- Missed risks: Frequent → Zero (90% error reduction)
- IC prep time: 3-5 days → 1 day

---

### Persona 2: Ahmed - Infrastructure Project Developer

**Profile:**
- Age: 35-50, Engineering/Business background
- Works at renewable energy developer (ACWA Power, Masdar, etc.)
- Developing $500M-5B green hydrogen/solar projects
- Seeking DFI co-financing (20-40% of capital stack)

**Pain Points:**
1. **DFI discovery** - Doesn't know which DFIs fund his sector/country
2. **Requirements confusion** - Each DFI has different compliance standards
3. **Documentation gaps** - Doesn't know what's "bankable" until late-stage rejection
4. **Communication delays** - Weeks waiting for feedback on submissions

**Key Needs:**
- 🎯 **DFI Matching** - See which DFIs fund projects like his (sector, size, country)
- 📋 **Requirements Checklist** - Know exactly what documents/data to prepare
- 📤 **Project Submission** - Upload documents, track review status
- 💬 **Q&A Chat** - Ask questions about requirements, get instant answers
- 🔔 **Status Updates** - Real-time notifications on deal progress
- 📊 **Benchmarking** - See how his project compares to funded comparables

**User Journey:**
```
1. Create account → Upload project overview
2. See DFI matches → EBRD, BII, Proparco interested
3. Review requirements → Upload missing ESG docs
4. Submit for review → DFI sees pre-scored project
5. Track progress → See "In Due Diligence" status
6. Get notification → "DFI requests more info on offtake"
```

**Success Metrics:**
- DFI discovery time: Weeks → Minutes
- Rejection rate: 60% → 30% (better preparation)
- Time to term sheet: 6-12 months → 3-6 months

---

### Persona 3: Lisa - Risk Analyst

**Profile:**
- Age: 28-38, CFA or risk management background
- Specializes in credit, political, or ESG risk
- Reviews 30-40 projects/year in detail
- Uses Excel, @RISK, internal risk models

**Pain Points:**
1. **Manual risk scoring** - Builds spreadsheets for each project from scratch
2. **Red flag hunting** - Must read every page looking for issues
3. **Portfolio monitoring** - Hard to track risk trends across 100+ projects
4. **Report generation** - Days preparing risk committee reports

**Key Needs:**
- 🎯 **Risk Scoring Dashboard** - See all projects on risk matrix (heat map)
- 🚨 **Automated Red Flags** - AI detects risks (political, currency, credit, ESG)
- 📊 **Portfolio Risk View** - Aggregated exposure by country, sector, risk type
- 📈 **Trend Analysis** - Risk evolution over time, early warning signals
- 📄 **Risk Report Generator** - One-click comprehensive risk assessment
- 🔍 **Deep Dive Tools** - Drill down into specific risks with supporting data

**User Journey:**
```
1. Open risk dashboard → See portfolio heat map
2. Filter: High-risk projects → 5 projects flagged
3. Click project → See risk breakdown by category
4. Review AI red flags → Currency risk increased 20%
5. Generate report → Export PDF for risk committee
6. Set alerts → Notify me if risk score changes >10%
```

**Success Metrics:**
- Risk assessment time: 3-5 days → 1 day
- Credit losses: 2-3%/year → 1-2%/year (early detection)
- Portfolio visibility: Quarterly → Real-time

---

### Persona 4: David - Executive Decision Maker (IC Member)

**Profile:**
- Age: 45-60, 20+ years experience, Board member
- Reviews 20-30 deals/year at Investment Committee
- Limited time (30 min per deal presentation)
- Needs high-level insights, not details

**Pain Points:**
1. **Information overload** - 100+ page memos, can't digest quickly
2. **Inconsistent presentation** - Each analyst presents differently
3. **Missing context** - Doesn't know how project fits portfolio strategy
4. **Decision pressure** - Must approve/reject with incomplete information

**Key Needs:**
- 📊 **Executive Dashboard** - Portfolio overview: AUM, IRR, sectors, countries, risks
- 📈 **Deal Summary Cards** - One-page visual summary per project
- 🎯 **Strategic Fit** - How deal aligns with mandate, SDGs, portfolio targets
- 💰 **Financial Snapshot** - Key metrics (IRR, NPV, DSCR) with traffic lights
- ⚖️ **Comparison View** - This deal vs similar deals (benchmarking)
- ✅ **Recommendation** - Clear approve/reject with AI rationale

**User Journey:**
```
1. Pre-IC review (night before) → See 6 deals on agenda
2. Click deal → Read 1-page AI summary
3. Review financials → IRR 14% (above 12% hurdle)
4. Check risks → 2 moderate risks, both mitigated
5. See recommendation → Analyst + AI both "Approve"
6. IC meeting → Ask clarifying questions, vote
```

**Success Metrics:**
- Pre-read time: 3-4 hours → 1 hour
- Decision confidence: Moderate → High
- IC efficiency: 4 hours → 2 hours (better prep)

---

## Information Architecture

### Site Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         InfraFlow AI                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
         ┌──────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
         │  Dashboard   │ │  Projects  │ │  Portfolio │
         │  (Overview)  │ │  (Browse)  │ │ (Analytics)│
         └──────────────┘ └────────────┘ └────────────┘
                │               │               │
        ┌───────┼───────┐      │       ┌───────┼───────┐
        │       │       │      │       │       │       │
     ┌──▼──┐ ┌─▼──┐ ┌──▼──┐  │    ┌──▼──┐ ┌──▼──┐ ┌──▼──┐
     │KPIs │ │Feed│ │Tasks│  │    │ Perf│ │Risk │ │ ESG │
     └─────┘ └────┘ └─────┘  │    └─────┘ └─────┘ └─────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
             ┌──────▼──┐ ┌────▼─────┐ ┌─▼────────┐
             │ Search/ │ │ Project  │ │ Tools/   │
             │ Filter  │ │ Detail   │ │ Actions  │
             └─────────┘ └──────────┘ └──────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
             ┌──────▼───┐ ┌──▼─────┐ ┌─▼────────┐
             │Overview/ │ │Financial│ │Documents/│
             │ Summary  │ │ Analysis│ │ DD       │
             └──────────┘ └─────────┘ └──────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
             ┌──────▼───┐ ┌──▼─────┐ ┌─▼────────┐
             │Compliance│ │  Risk   │ │Investment│
             │  Check   │ │Assessment│ │  Memo   │
             └──────────┘ └─────────┘ └──────────┘
```

### Navigation Structure

**Primary Navigation (Top):**
- 🏠 Dashboard - Overview and activity feed
- 📂 Projects - Browse all projects with filters
- 📊 Portfolio - Analytics and reporting
- ⚙️ Settings - User preferences

**Secondary Navigation (Contextual):**
- Within Projects: Grid/List view, Filters, Sort, Search
- Within Project Detail: Tabs (Overview, Financials, Risk, Compliance, Documents, Activity)
- Within Tools: Quick actions (Upload Document, Create Memo, Run Analysis)

**User Profile Menu (Top Right):**
- Profile & Settings
- Notifications (🔔 with badge)
- Help & Support
- Sign Out

---

## Core Features & Modules

### Module 1: Dashboard (Home/Overview)

**Purpose:** Provide at-a-glance visibility into portfolio status, activity, and priorities.

**Target Users:** All personas (customized by role)

**Key Components:**

#### 1.1 KPI Cards (Top Row)
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Projects│ Total Value  │  Countries   │ DFI Partners │
│      24      │   $110B+     │      18      │      17      │
│  +2 this month│  +$12B YTD   │   +3 new     │   +1 new     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Data Source:** Supabase → `SELECT COUNT(*), SUM(total_value) FROM projects`

**Design:**
- Large number (32px, bold)
- Label (14px, gray)
- Trend indicator (+/- with arrow, green/red)
- Icon (building, dollar, globe, handshake)
- Background: White card with subtle shadow

#### 1.2 Deal Pipeline Visualization (Kanban-style)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Screening  │Due Diligence│ IC Review   │  Approved   │
│     12      │      8      │      3      │      1      │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Egypt Solar │ NEOM H2     │ Poland Wind │ India Hub   │
│ $450M       │ $8.4B       │ $200M       │ $21B        │
│ 2 days ago  │ In progress │ Next IC     │ Closed      │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Oman H2     │ Chile eFuels│             │             │
│ $6B         │ $500M       │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Data Source:** Supabase → `SELECT * FROM projects ORDER BY status, updated_at`

**Interactions:**
- Drag & drop to move between stages (updates status)
- Click card to open project detail
- Filter by user, date, sector

**Design:**
- 4 columns (equal width, responsive to 2 columns on mobile)
- Cards: Project name, value, last activity, avatar
- Color-coded headers (blue → yellow → orange → green)

#### 1.3 Activity Feed (Right Sidebar or Bottom Section)
```
┌────────────────────────────────────────────┐
│ Recent Activity                            │
├────────────────────────────────────────────┤
│ 🟢 Ahmed updated Egypt South Sinai docs   │
│    2 hours ago                              │
├────────────────────────────────────────────┤
│ 🔵 Sarah added comment on NEOM H2         │
│    5 hours ago                              │
├────────────────────────────────────────────┤
│ 🟡 Risk score changed: Shell Holland +5%  │
│    Yesterday at 3:24 PM                     │
├────────────────────────────────────────────┤
│ 🔴 IC deadline: Poland Wind (3 days)      │
│    Yesterday                                │
└────────────────────────────────────────────┘
```

**Data Source:** Supabase → `SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 10`

**Design:**
- Chronological list
- Icons by activity type (color-coded)
- Clickable items (navigate to project)
- "View All" link at bottom

#### 1.4 Quick Actions Panel
```
┌────────────────────────────────────────────┐
│ Quick Actions                              │
├────────────────────────────────────────────┤
│ [📤 Upload Document]   [📝 Create Memo]   │
│ [🔍 Search Projects]   [📊 Run Analysis] │
└────────────────────────────────────────────┘
```

**Interactions:** Buttons open modals or navigate to tools

---

### Module 2: Project Discovery & Browse

**Purpose:** Find and filter infrastructure projects using advanced search and semantic matching.

**Target Users:** Investment Officers, Developers, Analysts

**Key Components:**

#### 2.1 Search Bar (Global + Semantic)
```
┌────────────────────────────────────────────────────────────┐
│ 🔍  Search projects by name, country, sector, DFI...      │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- **Keyword Search** - Supabase full-text: `SELECT * FROM projects WHERE name ILIKE '%hydrogen%'`
- **Semantic Search** - Pinecone: Find similar projects by description
  - "Green hydrogen in Middle East" → Returns NEOM, Egypt, Oman projects
  - "Solar projects with battery storage" → Returns renewable + storage projects
- **Autocomplete** - Suggest countries, sectors, DFI names as user types

**Implementation:**
```typescript
// Hybrid search (keyword + semantic)
const keywordResults = await supabase
  .from('projects')
  .select('*')
  .ilike('name', `%${query}%`)

const embedding = await openai.embeddings.create({ input: query })
const semanticResults = await pinecone.query({ vector: embedding.data[0].embedding, topK: 10 })

// Merge and deduplicate results
```

#### 2.2 Advanced Filters (Left Sidebar)
```
┌─────────────────────────┐
│ Filters                 │
├─────────────────────────┤
│ ☑ Sector                │
│   ☐ Green Hydrogen (12) │
│   ☐ Renewable Energy(6) │
│   ☐ Water (2)           │
│   ☐ Other (4)           │
├─────────────────────────┤
│ ☑ Country               │
│   ☐ Egypt (3)           │
│   ☐ Poland (3)          │
│   ☐ Oman (2)            │
│   ☐ [+15 more]          │
├─────────────────────────┤
│ ☑ Status                │
│   ☐ Draft (19)          │
│   ☐ Active (3)          │
│   ☐ Completed (2)       │
├─────────────────────────┤
│ ☑ Investment Range      │
│   [─────●────] $0-$10B │
├─────────────────────────┤
│ ☑ DFI Partners          │
│   ☐ EBRD (5)            │
│   ☐ AfDB (3)            │
│   ☐ [+15 more]          │
└─────────────────────────┘
```

**Data Source:** Supabase with dynamic queries
```typescript
let query = supabase.from('projects').select('*')

if (filters.sector.length > 0) {
  query = query.in('sector', filters.sector)
}
if (filters.country.length > 0) {
  query = query.in('country', filters.country)
}
if (filters.minValue || filters.maxValue) {
  query = query.gte('total_value', filters.minValue)
                .lte('total_value', filters.maxValue)
}
if (filters.dfi.length > 0) {
  // JSONB array contains check
  query = query.contains('dfi_partners', filters.dfi)
}
```

**Design:**
- Collapsible sections (Accordion component)
- Count badges showing matching results
- "Clear All" button
- Responsive: Drawer on mobile

#### 2.3 Project Grid/List View (Main Area)

**Grid View:**
```
┌──────────────┬──────────────┬──────────────┐
│ NEOM H2      │ Western Hub  │ Egypt Sinai  │
│ Saudi Arabia │ Australia    │ Egypt        │
│ $8.4B        │ 3.5M t/yr    │ $17B         │
│ 🟢 Active    │ 🟡 Draft     │ 🟡 Draft     │
│ [View →]     │ [View →]     │ [View →]     │
└──────────────┴──────────────┴──────────────┘
```

**List View:**
```
┌────────────────────────────────────────────────────────────┐
│ Name                 │ Country  │ Value  │ Status  │ DFIs  │
├────────────────────────────────────────────────────────────┤
│ NEOM Green Hydrogen  │ Saudi    │ $8.4B  │ Active  │ 3     │
│ Western Green Hub    │ Australia│ N/A    │ Draft   │ 2     │
│ Egypt South Sinai    │ Egypt    │ $17B   │ Draft   │ 2     │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- Toggle Grid/List view (icons in top right)
- Sort by: Name, Value, Date, Status (ascending/descending)
- Pagination: 12 per page (grid), 20 per page (list)
- Hover effect: Card lifts, shows "View Details" button

**Data Source:** Supabase paginated query
```typescript
const { data, count } = await supabase
  .from('projects')
  .select('*', { count: 'exact' })
  .range((page - 1) * pageSize, page * pageSize - 1)
```

---

### Module 3: Project Detail Page

**Purpose:** Comprehensive view of a single project with all analysis tools.

**Target Users:** All personas (different sections prioritized by role)

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ [← Back to Projects]          NEOM Green Hydrogen Project  │
│                                                             │
│ Saudi Arabia • Green Hydrogen • $8.4B • Active             │
│                                                             │
│ [Overview] [Financials] [Risk] [Compliance] [Documents]   │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  (Tab content here)                                         │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

#### 3.1 Overview Tab

**Project Summary Card:**
```
┌────────────────────────────────────────────────────────────┐
│ Project Overview                                            │
├────────────────────────────────────────────────────────────┤
│ Name:        NEOM Green Hydrogen Project (Helios)          │
│ Location:    NEOM, Saudi Arabia                            │
│ Sector:      Green Hydrogen                                │
│ Capacity:    600 tonnes H2/day (219,000 tonnes/year)       │
│ Investment:  $8.4 billion                                   │
│ Partners:    ACWA Power, Air Products, NEOM                │
│ Status:      Under Construction (80% complete)             │
│ Timeline:    2020-2026 (COD: Dec 2026)                     │
│ Technology:  PEM/Alkaline Electrolyzer (2.2 GW)            │
│              Wind (1.6 GW) + Solar (2.2 GW)                │
│ Offtaker:    Air Products (exclusive)                      │
│ Financing:   23 financial institutions, closed May 2023    │
└────────────────────────────────────────────────────────────┘
```

**Data Source:** Supabase → `SELECT * FROM projects WHERE id = ?`
Metadata stored in JSONB `metadata` column

**Key Metrics Row:**
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Capacity     │ Investment   │ CO2 Reduction│ Jobs Created │
│ 219K t/year  │ $8.4B        │ TBD          │ TBD          │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**AI-Generated Summary:**
```
┌────────────────────────────────────────────────────────────┐
│ 🤖 AI Summary                                               │
├────────────────────────────────────────────────────────────┤
│ World's largest green hydrogen project using 100%          │
│ renewable energy (wind + solar). Demonstrates commercial    │
│ scale hydrogen production for global export as green        │
│ ammonia. Strong sponsors (ACWA Power, Air Products) with    │
│ long-term offtake secured. Construction 80% complete.       │
│                                                             │
│ Key Strengths: Scale, proven technology, creditworthy      │
│ offtaker, government support                                │
│                                                             │
│ Key Risks: Construction completion risk, hydrogen market   │
│ price volatility, regulatory framework evolution           │
└────────────────────────────────────────────────────────────┘
```

**Implementation:** Call Claude API with project data:
```typescript
const summary = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  messages: [{
    role: "user",
    content: `Summarize this infrastructure project in 100 words: ${JSON.stringify(project)}`
  }]
})
```

**Interactive Map:**
```
┌────────────────────────────────────────────────────────────┐
│ 🗺️ Project Location                                         │
│                                                             │
│         [Interactive map with pin at NEOM, Saudi Arabia]   │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Library:** MapLibre GL + marker at project coordinates

#### 3.2 Financial Analysis Tab

**DCF Model Summary:**
```
┌────────────────────────────────────────────────────────────┐
│ Financial Model                                             │
├────────────────────────────────────────────────────────────┤
│ Base Case:                                                  │
│   IRR:         15.3%    (Hurdle: 12%)    ✅ PASS           │
│   NPV:         $1.25B   (@ 10% discount) ✅ POSITIVE        │
│   Payback:     8.5 years                 ✅ ACCEPTABLE      │
│   DSCR:        1.85x    (Min: 1.3x)      ✅ STRONG          │
│                                                             │
│ Downside Case (-20% revenue):                              │
│   IRR:         11.2%    ❌ BELOW HURDLE                     │
│   DSCR:        1.21x    ❌ BELOW MINIMUM                    │
│                                                             │
│ Upside Case (+20% revenue):                                │
│   IRR:         19.8%    ✅ STRONG RETURNS                   │
└────────────────────────────────────────────────────────────┘
```

**Data Source:** Supabase → `financial_models` table linked to project

**Sensitivity Analysis Chart:**
```
┌────────────────────────────────────────────────────────────┐
│ Sensitivity: IRR to Revenue & CAPEX                        │
│                                                             │
│        CAPEX -10%    Base    CAPEX +10%                    │
│ Rev+20%  18.5%      19.8%      17.2%                       │
│ Rev+10%  16.8%      17.1%      15.9%                       │
│ Base     15.3%      15.3%      14.1%                       │
│ Rev-10%  13.1%      12.9%      11.8%                       │
│ Rev-20%  11.2%      10.9%       9.8%                       │
│                                                             │
│ [Heat map: Green = >15%, Yellow = 12-15%, Red = <12%]     │
└────────────────────────────────────────────────────────────┘
```

**Library:** Recharts → Heatmap or Nivo → HeatMap

**Cash Flow Waterfall (Sankey Diagram):**
```
┌────────────────────────────────────────────────────────────┐
│ Sources & Uses of Funds                                     │
│                                                             │
│ Equity ($2.5B) ─────────────┐                              │
│                             ├──→ CAPEX ($8.0B)             │
│ Debt ($6.0B) ───────────────┘                              │
│                                                             │
│ Revenue ($15B) ──────┬──→ OPEX ($3B)                       │
│  (20 years)          ├──→ Debt Service ($7B)               │
│                      └──→ Equity Returns ($5B)             │
└────────────────────────────────────────────────────────────┘
```

**Library:** Nivo → Sankey component

**Actions:**
- "📊 Run Scenario Analysis" → Modal with sliders for variables
- "📥 Export Model to Excel" → Download XLSX with formulas
- "📝 Add to Investment Memo" → Include financial summary

#### 3.3 Risk Assessment Tab

**Risk Matrix (Heat Map):**
```
┌────────────────────────────────────────────────────────────┐
│ Risk Assessment                    Overall Score: 6.2/10   │
├────────────────────────────────────────────────────────────┤
│               Likelihood →                                  │
│        Low      Medium      High                            │
│ High │        │  Political │            │                   │
│      │        │  Currency  │            │                   │
│ Med  │        │  Market    │Construction│                   │
│      │        │            │            │                   │
│ Low  │  Tech  │  ESG       │            │                   │
│      │        │            │            │                   │
│      └────────┴────────────┴────────────┘                   │
└────────────────────────────────────────────────────────────┘
```

**Data Source:** Supabase → `risk_assessments` table

**Library:** Recharts → ScatterChart with quadrants

**Risk Detail Cards:**
```
┌────────────────────────────────────────────────────────────┐
│ 🚨 Construction Risk                                        │
│ Level: MEDIUM  |  Impact: HIGH  |  Likelihood: MEDIUM      │
├────────────────────────────────────────────────────────────┤
│ Description: Project is 80% complete but faces potential   │
│ delays in final commissioning. Electrolyzer technology is  │
│ proven but at unprecedented scale.                          │
│                                                             │
│ Mitigations:                                                │
│ ✓ Experienced EPC contractor (ThyssenKrupp)                │
│ ✓ Performance guarantees in place                          │
│ ✓ Contingency budget (15% of CAPEX)                        │
│ ✓ Independent engineer oversight                           │
│                                                             │
│ Recommendations:                                            │
│ • Request quarterly construction progress reports           │
│ • Include completion delay penalties in loan agreement     │
│ • Consider construction insurance coverage                  │
└────────────────────────────────────────────────────────────┘
```

**AI Red Flags (Auto-detected):**
```
┌────────────────────────────────────────────────────────────┐
│ 🔍 AI-Detected Red Flags                                    │
├────────────────────────────────────────────────────────────┤
│ ⚠️  Hydrogen market price volatility (Low confidence)      │
│     Source: Metadata mentions "market price risk"          │
│     Recommendation: Stress test revenue scenarios          │
│                                                             │
│ ⚠️  Single offtaker dependency (Medium confidence)         │
│     Source: "Air Products exclusive offtaker"              │
│     Recommendation: Review offtake agreement terms         │
│                                                             │
│ ✅ No critical red flags detected in documents             │
└────────────────────────────────────────────────────────────┘
```

**Implementation:** Claude API analyzes project metadata:
```typescript
const redFlags = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  messages: [{
    role: "user",
    content: `Analyze this project for risks and red flags: ${JSON.stringify(project)}`
  }]
})
```

#### 3.4 Compliance Tab

**Multi-Framework Checker:**
```
┌────────────────────────────────────────────────────────────┐
│ ESG Compliance Assessment                                   │
├────────────────────────────────────────────────────────────┤
│ Framework              Status        Score    Issues        │
├────────────────────────────────────────────────────────────┤
│ EBRD ESP 2024         ✅ Compliant   92%      1 minor      │
│ IFC Performance Stds  ⚠️  Review      85%      3 gaps      │
│ EU Taxonomy           ✅ Aligned     100%      0           │
│ Equator Principles    ✅ Compliant   95%      0           │
│ UN PRI                ⚠️  Partial     78%      2 gaps      │
└────────────────────────────────────────────────────────────┘
```

**Data Source:** Supabase → `compliance_checks` table

**Drill-Down: IFC Performance Standards**
```
┌────────────────────────────────────────────────────────────┐
│ IFC Performance Standards Gap Analysis                      │
├────────────────────────────────────────────────────────────┤
│ PS1: Social & Environmental Assessment      ✅ 95%         │
│ PS2: Labor & Working Conditions             ✅ 90%         │
│ PS3: Resource Efficiency & Pollution        ⚠️  80% (Gap)  │
│   Issue: Water discharge standards unclear                  │
│   Action: Request detailed water management plan           │
│                                                             │
│ PS4: Community Health & Safety              ✅ 100%        │
│ PS5: Land Acquisition & Resettlement        N/A            │
│ PS6: Biodiversity Conservation              ⚠️  75% (Gap)  │
│   Issue: Baseline biodiversity survey missing              │
│   Action: Commission ecological assessment                 │
│                                                             │
│ PS7: Indigenous Peoples                     N/A            │
│ PS8: Cultural Heritage                      ✅ 100%        │
└────────────────────────────────────────────────────────────┘
```

**Actions:**
- "📄 Generate Compliance Report" → PDF summary
- "✉️ Send Gap Analysis to Developer" → Email with issues
- "📋 Create ESAP" → Environmental & Social Action Plan

#### 3.5 Documents Tab

**Document Library:**
```
┌────────────────────────────────────────────────────────────┐
│ Documents & Due Diligence                                   │
├────────────────────────────────────────────────────────────┤
│ [📤 Upload Document]  [🔍 Search]  [📁 Filter by Type]     │
├────────────────────────────────────────────────────────────┤
│ Name                      Type        Date        Actions   │
├────────────────────────────────────────────────────────────┤
│ 📄 Financial Model.xlsx   Financial   Nov 2024    [View]   │
│ 📄 EPC Contract.pdf       Legal       Oct 2024    [View]   │
│ 📄 ESIA Report.pdf        ESG         Sep 2024    [View]   │
│ 📄 Offtake Agreement.pdf  Commercial  Aug 2024    [View]   │
└────────────────────────────────────────────────────────────┘
```

**Data Source:** Supabase → `documents` table + Supabase Storage for files

**Document Viewer (Modal or Side Panel):**
```
┌────────────────────────────────────────────────────────────┐
│ [← Back]          Financial Model.xlsx              [✕]    │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  [PDF/Excel preview here]                                   │
│                                                             │
│  AI Summary:                                                │
│  This financial model projects IRR of 15.3% based on...    │
│                                                             │
│  Key Figures Extracted:                                     │
│  • CAPEX: $8.4B                                             │
│  • Revenue Year 1: $450M                                    │
│  • DSCR Minimum: 1.85x                                      │
│                                                             │
│  [💬 Ask Questions] [🔍 Extract Data] [📥 Download]        │
└────────────────────────────────────────────────────────────┘
```

**AI Document Q&A:**
```
User: "What is the assumed hydrogen selling price in year 5?"

AI: Based on the financial model (Sheet: Revenue, Cell D12),
the assumed hydrogen selling price in Year 5 is $3.50/kg,
escalating at 2% annually from a Year 1 price of $3.20/kg.
```

**Implementation:** Claude API with document content:
```typescript
const answer = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  messages: [
    { role: "user", content: documentText },
    { role: "assistant", content: "I've read the document." },
    { role: "user", content: userQuestion }
  ]
})
```

---

### Module 4: Investment Memo Generator

**Purpose:** AI-powered drafting of investment committee memos.

**Target Users:** Investment Officers

**Workflow:**
```
1. Select project
2. Choose memo template (Standard, Fast-Track, Complex)
3. AI generates first draft (30 seconds)
4. User edits inline
5. Export to PDF/Word
```

**Memo Structure (Auto-Generated):**
```
┌────────────────────────────────────────────────────────────┐
│ INVESTMENT COMMITTEE MEMORANDUM                             │
│                                                             │
│ Project:    NEOM Green Hydrogen Project                    │
│ Country:    Saudi Arabia                                   │
│ Sector:     Green Hydrogen                                 │
│ Loan Size:  $500M (Tranche A: Senior Debt)                │
│ IC Date:    2025-12-15                                     │
│ Officer:    Sarah Johnson                                  │
│                                                             │
│ EXECUTIVE SUMMARY                                           │
│ [AI generates 2-paragraph summary]                          │
│                                                             │
│ INVESTMENT RATIONALE                                        │
│ [AI explains why DFI should invest]                         │
│                                                             │
│ FINANCIAL ANALYSIS                                          │
│ [AI inserts key metrics, sensitivity]                       │
│                                                             │
│ RISK ASSESSMENT                                             │
│ [AI lists risks from risk_assessments table]               │
│                                                             │
│ ESG COMPLIANCE                                              │
│ [AI summarizes compliance_checks]                           │
│                                                             │
│ TERMS & CONDITIONS                                          │
│ • Loan Amount: $500M                                        │
│ • Tenor: 15 years                                           │
│ • Interest Rate: SOFR + 250 bps                            │
│ • DSCR Covenant: Minimum 1.3x                              │
│ [AI suggests standard terms based on sector/risk]           │
│                                                             │
│ RECOMMENDATION                                              │
│ The Investment Officer recommends APPROVAL of this          │
│ financing based on strong financial returns (IRR 15.3%),   │
│ proven sponsors, and alignment with DFI green hydrogen     │
│ strategy.                                                   │
└────────────────────────────────────────────────────────────┘
```

**Implementation:** Claude API with structured prompt:
```typescript
const memo = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  messages: [{
    role: "user",
    content: `Generate an investment committee memo for this project:
              Project: ${project}
              Financials: ${financialModel}
              Risks: ${risks}
              Compliance: ${compliance}

              Use formal DFI language. Include executive summary,
              rationale, financial analysis, risks, ESG, terms,
              and recommendation.`
  }]
})
```

**Export Options:**
- 📄 PDF (pdfmake library)
- 📝 Word (docx library)
- 📧 Email draft (pre-filled with memo text)

---

### Module 5: Portfolio Analytics

**Purpose:** Aggregate view of all projects for executives and analysts.

**Target Users:** Executives, Risk Analysts

**Dashboard Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Portfolio Overview                       As of: Nov 25, 2025│
├────────────────────────────────────────────────────────────┤
│ ┌──────────┬──────────┬──────────┬──────────┐              │
│ │  AUM     │ Projects │ Countries│ Avg IRR  │              │
│ │ $110B+   │    24    │    18    │  14.2%   │              │
│ └──────────┴──────────┴──────────┴──────────┘              │
├────────────────────────────────────────────────────────────┤
│ Portfolio by Sector (Pie Chart)                             │
│   Green Hydrogen: 50%                                       │
│   Renewable Energy: 25%                                     │
│   Water/Other: 25%                                          │
│                                                             │
│ Portfolio by Country (Bar Chart)                            │
│   Egypt:  ████████ $20B                                     │
│   Poland: ███████ $18B                                      │
│   Saudi:  ██████ $15B                                       │
│                                                             │
│ Portfolio by Risk Level (Gauge Chart)                       │
│   Low Risk:    8 projects                                   │
│   Medium Risk: 14 projects                                  │
│   High Risk:   2 projects                                   │
│                                                             │
│ Recent Approvals (Timeline)                                 │
│   Nov 2025: India Hub ($21B)                                │
│   Oct 2025: Poland Wind ($200M)                             │
│   Sep 2025: Egypt Solar ($450M)                             │
└────────────────────────────────────────────────────────────┘
```

**Charts:**
- **Pie Chart** - Recharts → PieChart with labels
- **Bar Chart** - Recharts → BarChart with values
- **Gauge Chart** - Recharts → RadialBarChart for risk levels
- **Timeline** - Custom component with milestones

**Filters:**
- Date range selector
- Sector/country/status filters
- Compare periods (e.g., YTD vs previous year)

---

## UI/UX Design System

### Design Framework: **Shadcn/ui + Tailwind CSS**

**Rationale:**
- Maximum customization for DFI branding
- Built on accessible Radix UI primitives
- TypeScript-first approach
- Modern, professional aesthetic
- Component library: https://ui.shadcn.com/

**Alternative:** Material UI (if team prefers more opinionated framework)

---

### Color Palette

**Primary Colors:**
```
Primary Blue:    #1E40AF  (Trust, Authority)
Primary Dark:    #1E3A8A  (Hover states)
Primary Light:   #3B82F6  (Accents)

Success Green:   #10B981  (Positive metrics)
Warning Amber:   #F59E0B  (Caution indicators)
Error Red:       #EF4444  (Risks, negative metrics)
Info Blue:       #3B82F6  (Informational)

Neutral Grays:
- Text Primary:  #111827  (Headings, important text)
- Text Secondary:#6B7280  (Labels, descriptions)
- Border:        #E5E7EB  (Card borders, dividers)
- Background:    #F9FAFB  (Page background)
- Card BG:       #FFFFFF  (Card backgrounds)
```

**Usage:**
- Primary Blue: Buttons, links, key actions
- Success Green: Approved status, positive trends, "Pass" indicators
- Warning Amber: Draft status, pending reviews, "Review" indicators
- Error Red: High risks, rejected status, "Fail" indicators
- Neutrals: Text, backgrounds, borders

**Accessibility:** All color combinations meet WCAG 2.1 AA standards (4.5:1 contrast ratio minimum)

---

### Typography

**Font Family:** Inter (Google Fonts)
- Clean, professional, excellent readability
- Wide character set (supports multiple languages)
- Optimized for screens

**Font Sizes (Tailwind classes):**
```
Heading 1:  text-4xl (36px) font-bold     - Page titles
Heading 2:  text-3xl (30px) font-semibold - Section titles
Heading 3:  text-2xl (24px) font-semibold - Subsections
Heading 4:  text-xl (20px) font-medium    - Card titles

Body Large: text-lg (18px) font-normal    - Important body text
Body:       text-base (16px) font-normal  - Default body text
Body Small: text-sm (14px) font-normal    - Secondary info
Caption:    text-xs (12px) font-normal    - Labels, metadata
```

**Line Height:** 1.5x (Tailwind default `leading-normal`)

**Font Weight:**
- Bold (700): Headings, emphasis
- Semibold (600): Subheadings
- Medium (500): Buttons, labels
- Normal (400): Body text

---

### Spacing & Layout

**Spacing Scale (Tailwind):**
```
xs:  0.25rem (4px)   - Tight spacing within components
sm:  0.5rem (8px)    - Component internal padding
md:  1rem (16px)     - Default spacing between elements
lg:  1.5rem (24px)   - Section spacing
xl:  2rem (32px)     - Major section spacing
2xl: 3rem (48px)     - Page-level spacing
```

**Grid System:**
- 12-column grid (Tailwind grid)
- Responsive breakpoints:
  - sm: 640px (mobile landscape)
  - md: 768px (tablet)
  - lg: 1024px (desktop)
  - xl: 1280px (large desktop)
  - 2xl: 1536px (ultra-wide)

**Container Max Width:** 1280px (centered)

---

### Component Library

**Core Components (Shadcn/ui):**

1. **Button**
   - Variants: Default, Outline, Ghost, Link
   - Sizes: Small, Medium, Large
   - States: Default, Hover, Active, Disabled, Loading

2. **Card**
   - Standard card with header, content, footer
   - Shadow: subtle (shadow-sm)
   - Border: 1px solid border color
   - Radius: rounded-lg (8px)

3. **Data Table**
   - Library: TanStack Table (@tanstack/react-table)
   - Features: Sort, filter, pagination, row selection
   - Responsive: Horizontal scroll on mobile

4. **Form Inputs**
   - Text input, textarea, select, checkbox, radio, date picker
   - Validation: React Hook Form + Zod
   - Error states with red border + message

5. **Modal/Dialog**
   - Library: Radix UI Dialog
   - Overlay: Semi-transparent dark background
   - Sizes: Small (400px), Medium (600px), Large (800px), Full

6. **Tabs**
   - Horizontal tabs for project detail sections
   - Active state: Blue underline + bold text

7. **Badge**
   - Status indicators (Draft, Active, Completed)
   - Color-coded by status
   - Rounded corners (rounded-full)

8. **Progress Bar**
   - Linear progress (Shadcn Progress component)
   - Used for loading states, completion %

9. **Charts**
   - Library: Recharts
   - Types: Line, Bar, Pie, Area, Scatter, Sankey (Nivo)
   - Responsive: Scale to container width

10. **Map**
    - Library: MapLibre GL
    - Markers: Custom SVG icons
    - Popups: Project info on click

---

### Responsive Design

**Mobile-First Approach:**

**Breakpoints:**
- Mobile: < 640px (1 column, stacked layout)
- Tablet: 640px - 1024px (2 columns where appropriate)
- Desktop: 1024px+ (3-4 columns, full layout)

**Mobile Adaptations:**
- Sidebar filters → Bottom sheet drawer
- Grid view → List view (easier scrolling)
- Charts → Simplified versions or horizontal scroll
- Tables → Card-based mobile view
- Navigation → Hamburger menu

**Example:**
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* KPI Cards - 1 col mobile, 2 col tablet, 4 col desktop */}
</div>
```

---

### Accessibility (WCAG 2.1 AA)

**Requirements:**
1. **Keyboard Navigation** - All interactive elements accessible via Tab, Enter, Space, Arrow keys
2. **Screen Reader Support** - Proper ARIA labels, roles, live regions
3. **Color Contrast** - 4.5:1 minimum for text, 3:1 for large text
4. **Focus Indicators** - Visible focus rings (ring-2 ring-blue-500)
5. **Form Labels** - All inputs have associated labels
6. **Error Messages** - Descriptive, linked to inputs
7. **Alt Text** - All images have descriptive alt attributes
8. **Semantic HTML** - Proper heading hierarchy (h1 → h6)

**Testing:**
- Use axe DevTools browser extension
- Lighthouse accessibility score: 90+
- Test with screen reader (NVDA, JAWS, VoiceOver)

---

## Technical Stack & Integration

### Frontend Stack

**Framework:** Next.js 14 (App Router)
- **Why:** React-based, excellent performance, built-in API routes, great developer experience
- **Version:** 14.x (App Router for file-based routing)

**Language:** TypeScript
- **Why:** Type safety, better IDE support, fewer runtime errors

**Styling:** Tailwind CSS + Shadcn/ui
- **Why:** Utility-first, rapid development, consistent design system

**State Management:**
- React Query (TanStack Query) for server state
- Zustand for client state (if needed)

**Form Handling:** React Hook Form + Zod
- **Why:** Performant, great validation, TypeScript support

**Charts:** Recharts (primary) + Nivo (Sankey diagrams)
- **Why:** React-native, simple API, responsive

**Maps:** MapLibre GL
- **Why:** Open-source, high-performance, Mapbox-compatible

---

### Backend/Database

**Database:** Supabase (PostgreSQL)
- **URL:** https://abhnlhbkmrozxtfoaxnv.supabase.co
- **Features:** REST API, Realtime subscriptions, Row Level Security (RLS), Auth

**Vector Search:** Pinecone
- **Index:** infraflow-documents
- **Dimension:** 1536 (OpenAI text-embedding-ada-002)
- **Use Case:** Semantic project search

**AI APIs:**
- **Claude Sonnet 4** (Anthropic) - Document analysis, memo generation, Q&A
- **GPT-4** (OpenAI) - Embeddings, structured data extraction

**File Storage:** Supabase Storage
- **Bucket:** project-documents
- **Access:** Authenticated users only

---

### API Endpoints (Supabase REST)

**Projects:**
```
GET    /rest/v1/projects                    - List all projects
GET    /rest/v1/projects?id=eq.{id}         - Get single project
POST   /rest/v1/projects                    - Create project
PATCH  /rest/v1/projects?id=eq.{id}         - Update project
DELETE /rest/v1/projects?id=eq.{id}         - Delete project

# Filtering
GET /rest/v1/projects?country=eq.Egypt               - Filter by country
GET /rest/v1/projects?sector=eq.green_hydrogen       - Filter by sector
GET /rest/v1/projects?total_value=gte.1000000000     - Filter by value
GET /rest/v1/projects?status=in.(draft,active)       - Multiple values

# Sorting
GET /rest/v1/projects?order=total_value.desc         - Sort by value

# Pagination
GET /rest/v1/projects?limit=20&offset=0              - Page 1
GET /rest/v1/projects?limit=20&offset=20             - Page 2

# Search (full-text)
GET /rest/v1/projects?name=ilike.*hydrogen*          - Keyword search
```

**Documents:**
```
GET    /rest/v1/documents?project_id=eq.{id}  - Get project documents
POST   /rest/v1/documents                     - Upload document metadata
DELETE /rest/v1/documents?id=eq.{id}          - Delete document

# File upload (Supabase Storage)
POST /storage/v1/object/project-documents/{file_path}
```

**Financial Models:**
```
GET    /rest/v1/financial_models?project_id=eq.{id}  - Get models
POST   /rest/v1/financial_models                     - Create model
PATCH  /rest/v1/financial_models?id=eq.{id}          - Update model
```

**Risk Assessments:**
```
GET    /rest/v1/risk_assessments?project_id=eq.{id}
POST   /rest/v1/risk_assessments
PATCH  /rest/v1/risk_assessments?id=eq.{id}
```

**Compliance Checks:**
```
GET    /rest/v1/compliance_checks?project_id=eq.{id}
POST   /rest/v1/compliance_checks
PATCH  /rest/v1/compliance_checks?id=eq.{id}
```

---

### Custom API Routes (Next.js)

**AI Services:**
```
POST /api/ai/analyze-document
Body: { documentUrl: string, projectId: string }
Returns: { summary: string, keyFindings: object, redFlags: array }

POST /api/ai/generate-memo
Body: { projectId: string, template: string }
Returns: { memo: string }

POST /api/ai/chat
Body: { projectId: string, question: string }
Returns: { answer: string, sources: array }
```

**Semantic Search:**
```
POST /api/search/semantic
Body: { query: string, filters: object }
Returns: { projects: array, scores: array }

Implementation:
1. Generate embedding: OpenAI API
2. Query Pinecone: index.query({ vector, topK: 10 })
3. Fetch full projects: Supabase
4. Return merged results
```

**Export Services:**
```
POST /api/export/investment-memo
Body: { projectId: string, format: 'pdf' | 'docx' }
Returns: File download

POST /api/export/financial-model
Body: { projectId: string }
Returns: Excel file with formulas
```

---

## Database Schema & API Endpoints

### Core Tables (Already in Supabase)

#### 1. `projects` Table
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  sponsor TEXT,
  country TEXT NOT NULL,
  sector TEXT NOT NULL,  -- green_hydrogen, renewable_energy, water, other
  total_value NUMERIC,   -- in USD
  dfi_partners JSONB DEFAULT '[]'::jsonb,  -- Array of DFI names
  status TEXT NOT NULL,  -- draft, active, analyzed, completed, archived
  risk_score DOUBLE PRECISION,
  user_id UUID REFERENCES users(id),
  metadata JSONB DEFAULT '{}'::jsonb,  -- Flexible field for extra data
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_projects_country ON projects(country);
CREATE INDEX idx_projects_sector ON projects(sector);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_metadata ON projects USING gin(metadata);
```

**Key Metadata Fields (stored in `metadata` JSONB):**
```json
{
  "location": "NEOM, Saudi Arabia",
  "timeline": "2020-2026",
  "capacity_tons_per_year": 219000,
  "investment_usd": 8400000000,
  "technology": {
    "electrolyzer": "PEM / Alkaline",
    "renewable": "Wind 1.6GW + Solar 2.2GW"
  },
  "partners": ["ACWA Power", "Air Products", "NEOM"],
  "source_url": "https://acwapower.com/...",
  "description": "World's largest green hydrogen project..."
}
```

#### 2. `users` Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  organization TEXT,  -- DFI name or developer company
  role TEXT,  -- admin, analyst, user, viewer
  is_active BOOLEAN DEFAULT true,
  preferences JSONB DEFAULT '{}'::jsonb,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3. `documents` Table
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  file_path TEXT NOT NULL,  -- Supabase Storage path
  file_type TEXT,  -- pdf, xlsx, docx, pptx
  file_size INTEGER,  -- bytes
  document_type TEXT,  -- financial, legal, technical, esg, commercial
  ai_processed BOOLEAN DEFAULT false,
  ai_summary TEXT,
  extracted_data JSONB DEFAULT '{}'::jsonb,
  uploaded_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_documents_project ON documents(project_id);
```

#### 4. `financial_models` Table
```sql
CREATE TABLE financial_models (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  model_name TEXT DEFAULT 'Base Case',
  discount_rate DOUBLE PRECISION,  -- e.g., 0.10 for 10%
  npv NUMERIC,
  irr DOUBLE PRECISION,
  payback_period DOUBLE PRECISION,  -- years
  dscr DOUBLE PRECISION,  -- debt service coverage ratio
  scenarios JSONB DEFAULT '{}'::jsonb,  -- { base: {}, upside: {}, downside: {} }
  assumptions JSONB DEFAULT '{}'::jsonb,  -- revenue, capex, opex assumptions
  cash_flows JSONB DEFAULT '{}'::jsonb,  -- yearly cash flow array
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_financial_project ON financial_models(project_id);
```

**Example `scenarios` JSONB:**
```json
{
  "base": {
    "revenue_growth": 0.03,
    "irr": 0.153,
    "npv": 1250000000
  },
  "upside": {
    "revenue_growth": 0.05,
    "irr": 0.198,
    "npv": 1850000000
  },
  "downside": {
    "revenue_growth": 0.01,
    "irr": 0.112,
    "npv": 650000000
  }
}
```

#### 5. `compliance_checks` Table
```sql
CREATE TABLE compliance_checks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  standard TEXT NOT NULL,  -- 'EBRD ESP 2024', 'IFC PS', 'EU Taxonomy', etc.
  category TEXT,  -- environmental, social, governance
  status TEXT DEFAULT 'pending',  -- pending, compliant, review, non_compliant
  score DOUBLE PRECISION,  -- 0-100
  issues JSONB DEFAULT '[]'::jsonb,  -- Array of issue objects
  recommendations JSONB DEFAULT '[]'::jsonb,
  evidence JSONB DEFAULT '[]'::jsonb,  -- Links to documents
  notes TEXT,
  checked_by UUID REFERENCES users(id),
  checked_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_compliance_project ON compliance_checks(project_id);
CREATE INDEX idx_compliance_standard ON compliance_checks(standard);
```

**Example `issues` JSONB:**
```json
[
  {
    "category": "IFC PS3",
    "severity": "medium",
    "description": "Water discharge standards unclear",
    "action_required": "Request detailed water management plan"
  }
]
```

#### 6. `risk_assessments` Table
```sql
CREATE TABLE risk_assessments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  risk_category TEXT NOT NULL,  -- credit, political, esg, market, construction, etc.
  risk_level TEXT,  -- low, medium, high, critical
  likelihood TEXT,  -- low, medium, high
  impact TEXT,  -- low, medium, high
  description TEXT,
  mitigations JSONB DEFAULT '[]'::jsonb,  -- Array of mitigation strategies
  residual_risk TEXT,  -- After mitigations
  red_flags JSONB DEFAULT '[]'::jsonb,  -- AI-detected red flags
  score DOUBLE PRECISION,  -- 0-10 risk score
  assessed_by UUID REFERENCES users(id),
  assessed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_risk_project ON risk_assessments(project_id);
CREATE INDEX idx_risk_category ON risk_assessments(risk_category);
```

#### 7. `stakeholders` Table
```sql
CREATE TABLE stakeholders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  organization TEXT,
  role TEXT,  -- sponsor, lender, developer, contractor, offtaker, etc.
  email TEXT,
  phone TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_stakeholders_project ON stakeholders(project_id);
```

#### 8. `reports` Table
```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  report_type TEXT NOT NULL,  -- investment_memo, risk_report, compliance_report
  title TEXT NOT NULL,
  content TEXT,  -- Markdown or HTML
  file_path TEXT,  -- If exported to PDF/DOCX
  generated_by UUID REFERENCES users(id),
  generated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reports_project ON reports(project_id);
CREATE INDEX idx_reports_type ON reports(report_type);
```

#### 9. `audit_log` Table
```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  action TEXT NOT NULL,  -- created, updated, deleted, viewed, exported
  resource_type TEXT NOT NULL,  -- project, document, report, etc.
  resource_id UUID,
  changes JSONB DEFAULT '{}'::jsonb,  -- Before/after values
  ip_address TEXT,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_resource ON audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_created ON audit_log(created_at DESC);
```

#### 10. `milestones` Table
```sql
CREATE TABLE milestones (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  due_date DATE,
  status TEXT DEFAULT 'pending',  -- pending, in_progress, completed, delayed
  completion_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_milestones_project ON milestones(project_id);
CREATE INDEX idx_milestones_due_date ON milestones(due_date);
```

---

### Supabase Client Setup

**Installation:**
```bash
npm install @supabase/supabase-js
```

**Configuration (`lib/supabase.ts`):**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Type-safe database types (optional but recommended)
export type Database = {
  public: {
    Tables: {
      projects: {
        Row: {
          id: string
          name: string
          sponsor: string | null
          country: string
          sector: string
          total_value: number | null
          dfi_partners: any
          status: string
          risk_score: number | null
          user_id: string | null
          metadata: any
          created_at: string
          updated_at: string
        }
        Insert: {
          // ...
        }
        Update: {
          // ...
        }
      }
      // ... other tables
    }
  }
}
```

**Usage Examples:**
```typescript
// Fetch all projects
const { data: projects, error } = await supabase
  .from('projects')
  .select('*')

// Fetch single project with related data
const { data: project } = await supabase
  .from('projects')
  .select(`
    *,
    documents (*),
    financial_models (*),
    risk_assessments (*),
    compliance_checks (*)
  `)
  .eq('id', projectId)
  .single()

// Insert new project
const { data, error } = await supabase
  .from('projects')
  .insert({
    name: 'New Project',
    country: 'Egypt',
    sector: 'green_hydrogen',
    status: 'draft'
  })
  .select()
  .single()

// Update project
const { data, error } = await supabase
  .from('projects')
  .update({ status: 'active' })
  .eq('id', projectId)

// Filter and sort
const { data } = await supabase
  .from('projects')
  .select('*')
  .eq('country', 'Egypt')
  .gte('total_value', 1000000000)
  .order('total_value', { ascending: false })
```

---

### Pinecone Integration

**Installation:**
```bash
npm install @pinecone-database/pinecone
npm install openai  # For embeddings
```

**Configuration (`lib/pinecone.ts`):**
```typescript
import { Pinecone } from '@pinecone-database/pinecone'
import { OpenAI } from 'openai'

const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY!
})

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!
})

const index = pinecone.index('infraflow-documents')

export async function semanticSearch(query: string, topK: number = 10) {
  // 1. Generate embedding for query
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: query
  })

  // 2. Query Pinecone
  const results = await index.query({
    vector: embedding.data[0].embedding,
    topK,
    includeMetadata: true
  })

  // 3. Return project IDs with scores
  return results.matches.map(match => ({
    projectId: match.id,
    score: match.score,
    metadata: match.metadata
  }))
}

export async function addProjectToIndex(projectId: string, projectData: any) {
  // Generate text representation of project
  const text = `
    ${projectData.name}
    ${projectData.country}
    ${projectData.sector}
    ${projectData.metadata?.description || ''}
  `.trim()

  // Generate embedding
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text
  })

  // Upsert to Pinecone
  await index.upsert([{
    id: projectId,
    values: embedding.data[0].embedding,
    metadata: {
      project_name: projectData.name,
      country: projectData.country,
      sector: projectData.sector
    }
  }])
}
```

---

## Development Phases

### Phase 1: MVP Foundation (Weeks 1-3)

**Goal:** Core dashboard with project browsing and basic filters

**Features:**
- [ ] Next.js project setup with Shadcn/ui
- [ ] Supabase client configuration
- [ ] Authentication (Supabase Auth)
- [ ] Dashboard home page with KPI cards
- [ ] Project list/grid view
- [ ] Basic search and filters (country, sector, status)
- [ ] Project detail page (Overview tab only)
- [ ] Responsive layout (mobile, tablet, desktop)

**Deliverables:**
- Users can browse 24 existing projects
- Users can filter by country, sector, status
- Users can view project details

**Success Criteria:**
- Dashboard loads in <2 seconds
- All 24 projects displayed correctly
- Filters work accurately

---

### Phase 2: AI-Powered Search & Analysis (Weeks 4-6)

**Goal:** Semantic search and basic AI features

**Features:**
- [ ] Pinecone semantic search integration
- [ ] Search bar with keyword + semantic matching
- [ ] AI project summary generation (Claude API)
- [ ] Document upload interface
- [ ] Document viewer (PDF/Excel)
- [ ] AI document Q&A (simple chatbot)

**Deliverables:**
- Users can search "green hydrogen in Middle East" and get relevant results
- Users can upload documents to projects
- Users can ask AI questions about project documents

**Success Criteria:**
- Semantic search returns relevant results (>80% accuracy)
- Document upload works for PDF, Excel, Word
- AI Q&A provides accurate answers

---

### Phase 3: Financial Analysis Tools (Weeks 7-9)

**Goal:** Financial modeling and scenario analysis

**Features:**
- [ ] Financial model data entry form
- [ ] DCF calculator (NPV, IRR, DSCR)
- [ ] Scenario analysis (base, upside, downside)
- [ ] Sensitivity analysis charts (Recharts)
- [ ] Cash flow waterfall (Sankey diagram with Nivo)
- [ ] Export financial model to Excel

**Deliverables:**
- Users can input financial assumptions and get calculated metrics
- Users can run 3 scenarios and compare results
- Users can visualize cash flows

**Success Criteria:**
- Calculations match Excel outputs
- Sensitivity charts update in real-time
- Excel export includes formulas

---

### Phase 4: Risk & Compliance (Weeks 10-12)

**Goal:** Risk assessment and compliance checking tools

**Features:**
- [ ] Risk assessment form (category, level, mitigations)
- [ ] Risk matrix visualization (heat map)
- [ ] AI red flag detection (Claude API analyzes project data)
- [ ] Compliance checker interface
- [ ] Multi-framework gap analysis (EBRD, IFC, EU Taxonomy)
- [ ] Compliance report generation

**Deliverables:**
- Users can log risks and visualize on matrix
- AI automatically detects potential red flags
- Users can check compliance against 5 frameworks

**Success Criteria:**
- Risk matrix updates in real-time
- AI identifies >80% of known risks
- Compliance reports are accurate

---

### Phase 5: Investment Memo Generator (Weeks 13-15)

**Goal:** AI-powered memo drafting and export

**Features:**
- [ ] Investment memo template selection
- [ ] AI memo generation (Claude API)
- [ ] Rich text editor for manual edits
- [ ] Export to PDF (pdfmake)
- [ ] Export to Word (docx library)
- [ ] Email draft integration

**Deliverables:**
- Users can generate first draft memo in 30 seconds
- Users can edit and finalize memo
- Users can export to PDF/Word

**Success Criteria:**
- Memos are 80% complete from AI draft
- Formatting is professional
- PDFs are print-ready

---

### Phase 6: Portfolio Analytics & Polish (Weeks 16-18)

**Goal:** Executive dashboards and production readiness

**Features:**
- [ ] Portfolio overview dashboard
- [ ] Aggregate charts (sector, country, risk)
- [ ] Portfolio metrics (AUM, avg IRR, risk distribution)
- [ ] Activity feed with real-time updates
- [ ] Notifications system
- [ ] User preferences and settings
- [ ] Performance optimization
- [ ] Accessibility audit
- [ ] Security hardening
- [ ] Deployment to production

**Deliverables:**
- Executive users can see portfolio at a glance
- Real-time updates (Supabase Realtime)
- Production-ready application

**Success Criteria:**
- Lighthouse score: 90+ (Performance, Accessibility, SEO)
- Load time <2 seconds
- Zero critical security vulnerabilities

---

## Success Metrics

### User Adoption Metrics

**Target (First 90 Days):**
- **Active Users:** 20+ DFI investment officers, 10+ developers
- **Projects Analyzed:** 100+ projects (including 24 existing)
- **Documents Processed:** 500+ documents uploaded
- **Investment Memos Generated:** 50+ memos

**Engagement:**
- Daily Active Users (DAU): 15+
- Weekly Active Users (WAU): 40+
- Average Session Duration: 20+ minutes
- Feature Adoption:
  - Semantic Search: 80% of users
  - AI Document Q&A: 60% of users
  - Financial Modeling: 70% of users
  - Compliance Checker: 90% of users
  - Memo Generator: 50% of users

---

### Business Impact Metrics

**Time Savings:**
- Due Diligence Time: 3 weeks → 3-5 days (70% reduction)
- Investment Memo Prep: 3-5 days → 1 day (70% reduction)
- Compliance Check: 2-3 days → 2 hours (95% reduction)

**Cost Savings:**
- Cost per Deal: $65K-128K saved (analyst time)
- Credit Loss Reduction: 20-40% (early risk detection)
- Operational Efficiency: 50% increase (automation)

**Revenue Impact (for DFIs):**
- Deal Flow Increase: 20-30% (faster processing enables more deals)
- Approval Rate: +10% (better-prepared deals)
- Portfolio IRR: +50-100 bps (better risk selection)

---

### Technical Performance Metrics

**Performance:**
- Page Load Time: <2 seconds (95th percentile)
- Time to Interactive (TTI): <3 seconds
- API Response Time: <500ms (median)
- Search Results: <1 second

**Reliability:**
- Uptime: 99.9% (3 minutes downtime/month max)
- Error Rate: <0.1%
- Data Accuracy: 99%+

**Security:**
- Zero data breaches
- OWASP Top 10 compliance
- SOC 2 readiness (if pursuing)

---

## Appendix

### NPM Package Recommendations

**Core:**
```json
{
  "next": "^14.0.0",
  "react": "^18.2.0",
  "typescript": "^5.0.0",
  "@supabase/supabase-js": "^2.38.0",
  "@pinecone-database/pinecone": "^1.1.0"
}
```

**UI Components:**
```json
{
  "@radix-ui/react-*": "latest",  // Accessible primitives
  "tailwindcss": "^3.3.0",
  "class-variance-authority": "^0.7.0",  // For Shadcn variants
  "clsx": "^2.0.0",
  "lucide-react": "^0.292.0"  // Icons
}
```

**Forms & Validation:**
```json
{
  "react-hook-form": "^7.48.0",
  "zod": "^3.22.0",
  "@hookform/resolvers": "^3.3.0"
}
```

**Data Fetching:**
```json
{
  "@tanstack/react-query": "^5.8.0",
  "axios": "^1.6.0"
}
```

**Charts & Visualization:**
```json
{
  "recharts": "^2.10.0",
  "@nivo/sankey": "^0.84.0",
  "maplibre-gl": "^3.6.0",
  "react-map-gl": "^7.1.0"
}
```

**Document Handling:**
```json
{
  "react-pdf": "^7.5.0",
  "pdfmake": "^0.2.9",
  "sheetjs": "^0.20.0",  // Excel
  "docx": "^8.5.0",  // Word
  "pptxgenjs": "^3.12.0"  // PowerPoint
}
```

**AI/ML:**
```json
{
  "@anthropic-ai/sdk": "^0.9.0",
  "openai": "^4.20.0"
}
```

---

### File Structure

```
infraflow-ai/
├── app/                          # Next.js 14 App Router
│   ├── (auth)/                  # Auth routes
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/             # Main app routes
│   │   ├── page.tsx            # Dashboard home
│   │   ├── projects/           # Projects module
│   │   │   ├── page.tsx        # List view
│   │   │   └── [id]/           # Detail pages
│   │   │       ├── page.tsx    # Overview
│   │   │       ├── financial/  # Financial tab
│   │   │       ├── risk/       # Risk tab
│   │   │       ├── compliance/ # Compliance tab
│   │   │       └── documents/  # Documents tab
│   │   ├── portfolio/          # Portfolio analytics
│   │   └── settings/           # User settings
│   ├── api/                     # API routes
│   │   ├── ai/                 # AI services
│   │   ├── search/             # Search endpoints
│   │   └── export/             # Export services
│   ├── layout.tsx               # Root layout
│   └── globals.css              # Global styles
├── components/                   # React components
│   ├── ui/                      # Shadcn/ui components
│   ├── dashboard/               # Dashboard-specific
│   ├── projects/                # Project components
│   ├── charts/                  # Chart components
│   └── shared/                  # Shared components
├── lib/                          # Utility libraries
│   ├── supabase.ts             # Supabase client
│   ├── pinecone.ts             # Pinecone client
│   ├── ai.ts                   # AI utilities
│   └── utils.ts                # General utilities
├── hooks/                        # Custom React hooks
│   ├── useProjects.ts
│   ├── useSearch.ts
│   └── useAuth.ts
├── types/                        # TypeScript types
│   ├── database.ts             # Supabase types
│   └── models.ts               # App models
├── public/                       # Static assets
├── .env.local                    # Environment variables
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

### Environment Variables

**Create `.env.local`:**
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://abhnlhbkmrozxtfoaxnv.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=sb_secret_sKMOGxOH23E9hlYz_v6wag_ToX2vpVI

# Pinecone
PINECONE_API_KEY=pcsk_5ok77S_...
PINECONE_INDEX_NAME=infraflow-documents

# OpenAI
OPENAI_API_KEY=sk-proj-h3qlrcNS9GhlVRfgn6Ja...

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-api03-whGVltDh4Kvz7y-fBcwNm...

# App Config
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

### Additional Resources

**Documentation:**
- [Next.js 14 Docs](https://nextjs.org/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Shadcn/ui](https://ui.shadcn.com/)
- [Recharts](https://recharts.org/)
- [Pinecone Docs](https://docs.pinecone.io/)

**Design References:**
- [DFI Platform UX Research](/home/claude-user/ai-consults-platform/00-pivot/DFI-Platform-UX-Research-Report.md)
- [DFI User Flows](/home/claude-user/ai-consults-platform/00-pivot/DFI-User-Flows-And-Wireframes.md)
- [Market Research](/home/claude-user/ai-consults-platform/00-pivot/infraflow-ai-market-research.md)
- [Technical Specification](/home/claude-user/ai-consults-platform/00-pivot/InfraFlow-AI-Technical-Specification.md)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-25
**Status:** Ready for Development
**GitHub:** https://github.com/nawsaafa/infraflow-ai
