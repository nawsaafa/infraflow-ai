# InfraFlow AI - Lovable Development Prompt

## Project Overview

Build **InfraFlow AI**, a production-ready infrastructure finance intelligence platform that helps DFI Investment Officers, Project Developers, and Risk Analysts screen, analyze, and underwrite infrastructure projects 70% faster using AI-powered automation.

The platform is already deployed with:
- **24 verified projects** ($110B+ investment) across 18 countries
- **Supabase cloud database** (10 tables, 80+ indexes, 40+ RLS policies) - production ready
- **Pinecone vector database** (24 embeddings) - semantic search ready
- **Complete backend** on GitHub: https://github.com/nawsaafa/infraflow-ai

Your task is to build the **Next.js 14 frontend dashboard** following the comprehensive design specification in `DASHBOARD_SPECIFICATION.md`.

## Quick Start Instructions

### 1. Create New Next.js Project
```bash
npx create-next-app@14 infraflow-dashboard --typescript --tailwind --app
cd infraflow-dashboard
```

### 2. Install Core Dependencies
```bash
npm install @supabase/supabase-js @pinecone-database/pinecone
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-tabs
npm install recharts lucide-react date-fns
npm install @tanstack/react-table
npm install class-variance-authority clsx tailwind-merge
```

### 3. Install Shadcn/ui Components
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input table dialog tabs badge
```

### 4. Configure Environment Variables
Create `.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=https://abhnlhbkmrozxtfoaxnv.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiaG5saGJrbXJvenh0Zm9heG52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg1ODQyNzAsImV4cCI6MjA3NDE2MDI3MH0.Dtz9jemJ7rXr9LSqkRbZ9HV_nS2qVI-74tabA_TzWEA

# Get these from the project's .env file
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note**: Contact the project owner for the actual API keys. They are stored securely in the project's `.env` file.

## Development Phases

### Phase 1: MVP Foundation (Build This First - Weeks 1-3)

**1.1 Setup Supabase Client** (`lib/supabase.ts`)
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Type definitions
export interface Project {
  id: string
  name: string
  sponsor: string | null
  country: string
  sector: string
  total_value: number | null
  dfi_partners: string[]
  status: 'draft' | 'active' | 'analyzed' | 'completed' | 'archived'
  risk_score: number | null
  metadata: Record<string, any>
  created_at: string
  updated_at: string
}
```

**1.2 Build Dashboard Page** (`app/page.tsx`)
Create the main dashboard with:
- **KPI Cards** (top row):
  - Total Projects (24)
  - Total Investment ($110B+)
  - Countries (18)
  - DFI Partners (17)

  Data source:
  ```typescript
  const { data: projects } = await supabase.from('projects').select('*')
  const totalValue = projects.reduce((sum, p) => sum + (p.total_value || 0), 0)
  const countries = new Set(projects.map(p => p.country)).size
  const dfis = new Set(projects.flatMap(p => p.dfi_partners || [])).size
  ```

- **Deal Pipeline Visualization** (Kanban-style):
  - Screening (status: 'draft')
  - Due Diligence (status: 'active')
  - IC Review (status: 'analyzed')
  - Approved (status: 'completed')

- **Recent Activity Feed**: Show 5 most recent projects by `created_at`

**1.3 Build Project List Page** (`app/projects/page.tsx`)
- **Grid/List Toggle**: Card grid view + compact table view
- **Filters** (left sidebar):
  - Country (multi-select dropdown)
  - Sector (checkboxes)
  - Status (checkboxes)
  - Investment Range (slider)
- **Sort Options**:
  - Name A-Z
  - Investment (high to low)
  - Date added (newest first)

**1.4 Build Project Detail Page** (`app/projects/[id]/page.tsx`)
- **Header**: Project name, country flag, sponsor, status badge
- **5 Tabs**:
  - Overview: Key metrics, description, timeline
  - Financial: Investment amount, DFI partners, financial structure
  - Risk: Risk score visualization (if available)
  - Compliance: Applicable standards
  - Documents: Placeholder for future document upload

### Phase 2: AI-Powered Search (Weeks 4-6)

**2.1 Semantic Search** (`app/api/search/route.ts`)
```typescript
import { Pinecone } from '@pinecone-database/pinecone'
import { OpenAI } from 'openai'

const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! })
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! })
const index = pinecone.index('infraflow-documents')

export async function POST(request: Request) {
  const { query } = await request.json()

  // 1. Generate embedding
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: query
  })

  // 2. Query Pinecone
  const results = await index.query({
    vector: embedding.data[0].embedding,
    topK: 10,
    includeMetadata: true
  })

  // 3. Fetch full projects from Supabase
  const projectIds = results.matches.map(m => m.id)
  const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .in('id', projectIds)

  return Response.json({ projects, scores: results.matches })
}
```

**2.2 Search Interface** (`components/semantic-search.tsx`)
- Smart search bar with natural language queries
- Example queries: "green hydrogen projects in Middle East", "wind energy above $1B"
- Display results with relevance scores

### Phase 3: Financial Analysis (Weeks 7-9)

**3.1 DCF Calculator** (`components/financial/dcf-calculator.tsx`)
- Input fields: Initial investment, annual cash flows (10 years), discount rate
- Outputs: NPV, IRR, Payback period, DSCR
- Visualization: Cash flow waterfall (use Recharts BarChart)

**3.2 Sensitivity Analysis** (`components/financial/sensitivity-analysis.tsx`)
- 2D heatmap: Discount rate vs. Revenue growth
- Color coding: Green (NPV > 0), Red (NPV < 0)
- Use Recharts or Nivo heatmap

### Phase 4: Risk & Compliance (Weeks 10-12)

**4.1 Risk Matrix Visualization** (`components/risk/risk-matrix.tsx`)
- 5x5 grid: Likelihood (Y-axis) vs. Impact (X-axis)
- Plot risks as bubbles
- Color zones: Green (low), Yellow (medium), Red (high)

**4.2 Compliance Checker** (`app/api/compliance/route.ts`)
```typescript
import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

export async function POST(request: Request) {
  const { projectDescription, framework } = await request.json()

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: `Analyze this project against ${framework} compliance framework:\n\n${projectDescription}\n\nProvide: 1) Compliance gaps, 2) Required documentation, 3) Risk rating`
    }]
  })

  return Response.json({ analysis: message.content[0].text })
}
```

### Phase 5: Investment Memo (Weeks 13-15)

**5.1 AI Memo Generator** (`app/api/memo/route.ts`)
```typescript
export async function POST(request: Request) {
  const { projectId } = await request.json()

  // Fetch project data
  const { data: project } = await supabase
    .from('projects')
    .select('*')
    .eq('id', projectId)
    .single()

  // Generate memo with Claude
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 8000,
    messages: [{
      role: 'user',
      content: `Generate investment memo for:\n${JSON.stringify(project, null, 2)}\n\nStructure: Executive Summary, Project Overview, Financial Analysis, Risk Assessment, Recommendation`
    }]
  })

  return Response.json({ memo: message.content[0].text })
}
```

**5.2 Memo Editor** (`components/memo/memo-editor.tsx`)
- Rich text editor (use Tiptap or similar)
- Sections: Executive Summary, Project Overview, Financial Analysis, Risk Assessment, Recommendation
- Export to PDF button

### Phase 6: Portfolio Analytics (Weeks 16-18)

**6.1 Executive Dashboard** (`app/analytics/page.tsx`)
- Geographic map with project clusters (use Mapbox GL or MapLibre GL)
- Sector breakdown (Pie chart)
- Investment timeline (Line chart)
- Top DFI partners (Bar chart)

## Design System Reference

### Colors (Tailwind)
```typescript
// tailwind.config.ts
colors: {
  primary: '#1E40AF',      // Blue-700 (Trust, Authority)
  success: '#10B981',      // Green-500 (Positive)
  warning: '#F59E0B',      // Amber-500 (Caution)
  error: '#EF4444',        // Red-500 (Risk)
  neutral: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    // ... standard Tailwind grays
  }
}
```

### Typography
- **Font**: Inter (from Google Fonts)
- **Headings**: font-bold
- **Body**: font-normal text-base (16px)
- **Captions**: text-xs (12px)

### Component Library
Use **Shadcn/ui** for all components:
- Buttons: Default, Outline, Ghost variants
- Cards: shadow-sm, rounded-lg, p-6
- Badges: status badges (draft, active, completed)
- Tables: TanStack Table with sorting/filtering
- Dialogs: Radix UI modals
- Dropdowns: Radix UI select/dropdown

## Priority Features (Build in This Order)

1. **Dashboard** (KPI cards, pipeline visualization)
2. **Project List** (grid/list view, filters, sort)
3. **Project Detail** (5 tabs with overview, financial, risk)
4. **Semantic Search** (Pinecone integration)
5. **Compliance Checker** (Claude integration)
6. **Financial Calculator** (DCF, sensitivity)
7. **Investment Memo Generator** (Claude integration)
8. **Portfolio Analytics** (charts, map)

## Testing Instructions

### Test with Real Data
```typescript
// Fetch all 24 projects
const { data: projects } = await supabase.from('projects').select('*')
console.log(`Loaded ${projects.length} projects`)

// Test semantic search
const response = await fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'green hydrogen projects in Saudi Arabia' })
})
const results = await response.json()
// Should return NEOM Green Hydrogen Project with high score
```

### Verify Supabase Connection
```bash
# In browser console
const { data, error } = await supabase.from('projects').select('count')
// Should return { count: 24 }
```

## Success Criteria

Your dashboard is ready when:
- [ ] All 24 projects display correctly
- [ ] Filters work (country, sector, status)
- [ ] Semantic search returns relevant results
- [ ] Financial calculator computes NPV/IRR correctly
- [ ] Compliance checker generates gap analysis
- [ ] Investment memo generates in <30 seconds
- [ ] UI matches design system (Shadcn/ui + Tailwind)
- [ ] Responsive on desktop and tablet (1024px+)

## Full Specification

For complete details, wireframes, user flows, and technical architecture, see:
**`DASHBOARD_SPECIFICATION.md`** (117 KB)

Contains:
- 4 detailed user personas with journey maps
- Complete information architecture
- 5 core modules with ASCII wireframes
- Full database schema and API endpoints
- UI/UX design system specifications
- 6-phase development roadmap
- Success metrics and KPIs

## Support Resources

- **GitHub Repo**: https://github.com/nawsaafa/infraflow-ai
- **Supabase Dashboard**: https://supabase.com/dashboard/project/abhnlhbkmrozxtfoaxnv
- **Research Documents**:
  - `DFI-Platform-UX-Research-Report.md` - UI/UX patterns
  - `infraflow-ai-market-research.md` - Pain points, competitive analysis
  - `InfraFlow-AI-Technical-Specification.md` - Technical stack, NPM packages
  - `DFI_Investment_Workflows_Research.md` - Investment processes, user stories

## Key Deliverable

Build a **production-ready Next.js 14 dashboard** that connects to existing Supabase/Pinecone data and enables DFI Investment Officers to screen 50+ deals per year 70% faster with zero missed risks.

Start with **Phase 1 MVP** (Dashboard + Project List + Project Detail) and iterate from there.
