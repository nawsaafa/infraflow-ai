# InfraFlow AI - Technical Specification & Feature Requirements

**Platform**: Infrastructure Finance Intelligence Platform
**Tech Stack**: Next.js 14, Supabase (PostgreSQL), Pinecone, OpenAI, Anthropic Claude
**Target Users**: DFI investment officers, project developers, risk analysts
**Date**: 2025-11-25

---

## Table of Contents

1. [Core Dashboard Features](#1-core-dashboard-features)
2. [AI/ML Tools Integration](#2-aiml-tools-integration)
3. [Data Visualization Tools](#3-data-visualization-tools)
4. [Document Management](#4-document-management)
5. [Export & Reporting](#5-export--reporting)
6. [Integration Requirements](#6-integration-requirements)
7. [Recommended NPM Packages](#7-recommended-npm-packages)
8. [API Endpoint Requirements](#8-api-endpoint-requirements)
9. [Database Schema Additions](#9-database-schema-additions)
10. [Third-Party Services](#10-third-party-services)
11. [Technical Feasibility Assessment](#11-technical-feasibility-assessment)

---

## 1. Core Dashboard Features

### 1.1 Project Discovery & Search

**Requirements**:
- Semantic search using vector embeddings
- Advanced filters (sector, geography, size, stage, risk level)
- Real-time search suggestions
- Saved search queries
- Search history tracking

**Technical Implementation**:
```typescript
// Semantic Search Architecture
- Pinecone for vector storage and similarity search
- OpenAI text-embedding-3-large for generating embeddings
- Supabase PostgreSQL for metadata filtering
- Hybrid search: Combine vector similarity + SQL filters
```

**Recommended Libraries**:
- `@pinecone-database/pinecone` (v2.0+)
- `openai` (v4.0+)
- `@supabase/supabase-js` (v2.39+)

**Key Features**:
- **Semantic Understanding**: Search "renewable energy projects in Africa" matches "solar power initiatives Kenya"
- **Metadata Filtering**: Combine semantic search with structured filters (budget range, timeline, risk score)
- **Relevance Scoring**: Rank results by semantic similarity + recency + user preferences

---

### 1.2 Document Upload & AI Analysis

**Supported Formats**:
- PDF (scanned and text-based)
- Excel (.xlsx, .xls)
- PowerPoint (.pptx)
- Word (.docx)
- Images (JPG, PNG for OCR)

**Processing Pipeline**:
```typescript
1. File Upload → Supabase Storage
2. Text Extraction → pdf-parse, mammoth, xlsx
3. OCR (if needed) → Tesseract.js
4. Chunking → LangChain text splitters
5. Embedding → OpenAI API
6. Vector Storage → Pinecone
7. Metadata → Supabase PostgreSQL
```

**Libraries**:
- `pdf-parse` (v1.1.1) - Text-based PDF extraction
- `tesseract.js` (v5.0+) - OCR for scanned documents
- `mammoth` (v1.6+) - DOCX to HTML/text
- `xlsx` (SheetJS v0.20+) - Excel parsing
- `langchain` (v0.1+) - Text chunking and processing

**AI Analysis Capabilities**:
- Financial metric extraction (IRR, NPV, payback period)
- Key date identification (milestones, deadlines)
- Party extraction (sponsors, lenders, contractors)
- Risk flag detection
- Compliance checking
- Auto-categorization

---

### 1.3 Financial Modeling Interface

**Core Models**:
- Discounted Cash Flow (DCF) calculator
- Scenario analysis (base, optimistic, pessimistic)
- Sensitivity analysis
- Monte Carlo simulations
- Debt service coverage ratios (DSCR)
- Project IRR calculations

**Technical Stack**:
- `financial` (Zero-dependency TypeScript library) - Core calculations
- `financejs` - Additional financial functions (IRR, NPV, PMT)
- Custom React components for model inputs
- Real-time calculation updates

**UI Components**:
```typescript
// Financial Model Components
- InputTable: Editable grid for cash flow assumptions
- ScenarioComparison: Side-by-side scenario analysis
- SensitivityChart: Tornado diagrams for variable impact
- WaterfallChart: Cash flow waterfall visualization
- MetricsSummary: Key output metrics dashboard
```

**Libraries**:
- `financial` (v0.3+) - Core financial calculations
- `financejs` (v4.1+) - Financial formulas
- `react-financial-charts` (v1.3+) - Financial charting
- `mathjs` (v12.0+) - Advanced mathematical operations

---

### 1.4 Compliance Checker

**Multi-Framework Assessment**:
- IFC Performance Standards (1-8)
- Equator Principles
- World Bank Environmental & Social Framework
- CDC Group Investment Standards
- Local regulatory requirements

**Features**:
- Automated compliance gap analysis
- Checklist generation per framework
- Document requirement tracking
- Non-compliance flagging
- Remediation recommendations

**Implementation**:
```typescript
// Compliance Engine
- Rule engine for framework requirements
- AI-powered document analysis (Claude/GPT-4)
- Compliance scoring algorithm
- Gap analysis reporting
- Automated checklist generation
```

**Data Structure**:
```sql
-- Compliance frameworks stored in PostgreSQL
compliance_frameworks (id, name, version, requirements_json)
compliance_assessments (project_id, framework_id, score, gaps_json)
compliance_documents (assessment_id, document_id, status, findings)
```

---

### 1.5 Risk Assessment Dashboard

**Risk Categories**:
- **Credit Risk**: Borrower creditworthiness, financial ratios, default probability
- **Political Risk**: Country risk ratings, political stability indices, currency risk
- **ESG Risk**: Environmental impact, social compliance, governance score
- **Market Risk**: Demand forecasts, commodity price sensitivity, competition
- **Execution Risk**: Construction delays, cost overruns, contractor capability

**Visualization**:
- Risk heatmaps (severity vs likelihood)
- Radar charts for multi-dimensional risk
- Trend analysis over time
- Risk score decomposition
- Scenario-based risk modeling

**ESG Scoring**:
- Integration with ESG data providers (LSEG, Sustainalytics)
- Custom ESG scoring algorithms
- Environmental metrics (carbon footprint, water usage)
- Social metrics (job creation, community impact)
- Governance metrics (board composition, transparency)

**Libraries**:
- Custom risk scoring engine
- Integration with external risk databases (World Bank, Moody's)
- Real-time country risk API feeds

---

### 1.6 Investment Memo Generator

**AI-Powered Drafting**:
- Executive summary generation
- Investment thesis formulation
- Risk section auto-population
- Financial analysis summary
- Compliance status overview

**Workflow**:
```typescript
1. Select project from database
2. Choose memo template (sector-specific)
3. AI analyzes all project documents via RAG
4. Generate draft sections using Claude/GPT-4
5. Human review and edit
6. Export to PDF/DOCX
```

**Template System**:
- Sector-specific templates (renewable energy, transport, water)
- Customizable section structure
- Version control for drafts
- Approval workflow

**Libraries**:
- `react-quill` (v2.0+) - Rich text editor
- `slate` (v0.103+) - Advanced text editing framework
- `@anthropic-ai/sdk` (v0.20+) - Claude API
- `openai` (v4.0+) - GPT-4 API

---

### 1.7 Portfolio Analytics

**Aggregated Metrics**:
- Total portfolio value and exposure
- Geographic diversification
- Sector allocation
- Risk concentration
- Performance trends (actual vs projected)

**Dashboard Views**:
- Portfolio overview (high-level KPIs)
- Drill-down by sector/geography/risk tier
- Performance attribution analysis
- Cash flow forecasting (portfolio level)
- Benchmark comparison

**Visualizations**:
- Geographic heatmaps
- Sector allocation pie/treemap charts
- Time-series performance charts
- Correlation matrices
- Risk-return scatter plots

---

### 1.8 Comparison Tools

**Features**:
- Side-by-side project comparison (up to 4 projects)
- Benchmark against sector averages
- Peer group analysis
- Historical performance comparison
- What-if scenario comparison

**Comparison Dimensions**:
- Financial metrics (IRR, NPV, payback)
- Risk scores
- ESG ratings
- Timeline to completion
- Sponsor experience
- Geographic/political risk

**UI Implementation**:
- Comparison table with highlighting (best/worst)
- Normalized metrics for fair comparison
- Spider/radar charts for multi-dimensional view
- Export comparison reports

---

## 2. AI/ML Tools Integration

### 2.1 Document Q&A (RAG System)

**Architecture**:
```typescript
// Retrieval-Augmented Generation Pipeline
1. User Query → Embed with OpenAI text-embedding-3-large
2. Vector Search → Pinecone similarity search (top-k=10)
3. Metadata Filtering → Supabase filter by project/document type
4. Reranking → Cohere rerank API (optional)
5. Context Assembly → Top 5 chunks + metadata
6. LLM Generation → Claude Sonnet 4 or GPT-4
7. Response with Citations → Show source documents/pages
```

**Implementation Best Practices**:
- **Chunking Strategy**: 1000 tokens with 200 token overlap
- **Metadata Tagging**: Document type, date, project ID, page number
- **Multi-modal Support**: Extract tables/charts as images, use GPT-4 Vision
- **Citation Tracking**: Return source document + page number with each answer
- **Conversation Memory**: Maintain chat history for follow-up questions

**Libraries**:
- `langchain` (v0.1+) - RAG orchestration
- `@pinecone-database/pinecone` (v2.0+) - Vector DB
- `@anthropic-ai/sdk` (v0.20+) - Claude API
- `openai` (v4.0+) - Embeddings + GPT-4

**Features**:
- Chat with individual documents
- Chat across entire project corpus
- Multi-document synthesis
- Comparative analysis queries
- Structured data extraction queries

---

### 2.2 Auto-Extraction

**Extraction Targets**:
- **Financial Metrics**: IRR, NPV, DSCR, loan terms, equity contributions
- **Key Dates**: Financial close, construction start/end, COD, repayment schedule
- **Parties**: Sponsors, lenders, contractors, offtakers, government entities
- **Project Details**: Capacity, location, technology, sector
- **Risk Factors**: Listed risks, mitigation measures

**Model Selection**:
- **GPT-4**: Best for complex logic and structured extraction
- **Claude Sonnet 4**: Superior for large documents, tables, vision
- **Gemini**: Fast, multimodal processing

**Implementation**:
```typescript
// Structured Extraction with Function Calling
const extractionSchema = {
  financial_metrics: { irr: number, npv: number, dscr: number },
  key_dates: { financial_close: date, cod: date },
  parties: [{ name: string, role: string, country: string }],
  risks: [{ category: string, description: string, severity: string }]
}

// Use OpenAI function calling or Claude tool use
const extracted = await extractFromDocument(doc, extractionSchema)
```

**Validation & Cleaning**:
- Post-processing with RegEx for date/number formats
- Cross-validation against known ranges (IRR 5-25% typical)
- Human-in-the-loop review for high-value fields
- Confidence scores for each extraction

**Libraries**:
- `openai` (v4.0+) - Function calling
- `@anthropic-ai/sdk` (v0.20+) - Tool use
- `zod` (v3.22+) - Schema validation

---

### 2.3 Red Flag Detection

**Categories**:
- **Financial Red Flags**: Unrealistic projections, poor debt coverage, weak sponsors
- **Risk Red Flags**: High political risk, unproven technology, lack of offtake agreements
- **Compliance Red Flags**: Missing permits, ESG violations, inadequate disclosures
- **Document Red Flags**: Inconsistencies between documents, outdated information, missing sections

**AI Detection Methods**:
```typescript
// Multi-stage Red Flag Detection
1. Rule-based checks (DSCR < 1.2, political risk score > 7)
2. Anomaly detection (outliers vs sector benchmarks)
3. LLM-powered semantic analysis (Claude reviews narratives)
4. Cross-document consistency checking
5. Temporal analysis (stale data flags)
```

**Output**:
- Severity classification (Critical, High, Medium, Low)
- Explanation and evidence
- Recommended actions
- Auto-generated risk mitigation suggestions

**Alert System**:
- Real-time notifications for critical flags
- Dashboard widget showing flag summary
- Drill-down to flag details and evidence
- Flag resolution workflow (acknowledge, remediate, dismiss)

---

### 2.4 Similar Project Recommendations

**Recommendation Engine**:
```typescript
// Hybrid Recommendation System
1. Content-based: Vector similarity of project descriptions
2. Collaborative: "Users who viewed X also viewed Y"
3. Metadata-based: Sector, geography, size, stage matching
4. Combined scoring: Weighted ensemble of above methods
```

**Features**:
- Show top 5-10 similar projects
- Explain similarity (e.g., "Similar sector and size")
- Filter by specific criteria (same geography, same sponsor)
- Learn from user interactions (clicks, saved projects)

**Use Cases**:
- Benchmarking against similar deals
- Learning from past similar projects
- Finding comparable precedents
- Portfolio diversification analysis

---

### 2.5 Auto-Completion of Forms/Templates

**Smart Forms**:
- Pre-fill fields based on uploaded documents
- Suggest values based on similar projects
- Validate inputs in real-time
- Flag missing required fields
- Auto-format dates, currencies, percentages

**Template System**:
- Investment committee memo template
- Due diligence checklist template
- Compliance assessment template
- Financial summary template

**Implementation**:
```typescript
// Form Auto-fill Logic
1. Identify form fields (name, type, description)
2. Search document corpus for matching data
3. Extract values using LLM structured outputs
4. Pre-populate form with confidence scores
5. User reviews and confirms/edits
```

**Libraries**:
- `react-hook-form` (v7.50+) - Form management
- `zod` (v3.22+) - Form validation
- `@tanstack/react-query` (v5.0+) - Data fetching

---

### 2.6 Summarization

**Summarization Types**:
- **Document Summary**: Executive summary of long reports (50 pages → 1 page)
- **Section Summary**: Key points from specific sections
- **Multi-document Summary**: Synthesize insights across multiple documents
- **Update Summary**: "What changed?" comparison of document versions

**Model Configuration**:
- Claude Opus 4.1 for long documents (200k context)
- GPT-4 Turbo for balanced performance
- Configurable summary length (brief, medium, detailed)

**Quality Controls**:
- Factual accuracy checks (no hallucinations)
- Key information preservation
- Citation of source sections
- Regenerate option if unsatisfactory

---

### 2.7 Multi-Language Support

**Supported Languages**:
- English (primary)
- French (common in African DFI context)
- Spanish (Latin America projects)
- Portuguese (Brazil, Lusophone Africa)
- Arabic (MENA region)

**Implementation**:
```typescript
// Multi-language Processing Pipeline
1. Language Detection → detect-language library
2. Translation → OpenAI GPT-4 or Google Translate API
3. Embedding → Multilingual embedding models (e.g., text-embedding-3-large supports 100+ languages)
4. Search → Cross-language semantic search
5. Response → Translate back to user's preferred language
```

**Features**:
- Auto-detect document language
- Translate queries for cross-language search
- Multilingual Q&A (ask in English, search Spanish docs)
- UI language switching
- Glossary for financial/technical terms

**Libraries**:
- `i18next` (v23.0+) - UI internationalization
- `react-i18next` (v14.0+) - React integration
- OpenAI GPT-4 for high-quality translation

---

## 3. Data Visualization Tools

### 3.1 Charting Libraries Comparison

| Library | Best For | Pros | Cons | Recommendation |
|---------|----------|------|------|----------------|
| **Recharts** | Standard charts, dashboards | Simple API, React-native, good docs | Limited customization, moderate performance | **PRIMARY CHOICE** for dashboards |
| **Nivo** | Rich, beautiful charts | Gorgeous defaults, D3 power, good motion | Learning curve, larger bundle | Use for showcase visualizations |
| **D3.js** | Custom, complex visualizations | Ultimate flexibility, community | Steep learning curve, verbose | Use for specialized charts (Sankey) |
| **Chart.js (react-chartjs-2)** | Beginners, quick charts | Simple, versatile, fast setup | Less React-idiomatic | Backup option |
| **Victory** | Mobile-first, animations | Great animations, touch support | Performance with large data | Consider for mobile app |
| **Apache ECharts** | Large datasets, financial charts | Performance, extensive chart types | Large bundle size | Use for advanced financial charts |

**Recommendation Strategy**:
```typescript
// Primary: Recharts for 80% of charts
import { LineChart, BarChart, PieChart, AreaChart } from 'recharts'

// Secondary: Nivo for specific beautiful charts
import { ResponsiveSankey } from '@nivo/sankey'
import { ResponsiveTreeMap } from '@nivo/treemap'

// Tertiary: D3.js for highly custom visualizations
import * as d3 from 'd3'
import { sankey } from 'd3-sankey'
```

---

### 3.2 Chart Types Needed

**Financial Charts**:
- **Line Charts**: Time-series (cash flows, IRR trends, portfolio value)
- **Bar Charts**: Comparative metrics (project performance, sector allocation)
- **Area Charts**: Stacked cash flows, cumulative metrics
- **Waterfall Charts**: Cash flow sources and uses
- **Combo Charts**: Actual vs projected (bars + line)

**Risk & Portfolio Charts**:
- **Heatmaps**: Risk matrix (likelihood vs impact), correlation matrix
- **Radar Charts**: Multi-dimensional risk profiles, ESG scores
- **Gauge Charts**: Risk scores (0-100), compliance percentage
- **Scatter Plots**: Risk-return analysis, portfolio positioning

**Geographic & Flow Charts**:
- **Maps**: Project locations, geographic concentration
- **Sankey Diagrams**: Cash flow waterfall, fund allocation flows
- **Treemaps**: Portfolio allocation (hierarchical), sector breakdown

**Timeline Charts**:
- **Gantt Charts**: Project milestones, construction timeline
- **Timeline**: Key dates, historical events

---

### 3.3 Map Libraries

| Library | Best For | Pricing | Recommendation |
|---------|----------|---------|----------------|
| **MapLibre GL** | Vector maps, performance, open-source | Free | **RECOMMENDED** (open-source Mapbox fork) |
| **Mapbox GL JS** | Advanced features, commercial support | Paid (free tier limited) | Use if budget allows |
| **Leaflet** | Simple maps, lightweight, plugins | Free | Backup for simple use cases |
| **Google Maps** | Familiar UX, street view | Paid ($200/month credit) | Avoid (expensive) |

**Implementation Choice**: **MapLibre GL JS**
```typescript
// MapLibre GL JS - Open-source, high-performance
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

// React wrapper
import Map, { Marker, Popup } from 'react-map-gl/maplibre'
```

**Features Needed**:
- Project location markers (color-coded by status/risk)
- Clustering for dense regions
- Popup info cards on marker click
- Heatmap overlay for geographic risk
- Custom basemap styling
- Drawing tools for region selection

**Libraries**:
- `react-map-gl` (v7.1+) - React wrapper for MapLibre
- `maplibre-gl` (v3.6+) - Core mapping library
- `@mapbox/mapbox-gl-draw` (v1.4+) - Drawing tools

---

### 3.4 Recommended Visualization Libraries

**Core Charting**:
```bash
npm install recharts@2.12.0 --save
npm install @nivo/core @nivo/sankey @nivo/treemap --save
npm install d3 d3-sankey --save
```

**Maps**:
```bash
npm install react-map-gl@7.1.7 --save
npm install maplibre-gl@3.6.2 --save
```

**Timeline**:
```bash
npm install react-gantt-chart --save
# OR
npm install vis-timeline --save
```

**Gauges & Specialized**:
```bash
npm install react-gauge-chart --save
npm install react-circular-progressbar --save
```

---

## 4. Document Management

### 4.1 PDF Viewers

**Comparison**:

| Library | Annotation | Collaboration | Mobile | Bundle Size | Recommendation |
|---------|------------|---------------|--------|-------------|----------------|
| **react-pdf** | No (DIY) | No | Yes | Small (45KB) | **RECOMMENDED** for viewing |
| **PDF.js** | Manual setup | No | Yes | Medium (500KB) | Underlying tech for react-pdf |
| **Nutrient (PSPDFKit)** | Yes (built-in) | Yes (real-time) | Yes | Large (5MB+) | Consider if budget allows |
| **react-pdf-viewer** | Plugins available | No | Yes | Small | Alternative to react-pdf |

**Decision**: **react-pdf** + custom annotation layer

```typescript
// PDF Viewer Implementation
import { Document, Page, pdfjs } from 'react-pdf'
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`

// Custom annotation layer (SVG overlay)
<div style={{ position: 'relative' }}>
  <Document file={pdfUrl}>
    <Page pageNumber={pageNumber} />
  </Document>
  <AnnotationLayer annotations={annotations} />
</div>
```

**Libraries**:
- `react-pdf` (v7.7+) - PDF rendering
- `pdf-lib` (v1.17+) - PDF manipulation (merge, annotate)
- Custom SVG annotation layer

---

### 4.2 Annotation Tools

**Features Needed**:
- Highlight text
- Add comments/notes
- Draw shapes (rectangle, arrow, circle)
- Sticky notes
- Freehand drawing
- Text annotations

**Implementation Strategy**:
```typescript
// Custom Annotation System
1. SVG Overlay Layer on PDF canvas
2. Mouse/touch event handlers for drawing
3. Annotation data structure:
   {
     id: string,
     type: 'highlight' | 'comment' | 'shape',
     page: number,
     coordinates: { x, y, width, height },
     content: string,
     author: userId,
     createdAt: timestamp
   }
4. Store in Supabase PostgreSQL
5. Real-time sync via Supabase Realtime
```

**Libraries**:
- `react-konva` (v18.2+) - Canvas/SVG drawing
- `fabric.js` (v6.0+) - Advanced drawing capabilities
- Custom SVG-based annotation system

---

### 4.3 Version Control

**Requirements**:
- Track document versions (v1, v2, v3...)
- Compare versions (diff view)
- Restore previous versions
- Version metadata (uploader, timestamp, change description)
- Version branching (optional: track approval workflows)

**Database Schema**:
```sql
CREATE TABLE document_versions (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  version_number INTEGER,
  file_url TEXT,
  file_size BIGINT,
  uploaded_by UUID REFERENCES users(id),
  uploaded_at TIMESTAMP,
  change_description TEXT,
  is_latest BOOLEAN DEFAULT false
);

CREATE INDEX idx_doc_versions ON document_versions(document_id, version_number DESC);
```

**Features**:
- Auto-versioning on upload (if file already exists)
- Manual version tagging ("Final", "Draft", "Approved")
- Version comparison UI (side-by-side PDF view)
- Download specific version
- Revert to previous version

---

### 4.4 Collaborative Editing Features

**Real-Time Collaboration**:
- Supabase Realtime for live updates
- Show active users viewing document
- Live cursor positions (optional)
- Real-time annotation sync
- Commenting and replies

**Architecture**:
```typescript
// Supabase Realtime Integration
const channel = supabase
  .channel(`document:${documentId}`)
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'annotations', filter: `document_id=eq.${documentId}` },
    (payload) => {
      // Update local annotation state
      updateAnnotations(payload.new)
    }
  )
  .on('presence', { event: 'sync' }, () => {
    // Show active users
    const users = channel.presenceState()
    updateActiveUsers(users)
  })
  .subscribe()
```

**Features**:
- Presence indicators (who's viewing)
- Live annotation updates (< 100ms latency)
- Comment threads with replies
- @mentions in comments
- Notification system for new comments
- Activity feed (recent annotations)

**Libraries**:
- `@supabase/supabase-js` (v2.39+) - Realtime subscriptions
- `zustand` (v4.5+) - Client-side state management
- `react-query` (v5.0+) - Server state caching

**Performance**:
- Supabase Broadcast: 224,000 messages/sec, 6ms median latency
- Significantly faster than Firebase (1,500ms round-trip)

---

### 4.5 Document Comparison

**Use Cases**:
- Compare two versions of same document
- Track changes between versions
- Highlight added/deleted/modified content

**Text-based Documents**:
- Use diff algorithms (Myers, Patience)
- Highlight insertions (green), deletions (red), modifications (yellow)
- Libraries: `diff`, `diff-match-patch`

**PDF Comparison**:
- Extract text from both PDFs
- Run diff algorithm on extracted text
- Render side-by-side with highlighted changes
- Visual diff: overlay PDFs with color-coded changes

**Libraries**:
- `diff` (v5.2+) - Text diffing
- `diff-match-patch` (v1.0+) - Smart diff algorithm
- `react-diff-viewer` (v3.1+) - Visual diff UI

**Implementation**:
```typescript
import { diffLines } from 'diff'
import ReactDiffViewer from 'react-diff-viewer-continued'

const changes = diffLines(oldText, newText)
<ReactDiffViewer
  oldValue={oldDocument}
  newValue={newDocument}
  splitView={true}
  showDiffOnly={false}
/>
```

---

## 5. Export & Reporting

### 5.1 PDF Reports (Investment Memos)

**Requirements**:
- Professional formatting (headers, footers, page numbers)
- Tables and charts
- Custom branding (logo, colors)
- Multi-page documents
- Table of contents
- Appendices

**Library Comparison**:

| Library | Complexity | Layout Control | Tables | Charts | Recommendation |
|---------|------------|----------------|--------|--------|----------------|
| **pdfmake** | Medium | Excellent | Excellent | Images only | **RECOMMENDED** for structured reports |
| **jsPDF** | Low | Good | Manual | Manual | Backup for simple PDFs |
| **@react-pdf/renderer** | Medium | Good (React) | Good | Via images | Good for React-heavy apps |
| **Puppeteer/Playwright** | High | Excellent (HTML→PDF) | Excellent | Excellent | Overkill, slow |

**Decision**: **pdfmake**

**Implementation**:
```typescript
import pdfMake from 'pdfmake/build/pdfmake'
import pdfFonts from 'pdfmake/build/vfs_fonts'
pdfMake.vfs = pdfFonts.pdfMake.vfs

// Document Definition (JSON structure)
const docDefinition = {
  pageSize: 'A4',
  pageMargins: [40, 60, 40, 60],
  header: { text: 'Investment Memo', style: 'header' },
  footer: (currentPage, pageCount) => ({ text: `Page ${currentPage} of ${pageCount}`, alignment: 'center' }),
  content: [
    { text: 'Executive Summary', style: 'sectionHeader' },
    { text: '...', style: 'body' },
    { table: { body: [[...], [...]] } },
    { image: chartImageBase64, width: 500 }
  ],
  styles: {
    header: { fontSize: 18, bold: true },
    sectionHeader: { fontSize: 14, bold: true, margin: [0, 10, 0, 5] },
    body: { fontSize: 11 }
  }
}

pdfMake.createPdf(docDefinition).download('investment-memo.pdf')
```

**Chart Embedding**:
- Render chart to canvas using Recharts/Nivo
- Convert canvas to base64 image
- Embed image in PDF

**Libraries**:
- `pdfmake` (v0.2+)
- `html2canvas` (v1.4+) - Capture charts as images

---

### 5.2 Excel Exports (Financial Models)

**Requirements**:
- Multiple sheets (assumptions, cash flows, outputs)
- Formulas preserved (SUM, NPV, IRR calculations)
- Formatting (bold headers, currency, percentages)
- Charts embedded (optional)
- Conditional formatting

**Library**: **SheetJS (xlsx)**

**Implementation**:
```typescript
import * as XLSX from 'xlsx'

// Create workbook
const wb = XLSX.utils.book_new()

// Sheet 1: Assumptions
const assumptionsData = [
  ['Parameter', 'Value'],
  ['Discount Rate', 0.10],
  ['Project Life', 20],
  // ...
]
const ws1 = XLSX.utils.aoa_to_sheet(assumptionsData)
XLSX.utils.book_append_sheet(wb, ws1, 'Assumptions')

// Sheet 2: Cash Flow (with formulas)
const cashFlowData = [
  ['Year', 'Revenue', 'Costs', 'Net Cash Flow'],
  [1, 1000, 800, { f: 'B2-C2' }], // Formula
  [2, 1200, 850, { f: 'B3-C3' }],
  // ...
]
const ws2 = XLSX.utils.aoa_to_sheet(cashFlowData)

// Add cell formatting
ws2['B2'].z = '$#,##0.00' // Currency format
ws2['D2'].z = '0.0%' // Percentage format

XLSX.utils.book_append_sheet(wb, ws2, 'Cash Flow')

// Write file
XLSX.writeFile(wb, 'financial-model.xlsx')
```

**Advanced Features**:
- Conditional formatting (via xlsx-style or exceljs)
- Data validation (dropdowns)
- Frozen panes (header rows)
- Cell merging
- Password protection

**Libraries**:
- `xlsx` (SheetJS v0.20+) - Core Excel generation
- `exceljs` (v4.4+) - Alternative with more formatting options
- `file-saver` (v2.0+) - Trigger file download

**Best Practices**:
- Paginate large datasets (avoid 100k+ rows in one sheet)
- Use streaming for very large exports
- Optimize with Web Workers for heavy processing

---

### 5.3 PowerPoint Presentations (Executive Summaries)

**Requirements**:
- Title slide, content slides, charts
- Consistent branding (theme, colors, fonts)
- Tables and bullet points
- Image/chart embedding
- Speaker notes

**Library**: **PptxGenJS**

**Implementation**:
```typescript
import pptxgen from 'pptxgenjs'

const pptx = new pptxgen()

// Define master slide/theme
pptx.defineLayout({ name: 'LAYOUT_16x9', width: 10, height: 5.625 })
pptx.layout = 'LAYOUT_16x9'

// Title Slide
const slide1 = pptx.addSlide()
slide1.addText('Investment Opportunity: Solar Project Kenya', {
  x: 1, y: 1, fontSize: 28, bold: true, color: '363636'
})
slide1.addText('InfraFlow AI Analysis', {
  x: 1, y: 2, fontSize: 18, color: '666666'
})

// Content Slide with Chart
const slide2 = pptx.addSlide()
slide2.addText('Financial Projections', { x: 0.5, y: 0.5, fontSize: 24, bold: true })

// Embed chart as image
slide2.addImage({ path: chartImageBase64, x: 1, y: 1.5, w: 8, h: 4 })

// Table
slide2.addTable([
  ['Metric', 'Value'],
  ['IRR', '15.2%'],
  ['NPV', '$45M'],
], { x: 1, y: 1, w: 5, h: 2, fontSize: 12 })

// Export
pptx.writeFile({ fileName: 'executive-summary.pptx' })
```

**Libraries**:
- `pptxgenjs` (v3.12+)
- `html2canvas` (v1.4+) - Capture charts

---

### 5.4 API Access for Integrations

**REST API Endpoints**:
```
GET    /api/projects - List projects
GET    /api/projects/:id - Get project details
POST   /api/projects - Create project
PUT    /api/projects/:id - Update project
DELETE /api/projects/:id - Delete project

GET    /api/documents/:id/download - Download document
POST   /api/documents/upload - Upload document
GET    /api/documents/:id/analysis - Get AI analysis

GET    /api/search?q={query} - Semantic search
POST   /api/chat - Document Q&A chat
POST   /api/extract - Extract structured data
POST   /api/analyze-risk - Risk assessment

GET    /api/portfolio/analytics - Portfolio metrics
POST   /api/reports/generate - Generate report (PDF/Excel/PPTX)
```

**Authentication**:
- JWT-based authentication
- API key for programmatic access
- Rate limiting (100 requests/minute per user)

**Webhooks**:
- Document processing complete
- Risk flag detected
- Compliance check failed
- New similar project available

**Libraries**:
- Next.js API Routes (built-in)
- `next-auth` (v4.24+) - Authentication
- `@upstash/ratelimit` (v1.0+) - Rate limiting

---

## 6. Integration Requirements

### 6.1 Email (Deal Flow Notifications)

**Use Cases**:
- New project uploaded → notify team
- Risk flag detected → alert analysts
- Compliance check failed → email compliance officer
- Document processing complete → notify uploader
- Weekly digest of portfolio performance

**Implementation**:
```typescript
// Email Service Options
1. Resend (recommended - developer-friendly, React email templates)
2. SendGrid (enterprise-grade, high deliverability)
3. AWS SES (cost-effective, requires setup)
```

**Recommended**: **Resend**

```typescript
import { Resend } from 'resend'
import { EmailTemplate } from '@/components/emails/RiskAlertEmail'

const resend = new Resend(process.env.RESEND_API_KEY)

await resend.emails.send({
  from: 'InfraFlow <noreply@infraflow.ai>',
  to: ['analyst@dfi.org'],
  subject: 'Risk Alert: Solar Project Kenya',
  react: EmailTemplate({ projectName, riskDetails })
})
```

**Email Templates** (React Email):
- Risk alerts
- Document processing status
- Weekly portfolio digest
- Compliance notifications

**Libraries**:
- `resend` (v3.0+) - Email API
- `react-email` (v2.0+) - Email templates
- `@react-email/components` (v0.0.14+) - Email UI components

---

### 6.2 Calendar (Milestone Tracking)

**Integration Options**:
- Google Calendar API
- Microsoft Outlook Calendar
- Apple Calendar (CalDAV)
- iCal file generation

**Use Cases**:
- Sync project milestones to team calendar
- Financial close deadlines
- Compliance deadline reminders
- Construction milestone events

**Implementation**:
```typescript
import { google } from 'googleapis'

const calendar = google.calendar({ version: 'v3', auth: oauth2Client })

await calendar.events.insert({
  calendarId: 'primary',
  requestBody: {
    summary: 'Financial Close: Solar Project Kenya',
    description: 'Expected financial close for 50MW solar project',
    start: { dateTime: '2025-06-15T09:00:00', timeZone: 'UTC' },
    end: { dateTime: '2025-06-15T10:00:00', timeZone: 'UTC' },
    reminders: {
      useDefault: false,
      overrides: [
        { method: 'email', minutes: 24 * 60 }, // 1 day before
        { method: 'popup', minutes: 60 }
      ]
    }
  }
})
```

**Alternative**: Generate `.ics` files (universal calendar format)

**Libraries**:
- `googleapis` (v133.0+) - Google Calendar API
- `ical-generator` (v7.0+) - Generate .ics files
- `@microsoft/microsoft-graph-client` (v3.0+) - Outlook Calendar

---

### 6.3 Slack/Teams (Collaboration)

**Use Cases**:
- New project notifications in #deal-flow channel
- Risk alerts in #risk-committee channel
- Document processing status updates
- Chat with AI bot in Slack

**Slack Integration**:
```typescript
import { WebClient } from '@slack/web-api'

const slack = new WebClient(process.env.SLACK_BOT_TOKEN)

await slack.chat.postMessage({
  channel: '#deal-flow',
  text: 'New project uploaded: Solar Project Kenya',
  blocks: [
    {
      type: 'section',
      text: { type: 'mrkdwn', text: '*New Project: Solar Project Kenya*\n50MW solar plant, $75M total cost\nIRR: 15.2% | Risk Score: 6.5/10' }
    },
    {
      type: 'actions',
      elements: [
        { type: 'button', text: { type: 'plain_text', text: 'View Details' }, url: 'https://app.infraflow.ai/projects/123' }
      ]
    }
  ]
})
```

**Microsoft Teams Integration**:
```typescript
// Incoming Webhook
await fetch(process.env.TEAMS_WEBHOOK_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    '@type': 'MessageCard',
    title: 'New Project: Solar Project Kenya',
    text: '50MW solar plant, $75M total cost',
    potentialAction: [
      { '@type': 'OpenUri', name: 'View Details', targets: [{ os: 'default', uri: 'https://app.infraflow.ai/projects/123' }] }
    ]
  })
})
```

**Libraries**:
- `@slack/web-api` (v7.0+) - Slack API
- `@microsoft/teams-js` (v2.19+) - Teams integration
- Webhooks (simplest approach for notifications)

---

### 6.4 Excel/Google Sheets (Import/Export)

**Import from Excel/Sheets**:
- Upload Excel file, parse with SheetJS
- Map columns to project fields
- Bulk import projects
- Validation and error reporting

**Export to Excel**: (See Section 5.2)

**Google Sheets Integration**:
```typescript
import { google } from 'googleapis'

const sheets = google.sheets({ version: 'v4', auth: oauth2Client })

// Read from Google Sheets
const response = await sheets.spreadsheets.values.get({
  spreadsheetId: 'SHEET_ID',
  range: 'Sheet1!A1:Z1000'
})
const rows = response.data.values

// Write to Google Sheets
await sheets.spreadsheets.values.update({
  spreadsheetId: 'SHEET_ID',
  range: 'Sheet1!A1',
  valueInputOption: 'RAW',
  requestBody: { values: [[...], [...]] }
})
```

**Use Cases**:
- Export portfolio analytics to Google Sheets for further analysis
- Import project data from Excel template
- Sync financial models bidirectionally
- Collaborative editing in Sheets, sync to InfraFlow

**Libraries**:
- `xlsx` (v0.20+) - Excel parsing
- `googleapis` (v133.0+) - Google Sheets API

---

### 6.5 Existing DFI Systems

**Common DFI Systems**:
- **SAP**: Enterprise resource planning (financial, HR, procurement)
- **Salesforce**: CRM (deal pipeline, client relationships)
- **SharePoint**: Document management
- **Oracle Financials**: Accounting, budgeting
- **Custom internal systems**: Legacy deal tracking databases

**Integration Approaches**:
1. **API Integration**: If DFI has REST/SOAP APIs, direct integration
2. **File-based**: Periodic CSV/Excel exports/imports
3. **Database replication**: Read-only access to DFI databases (if permissible)
4. **RPA (Robotic Process Automation)**: Automate manual data entry between systems
5. **Middleware**: Use integration platform (Zapier, n8n, MuleSoft)

**Data Sync**:
- Projects: One-way sync (DFI → InfraFlow)
- Documents: Bidirectional (upload in InfraFlow, mirror to SharePoint)
- Analytics: One-way (InfraFlow → DFI reporting)

**Security & Compliance**:
- SSO integration (SAML, OAuth)
- Data encryption in transit and at rest
- Audit logs for all data access
- Compliance with DFI data policies

**Libraries**:
- `jsforce` (v2.0+) - Salesforce integration
- `node-soap` (v1.0+) - SOAP API client
- Custom connectors per DFI system

---

## 7. Recommended NPM Packages

### 7.1 Core Framework & Infrastructure

```bash
# Next.js 14 with TypeScript
npm install next@14.1.0 react@18.2.0 react-dom@18.2.0
npm install -D typescript@5.3.3 @types/react@18.2.48 @types/node@20.11.5

# Supabase
npm install @supabase/supabase-js@2.39.7 @supabase/ssr@0.1.0

# Pinecone
npm install @pinecone-database/pinecone@2.0.1

# AI/ML APIs
npm install openai@4.28.0 @anthropic-ai/sdk@0.20.1
```

---

### 7.2 Data Visualization

```bash
# Charting
npm install recharts@2.12.0
npm install @nivo/core@0.85.1 @nivo/sankey@0.85.1 @nivo/treemap@0.85.1
npm install d3@7.8.5 d3-sankey@0.12.3

# Maps
npm install react-map-gl@7.1.7 maplibre-gl@3.6.2

# Gauges & Specialized
npm install react-circular-progressbar@2.1.0
npm install react-gauge-chart@0.4.1
```

---

### 7.3 Document Management

```bash
# PDF
npm install react-pdf@7.7.0 pdf-lib@1.17.1 pdfjs-dist@3.11.174
npm install pdf-parse@1.1.1

# OCR
npm install tesseract.js@5.0.4

# DOCX/XLSX
npm install mammoth@1.6.0
npm install xlsx@0.20.1

# Document Processing
npm install langchain@0.1.25
```

---

### 7.4 Export & Reporting

```bash
# PDF Generation
npm install pdfmake@0.2.10

# Excel Export
npm install xlsx@0.20.1 file-saver@2.0.5

# PowerPoint
npm install pptxgenjs@3.12.0

# Chart to Image
npm install html2canvas@1.4.1
```

---

### 7.5 Forms & UI Components

```bash
# Forms
npm install react-hook-form@7.50.1 zod@3.22.4 @hookform/resolvers@3.3.4

# UI Components
npm install @radix-ui/react-dialog@1.0.5
npm install @radix-ui/react-dropdown-menu@2.0.6
npm install @radix-ui/react-select@2.0.0
npm install @headlessui/react@1.7.18

# Rich Text Editor
npm install react-quill@2.0.0 quill@1.3.7

# Tables
npm install @tanstack/react-table@8.12.0
```

---

### 7.6 State Management & Data Fetching

```bash
# State Management
npm install zustand@4.5.0

# Data Fetching
npm install @tanstack/react-query@5.20.1 axios@1.6.7

# Real-time
npm install @supabase/supabase-js@2.39.7 # (includes Realtime)
```

---

### 7.7 Authentication & Security

```bash
# Authentication
npm install next-auth@4.24.6

# Rate Limiting
npm install @upstash/ratelimit@1.0.1 @upstash/redis@1.28.2

# Validation
npm install zod@3.22.4
```

---

### 7.8 Utilities

```bash
# Date/Time
npm install date-fns@3.3.1

# Formatting
npm install numeral@2.0.6

# File Upload
npm install react-dropzone@14.2.3

# Notifications
npm install react-hot-toast@2.4.1

# Icons
npm install lucide-react@0.323.0

# Styling
npm install tailwindcss@3.4.1 autoprefixer@10.4.17 postcss@8.4.35
```

---

### 7.9 Financial Calculations

```bash
npm install financial@0.3.1
npm install financejs@4.1.0
npm install mathjs@12.3.2
```

---

### 7.10 Internationalization

```bash
npm install i18next@23.8.2 react-i18next@14.0.5
```

---

### 7.11 Email & Integrations

```bash
# Email
npm install resend@3.2.0 react-email@2.1.0

# Calendar
npm install googleapis@133.0.0 ical-generator@7.0.0

# Slack
npm install @slack/web-api@7.0.2

# Diff/Comparison
npm install diff@5.2.0 react-diff-viewer-continued@3.3.1
```

---

### 7.12 Testing (Recommended)

```bash
npm install -D vitest@1.2.2 @testing-library/react@14.2.1
npm install -D @playwright/test@1.41.2
npm install -D eslint@8.56.0 prettier@3.2.5
```

---

## 8. API Endpoint Requirements

### 8.1 Project Management

```typescript
// GET /api/projects
// Query params: page, limit, sector, geography, status, minRiskScore, maxRiskScore
{
  projects: [
    {
      id: string,
      name: string,
      sector: string,
      geography: { country: string, region: string },
      totalCost: number,
      status: 'pipeline' | 'diligence' | 'approved' | 'active' | 'completed',
      riskScore: number,
      irr: number,
      createdAt: timestamp
    }
  ],
  pagination: { page: number, totalPages: number, totalCount: number }
}

// GET /api/projects/:id
{
  project: {
    id, name, description, sector, geography,
    financials: { totalCost, debtEquityRatio, irr, npv, paybackPeriod },
    timeline: { financialClose, constructionStart, constructionEnd, cod },
    parties: [{ name, role, country }],
    risks: [{ category, description, severity, mitigationPlan }],
    documents: [{ id, name, type, uploadedAt, url }],
    complianceStatus: { framework: string, score: number, gaps: [] },
    esgScore: { environmental: number, social: number, governance: number, overall: number }
  }
}

// POST /api/projects
Body: { name, description, sector, geography, ... }
Response: { projectId, status: 'created' }

// PUT /api/projects/:id
Body: { updated fields }
Response: { status: 'updated' }

// DELETE /api/projects/:id
Response: { status: 'deleted' }
```

---

### 8.2 Document Management

```typescript
// POST /api/documents/upload
FormData: file, projectId, documentType
Response: { documentId, status: 'processing' | 'completed', processingJobId }

// GET /api/documents/:id
{
  document: {
    id, name, type, size, uploadedAt, uploadedBy,
    projectId, url, thumbnailUrl, pageCount,
    processingStatus: 'pending' | 'processing' | 'completed' | 'failed',
    extractedData: { financials: {}, keyDates: {}, parties: [] }
  }
}

// GET /api/documents/:id/download
Response: File stream

// DELETE /api/documents/:id
Response: { status: 'deleted' }

// GET /api/documents/:id/versions
Response: { versions: [{ versionNumber, uploadedAt, uploadedBy, changeDescription }] }

// POST /api/documents/:id/annotations
Body: { type, page, coordinates, content }
Response: { annotationId }

// GET /api/documents/:id/annotations
Response: { annotations: [{ id, type, page, coordinates, content, author, createdAt }] }
```

---

### 8.3 AI & Search

```typescript
// GET /api/search
Query: q (query string), filters (sector, geography, etc.), limit
Response: {
  results: [{ projectId, name, similarity, snippet, highlights }],
  totalResults: number,
  queryTime: number
}

// POST /api/chat
Body: { documentId, message, conversationId (optional) }
Response: {
  answer: string,
  sources: [{ documentId, page, snippet }],
  conversationId: string
}

// POST /api/extract
Body: { documentId, extractionSchema }
Response: {
  extractedData: { ... },
  confidence: { field1: 0.95, field2: 0.87 }
}

// POST /api/analyze-risk
Body: { projectId }
Response: {
  overallRiskScore: number,
  riskBreakdown: { credit: 7, political: 6, esg: 4, market: 5, execution: 6 },
  redFlags: [{ category, severity, description, evidence }],
  recommendations: [string]
}

// POST /api/summarize
Body: { documentId, summaryType: 'brief' | 'medium' | 'detailed' }
Response: { summary: string, keyPoints: [string] }

// GET /api/similar-projects/:id
Response: {
  similarProjects: [{ projectId, name, similarityScore, reason }]
}
```

---

### 8.4 Financial Modeling

```typescript
// POST /api/financial-models/dcf
Body: {
  assumptions: { discountRate, projectLife, taxRate },
  cashFlows: [{ year, revenue, opex, capex }]
}
Response: {
  npv: number,
  irr: number,
  paybackPeriod: number,
  discountedCashFlows: [{ year, dcf }]
}

// POST /api/financial-models/scenario-analysis
Body: {
  baseCase: { assumptions, cashFlows },
  optimistic: { adjustments },
  pessimistic: { adjustments }
}
Response: {
  scenarios: {
    base: { npv, irr, paybackPeriod },
    optimistic: { npv, irr, paybackPeriod },
    pessimistic: { npv, irr, paybackPeriod }
  }
}

// POST /api/financial-models/sensitivity
Body: {
  baseCase: { assumptions, cashFlows },
  sensitivityVariables: [{ variable: 'discountRate', range: [0.08, 0.12], steps: 5 }]
}
Response: {
  results: [{ variable, value, npv, irr }],
  tornadoChart: { variable, impact }
}
```

---

### 8.5 Compliance & ESG

```typescript
// POST /api/compliance/assess
Body: { projectId, frameworks: ['IFC', 'Equator'] }
Response: {
  assessments: [
    {
      framework: 'IFC',
      overallScore: 85,
      requirements: [{ id, name, status: 'met' | 'partial' | 'not_met', evidence: [documentId] }],
      gaps: [{ requirement, description, severity }]
    }
  ]
}

// GET /api/esg/score/:projectId
Response: {
  esgScore: {
    overall: 72,
    environmental: 68,
    social: 75,
    governance: 74,
    breakdown: {
      carbonFootprint: { score, value, unit },
      jobsCreated: { score, value },
      communityImpact: { score, description },
      boardDiversity: { score, value }
    }
  }
}
```

---

### 8.6 Portfolio Analytics

```typescript
// GET /api/portfolio/analytics
Response: {
  overview: {
    totalProjects: number,
    totalValue: number,
    avgIRR: number,
    totalCapitalDeployed: number
  },
  byGeography: [{ country, projectCount, totalValue }],
  bySector: [{ sector, projectCount, totalValue }],
  riskDistribution: [{ riskTier, count }],
  performanceTrends: [{ date, portfolioValue, avgIRR }]
}

// GET /api/portfolio/cash-flow-forecast
Query: timeHorizon (months)
Response: {
  forecast: [{ month, inflows, outflows, netCashFlow }],
  assumptions: string
}
```

---

### 8.7 Export & Reporting

```typescript
// POST /api/reports/generate
Body: {
  reportType: 'investment_memo' | 'executive_summary' | 'compliance_report',
  projectId: string,
  format: 'pdf' | 'docx' | 'pptx',
  sections: [string], // optional: customize sections
  template: string // optional: template ID
}
Response: {
  reportId: string,
  status: 'generating' | 'completed',
  downloadUrl: string (when completed)
}

// GET /api/reports/:id/status
Response: { status, progress, downloadUrl }

// POST /api/export/excel
Body: { projectId, includeFinancialModel: boolean }
Response: { downloadUrl }
```

---

### 8.8 Webhooks & Notifications

```typescript
// POST /api/webhooks/register
Body: {
  url: string,
  events: ['document.processed', 'risk.detected', 'compliance.failed'],
  secret: string
}
Response: { webhookId }

// POST /api/notifications/preferences
Body: { emailAlerts: boolean, slackAlerts: boolean, channels: ['#deal-flow'] }
Response: { status: 'updated' }
```

---

### 8.9 Authentication & User Management

```typescript
// POST /api/auth/login
Body: { email, password }
Response: { token (JWT), user: { id, name, email, role } }

// POST /api/auth/sso
Body: { samlToken }
Response: { token (JWT), user: { ... } }

// GET /api/users/me
Headers: Authorization: Bearer {token}
Response: { user: { id, name, email, role, organization, preferences } }

// PUT /api/users/me
Body: { updated preferences }
Response: { status: 'updated' }
```

---

## 9. Database Schema Additions

### 9.1 Projects Table (Enhanced)

```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  sector TEXT NOT NULL, -- 'renewable_energy', 'transport', 'water', etc.
  subsector TEXT, -- 'solar', 'wind', 'roads', 'ports', etc.
  geography JSONB NOT NULL, -- { country, region, coordinates }
  status TEXT NOT NULL DEFAULT 'pipeline', -- 'pipeline', 'diligence', 'approved', 'active', 'completed'

  -- Financial data
  total_cost DECIMAL(15, 2),
  debt_amount DECIMAL(15, 2),
  equity_amount DECIMAL(15, 2),
  currency TEXT DEFAULT 'USD',
  irr DECIMAL(5, 2),
  npv DECIMAL(15, 2),
  payback_period INTEGER, -- months

  -- Timeline
  financial_close_date DATE,
  construction_start_date DATE,
  construction_end_date DATE,
  commercial_operation_date DATE,

  -- Risk & Compliance
  risk_score DECIMAL(3, 1), -- 0-10
  esg_score DECIMAL(3, 1), -- 0-100
  compliance_score DECIMAL(3, 1), -- 0-100

  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  created_by UUID REFERENCES users(id),
  organization_id UUID REFERENCES organizations(id)
);

CREATE INDEX idx_projects_sector ON projects(sector);
CREATE INDEX idx_projects_geography ON projects USING gin(geography);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_risk_score ON projects(risk_score);
CREATE INDEX idx_projects_org ON projects(organization_id);
```

---

### 9.2 Documents Table

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  file_path TEXT NOT NULL, -- Supabase Storage path
  file_size BIGINT,
  file_type TEXT, -- 'pdf', 'xlsx', 'docx', 'pptx'
  mime_type TEXT,

  -- Processing status
  processing_status TEXT DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
  processing_error TEXT,

  -- Extracted metadata
  page_count INTEGER,
  language TEXT,
  extracted_text TEXT, -- Full text for search

  -- Embeddings (for vector search)
  embedding_status TEXT DEFAULT 'pending',
  pinecone_indexed BOOLEAN DEFAULT false,

  -- Versioning
  version_number INTEGER DEFAULT 1,
  is_latest BOOLEAN DEFAULT true,
  parent_document_id UUID REFERENCES documents(id),

  -- Metadata
  uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  uploaded_by UUID REFERENCES users(id),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_documents_project ON documents(project_id);
CREATE INDEX idx_documents_status ON documents(processing_status);
CREATE INDEX idx_documents_text ON documents USING gin(to_tsvector('english', extracted_text));
```

---

### 9.3 Document Chunks (for RAG)

```sql
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  page_number INTEGER,

  -- Vector embedding reference
  pinecone_id TEXT, -- ID in Pinecone vector DB

  -- Metadata for filtering
  metadata JSONB, -- { section, table_detected, chart_detected, etc. }

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_chunks_pinecone ON document_chunks(pinecone_id);
```

---

### 9.4 Extracted Data Table

```sql
CREATE TABLE extracted_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Structured extraction
  data_type TEXT NOT NULL, -- 'financial', 'parties', 'dates', 'risks'
  extracted_values JSONB NOT NULL,

  -- Confidence scores
  confidence JSONB, -- { field1: 0.95, field2: 0.87 }

  -- Validation
  validated BOOLEAN DEFAULT false,
  validated_by UUID REFERENCES users(id),
  validated_at TIMESTAMP WITH TIME ZONE,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_extracted_document ON extracted_data(document_id);
CREATE INDEX idx_extracted_project ON extracted_data(project_id);
CREATE INDEX idx_extracted_type ON extracted_data(data_type);
```

---

### 9.5 Annotations Table

```sql
CREATE TABLE annotations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  page_number INTEGER NOT NULL,

  -- Annotation type and data
  annotation_type TEXT NOT NULL, -- 'highlight', 'comment', 'shape', 'sticky_note'
  coordinates JSONB NOT NULL, -- { x, y, width, height }
  content TEXT,
  color TEXT,

  -- Collaboration
  author_id UUID REFERENCES users(id),
  parent_annotation_id UUID REFERENCES annotations(id), -- for replies

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_annotations_document ON annotations(document_id);
CREATE INDEX idx_annotations_author ON annotations(author_id);
```

---

### 9.6 Risk Assessments Table

```sql
CREATE TABLE risk_assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Overall risk score
  overall_risk_score DECIMAL(3, 1), -- 0-10

  -- Risk breakdown
  credit_risk DECIMAL(3, 1),
  political_risk DECIMAL(3, 1),
  esg_risk DECIMAL(3, 1),
  market_risk DECIMAL(3, 1),
  execution_risk DECIMAL(3, 1),

  -- Red flags
  red_flags JSONB, -- [{ category, severity, description, evidence }]

  -- Assessment metadata
  assessed_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  assessed_by UUID REFERENCES users(id), -- NULL if AI-generated
  is_ai_generated BOOLEAN DEFAULT true,
  reviewed_by UUID REFERENCES users(id),
  reviewed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_risk_project ON risk_assessments(project_id);
CREATE INDEX idx_risk_score ON risk_assessments(overall_risk_score);
```

---

### 9.7 Compliance Assessments Table

```sql
CREATE TABLE compliance_assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  framework TEXT NOT NULL, -- 'IFC', 'Equator', 'World_Bank', etc.
  framework_version TEXT,

  -- Scores
  overall_score DECIMAL(5, 2), -- 0-100

  -- Detailed requirements
  requirements JSONB, -- [{ id, name, status: 'met'|'partial'|'not_met', evidence: [docId] }]
  gaps JSONB, -- [{ requirement, description, severity }]

  -- Assessment metadata
  assessed_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  assessed_by UUID REFERENCES users(id),
  is_ai_generated BOOLEAN DEFAULT true,
  reviewed_by UUID REFERENCES users(id),
  reviewed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_compliance_project ON compliance_assessments(project_id);
CREATE INDEX idx_compliance_framework ON compliance_assessments(framework);
```

---

### 9.8 ESG Scores Table

```sql
CREATE TABLE esg_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Overall ESG score
  overall_score DECIMAL(5, 2), -- 0-100

  -- Pillar scores
  environmental_score DECIMAL(5, 2),
  social_score DECIMAL(5, 2),
  governance_score DECIMAL(5, 2),

  -- Detailed metrics
  metrics JSONB, -- { carbonFootprint: { score, value, unit }, jobsCreated: { score, value }, ... }

  -- Data source
  data_source TEXT, -- 'manual', 'ai_extracted', 'api_import'
  external_provider TEXT, -- 'LSEG', 'Sustainalytics', NULL

  scored_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  scored_by UUID REFERENCES users(id)
);

CREATE INDEX idx_esg_project ON esg_scores(project_id);
CREATE INDEX idx_esg_overall ON esg_scores(overall_score);
```

---

### 9.9 Financial Models Table

```sql
CREATE TABLE financial_models (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,

  -- Model type
  model_type TEXT NOT NULL, -- 'dcf', 'scenario_analysis', 'sensitivity'

  -- Assumptions
  assumptions JSONB NOT NULL, -- { discountRate, projectLife, taxRate, ... }

  -- Cash flow data
  cash_flows JSONB NOT NULL, -- [{ year, revenue, opex, capex, netCashFlow }]

  -- Outputs
  npv DECIMAL(15, 2),
  irr DECIMAL(5, 2),
  payback_period INTEGER, -- months
  outputs JSONB, -- Additional model-specific outputs

  -- Versioning
  version_number INTEGER DEFAULT 1,
  is_baseline BOOLEAN DEFAULT false,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_models_project ON financial_models(project_id);
CREATE INDEX idx_models_type ON financial_models(model_type);
```

---

### 9.10 Chat Conversations Table (for Document Q&A)

```sql
CREATE TABLE chat_conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE, -- NULL for multi-doc chats
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  title TEXT, -- Auto-generated from first message

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES chat_conversations(id) ON DELETE CASCADE,

  role TEXT NOT NULL, -- 'user', 'assistant'
  content TEXT NOT NULL,

  -- Sources (for assistant messages)
  sources JSONB, -- [{ documentId, page, snippet }]

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_conversations_user ON chat_conversations(user_id);
CREATE INDEX idx_conversations_project ON chat_conversations(project_id);
CREATE INDEX idx_messages_conversation ON chat_messages(conversation_id);
```

---

### 9.11 Search History Table

```sql
CREATE TABLE search_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  query TEXT NOT NULL,
  filters JSONB, -- Applied filters
  result_count INTEGER,
  clicked_results JSONB, -- [{ projectId, rank }]

  searched_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_timestamp ON search_history(searched_at);
```

---

### 9.12 Webhooks Table

```sql
CREATE TABLE webhooks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,

  url TEXT NOT NULL,
  events TEXT[] NOT NULL, -- ['document.processed', 'risk.detected']
  secret TEXT NOT NULL, -- For signature verification

  is_active BOOLEAN DEFAULT true,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  created_by UUID REFERENCES users(id)
);

CREATE TABLE webhook_deliveries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  webhook_id UUID REFERENCES webhooks(id) ON DELETE CASCADE,

  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,

  status TEXT NOT NULL, -- 'pending', 'delivered', 'failed'
  response_status_code INTEGER,
  error_message TEXT,

  attempted_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  delivered_at TIMESTAMP WITH TIME ZONE
);
```

---

## 10. Third-Party Services

### 10.1 AI/ML Services

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **OpenAI** | Embeddings, GPT-4, structured extraction | $0.00010/1K tokens (embeddings), $0.01/1K tokens (GPT-4 Turbo) | **PRIMARY** for embeddings & extraction |
| **Anthropic Claude** | Document analysis, long-context RAG, vision | $3/$15 per 1M tokens (input/output, Sonnet 4) | **PRIMARY** for long documents |
| **Pinecone** | Vector database | Free tier (1 index, 100K vectors), $70/month (Starter) | **PRIMARY** for semantic search |
| **Cohere** | Reranking, multilingual embeddings | $1/1K searches (rerank), $0.0001/1K tokens (embed) | **OPTIONAL** for reranking |

**Estimated Monthly Costs** (for 1000 projects, 10K documents):
- OpenAI Embeddings: $50-100/month
- GPT-4 for extraction: $200-500/month
- Claude for RAG: $100-300/month
- Pinecone: $70/month (Starter)
- **Total**: ~$420-970/month

---

### 10.2 Document Processing

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **Tesseract.js** | OCR (client-side) | Free (open-source) | **PRIMARY** for OCR |
| **Google Cloud Vision** | Advanced OCR, handwriting | $1.50/1K images | **OPTIONAL** for complex scans |
| **AWS Textract** | Form extraction, table detection | $1.50/1K pages | **OPTIONAL** for complex tables |

**Recommendation**: Start with Tesseract.js (free), upgrade to Cloud Vision/Textract if needed.

---

### 10.3 Data & Risk Intelligence

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **World Bank API** | Country risk data, economic indicators | Free | **RECOMMENDED** |
| **LSEG (Refinitiv)** | ESG scores, financial data | Enterprise pricing (contact) | **OPTIONAL** if budget allows |
| **Sustainalytics** | ESG risk ratings | Enterprise pricing | **OPTIONAL** |
| **Trading Economics API** | Economic indicators, country risk | $750/month | **OPTIONAL** |

**Recommendation**: Use free World Bank API initially, integrate paid providers for premium features.

---

### 10.4 Email & Communication

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **Resend** | Email sending, React templates | Free (100 emails/day), $20/month (50K emails) | **RECOMMENDED** |
| **SendGrid** | Email delivery, enterprise features | Free (100 emails/day), $19.95/month (40K emails) | Alternative |
| **AWS SES** | Cost-effective email | $0.10/1K emails | Good for high volume |

**Recommendation**: **Resend** for developer experience and React Email templates.

---

### 10.5 Calendar Integration

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **Google Calendar API** | Calendar sync, event creation | Free | **RECOMMENDED** |
| **Microsoft Graph API** | Outlook Calendar | Free | **RECOMMENDED** for enterprise |

**Recommendation**: Support both Google and Microsoft for broad compatibility.

---

### 10.6 Collaboration

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **Slack API** | Notifications, bot integration | Free (Slack app) | **RECOMMENDED** |
| **Microsoft Teams** | Notifications, enterprise chat | Free (webhook) | **RECOMMENDED** for enterprise |

**Recommendation**: Support both Slack and Teams via webhooks (simplest approach).

---

### 10.7 Maps & Geospatial

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **MapLibre GL** | Vector maps, high performance | Free (open-source) | **RECOMMENDED** |
| **Mapbox** | Advanced features, commercial support | $5/1K map loads (after free tier) | **OPTIONAL** if budget allows |
| **OpenStreetMap** | Free map data | Free | Use as basemap with MapLibre |

**Recommendation**: **MapLibre GL JS** with OpenStreetMap data (fully free).

---

### 10.8 Authentication & Infrastructure

| Service | Purpose | Pricing | Recommendation |
|---------|---------|---------|----------------|
| **Supabase Auth** | Authentication, SSO | Included with Supabase | **RECOMMENDED** |
| **Auth0** | Enterprise auth, advanced SSO | $240/month (Essentials) | **OPTIONAL** for complex SSO |
| **Upstash Redis** | Rate limiting, caching | Free tier, $0.20/100K commands | **RECOMMENDED** |
| **Vercel** | Hosting (Next.js) | Free tier, $20/month (Pro) | **RECOMMENDED** |

**Recommendation**: Use Supabase Auth + Upstash Redis for rate limiting.

---

## 11. Technical Feasibility Assessment

### 11.1 Complexity Rating (1-5, 5=most complex)

| Feature | Complexity | Estimated Dev Time | Notes |
|---------|------------|-------------------|-------|
| **Semantic Search** | 3 | 2-3 weeks | Well-documented with Pinecone + OpenAI |
| **Document Upload & Processing** | 3 | 2-3 weeks | Standard pattern, OCR adds complexity |
| **Document Q&A (RAG)** | 4 | 3-4 weeks | Requires careful chunking, testing |
| **Financial Modeling** | 3 | 2-3 weeks | Standard formulas, UI complexity |
| **Risk Assessment Dashboard** | 3 | 2-3 weeks | Visualization + scoring logic |
| **Compliance Checker** | 4 | 4-6 weeks | Rule engine + AI analysis |
| **Auto-Extraction** | 4 | 3-4 weeks | LLM function calling, validation |
| **Investment Memo Generator** | 3 | 2-3 weeks | Template system + AI drafting |
| **Portfolio Analytics** | 3 | 2-3 weeks | Aggregation queries + charts |
| **PDF Viewer + Annotations** | 3 | 2-3 weeks | react-pdf + custom annotation layer |
| **Real-time Collaboration** | 4 | 3-4 weeks | Supabase Realtime, state sync |
| **Export (PDF/Excel/PPTX)** | 2 | 1-2 weeks | Well-documented libraries |
| **Multi-language Support** | 3 | 2-3 weeks | i18n + translation API |
| **Geographic Visualization** | 2 | 1-2 weeks | MapLibre GL is straightforward |
| **Integrations (Email/Slack/Calendar)** | 2 | 1-2 weeks | Standard APIs |

**Total Estimated Development Time**: 32-48 weeks (8-12 months) for full MVP

---

### 11.2 Risks & Challenges

**High-Risk Areas**:
1. **RAG Quality**: Ensuring accurate, hallucination-free answers from documents
   - Mitigation: Extensive testing, confidence scores, human-in-the-loop review

2. **Compliance Rule Engine**: Keeping up with changing frameworks
   - Mitigation: Flexible rule structure, regular updates, legal review

3. **Performance with Large Documents**: Processing 100+ page PDFs
   - Mitigation: Background jobs, streaming, chunking optimization

4. **Data Security**: Handling sensitive financial documents
   - Mitigation: Encryption, access controls, audit logs, SOC2 compliance

5. **Integration Complexity**: Connecting with legacy DFI systems
   - Mitigation: Phased approach, start with file-based, add API later

**Medium-Risk Areas**:
- Real-time collaboration scaling (many users on same document)
- Financial model accuracy (requires domain expert validation)
- Multi-language accuracy (translation quality for technical terms)

---

### 11.3 Scalability Considerations

**Expected Load**:
- Users: 100-500 concurrent users
- Projects: 1,000-10,000 projects
- Documents: 10,000-100,000 documents
- Searches: 1,000-10,000 per day

**Scalability Strategies**:

1. **Database (Supabase/PostgreSQL)**:
   - Indexed queries for fast lookups
   - Partitioning for large tables (documents, chunks)
   - Read replicas for analytics queries
   - Expected capacity: 10K+ projects, 100K+ documents

2. **Vector Search (Pinecone)**:
   - Pinecone handles up to 100M vectors on Starter plan
   - 1K documents × 10 chunks/doc = 10K vectors (well within limits)
   - Scale to Enterprise plan ($500/month) for larger datasets

3. **Document Processing**:
   - Background jobs (Supabase Edge Functions, Vercel cron)
   - Queue system (BullMQ + Redis) for heavy processing
   - Parallel processing for batch uploads

4. **File Storage (Supabase Storage)**:
   - Supabase Storage: 100GB free, $0.021/GB/month after
   - CDN caching for frequently accessed files
   - Expected: 10K documents × 2MB avg = 20GB (within free tier)

5. **API Rate Limiting**:
   - Per-user: 100 requests/minute
   - Per-IP: 1,000 requests/hour
   - Upstash Redis for distributed rate limiting

**Cost Estimates** (for 5,000 projects, 50K documents, 200 users):
- Supabase: $25/month (Pro plan)
- Pinecone: $70/month (Starter)
- Vercel: $20/month (Pro)
- AI APIs: $500-1,000/month
- Upstash Redis: $10/month
- **Total**: ~$625-1,125/month

---

### 11.4 Development Phases (Recommended Roadmap)

**Phase 1: Core Platform (Months 1-3)**
- User authentication (Supabase Auth)
- Project CRUD operations
- Document upload & storage
- Basic search (SQL full-text search)
- Simple dashboard (project list, basic filters)

**Phase 2: AI Foundation (Months 3-5)**
- Semantic search (Pinecone + embeddings)
- Basic document Q&A (RAG)
- Auto-extraction (financial metrics, parties, dates)
- Document summarization

**Phase 3: Analytics & Modeling (Months 5-7)**
- Financial modeling interface (DCF, scenarios)
- Risk assessment dashboard
- Portfolio analytics
- Data visualization (charts, maps)

**Phase 4: Advanced Features (Months 7-9)**
- Compliance checker
- ESG scoring
- Investment memo generator
- Red flag detection

**Phase 5: Collaboration & Export (Months 9-11)**
- PDF viewer + annotations
- Real-time collaboration
- Export (PDF, Excel, PPTX)
- Version control

**Phase 6: Integrations & Polish (Months 11-12)**
- Email notifications (Resend)
- Slack/Teams integration
- Calendar sync
- Multi-language support
- Performance optimization
- User testing & feedback

---

### 11.5 Success Metrics

**User Engagement**:
- Daily Active Users (DAU)
- Documents uploaded per user per month
- Average session duration
- Search queries per session

**AI Performance**:
- Document Q&A accuracy (target: >90% helpful answers)
- Extraction accuracy (target: >95% for key fields)
- RAG citation accuracy (target: >95% correct source attribution)
- User feedback on AI features (thumbs up/down)

**Business Value**:
- Time saved per investment memo (target: 50% reduction)
- Projects analyzed per analyst (target: 2x increase)
- Compliance assessment time (target: 70% reduction)
- Document processing time (target: instant vs days)

**Platform Health**:
- API response time (target: <200ms p95)
- Document processing time (target: <5 min for 50-page PDF)
- Search latency (target: <1 second)
- Uptime (target: 99.9%)

---

## 12. Summary & Recommendations

### 12.1 Technology Stack (Final)

**Frontend**:
- Next.js 14 (App Router, Server Components)
- TypeScript
- Tailwind CSS + Radix UI
- Recharts + Nivo (visualization)
- react-pdf + custom annotations
- MapLibre GL (maps)

**Backend**:
- Next.js API Routes
- Supabase (PostgreSQL, Auth, Storage, Realtime)
- Pinecone (vector search)
- OpenAI (embeddings, GPT-4)
- Anthropic Claude (long documents, vision)

**Infrastructure**:
- Vercel (hosting)
- Upstash Redis (rate limiting, caching)
- Resend (email)

**DevOps**:
- GitHub (version control)
- Vercel CI/CD
- Playwright (E2E testing)
- Sentry (error monitoring)

---

### 12.2 Critical Success Factors

1. **RAG Quality**: Invest heavily in prompt engineering, chunking strategy, and testing
2. **User Experience**: Prioritize fast, intuitive UX over feature completeness
3. **Data Security**: Implement robust security from day one (encryption, access controls)
4. **Performance**: Optimize for speed (document processing, search, page loads)
5. **Domain Expertise**: Partner with DFI professionals to validate features and outputs

---

### 12.3 Next Steps

1. **Prototype Phase** (Weeks 1-4):
   - Build minimal RAG system (upload PDF, ask questions)
   - Test semantic search with sample projects
   - Validate financial modeling formulas with domain experts

2. **User Research** (Weeks 2-6):
   - Interview 10-15 DFI investment officers
   - Observe current workflows (manual document review, Excel models)
   - Validate feature priorities

3. **Architecture Design** (Weeks 3-6):
   - Finalize database schema
   - Design API contracts
   - Plan deployment architecture

4. **Development Kickoff** (Week 7+):
   - Set up development environment
   - Implement Phase 1 features
   - Weekly demos to stakeholders

---

## References & Sources

### Data Visualization
- [8 Best React Chart Libraries for 2025](https://embeddable.com/blog/react-chart-libraries)
- [Best React chart libraries - LogRocket](https://blog.logrocket.com/best-react-chart-libraries-2025/)
- [Top 11 React chart libraries - Ably](https://ably.com/blog/top-react-chart-libraries)
- [Top 10 React Chart Libraries - OpenReplay](https://blog.openreplay.com/react-chart-libraries-2025/)

### PDF & Document Management
- [Comparing React PDF viewers - Nutrient](https://www.nutrient.io/blog/top-react-pdf-viewers/)
- [Best React PDF Viewer Libraries 2025](https://blog.react-pdf.dev/top-6-pdf-viewers-for-reactjs-developers-in-2025)
- [react-pdf GitHub](https://github.com/wojtekmaj/react-pdf)

### Financial Tools
- [financejs - npm](https://www.npmjs.com/package/financejs)
- [financial (TypeScript library) - GitHub](https://github.com/lmammino/financial)

### AI Document Extraction
- [2025 Guide to Document Extraction - Cradl AI](https://www.cradl.ai/post/document-data-extraction-using-ai)
- [Document Data Extraction: LLMs vs OCRs - Vellum](https://www.vellum.ai/blog/document-data-extraction-in-2025-llms-vs-ocrs)
- [GPT-4o vs Claude Sonnet - Invofox](https://www.invofox.com/en/post/document-parsing-using-gpt-4o-api-vs-claude-sonnet-3-5-api-vs-invofox-api-with-code-samples)
- [Claude PDF Support - Anthropic](https://docs.claude.com/en/docs/build-with-claude/pdf-support)

### Maps
- [Leaflet vs Mapbox - Visarsoft](https://medium.com/visarsoft-blog/leaflet-or-mapbox-choosing-the-right-tool-for-interactive-maps-53dea7cc3c40)
- [React map library comparison - LogRocket](https://blog.logrocket.com/react-map-library-comparison/)

### PDF/PowerPoint Generation
- [JS PDF libraries comparison - DEV](https://dev.to/handdot/generate-a-pdf-in-js-summary-and-comparison-of-libraries-3k0p)
- [Top 6 PDF Libraries for React - Medium](https://medium.com/@ansonch/top-6-open-source-pdf-libraries-for-react-developers-62033fca5fff)
- [PptxGenJS - GitHub](https://github.com/gitbrent/PptxGenJS)

### Excel Export
- [SheetJS React demos](https://docs.sheetjs.com/docs/demos/frontend/react/)
- [Export to Excel in React - Medium](https://medium.com/@gb.usmanumar/how-to-export-data-to-excel-xlsx-in-react-js-8f3ccccba875)

### OCR & Document Processing
- [PDF OCR in Next.js - Cortex](https://blog.trycortex.ai/nextjs-ocr-pdf-extract)
- [OCR with Tesseract.js in Next.js - Medium](https://javascript.plainenglish.io/implementing-ocr-with-tesseract-js-in-next-js-ac4143ff5218)
- [next-ocr GitHub](https://github.com/arshad-yaseen/next-ocr)

### Real-time Collaboration
- [Supabase Realtime](https://supabase.com/docs/guides/realtime)
- [Build Collaborative Whiteboard - DEV](https://dev.to/keyurparalkar/mastering-real-time-collaboration-building-figma-and-miro-inspired-features-with-supabase-57eh)
- [Supabase vs Firebase - Propelius](https://propelius.ai/blogs/real-time-collaboration-tools-supabase-vs-firebase)

### Semantic Search & RAG
- [Semantic Search with Pinecone - OpenAI Cookbook](https://cookbook.openai.com/examples/vector_databases/pinecone/semantic_search)
- [RAG Q&A with Pinecone - OpenAI Cookbook](https://cookbook.openai.com/examples/vector_databases/pinecone/gen_qa)
- [Pinecone Vector Database Guide - DevBlogIt](https://devblogit.com/pinecone-vector-database-guide)
- [OpenAI Integration - Pinecone Docs](https://docs.pinecone.io/integrations/openai)

### ESG & Compliance
- [ESG Risk Ratings - Sustainalytics](https://www.sustainalytics.com/esg-data)
- [Top ESG Reporting Software - Prophix](https://www.prophix.com/blog/esg-software/)
- [LSEG ESG Scores](https://www.lseg.com/en/data-analytics/sustainable-finance/esg-scores)

### Sankey Diagrams
- [Sankey Diagram with React and D3 - React Graph Gallery](https://www.react-graph-gallery.com/sankey-diagram)
- [Nivo Sankey](https://nivo.rocks/sankey/)
- [D3 Sankey - GitHub](https://github.com/d3/d3-sankey)

### Next.js Security & Rate Limiting
- [Complete Next.js Security Guide 2025 - TurboStarter](https://www.turbostarter.dev/blog/complete-nextjs-security-guide-2025-authentication-api-protection-and-best-practices)
- [4 Best Rate Limiting Solutions - DEV](https://dev.to/ethanleetech/4-best-rate-limiting-solutions-for-nextjs-apps-2024-3ljj)
- [Next.js API Rate Limiting - Compile N Run](https://www.compilenrun.com/docs/framework/nextjs/nextjs-api-development/nextjs-api-rate-limiting/)
- [Next.js 15 API Best Practice - Medium](https://medium.com/@lior_amsalem/nextjs-api-best-practice-2025-250c0a6514b9)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-25
**Prepared for**: InfraFlow AI Development Team
