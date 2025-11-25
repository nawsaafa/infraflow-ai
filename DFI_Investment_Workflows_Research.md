# DFI Investment Workflows and Operational Procedures
## Comprehensive Research Documentation

**Prepared for:** AI Consults Platform - DFI CRM Development
**Date:** November 25, 2025
**Purpose:** Document typical DFI investment workflows, decision-making processes, and operational procedures to inform CRM system design

---

## Table of Contents

1. [DFI Investment Process Flow](#1-dfi-investment-process-flow)
2. [Due Diligence Comprehensive Checklist](#2-due-diligence-comprehensive-checklist)
3. [Investment Memo Structure](#3-investment-memo-structure)
4. [Key Decision Criteria Framework](#4-key-decision-criteria-framework)
5. [Reporting Requirements and Metrics](#5-reporting-requirements-and-metrics)
6. [Common Bottlenecks and Solutions](#6-common-bottlenecks-and-solutions)
7. [User Stories for CRM Development](#7-user-stories-for-crm-development)

---

## 1. DFI Investment Process Flow

### Overview
The DFI investment process typically follows a structured workflow from initial deal sourcing through to post-investment monitoring. This process is designed to ensure thorough evaluation, risk management, and alignment with development objectives.

### 1.1 Deal Sourcing

**Definition:** The entry point where investment opportunities are identified and brought to the DFI's attention.

**Key Channels:**
- **Proprietary Deals:** Sourced directly by the DFI through relationship building, conferences, sector analysis
- **Intermediated Deals:** Received via third parties including:
  - Investment banks
  - M&A advisors
  - Financial intermediaries
  - Development agencies
  - Government partnerships
  - Co-investment partners (other DFIs, pension funds)

**Initial Documentation:**
- Project concept note
- Sponsor profile
- Preliminary financial information
- Location and sector identification

**CRM Implication:** System must track deal source, referral partner, initial contact date, and preliminary screening status.

---

### 1.2 Initial Screening (Quick Go/No-Go)

**Purpose:** Filter out projects that don't meet basic eligibility criteria before significant resources are invested.

**Screening Criteria:**
1. **Geographic Eligibility:** Does the project location align with DFI's mandate?
2. **Sector Fit:** Is the sector within DFI's investment scope?
3. **Size Threshold:** Does the project meet minimum/maximum investment size criteria?
4. **Development Rationale:** Clear development impact potential?
5. **Financial Viability:** Preliminary assessment of financial sustainability
6. **Sponsor Quality:** Track record and capacity of project sponsor
7. **Red Flags:** Any obvious ESG, corruption, or reputational risks?

**Timeline:** 2-4 weeks typically

**Output:** Go/No-Go decision
- **Go:** Proceed to detailed due diligence
- **No-Go:** Provide feedback to sponsor; maintain relationship for future opportunities

**Key Players:** Investment Officers, Sector Specialists

**CRM Implication:** Checklist-based screening module with automated status updates and rejection reason tracking.

---

### 1.3 Due Diligence Phases

**Duration:** 3-6 months (varies by complexity)

Due diligence is conducted across multiple parallel tracks:

#### A. Financial Due Diligence
- Review historical financial statements (3-5 years)
- Analyze financial projections and assumptions
- Assess debt capacity and capital structure
- Validate cash flow models
- Review existing debt obligations and covenants
- Tax structure analysis
- Working capital requirements

**Key Outputs:**
- Financial due diligence report
- Independent financial model
- Sensitivity analysis
- Credit rating assessment

#### B. Technical Due Diligence
- Engineering feasibility studies
- Technology assessment
- Construction cost validation
- Project timeline review
- Operational requirements
- Supply chain analysis
- Technical risk identification

**Key Outputs:**
- Technical due diligence report
- Construction plan validation
- Cost estimate review
- Technology risk assessment

#### C. Legal Due Diligence
- Corporate structure review
- Contract analysis (offtake, supply, EPC)
- Permits and licenses verification
- Land rights and title verification
- Regulatory compliance review
- Intellectual property assessment
- Litigation history

**Key Outputs:**
- Legal due diligence report
- Title opinions
- Permit status summary
- Contract risk matrix

#### D. Environmental, Social & Governance (ESG) Due Diligence
- Environmental Impact Assessment (EIA)
- Social Impact Assessment (SIA)
- Alignment with IFC Performance Standards
- Climate risk assessment
- Biodiversity and natural resource impacts
- Community consultation requirements
- Labor and working conditions
- Governance structure assessment
- Anti-corruption due diligence

**Key Frameworks:**
- IFC Performance Standards (PS 1-8)
- Equator Principles
- UN Global Compact
- SDG alignment

**Key Outputs:**
- Environmental and Social Action Plan (ESAP)
- ESG risk rating
- Climate assessment report
- Stakeholder engagement plan

#### E. Political & Country Risk Due Diligence
- Political stability assessment
- Regulatory framework review
- Currency convertibility and transfer risk
- Expropriation risk
- Political violence risk
- Force majeure considerations
- Host government support assessment

**Key Outputs:**
- Country risk assessment
- Political risk insurance recommendations
- Currency risk mitigation strategy

#### F. Commercial Due Diligence
- Market size and growth analysis
- Competitive landscape
- Demand projections
- Pricing assumptions
- Offtake agreement validation
- Customer concentration risk
- Market entry barriers

**Key Outputs:**
- Market analysis report
- Competitive positioning assessment
- Revenue model validation
- Commercial risk matrix

**CRM Implication:** Track DD progress across all dimensions, assign tasks to internal/external experts, manage document collection, flag blockers.

---

### 1.4 Investment Committee Process

**Purpose:** Senior decision-making body reviews all due diligence findings and makes investment decision.

**Composition:**
- Managing Director / CEO
- Chief Investment Officer
- Chief Risk Officer
- Chief Financial Officer
- Regional Directors
- Sector Heads
- Legal Counsel
- ESG Director

**Investment Memo Review:**
The IC reviews a comprehensive investment memorandum covering:
1. Executive Summary
2. Project Overview
3. Investment Rationale
4. Financial Analysis
5. Risk Assessment
6. ESG Compliance
7. Development Impact
8. Terms and Conditions
9. Recommendations

**IC Meeting Stages:**
1. **Initial Screening IC:** Brief overview (7-10 slides), preliminary go/no-go
2. **Full IC Review:** Comprehensive presentation (20-25 slides + appendices)
3. **Final Approval IC:** Review of final negotiated terms

**Decision Outcomes:**
- **Approved:** Proceed to legal documentation
- **Approved with Conditions:** Additional requirements before legal close
- **Deferred:** More information needed, resubmit
- **Rejected:** Investment does not meet criteria

**Timeline:** IC meetings typically monthly; decisions within 1-2 weeks of presentation

**CRM Implication:** IC scheduling module, document package assembly, decision tracking, conditions monitoring.

---

### 1.5 Approval and Disbursement

**Legal Documentation Phase (2-4 months):**
- Term sheet negotiation
- Legal agreement drafting
- Shareholder agreements
- Security documentation
- Government approvals
- Board approvals (both DFI and sponsor)

**Conditions Precedent:**
Before disbursement, certain conditions must be satisfied:
- Corporate registrations complete
- Permits and licenses obtained
- Co-financing commitments secured
- Insurance policies in place
- Security perfection complete
- ESAP implementation plan approved

**Disbursement Process:**
- Verification of conditions precedent
- Disbursement request submission
- Multi-level approval (Investment Officer, CFO, Authorized Signatories)
- Fund transfer
- Documentation and reporting

**CRM Implication:** Conditions tracking checklist, disbursement workflow automation, approval routing, payment tracking.

---

### 1.6 Monitoring and Reporting

**Post-Investment Oversight:**
Once funds are disbursed, active portfolio management begins.

**Monitoring Activities:**

#### Financial Monitoring
- **Frequency:** Quarterly financial statements
- **Key Metrics:**
  - Revenue vs projections
  - EBITDA and margins
  - Debt service coverage ratio (DSCR)
  - Cash flow analysis
  - Covenant compliance

#### Development Impact Monitoring
- **Frequency:** Semi-annual or annual
- **Key Metrics (HIPSO/IRIS+ framework):**
  - Jobs created (direct, indirect)
  - Gender disaggregation
  - CO2 emissions avoided
  - Energy generated/saved
  - People served
  - SDG contribution tracking

#### ESG Monitoring
- **Frequency:** Annual ESG reports
- **Activities:**
  - ESAP implementation progress
  - Incident reporting (accidents, environmental events)
  - Stakeholder grievance tracking
  - Site visits and audits
  - Community engagement updates

#### Risk Monitoring
- **Watch List:** Projects flagged for elevated risk
- **Risk Rating:** Regular reassessment of credit, ESG, country risk
- **Early Warning Indicators:** Covenant breaches, delayed payments, regulatory issues

**Reporting Requirements (from Sponsor to DFI):**
- Monthly: Construction progress reports (during construction phase)
- Quarterly: Financial statements, operational KPIs
- Semi-annual: Development impact metrics
- Annual: Audited financial statements, ESG compliance reports
- Ad-hoc: Material event reporting (accidents, regulatory changes, force majeure)

**Internal Reporting (within DFI):**
- Portfolio reviews with senior management
- Board reporting (quarterly)
- Risk committee updates
- Public disclosure reporting

**Site Visits:**
- Annual or bi-annual on-site visits
- More frequent for higher-risk projects
- Focused reviews during construction phase

**CRM Implication:** Portfolio dashboard, automated reporting reminders, document repository, metric tracking, risk flag alerts, site visit scheduling.

---

## 2. Due Diligence Comprehensive Checklist

### 2.1 Financial Due Diligence Checklist

**Historical Financial Information:**
- [ ] Audited financial statements (last 3-5 years)
- [ ] Management accounts (last 12-24 months)
- [ ] Tax returns
- [ ] Budget vs actual analysis
- [ ] Cash flow statements
- [ ] Working capital analysis
- [ ] Account receivable aging
- [ ] Account payable aging
- [ ] Inventory analysis (if applicable)

**Financial Projections:**
- [ ] Revenue projections with assumptions
- [ ] Operating expense forecasts
- [ ] Capital expenditure plan
- [ ] Working capital requirements
- [ ] Cash flow projections (monthly for Year 1-2, annual thereafter)
- [ ] Debt service schedule
- [ ] Sensitivity analysis (base, upside, downside cases)
- [ ] Break-even analysis

**Debt and Capital Structure:**
- [ ] Existing debt schedule (maturity, interest rates, covenants)
- [ ] Security granted on existing debt
- [ ] Guarantees and contingent liabilities
- [ ] Off-balance sheet items
- [ ] Related party transactions
- [ ] Equity contributions and shareholding structure
- [ ] Proposed debt sizing and ratios
- [ ] Financial covenants proposed

**Financial Metrics Analysis:**
- [ ] IRR (Internal Rate of Return)
- [ ] NPV (Net Present Value)
- [ ] DSCR (Debt Service Coverage Ratio) - typically >1.25x
- [ ] Loan Life Coverage Ratio (LLCR)
- [ ] Project Life Coverage Ratio (PLCR)
- [ ] Debt-to-Equity ratio
- [ ] Return on Equity (ROE)
- [ ] Payback period

**Key Financial Risks:**
- [ ] Revenue risk (demand, pricing)
- [ ] Cost overrun risk
- [ ] Operating cost escalation
- [ ] Interest rate risk
- [ ] Currency risk
- [ ] Refinancing risk
- [ ] Counterparty credit risk

---

### 2.2 Technical Due Diligence Checklist

**Engineering and Design:**
- [ ] Preliminary design documents
- [ ] Detailed engineering plans
- [ ] Technology selection rationale
- [ ] Equipment specifications
- [ ] Plant layout and site plans
- [ ] Geotechnical studies
- [ ] Environmental baseline studies
- [ ] Energy efficiency analysis

**Construction:**
- [ ] EPC (Engineering, Procurement, Construction) contract review
- [ ] Contractor track record and financial capacity
- [ ] Construction timeline and critical path
- [ ] Construction cost estimate (broken down)
- [ ] Contingency allowances
- [ ] Construction supervision plan
- [ ] Quality assurance/quality control (QA/QC) procedures
- [ ] Health and safety plan

**Technology:**
- [ ] Technology maturity and proven track record
- [ ] Technology supplier reputation
- [ ] Operations and maintenance requirements
- [ ] Spare parts availability
- [ ] Technology risk assessment
- [ ] Performance guarantees
- [ ] Warranty provisions

**Operations:**
- [ ] Operating model and staffing plan
- [ ] Maintenance program
- [ ] Supply chain logistics
- [ ] Raw material sourcing
- [ ] Utility requirements (water, power)
- [ ] Waste management plan
- [ ] Operating cost assumptions

**Independent Technical Consultant Reports:**
- [ ] Independent Engineer (IE) report
- [ ] Technology assessment report
- [ ] Market assessment (demand/supply)
- [ ] Cost validation report
- [ ] Schedule assessment

---

### 2.3 Legal Due Diligence Checklist

**Corporate and Governance:**
- [ ] Articles of incorporation
- [ ] By-laws and shareholder agreements
- [ ] Corporate registry search
- [ ] Organizational chart
- [ ] Board composition and minutes
- [ ] Ownership structure (including beneficial ownership)
- [ ] Related party relationships
- [ ] Corporate governance policies

**Contracts and Agreements:**
- [ ] Offtake agreements (Power Purchase Agreement, Supply Agreement)
- [ ] EPC contract
- [ ] O&M (Operations & Maintenance) contract
- [ ] Fuel/feedstock supply agreements
- [ ] Land lease or purchase agreements
- [ ] Interconnection agreements
- [ ] Transmission/transportation agreements
- [ ] Insurance policies
- [ ] Force majeure provisions across contracts

**Permits, Licenses, and Approvals:**
- [ ] Environmental permits/licenses
- [ ] Construction permits
- [ ] Operating licenses
- [ ] Water abstraction permits
- [ ] Discharge permits
- [ ] Import/export licenses (for equipment)
- [ ] Business registration certificates
- [ ] Tax clearances
- [ ] Government concession agreements
- [ ] Timeline for outstanding permits

**Land and Real Property:**
- [ ] Land title search and verification
- [ ] Survey reports
- [ ] Zoning compliance
- [ ] Easements and rights of way
- [ ] Encumbrances on property
- [ ] Land valuation
- [ ] Property insurance

**Litigation and Disputes:**
- [ ] Pending litigation
- [ ] Past litigation history
- [ ] Arbitration proceedings
- [ ] Regulatory investigations
- [ ] Labor disputes
- [ ] Tax disputes
- [ ] Contingent liabilities

**Compliance:**
- [ ] Anti-money laundering (AML) compliance
- [ ] Know Your Customer (KYC) documentation
- [ ] Anti-corruption and bribery assessment
- [ ] Sanctions screening (sponsor, shareholders, counterparties)
- [ ] Tax compliance
- [ ] Labor law compliance
- [ ] Regulatory compliance

---

### 2.4 Environmental, Social & Governance (ESG) Due Diligence Checklist

#### Environmental Assessment

**IFC Performance Standard 1: Assessment and Management of E&S Risks**
- [ ] Environmental and Social Impact Assessment (ESIA)
- [ ] Environmental and Social Management System (ESMS)
- [ ] Environmental and Social Action Plan (ESAP)
- [ ] Stakeholder engagement plan
- [ ] Grievance mechanism

**IFC Performance Standard 2: Labor and Working Conditions**
- [ ] Human resources policies
- [ ] Working conditions assessment
- [ ] Child labor and forced labor policies
- [ ] Occupational health and safety program
- [ ] Worker grievance mechanism
- [ ] Contractor and supply chain labor practices

**IFC Performance Standard 3: Resource Efficiency and Pollution Prevention**
- [ ] Greenhouse gas emissions assessment
- [ ] Energy efficiency measures
- [ ] Water consumption and efficiency
- [ ] Waste management plan
- [ ] Hazardous materials management
- [ ] Air emissions control
- [ ] Effluent and water quality

**IFC Performance Standard 4: Community Health, Safety and Security**
- [ ] Community health and safety risks
- [ ] Infrastructure and equipment safety
- [ ] Hazardous materials transport and storage
- [ ] Security personnel conduct
- [ ] Emergency preparedness and response
- [ ] Disease prevention measures

**IFC Performance Standard 5: Land Acquisition and Involuntary Resettlement**
- [ ] Resettlement action plan (if applicable)
- [ ] Compensation framework
- [ ] Livelihood restoration plan
- [ ] Consultation with affected communities
- [ ] Grievance mechanism for displaced persons

**IFC Performance Standard 6: Biodiversity Conservation**
- [ ] Biodiversity baseline assessment
- [ ] Critical habitat screening
- [ ] Protected areas proximity
- [ ] Mitigation hierarchy (avoid, minimize, restore, offset)
- [ ] Biodiversity action plan

**IFC Performance Standard 7: Indigenous Peoples**
- [ ] Indigenous peoples screening
- [ ] Free, Prior and Informed Consent (FPIC) process
- [ ] Indigenous Peoples Plan
- [ ] Cultural heritage considerations

**IFC Performance Standard 8: Cultural Heritage**
- [ ] Cultural heritage baseline
- [ ] Chance finds procedure
- [ ] Consultation with stakeholders
- [ ] Cultural heritage management plan

**Climate Risk Assessment:**
- [ ] Physical climate risks (flooding, drought, extreme weather)
- [ ] Transition risks (policy changes, carbon pricing)
- [ ] Climate adaptation measures
- [ ] GHG emissions baseline and projections
- [ ] Paris Agreement alignment

**Additional Environmental Considerations:**
- [ ] Environmental permits status
- [ ] Compliance with national environmental law
- [ ] Compliance with international conventions
- [ ] Environmental liabilities and legacy issues
- [ ] Decommissioning plan
- [ ] Environmental insurance

#### Social Assessment

**Community Engagement:**
- [ ] Stakeholder mapping
- [ ] Consultation records
- [ ] Community needs assessment
- [ ] Social investment program
- [ ] Local content and employment strategy
- [ ] Community development agreement

**Labor and Human Rights:**
- [ ] Labor practices review
- [ ] Wages and benefits comparison to local standards
- [ ] Freedom of association
- [ ] Non-discrimination policies
- [ ] Gender equity policies
- [ ] Human rights due diligence

**Gender Analysis:**
- [ ] Gender impact assessment
- [ ] Women's employment opportunities
- [ ] Gender-based violence and harassment prevention
- [ ] Women-owned business opportunities in supply chain

#### Governance Assessment

**Corporate Governance:**
- [ ] Board structure and independence
- [ ] Management team track record
- [ ] Financial controls and internal audit
- [ ] Risk management framework
- [ ] Transparency and disclosure practices
- [ ] Dividend and profit distribution policies

**Business Integrity:**
- [ ] Anti-corruption policies and training
- [ ] Code of conduct
- [ ] Conflict of interest policies
- [ ] Whistleblower mechanism
- [ ] Third-party due diligence on agents and intermediaries
- [ ] Political contributions and lobbying
- [ ] Beneficial ownership transparency

**Tax Transparency:**
- [ ] Tax strategy and planning
- [ ] Transfer pricing policies
- [ ] Tax haven structure assessment
- [ ] Country-by-country reporting

---

### 2.5 Political and Country Risk Due Diligence Checklist

**Political Risk:**
- [ ] Political stability index
- [ ] Sovereign credit rating
- [ ] Expropriation risk assessment
- [ ] Political violence and civil unrest risk
- [ ] Government effectiveness and corruption indices
- [ ] Election cycles and political transitions
- [ ] Host government support letters

**Regulatory Framework:**
- [ ] Energy/sector regulatory framework
- [ ] Tariff setting and adjustment mechanism
- [ ] Regulatory body independence and capacity
- [ ] Track record of regulatory changes
- [ ] Investment treaty protections
- [ ] Dispute resolution mechanisms

**Currency and Transfer Risk:**
- [ ] Currency convertibility
- [ ] Foreign exchange availability
- [ ] Capital repatriation restrictions
- [ ] Transfer and convertibility risk assessment
- [ ] Exchange rate volatility
- [ ] Hedging options

**Economic Risk:**
- [ ] Macroeconomic stability
- [ ] Inflation trends
- [ ] Fiscal position
- [ ] Balance of payments
- [ ] Debt sustainability
- [ ] Banking sector health

**Risk Mitigation Options:**
- [ ] Political risk insurance (PRI) options
- [ ] Multilateral Investment Guarantee Agency (MIGA) coverage
- [ ] Export credit agency (ECA) support
- [ ] Bilateral investment treaty (BIT) protections
- [ ] Government guarantees

---

### 2.6 Commercial Due Diligence Checklist

**Market Analysis:**
- [ ] Market size and growth projections
- [ ] Demand drivers and trends
- [ ] Supply-demand balance
- [ ] Market segmentation
- [ ] Pricing trends and benchmarks
- [ ] Seasonality and cyclicality
- [ ] Import/export dynamics

**Competitive Analysis:**
- [ ] Competitive landscape
- [ ] Market share analysis
- [ ] Competitor profiles (capacity, cost structure)
- [ ] Barriers to entry
- [ ] Competitive advantages of the project
- [ ] Substitute products/technologies
- [ ] New entrant threat

**Customer and Offtake:**
- [ ] Offtaker credit rating and financial capacity
- [ ] Offtake agreement terms (take-or-pay, price adjustment)
- [ ] Customer concentration risk
- [ ] Alternative offtake options
- [ ] Demand risk allocation

**Revenue Model Validation:**
- [ ] Pricing assumptions and benchmarks
- [ ] Volume assumptions
- [ ] Escalation clauses
- [ ] Revenue sensitivity to key variables
- [ ] Contract backlog (if applicable)

**Supply Chain:**
- [ ] Feedstock/raw material availability
- [ ] Supplier concentration
- [ ] Supply contract terms
- [ ] Price volatility and hedging
- [ ] Logistics and transportation

---

## 3. Investment Memo Structure

### Purpose
The Investment Memo (IM) is the primary document presented to the Investment Committee to seek approval for an investment. It synthesizes all due diligence findings, presents the investment thesis, and recommends a course of action.

### Recommended Structure

---

#### 3.1 EXECUTIVE SUMMARY (1-2 pages)

**Key Elements:**
- **Investment Highlights:** 2-3 sentence overview of the opportunity
- **Sponsor:** Brief description and track record
- **Location:** Country, region, specific site
- **Sector:** Specific sub-sector (e.g., Solar PV, Healthcare, Financial Services)
- **Project Description:** 3-4 sentences describing what the project does
- **Total Project Cost:** USD amount
- **DFI Financing:** Amount, instrument (senior debt, subordinated debt, equity, guarantee)
- **Terms:** Tenor, interest rate/return, security
- **Co-Financiers:** Other DFIs, commercial banks, sponsors
- **Key Financial Metrics:**
  - Project IRR: X%
  - Equity IRR: Y%
  - DSCR: Z.Xx (minimum)
  - Debt/Equity Ratio: X:Y
- **Development Impact Summary:** Jobs, emissions reduction, SDG alignment
- **ESG Risk Rating:** A, B+, B, C (per IFC categorization)
- **Country Risk Rating:** Sovereign rating or internal assessment
- **Additionality Statement:** 2-3 sentences on financial and value additionality
- **Recommendation:** Approve / Approve with conditions / Defer / Reject

---

#### 3.2 PROJECT OVERVIEW (2-3 pages)

**Sponsor Profile:**
- Company name, incorporation, ownership structure
- Management team (key individuals, experience)
- Track record in similar projects
- Financial capacity
- Corporate governance assessment
- Reputation and ESG track record

**Project Description:**
- Detailed description of the project (technology, capacity, output)
- Location details and site conditions
- Project timeline (development, construction, operations)
- Key project milestones
- Current status (development stage, permits obtained)

**Sector Context:**
- Sector overview and importance to country development
- Market dynamics (supply, demand, pricing)
- Regulatory environment
- Sector growth trends
- Competitive landscape

**Transaction Structure:**
- Corporate structure diagram
- Sources and uses of funds table
- DFI role and instrument
- Co-financiers and terms
- Security package
- Step-in rights and control mechanisms

---

#### 3.3 INVESTMENT RATIONALE (2-3 pages)

**Strategic Fit:**
- Alignment with DFI's sector and geographic priorities
- Contribution to DFI's strategic objectives
- Fit with portfolio diversification strategy

**Development Impact:**
- Economic impact (GDP contribution, tax revenues)
- Job creation (direct, indirect, induced)
  - Number of jobs
  - Gender disaggregation
  - Skill level
- Environmental benefits
  - GHG emissions avoided (tCO2e)
  - Renewable energy generated (MWh)
  - Energy saved
  - Water conserved
- Social benefits
  - People served (e.g., patients, students, customers)
  - Improved access (e.g., to electricity, healthcare, finance)
  - Affordability improvements
- SDG Alignment (identify primary SDGs and specific targets)
  - SDG 7: Affordable and Clean Energy
  - SDG 8: Decent Work and Economic Growth
  - SDG 13: Climate Action
  - Others as applicable

**Additionality:**
- **Financial Additionality:**
  - Project could not be financed on commercial terms alone
  - DFI financing fills a market gap
  - Tenor, pricing, or risk appetite not available commercially
  - Catalyzing co-investment from others

- **Value Additionality (Non-Financial):**
  - Technical assistance or capacity building provided
  - ESG support and monitoring
  - Governance improvements
  - Demonstration effect / market creation
  - Bringing international best practices

**Replicability and Market Development:**
- Potential for model to be replicated
- Market signaling effect
- Crowding-in of private capital
- Policy dialogue opportunities

---

#### 3.4 FINANCIAL ANALYSIS (3-4 pages)

**Financial Model Overview:**
- Model structure and key assumptions
- Base case scenario description
- Revenue assumptions (volume, price, escalation)
- Operating cost assumptions
- Capital expenditure plan
- Financing plan and debt service

**Key Financial Metrics:**

| Metric | Base Case | Upside Case | Downside Case | Threshold |
|--------|-----------|-------------|---------------|-----------|
| Project IRR | X% | Y% | Z% | >10% |
| Equity IRR | X% | Y% | Z% | >15% |
| Min DSCR | X.Xx | X.Xx | X.Xx | >1.25x |
| Avg DSCR | X.Xx | X.Xx | X.Xx | >1.40x |
| LLCR | X.Xx | X.Xx | X.Xx | >1.20x |
| Payback Period | X years | X years | X years | <10 years |

**Sensitivity Analysis:**
Present impact on key metrics from changes in:
- Revenue (-10%, -20%)
- Operating costs (+10%, +20%)
- Capital costs (+10%, +20%)
- Interest rates (+1%, +2%)
- Foreign exchange rate (-10%, -20% depreciation)
- Delay in COD (6 months, 12 months)

**Scenario Analysis:**
- **Base Case:** Most likely scenario given available information
- **Upside Case:** Optimistic but plausible scenario
- **Downside Case:** Stress scenario but still allows debt service
- **Break-even Analysis:** Identify key variables at which project breaks even

**Financial Strengths:**
- List 3-5 key financial strengths

**Financial Risks:**
- List 3-5 key financial risks and mitigations

**Covenant Structure:**
- Financial covenants (DSCR, Debt/Equity, Current Ratio)
- Affirmative and negative covenants
- Events of default

**Pricing and Returns:**
- DFI pricing (spread over benchmark, all-in rate)
- Return on DFI's investment
- Comparison to DFI's hurdle rate
- Comparison to risk-adjusted benchmark

---

#### 3.5 RISK ASSESSMENT (3-4 pages)

**Risk Matrix Summary:**

| Risk Category | Risk Level | Key Risks | Mitigations |
|---------------|------------|-----------|-------------|
| Credit Risk | Medium | [List] | [List] |
| Construction Risk | Medium-High | [List] [List] |
| Technology Risk | Low | [List] | [List] |
| Operational Risk | Low-Medium | [List] | [List] |
| Market/Revenue Risk | Medium | [List] | [List] |
| ESG Risk | Medium | [List] | [List] |
| Political/Country Risk | Medium-High | [List] | [List] |
| Currency Risk | Medium | [List] | [List] |
| Regulatory Risk | Low-Medium | [List] | [List] |

**Detailed Risk Analysis:**

For each material risk category, provide:

**1. Construction Risk**
- **Risks:**
  - Cost overruns due to [specify]
  - Schedule delays due to [specify]
  - Contractor default
  - Force majeure events

- **Mitigations:**
  - Fixed-price, date-certain EPC contract
  - Experienced contractor with track record
  - Liquidated damages for delay
  - Performance bonds and parent guarantees
  - Construction insurance
  - Independent engineer oversight
  - Adequate contingency budget
  - Conditions precedent for disbursement tied to milestones

**2. Revenue/Market Risk**
- **Risks:**
  - Demand lower than projected
  - Pricing pressure
  - Offtaker credit risk
  - Contract renegotiation

- **Mitigations:**
  - Long-term offtake agreement (take-or-pay)
  - Investment-grade offtaker
  - Government guarantee (if applicable)
  - Market demand studies by independent consultant
  - Diversified customer base
  - Price escalation mechanisms

**3. ESG Risk**
- **Risks:**
  - Environmental incidents (spills, accidents)
  - Community opposition or grievances
  - Labor disputes
  - Reputational risk from ESG non-compliance

- **Mitigations:**
  - Comprehensive ESMS implementation
  - ESAP with clear milestones and monitoring
  - Independent ESG monitoring consultant
  - Grievance mechanism in place
  - Regular reporting to DFI
  - Covenant to maintain IFC PS compliance
  - Site visits and audits

**4. Political/Country Risk**
- **Risks:**
  - Political instability
  - Expropriation
  - Currency inconvertibility
  - Regulatory changes
  - Breach of contract by government entities

- **Mitigations:**
  - Political risk insurance (MIGA, ECAs)
  - Government support letters or guarantees
  - Bilateral investment treaty protections
  - Project agreement with government
  - Dispute resolution clause (international arbitration)
  - Co-investment with other DFIs (deterrent effect)

**5. Currency Risk**
- **Risks:**
  - Local currency depreciation affecting debt service
  - Limited availability of foreign exchange
  - Transfer restrictions

- **Mitigations:**
  - Revenue in hard currency or indexed to USD
  - Natural hedge (costs and revenues in same currency)
  - Currency hedging instruments (if available)
  - OPIC/DFC/MIGA coverage for inconvertibility
  - Foreign exchange reserve account

**Overall Risk Rating:**
- Assign overall risk rating: Low / Low-Medium / Medium / Medium-High / High
- Justify rating based on balance of risks and mitigations

---

#### 3.6 ESG COMPLIANCE (2-3 pages)

**ESG Categorization:**
- Category A: Significant adverse environmental or social risks (requires full ESIA)
- Category B: Limited adverse environmental or social risks (focused ESIA)
- Category C: Minimal or no adverse risks
- Category FI: Financial intermediary investments

**Environmental Assessment:**
- Summary of key environmental impacts
- Mitigation measures
- Environmental permits status
- Climate risk assessment results
- GHG emissions (absolute and avoided)

**Social Assessment:**
- Community impacts (positive and negative)
- Resettlement requirements (if any)
- Job creation breakdown
- Stakeholder engagement summary
- Key social risks and mitigations

**IFC Performance Standards Compliance:**
- Gap analysis against each applicable PS
- ESAP summary (key actions, timeline, responsibility)
- Notable gaps and remediation plan

**Development Impact Metrics:**
Quantified metrics aligned with HIPSO/IRIS+ framework:

| Indicator | Baseline | Year 1 Target | Year 3 Target | Year 5 Target |
|-----------|----------|---------------|---------------|---------------|
| Direct Jobs | 0 | 50 | 200 | 200 |
| - Women (%) | - | 30% | 30% | 30% |
| Indirect Jobs | 0 | 100 | 300 | 300 |
| GHG Avoided (tCO2e/yr) | 0 | 10,000 | 50,000 | 50,000 |
| Energy Generated (MWh/yr) | 0 | 20,000 | 100,000 | 100,000 |
| People Served | 0 | 50,000 | 200,000 | 200,000 |

**SDG Alignment:**
- Primary SDGs with specific targets
- Contribution narrative for each SDG

**Gender Analysis:**
- Women's employment in project
- Gender-responsive design elements
- Women-owned businesses in supply chain

**Governance Assessment:**
- Corporate governance rating
- Business integrity due diligence summary
- Any red flags and how addressed

**ESG Covenants:**
- ESAP implementation covenant
- Reporting requirements
- Right to conduct ESG audits
- Material incident reporting

---

#### 3.7 TERMS AND CONDITIONS (1-2 pages)

**Financing Terms:**
- **Instrument:** Senior Secured Debt / Subordinated Debt / Equity / Guarantee / Blended
- **DFI Commitment:** USD [X] million
- **Tenor:** [X] years
- **Grace Period:** [X] years
- **Amortization:** [Structure, e.g., semi-annual, sculpted to cash flow]
- **Interest Rate:** [X]% fixed or [SOFR/LIBOR + X%] floating
- **Fees:**
  - Commitment fee: [X]% per annum on undrawn amounts
  - Management fee: [X]% upfront
- **Security:**
  - First-ranking security over project assets
  - Pledge of shares
  - Assignment of contracts (EPC, offtake, supply)
  - Offshore escrow accounts
  - Any other security

**Financial Covenants:**
- Minimum DSCR: [X.Xx]
- Maximum Debt/Equity: [X%]
- Minimum Current Ratio: [X.Xx]
- Maximum Total Debt: [USD X million]

**Other Key Covenants:**
- Restrictions on additional debt
- Dividend restrictions (e.g., DSCR >1.3x for last two periods)
- Restrictions on change of control
- Asset disposal restrictions
- Maintenance of insurance
- ESAP implementation
- Reporting requirements

**Conditions Precedent (CP):**
Key conditions to be satisfied before disbursement:
- Financial close of all financing
- Effectiveness of all material contracts (EPC, offtake, supply)
- All material permits and licenses obtained
- Equity contribution evidence
- Security perfection
- Insurance policies in place
- ESAP approved
- Legal opinions delivered
- Government approvals (if required)
- Offshore accounts opened

**Conditions Subsequent (CS):**
Conditions to be satisfied post-disbursement within defined timeframe:
- Outstanding permits (if allowed)
- Certain ESAP actions (non-critical for disbursement)

**Other Terms:**
- Prepayment terms (voluntary and mandatory)
- Events of default
- Step-in rights
- Sponsor guarantees (if any)
- Governance rights (board observer, information rights)

---

#### 3.8 RECOMMENDATION AND NEXT STEPS (1 page)

**Recommendation:**
[Clear statement: "Management recommends that the Investment Committee approve..."]

**Rationale for Recommendation:**
- Summarize 3-5 key reasons supporting the recommendation
- Alignment with strategy, strong development impact, manageable risks, additionality

**Conditions to Approval (if any):**
- List any conditions that must be met before legal documentation proceeds
- e.g., "Approval is conditioned upon receipt of government support letter"

**Next Steps and Timeline:**

| Milestone | Target Date |
|-----------|-------------|
| IC Approval | [Date] |
| Term Sheet Signing | [Date] |
| Due Diligence Finalization | [Date] |
| Legal Documentation | [Date] - [Date] |
| Financial Close | [Date] |
| First Disbursement | [Date] |
| Construction Completion | [Date] |
| Commercial Operations Date (COD) | [Date] |

**Open Items:**
- Any outstanding issues to be resolved

**Approvals Required:**
- IC approval
- Board approval (if above certain threshold)
- Government approvals (for the DFI, if applicable)

---

#### 3.9 APPENDICES

**Appendix A: Project Summary Sheet (1-pager)**
- Quick reference summary of key terms, metrics, and parties

**Appendix B: Financial Model Outputs**
- Detailed financial statements (P&L, Balance Sheet, Cash Flow)
- Sources and uses table
- Debt sizing and sculpting
- Sensitivity tables
- Ratio calculations

**Appendix C: Risk Matrix**
- Comprehensive risk matrix with all identified risks, likelihood, impact, and mitigations

**Appendix D: Due Diligence Reports Summary**
- List of all DD reports received
- Summary of key findings and recommendations from each report

**Appendix E: ESG Documentation**
- ESIA executive summary
- ESAP summary table
- IFC PS gap analysis

**Appendix F: Legal Structure Chart**
- Corporate structure
- Security structure

**Appendix G: Map and Photos**
- Project location map
- Site photos

**Appendix H: Sponsor Information**
- Sponsor profile
- Management bios
- Financial statements of sponsor

---

## 4. Key Decision Criteria Framework

### Overview
DFI investment decisions are based on a multi-dimensional assessment that balances financial returns, development impact, risk management, and alignment with strategic priorities. Unlike purely commercial investors, DFIs have a dual mandate: to achieve financial sustainability while maximizing development outcomes.

---

### 4.1 Financial Return Criteria

**Hurdle Rate / Minimum IRR:**
- While specific thresholds vary by DFI and sector, typical expectations:
  - **Equity investments:** 12-20% IRR (depending on risk)
  - **Debt investments:** Risk-adjusted return above cost of capital
  - **Infrastructure projects:** 10-15% project IRR
  - **Higher-risk markets/sectors:** Higher required returns

- DFIs are still investors with mandates compelling them to expect a return on their capital, compensating for opportunity cost and credit risk

**Return Considerations:**
- Returns must be sufficient to ensure portfolio financial sustainability
- Risk-adjusted returns relative to country and sector risk
- Comparison to alternative investments with similar risk profile
- Long-term portfolio returns typically target 5-8% real return

**Financial Viability Metrics:**

| Metric | Typical Threshold | Purpose |
|--------|------------------|---------|
| Project IRR | >10-12% | Overall project viability |
| Equity IRR | >15-20% | Sponsor return adequacy |
| DSCR (minimum) | >1.20-1.35x | Debt service capacity under stress |
| DSCR (average) | >1.40-1.50x | Cushion for variability |
| LLCR | >1.20x | Loan life coverage |
| Debt/Equity Ratio | 60:40 to 75:25 | Leverage appropriateness |
| Payback Period | <10-12 years | Investor return timeline |

**Break-even Resilience:**
- Projects must demonstrate ability to service debt under reasonable downside scenarios
- Sensitivity analysis must show that under -20% revenue stress, DSCR remains >1.1x

---

### 4.2 Development Impact Criteria

Development impact is often equally important to financial returns in DFI decision-making.

**Impact Measurement Frameworks:**
- HIPSO (Harmonized Indicators for Private Sector Operations)
- IRIS+ (Impact Reporting and Investment Standards)
- Joint Impact Indicators (JII) - jobs, gender, climate
- Sustainable Development Goals (SDGs)

**Core Impact Dimensions:**

#### Economic Impact
- **GDP Contribution:** Project's contribution to national GDP
- **Tax Revenues:** Direct and indirect tax generation
- **Foreign Exchange:** Export earnings or import substitution
- **Economic Multiplier:** Indirect economic activity generated

#### Employment Impact
- **Direct Jobs Created:** Permanent positions during operations
  - Target: Significant job creation relative to investment size
  - Gender breakdown: % women employed
  - Skill levels: Unskilled, semi-skilled, skilled, professional
- **Indirect Jobs:** Employment in supply chain and induced in local economy
- **Construction Jobs:** Temporary employment during construction
- **Quality of Jobs:** Living wages, benefits, working conditions
- **Target:** At least 1 job per USD $50,000-$100,000 invested (varies by sector)

#### Environmental/Climate Impact
- **GHG Emissions Avoided:** tCO2e per year
  - Target for renewable energy: >100,000 tCO2e/year for large projects
- **Renewable Energy Generated:** MWh per year
- **Energy Access:** Number of people/households gaining access to electricity
- **Energy Saved:** Through efficiency projects (MWh)
- **Water Conserved:** Cubic meters per year
- **Waste Reduced:** Tons per year
- **Paris Agreement Alignment:** Contribution to NDCs (Nationally Determined Contributions)

#### Social Impact
- **People Served:** Number of beneficiaries (e.g., patients treated, students educated, customers served)
- **Improved Access:** To essential services (electricity, water, healthcare, education, finance)
- **Affordability:** Cost reduction for end-users
- **Gender Impact:**
  - Women employed (target >30% for many DFIs)
  - Women in management
  - Women-owned businesses in supply chain
  - Gender-responsive design
- **Community Development:** Local infrastructure, schools, health facilities

#### SDG Alignment
Projects must demonstrate clear alignment with one or more SDGs:
- **Primary SDG:** Most significant contribution
- **Secondary SDGs:** Additional contributions
- **Specific Targets:** Identify specific SDG targets addressed

**Most common SDGs for DFI investments:**
- SDG 7: Affordable and Clean Energy
- SDG 8: Decent Work and Economic Growth
- SDG 9: Industry, Innovation and Infrastructure
- SDG 13: Climate Action
- SDG 5: Gender Equality (cross-cutting)

**Impact Thresholds:**
- Projects must demonstrate material, measurable development impact
- Quantitative targets established and monitored
- Theory of change articulated (how investment leads to impact)

---

### 4.3 Additionality Criteria

Additionality is considered **"a threshold condition, sine qua non"** for DFI investment. Without additionality, DFI participation cannot be justified.

**Financial Additionality:**

DFIs must demonstrate that their investment fills a financing gap:
- **Market Gap:** Commercial finance not available on reasonable terms
- **Tenor Mismatch:** Long tenor needed not available commercially (e.g., 15-20 year loans)
- **Risk Appetite:** Project too risky for commercial lenders alone
- **Pricing:** Commercial pricing would make project unviable
- **Crowding In:** DFI participation enables participation of commercial co-lenders who would not invest alone
- **Counter-cyclical:** Investment during market downturn when commercial capital retreats

**Evidence of Financial Additionality:**
- Demonstrated efforts to secure commercial finance failed or inadequate
- Commercial terms (tenor, pricing, covenants) would make project unviable
- Credit rating/country risk too high for commercial lenders
- Market failure documentation (thin or non-existent capital markets)

**Value Additionality (Non-Financial):**

Beyond financing, DFIs add value through:
- **Technical Assistance:**
  - Pre-investment project development support
  - Transaction advisory
  - Capacity building for sponsor
- **ESG Support:**
  - Bringing international ESG standards (IFC PS)
  - ESG capacity building
  - Monitoring and reporting frameworks
- **Governance Improvements:**
  - Board representation or observer seats
  - Corporate governance advisory
  - Financial management systems improvement
- **Demonstration Effect:**
  - Pioneering new technologies or business models
  - Signaling viability to other investors
  - Market creation in frontier sectors
- **Policy Dialogue:**
  - Engaging with government on policy reforms
  - Regulatory framework improvements
  - Sector development initiatives
- **Mobilization:**
  - Catalyzing investment from other DFIs, pension funds, institutional investors
  - Reducing perceived risk through participation

**Additionality Assessment:**
- DFI must establish and document a credible narrative regarding additionality
- Supported by data and evidence from credible sources
- Assessment is binary: either additional or not
- If not additional, investment should not proceed (risk of "crowding out" private sector)

---

### 4.4 Risk Tolerance and Management

**Risk Appetite:**
- DFIs accept higher risk than commercial investors, but not unlimited risk
- Risk must be commensurate with expected return and development impact
- Risk acceptance balanced across portfolio

**Risk-Impact Trade-off:**
- DFIs recognize that high-impact projects may have higher risk or lower returns
- "Projects with high development impact and additionality may not always have the best credit"
- Explicit trade-offs are made and documented

**Risk Rating Scale:**
Typical DFI risk rating:
1. Excellent (minimal risk)
2. Good (low risk)
3. Satisfactory (acceptable risk)
4. Fair (elevated risk, requires close monitoring)
5. Watch (high risk, corrective action needed)
6. Substandard (serious problems, likely restructuring)
7. Doubtful (loss probable)
8. Loss (write-off)

**Investment Decision Thresholds:**
- Investments rated 1-3: Proceed if other criteria met
- Rating 4: Proceed only if strong development impact and mitigations in place
- Rating 5-6: Only in exceptional circumstances with Board approval
- Rating 7-8: No new investments

**Risk Management Requirements:**
- Comprehensive risk assessment in IM
- Clear risk mitigation measures for each material risk
- Risk allocation aligned with party best able to manage
- Political risk insurance for high country risk
- Security package commensurate with risk
- Covenants to monitor and control risk
- Active portfolio management and early warning systems

---

### 4.5 Strategic Fit and Portfolio Considerations

**Geographic Priorities:**
- Alignment with DFI's geographic mandate
- Specific country or region priorities
- Frontier vs established markets
- Concentration limits by country

**Sector Priorities:**
- Alignment with sector strategy
- Priority sectors (varies by DFI):
  - Infrastructure (power, transport, water)
  - Renewable energy and climate
  - Financial institutions (SME finance, financial inclusion)
  - Healthcare
  - Education
  - Agribusiness
  - Manufacturing
- Emerging priorities: digitalization, climate adaptation, pandemic resilience

**Ticket Size:**
- Minimum investment size (e.g., $5-10 million)
- Maximum investment size (portfolio concentration)
- Efficient use of resources (due diligence costs relative to investment)

**Portfolio Diversification:**
- Single obligor limits
- Country concentration limits
- Sector concentration limits
- Currency exposure limits

**Catalytic and Innovative Projects:**
- First-of-kind projects given priority
- Projects that can demonstrate new models
- Potential for replication and scale

---

### 4.6 ESG and Safeguards Compliance

**Non-Negotiable Requirements:**
- Full compliance with IFC Performance Standards (or equivalent)
- No Category A projects without full ESIA and stakeholder consultation
- Compliance with Exclusion List (no tobacco, weapons, etc.)
- No projects with high residual ESG risks without mitigation

**ESG Decision Factors:**
- ESG risk rating (A, B+, B, C)
- Comprehensiveness of ESMS
- Sponsor's capacity and commitment to implement ESAP
- Reputational risk assessment
- Potential for ESG controversy or opposition
- Climate risk assessment results

**ESG as Deal-Breaker:**
- Serious ESG gaps can lead to deal rejection
- Projects with community opposition or unresolved land conflicts often paused
- Lack of sponsor commitment to ESG compliance is red flag

---

### 4.7 Replicability and Market Development

**Demonstration Value:**
- Can this project be a model for others?
- Does it prove viability of a technology, business model, or structure?
- Will it attract other investors to the sector/market?

**Crowding-In Potential:**
- Does DFI participation enable commercial co-investment?
- Will project success lead to commercial investment in follow-on projects?
- Market signaling effect

**Sectoral Impact:**
- Contribution to sector development beyond single project
- Policy dialogue opportunities
- Standard-setting (e.g., ESG, governance)

---

### 4.8 Decision-Making Process

**Comparative Assessment:**
- ICs review multiple projects in a portfolio context
- Better projects prioritized when capital constrained
- Development impact per dollar invested
- Risk-adjusted returns

**Typical IC Decision Criteria Weighting (Illustrative):**

This varies significantly by DFI, but an illustrative framework:

| Criterion | Weight | Assessment |
|-----------|--------|------------|
| Financial Viability & Returns | 25% | IRR, DSCR, financial sustainability |
| Development Impact | 30% | Jobs, climate, SDG alignment, impact per $ |
| Additionality | 20% | Financial and value additionality clearly demonstrated |
| Risk & Mitigations | 15% | Acceptable risk with adequate mitigations |
| ESG Compliance | 10% | IFC PS compliance, ESAP adequacy |

(Note: Some DFIs use a pass/fail assessment for each dimension rather than weighted scoring)

**Deal Killers (Red Flags):**
- Lack of additionality (crowding out private sector)
- Serious ESG violations or sponsor unwillingness to address gaps
- Unsustainable financial structure (inadequate debt service coverage)
- Sponsor integrity issues (corruption, sanctions)
- Unmitigated catastrophic risks
- Misalignment with DFI mandate or strategy
- Reputational risk exceeds benefit

**Approval Thresholds:**
- Projects below certain $ threshold: IC approval sufficient
- Projects above threshold: Board approval required
- Very large or high-risk projects: Additional governance approvals

---

## 5. Reporting Requirements and Metrics

### Overview
Post-investment monitoring and reporting are critical to ensuring projects deliver expected financial returns and development impacts, comply with ESG standards, and manage risks. Reporting requirements are specified in legal agreements and enforced through covenants.

---

### 5.1 Frequency of Reporting

**During Construction Phase:**
- **Monthly:** Construction progress reports
- **Quarterly:** Financial reports (expenditures vs budget)
- **Ad-hoc:** Material events (delays, cost overruns, accidents, regulatory issues)

**During Operations Phase:**
- **Quarterly:** Financial statements and operational KPIs
- **Semi-annually:** Development impact metrics (some DFIs)
- **Annually:**
  - Audited financial statements
  - ESG compliance reports
  - Development impact reports
  - Corporate governance updates
- **Ad-hoc:** Material events, incidents, covenant breaches

---

### 5.2 Financial Reporting

**Quarterly Financial Statements:**
- Income statement (P&L)
- Balance sheet
- Cash flow statement
- Notes to financial statements
- Comparison to budget and prior period
- Narrative explaining variances

**Key Financial Metrics to Track:**

| Metric | Reporting Frequency | Covenant Threshold (Example) |
|--------|-------------------|----------------------------|
| Revenue | Quarterly | N/A (monitoring only) |
| EBITDA | Quarterly | N/A (monitoring only) |
| Debt Service Coverage Ratio | Quarterly | >1.25x |
| Current Ratio | Quarterly | >1.2x |
| Debt-to-Equity Ratio | Quarterly | <70:30 |
| Total Outstanding Debt | Quarterly | <USD X million |
| Cash and Cash Equivalents | Quarterly | Minimum USD X million |
| Capex vs Budget | Quarterly (construction) | Within 110% of approved budget |

**Annual Audited Financials:**
- Full audited financial statements prepared by reputable audit firm
- Auditor's opinion (unqualified opinion required)
- Due within 120-180 days of fiscal year end
- Management discussion and analysis

**Other Financial Reporting:**
- Utilization of loan proceeds (during disbursement)
- Debt service payment confirmations
- Insurance policy renewals
- Project completion certificate (post-construction)

---

### 5.3 Operational Reporting

**Key Performance Indicators (KPIs):**

KPIs vary by sector. Examples:

**Power Generation Project:**
| KPI | Unit | Reporting Frequency |
|-----|------|-------------------|
| Generation Output | MWh | Monthly/Quarterly |
| Plant Availability | % | Monthly/Quarterly |
| Capacity Factor | % | Monthly/Quarterly |
| Forced Outage Rate | % | Quarterly |
| Planned Maintenance Days | Days | Quarterly |
| Fuel Consumption | Tons/m³ | Quarterly |
| Operating Costs | USD/MWh | Quarterly |

**Healthcare Project:**
| KPI | Unit | Reporting Frequency |
|-----|------|-------------------|
| Patient Visits | Number | Quarterly |
| Bed Occupancy Rate | % | Quarterly |
| Average Length of Stay | Days | Quarterly |
| Revenue per Patient | USD | Quarterly |
| Operating Margin | % | Quarterly |

**Financial Institution:**
| KPI | Unit | Reporting Frequency |
|-----|------|-------------------|
| Loan Portfolio Size | USD | Quarterly |
| Number of Borrowers | Number | Quarterly |
| Portfolio at Risk >30 days | % | Quarterly |
| Non-Performing Loan Ratio | % | Quarterly |
| Capital Adequacy Ratio | % | Quarterly |
| Return on Assets | % | Quarterly |
| Return on Equity | % | Quarterly |

---

### 5.4 Development Impact Reporting

DFIs increasingly use **harmonized indicators** through frameworks like HIPSO and IRIS+.

**Core Impact Indicators (Aligned with HIPSO/IRIS+):**

#### Jobs Indicators

| Indicator | Definition | Reporting Frequency |
|-----------|-----------|-------------------|
| #Direct Jobs | Full-time equivalent permanent jobs | Annual |
| - #Women | Number of women employed | Annual |
| - %Women | Percentage of women employed | Annual |
| #Temporary Jobs | Construction or seasonal jobs | Annual |
| #Indirect Jobs | Jobs in supply chain (estimated) | Annual (or one-time) |
| Avg. Wage | Average monthly wage | Annual |
| Living Wage Benchmark | % of living wage paid | Annual |

**Methodology notes:**
- Jobs measured as full-time equivalents (FTEs)
- Gender disaggregation mandatory
- Indirect jobs estimated using multipliers or surveys

#### Climate and Environment Indicators

| Indicator | Definition | Reporting Frequency |
|-----------|-----------|-------------------|
| GHG Emissions Avoided | tCO2e per year (relative to baseline) | Annual |
| GHG Emissions Absolute | tCO2e per year (scope 1, 2, 3) | Annual |
| Renewable Energy Generated | MWh per year | Annual |
| Energy Saved | MWh per year (efficiency projects) | Annual |
| Water Consumed | m³ per year | Annual |
| Water Saved | m³ per year (efficiency projects) | Annual |
| Waste Generated | Tons per year | Annual |
| Waste Recycled | Tons per year | Annual |

**Methodology notes:**
- GHG calculations follow GHG Protocol
- Additionality calculation for emissions avoided
- Climate metrics increasingly mandatory for all projects

#### People Served / Beneficiaries

| Indicator | Definition | Sector Example | Reporting Frequency |
|-----------|-----------|---------------|-------------------|
| #People Served | Beneficiaries reached | Households electrified (power); Patients treated (health); Students (education) | Annual |
| - #Women | Women beneficiaries | | Annual |
| - %Underserved | Low-income or underserved populations | | Annual |

#### Financial Inclusion (Financial Intermediary Investments)

| Indicator | Definition | Reporting Frequency |
|-----------|-----------|-------------------|
| #MSMEs Financed | Number of MSMEs receiving loans | Annual |
| #Women-Owned MSMEs | Women-owned businesses financed | Annual |
| Volume of MSME Loans | Total USD loaned to MSMEs | Annual |
| Avg. Loan Size | Average loan size | Annual |

#### SDG Contribution Tracking

Projects report contribution to specific SDG targets:

- SDG 7.1: Access to affordable, reliable, modern energy
- SDG 8.5: Decent work and equal pay
- SDG 13.2: Integrate climate measures into policies
- Etc.

**Reporting format:**
- Quantitative indicators mapped to SDG targets
- Narrative on contribution and progress

---

### 5.5 ESG Compliance Reporting

**Environmental and Social Action Plan (ESAP) Progress:**
- Status of each ESAP action item
- Timeline vs actual completion
- Explanation of delays
- Evidence of completion (photos, reports, certificates)
- Typically reported quarterly or semi-annually

**Environmental Monitoring:**
- Air quality monitoring results
- Water quality (abstraction and discharge)
- Noise levels
- Waste disposal records
- Hazardous materials management

**Social Monitoring:**
- Community engagement activities
- Grievances received and resolved
- Resettlement progress (if applicable)
- Community investment activities

**Incident Reporting:**
- Environmental incidents (spills, exceedances)
- Health and safety incidents
  - Lost Time Injury Frequency Rate (LTIFR)
  - Fatalities (immediate reporting)
  - Serious injuries
- Community incidents
- Security incidents

**Materiality Threshold:**
- Major incidents: Within 24-48 hours
- Fatalities: Immediate notification
- Annual summary of all incidents

**Labor and Human Rights:**
- Employment breakdown (gender, local/expat)
- Labor turnover
- Training hours
- Collective bargaining status
- Grievances received and resolved

**Gender Reporting:**
- Women employed (absolute and %)
- Women in management
- Women in governance (board)
- Gender pay gap analysis
- Gender-based violence and harassment (GBVH) incidents and prevention measures

**ESG Compliance Certificate:**
- Annual certificate from project company confirming compliance with ESG covenants
- Signed by authorized officer

---

### 5.6 Risk and Covenant Compliance Reporting

**Financial Covenant Compliance:**
- Quarterly compliance certificate
- Calculation of each financial covenant
- Certification of compliance or disclosure of breach
- If breach: explanation and remediation plan

**Non-Financial Covenant Compliance:**
- Confirmation of compliance with affirmative covenants (e.g., maintain insurance, maintain permits)
- Confirmation of compliance with negative covenants (e.g., no additional debt, no asset sales)

**Risk Indicators / Early Warning Signals:**
- Material adverse changes in business environment
- Changes in management
- Disputes with offtakers, suppliers, government
- Regulatory changes affecting project
- Force majeure events
- Credit rating downgrades (if rated)

---

### 5.7 Site Visits and Portfolio Reviews

**On-Site Supervision:**
- DFI conducts periodic site visits (annual or bi-annual)
- More frequent during construction
- Independent engineers or ESG consultants may conduct visits

**Site Visit Objectives:**
- Physical inspection of project progress/conditions
- Meetings with management
- Verification of reported information
- ESG compliance spot-checks
- Community engagement observation
- Identification of issues not evident in reports

**Portfolio Review Meetings:**
- Regional investment teams regularly review portfolios with senior management
- Risk ratings updated
- Problem projects identified for intensive support or workout

---

### 5.8 Reporting Platforms and Systems

**Reporting Submission:**
- Typically through secure online portal
- Standardized templates provided by DFI
- Required file formats (PDF, Excel)

**Reporting Quality Requirements:**
- Complete: All required fields filled
- Accurate: Verified and reconciled data
- Timely: Submitted by due date
- Consistent: Methodologies consistent over time

**Consequences of Non-Reporting:**
- Formal notice of non-compliance
- Potential event of default if persistent
- Impacts future disbursements (if multi-tranche)
- Increased supervision (more frequent visits)
- Potential acceleration of loan

---

### 5.9 Public Disclosure and Transparency

**DFI Transparency Obligations:**
- Many DFIs commit to transparency standards (e.g., IFC Access to Information Policy)
- Project information disclosed on DFI websites:
  - Project summary
  - Environmental and social category
  - Development impact objectives
  - Investment amount and terms (summary)

**Aggregated Portfolio Reporting:**
- DFIs publish annual reports with portfolio-level impact metrics
- Aggregate HIPSO indicators reported
- SDG contribution reported at portfolio level

**Investee Confidentiality:**
- Detailed financial information typically confidential
- ESG documents often publicly available (ESIA summaries)
- Balance between transparency and commercial confidentiality

---

## 6. Common Bottlenecks and Solutions

### Overview
DFI investment processes, while thorough, often encounter bottlenecks that delay transactions, increase costs, or prevent deals from reaching financial close. Understanding these bottlenecks and implementing solutions is critical for improving efficiency.

---

### 6.1 Document Collection Bottlenecks

**Problem:**
- Sponsors fail to provide required due diligence documents on time
- Documents provided are incomplete, outdated, or in wrong format
- Repeated requests and follow-ups delay process
- Studies find that businesses lose 21% of productivity due to poor document handling, with employees wasting 5 hours weekly searching for files

**Root Causes:**
- Sponsor lacks capacity or resources to compile documents
- Sponsor doesn't understand what's needed (despite checklist)
- Documents don't exist (e.g., financial statements not audited, no ESMS)
- Sponsor prioritizes other activities over DFI requests
- Multiple DFIs and lenders requesting overlapping but slightly different documents

**Impact:**
- Due diligence phase drags from 3-6 months to 9-12 months
- Increased transaction costs
- Deal momentum lost; sponsors frustrated
- Market or regulatory conditions may change, affecting viability

**Solutions:**

1. **Upfront Document Checklist with Clarity:**
   - Provide comprehensive checklist at screening stage
   - Include examples and templates
   - Specify format, version, and language requirements
   - Explain why each document is needed (context helps sponsors prioritize)

2. **Phased Document Requests:**
   - Phase 1: Critical documents for initial assessment
   - Phase 2: Detailed DD documents after initial approval
   - Phase 3: Legal close documents
   - Prevents overwhelming sponsor upfront

3. **Document Room / Virtual Data Room:**
   - Set up secure online data room early
   - Sponsor uploads documents directly
   - DFI team and advisors can access centrally
   - Track document status (pending, uploaded, reviewed, approved)
   - Automated reminders for missing documents

4. **Dedicated Document Coordination:**
   - Assign a document coordinator (from sponsor side)
   - Single point of contact for all document requests
   - Regular check-in calls on document status

5. **Standardization Across DFIs:**
   - DFIs collaborating on a deal should harmonize document requests
   - Joint due diligence where possible
   - Share due diligence reports among co-lenders (with sponsor consent)

6. **Technical Assistance for Document Preparation:**
   - For frontier markets or first-time sponsors, DFI provides TA grant
   - Support for preparing financial models, ESIA, business plan
   - Increases quality and speed of document provision

**CRM Implication:**
- Document tracking module with status indicators
- Automated reminder emails
- Document version control
- Integration with virtual data room

---

### 6.2 Compliance Gaps (ESG, Permits, Legal)

**Problem:**
- During due diligence, gaps identified in ESG compliance, permits, or legal documentation
- Sponsor must remediate gaps before DFI can proceed
- Remediation can take months or years (e.g., obtaining environmental permit)
- 93% of fintechs find it challenging to meet compliance requirements

**Specific ESG Gaps:**
- No Environmental Impact Assessment conducted
- Community consultation insufficient or absent
- Resettlement not addressed
- Labor practices don't meet IFC PS2 standards
- No grievance mechanism in place
- Biodiversity risks not assessed

**Permit Gaps:**
- Key permits not obtained (environmental license, construction permit)
- Permits expired or in renewal process
- Regulatory approvals pending (tariff approval, concession agreement)

**Legal Gaps:**
- Land title unclear or disputed
- Key contracts not finalized (EPC, offtake)
- Shareholder agreements missing provisions required by DFI
- Corporate registration not complete

**Impact:**
- Deal placed on hold pending gap closure
- Sponsor incurs unexpected costs for studies, consultants
- Project timeline slips
- In some cases, gaps cannot be closed, deal aborted

**Solutions:**

1. **Early Screening for Major Gaps:**
   - High-level ESG and legal screening at initial review stage
   - Red-flag major gaps early (e.g., "No ESIA has been conducted")
   - Decision: Is sponsor willing and able to close gaps? If not, decline early.

2. **Gap Closure as Condition Precedent:**
   - IC approval "subject to satisfactory closure of identified gaps"
   - Clearly define what "satisfactory closure" means
   - Timeline and milestones for gap closure
   - If not closed by target date, deal can be abandoned

3. **ESAP (Environmental and Social Action Plan):**
   - Document all ESG gaps and required actions in ESAP
   - Assign responsibility, timeline, and verification method for each action
   - Some actions can be Conditions Precedent (must close before disbursement)
   - Others can be Conditions Subsequent (close within X months after disbursement)
   - Prioritization: Critical gaps vs. nice-to-have improvements

4. **Technical Assistance for Gap Closure:**
   - DFI provides grant or concessional loan for compliance studies
   - E.g., funding for ESIA, resettlement plan, labor audit
   - Accelerates gap closure and ensures quality

5. **Structured Legal Close Process:**
   - Legal checklist with all required documents and actions
   - Legal advisors track progress on legal gaps
   - Weekly status calls during legal documentation phase
   - "Long-stop date" in term sheet: if legal close not achieved by date X, deal terminates

6. **Engagement with Government/Regulators:**
   - For permits and approvals, DFI can engage with government
   - Letters of support or facilitation
   - Policy dialogue to address systemic bottlenecks (e.g., slow permit processes)

**CRM Implication:**
- Gap tracking module (ESAP tracker)
- Status of each gap: Open, In Progress, Closed, Overdue
- Alert system for overdue gap closure
- Integration with conditions precedent tracking

---

### 6.3 Financial Model Validation and Assumptions Clarity

**Problem:**
- Sponsor's financial model is incomplete, has errors, or uses unrealistic assumptions
- DFI's financial advisors raise questions; model must be revised
- Multiple iterations of model and back-and-forth on assumptions
- Lack of consensus on key assumptions (e.g., tariff escalation, demand growth)

**Common Model Issues:**
- Errors in formulas (Excel errors)
- Opaque structure (hard to follow logic)
- Revenue assumptions not supported by market studies
- Cost assumptions too optimistic
- No sensitivity analysis
- Currency mismatch (revenues in local, debt in USD, no hedge)
- Debt sizing doesn't meet lender requirements (DSCR too low)

**Impact:**
- Delays in financial DD completion
- Erosion of confidence in sponsor's capacity
- Potential deal redesign (e.g., need more equity, less debt)
- Increased transaction costs for model rework

**Solutions:**

1. **Standard Financial Model Template:**
   - DFI provides financial model template
   - Standard structure, tabs, and formulas
   - Clear assumption input section
   - Built-in sensitivity and scenario analysis
   - Reduces errors and improves comparability

2. **Upfront Assumptions Workshop:**
   - Early in DD, conduct workshop with sponsor, DFI, and advisors
   - Agree on key assumptions and methodology
   - Document agreed assumptions in memo
   - Reference market studies, benchmarks, and precedents
   - Reduces later disputes

3. **Independent Financial Model Review:**
   - DFI hires independent financial advisor to review sponsor's model
   - Identify issues early
   - Provide constructive feedback to sponsor
   - Sponsor revises model; advisor re-reviews
   - Ideally, 2-3 iterations, not 10

4. **Benchmarking and Sensitivity:**
   - Require sponsor to benchmark assumptions against peers and market data
   - Sensitivity analysis on key variables mandatory
   - Downside scenario must still show adequate DSCR

5. **Model Audit Trail:**
   - Track model versions (v1, v2, v3, etc.)
   - Change log explaining what changed between versions
   - Sign-off by sponsor, advisors, and DFI on final model

6. **Training and Capacity Building:**
   - For less sophisticated sponsors, DFI provides training on financial modeling
   - Or funds a financial advisor to work with sponsor to build model

**CRM Implication:**
- Model version tracking
- Assumption register (key assumptions and their sources)
- Audit trail of model changes

---

### 6.4 Investment Committee Scheduling and Decision Delays

**Problem:**
- IC meetings held infrequently (e.g., once per month)
- IC members are senior executives with busy schedules
- Difficulty getting quorum
- Deal not ready in time for scheduled IC, must wait for next month
- IC defers decision, requests more information, deal cycles back

**Impact:**
- Deals delayed by 1-3 months waiting for IC slot
- Momentum lost; market conditions may change
- Sponsor frustration and potential deal fatigue

**Solutions:**

1. **Frequent IC Meetings:**
   - Schedule ICs more frequently (e.g., bi-weekly or even weekly)
   - Or have standing IC calls for urgent deals

2. **Tiered Approval Authority:**
   - Smaller deals (below threshold, e.g., <$10M): Delegated authority to CIO or IC sub-committee
   - Medium deals: Full IC
   - Large deals: IC + Board
   - Reduces IC burden and speeds smaller deals

3. **Rolling IC Pipeline Management:**
   - Maintain pipeline of deals approaching IC readiness
   - Forecast IC submissions 2-3 months ahead
   - Ensure deals are truly ready before IC submission (avoid deferrals)

4. **Pre-IC Review (IC Lite):**
   - Informal preliminary IC review (7-10 slides)
   - Get early feedback and directional approval
   - Identify issues that would cause deferral
   - Address before full IC submission
   - Increases likelihood of approval at full IC

5. **IC Materials Deadline Discipline:**
   - IC memos due 1 week before IC meeting (strict deadline)
   - IC members commit to pre-reading
   - IC meeting focused on Q&A and decision, not presentation of content

6. **Virtual IC Participation:**
   - Allow IC members to participate via video conference
   - Easier to achieve quorum

7. **Written Approval Process:**
   - For non-controversial deals, written approval (circulated for signature)
   - Reserve IC meetings for complex or contentious deals

**CRM Implication:**
- IC calendar and scheduling module
- Deal pipeline dashboard (stage tracking: pre-IC, IC-ready, IC-approved)
- IC materials checklist and submission tracking
- Automated notifications to IC members

---

### 6.5 Legal Documentation and Negotiation

**Problem:**
- Legal documentation phase takes 3-6 months
- Multiple rounds of negotiation on legal terms
- Disagreements on covenants, security, events of default, etc.
- Involvement of multiple lawyers (DFI counsel, sponsor counsel, co-lender counsels)
- In syndicated deals, aligning multiple lenders' requirements

**Common Sticking Points:**
- Covenant levels (how tight?)
- Security package (what assets, first vs second lien?)
- Events of default (what triggers default?)
- Sponsor guarantees
- Change of control provisions
- Representations and warranties
- Governing law and dispute resolution

**Impact:**
- Deals delayed post-IC approval
- Increased legal costs
- Risk that deal economics change during delay (e.g., interest rates rise)
- Sponsor frustration

**Solutions:**

1. **Term Sheet with Key Legal Terms:**
   - Detailed term sheet signed post-IC, pre-legal documentation
   - Cover major legal terms (covenants, security, defaults)
   - Reduces scope of negotiation during legal doc phase

2. **Standard Loan Agreement Templates:**
   - DFI uses standard form agreements as starting point
   - Sponsor counsel familiar with DFI's standard terms
   - Redlines focused on project-specific issues, not renegotiating standard clauses

3. **Joint Legal Documentation (Syndicated Deals):**
   - Co-lenders agree to use common legal documentation
   - One set of legal agreements for all lenders
   - Joint legal advisors or one lender's counsel as lead
   - Reduces duplication and conflicting requirements

4. **Parallel Legal Workstreams:**
   - While main loan agreement is negotiated, work in parallel on:
     - Security documents
     - Intercreditor agreement
     - Sponsor agreements (shareholder, subordination)
   - Don't wait for one document to be final before starting next

5. **Escalation Process for Disputes:**
   - If lawyers stuck on a point, escalate to business principals
   - Deal teams decide: Is this issue material? Can we compromise?
   - Avoid lawyers negotiating indefinitely on minor points

6. **Legal Close Checklist and Tracking:**
   - Comprehensive checklist of all legal documents and actions
   - Responsibility assigned (DFI, sponsor, co-lender, government)
   - Track progress weekly
   - Identify blockers early

7. **Conditions Precedent Waiver Authority:**
   - For minor CPs, delegate authority to legal team to waive or accept alternative evidence
   - Avoid need to reconvene IC for CP waiver approvals

**CRM Implication:**
- Legal documentation tracker (list of agreements, status, responsible party)
- Negotiation log (issues raised, position of each party, resolution)
- Conditions precedent tracker
- Automated alerts for long-stop date approaching

---

### 6.6 Co-Financier Coordination

**Problem:**
- DFI rarely finances 100% of a project; co-financing is common
- Coordinating with other DFIs, ECAs, commercial banks, equity investors
- Different institutions have different:
  - Due diligence requirements
  - Documentation standards
  - Approval processes and timelines
  - Covenant requirements
  - ESG frameworks
- One co-financier's delay holds up the entire deal

**Impact:**
- Extends timeline significantly (slowest lender sets the pace)
- Duplication of due diligence (each lender does their own)
  - Sponsor overwhelmed with requests
- Risk of deal falling apart if one lender drops out

**Solutions:**

1. **Lead Arranger Model:**
   - One DFI acts as lead arranger
   - Lead conducts due diligence on behalf of all lenders
   - Other lenders review and rely on lead's DD (with consent)
   - Lead negotiates terms; others join on same terms

2. **Joint Due Diligence:**
   - Co-financiers agree to jointly conduct DD
   - Share cost of advisors (legal, technical, financial, ESG)
   - Joint DD reports shared with all
   - Single set of site visits

3. **Harmonized Documentation:**
   - Common loan agreement for all lenders (parallel debt structure)
   - Intercreditor agreement defining rights among lenders
   - Reduces negotiation complexity

4. **Alignment of Timelines:**
   - Early coordination meeting among co-financiers
   - Agree on timeline: DD complete by X, IC approvals by Y, legal close by Z
   - Identify critical path and potential delays
   - Commit to meeting milestones

5. **Standardization of Requirements:**
   - DFIs increasingly adopting common standards (IFC PS, HIPSO metrics)
   - Reduces divergence in ESG and reporting requirements
   - Sponsors report once using standard templates

6. **Regular Co-Financier Coordination Calls:**
   - Weekly or bi-weekly calls among lenders during DD and legal phase
   - Share progress, raise issues, align on next steps

7. **Commitment Letters / Term Sheets Signed Simultaneously:**
   - Co-financiers aim to sign term sheets on same day (or within short window)
   - Signals alignment and momentum

**CRM Implication:**
- Co-financier tracking (list of co-financiers, roles, commitment amounts, status)
- Shared document repository access for co-financiers
- Timeline tracking with milestones for each co-financier
- Alerts if one co-financier falls behind

---

### 6.7 Government Approvals and Permits

**Problem:**
- Many projects require government approvals (concessions, tariff approvals, permits)
- Government processes are slow, opaque, and unpredictable
- Changes in government or policy can delay or derail approvals
- Corruption or bureaucratic inefficiency

**Common Approvals Needed:**
- Environmental permit (often slowest)
- Construction permit
- Operating license
- Tariff or pricing approval (for regulated sectors)
- Concession agreement
- Tax incentives or exemptions
- Land allocation or use permits
- Import permits for equipment

**Impact:**
- Delays of 6-12 months or more
- Uncertainty makes financial close impossible (lenders won't commit without key approvals)
- Costs escalate while waiting
- Risk of approval denial, killing the project

**Solutions:**

1. **Early Engagement with Government:**
   - Sponsor engages government early in project development
   - Understand approval process, timeline, requirements
   - Submit applications as early as possible
   - DFI can support through policy dialogue and engagement with ministries

2. **Government Support Letters:**
   - DFI requests letter of support from host government
   - Government commits to facilitating approvals
   - Signals political will and reduces risk of blockage

3. **Conditions Precedent vs Subsequent:**
   - Absolutely critical approvals: Condition Precedent (must have before disbursement)
   - Less critical approvals: Condition Subsequent (must obtain within X months after disbursement)
   - Allows deal to proceed while some approvals are in process
   - Risk mitigation: Escrow funds until approval obtained, or partial disbursement

4. **Government Guarantees:**
   - For government-related risks (e.g., tariff approval), government provides guarantee
   - E.g., "If tariff not approved within 6 months, government will provide alternate revenue mechanism"

5. **Parallel Processing:**
   - While government approval is pending, proceed with other workstreams (DD, legal drafting)
   - Be ready to close quickly once approval obtained

6. **Policy Dialogue and Advocacy:**
   - DFIs work with government to streamline approval processes
   - Support regulatory reforms (e.g., one-stop shop for permits)
   - Capacity building for regulators
   - Longer-term solution beyond individual project

7. **Political Risk Insurance:**
   - Insurance against government actions (expropriation, breach of contract)
   - Provides downside protection if approvals denied or revoked
   - MIGA, ECAs, private insurers

**CRM Implication:**
- Government approval tracker (list of required approvals, application date, expected date, status)
- Escalation alerts if approvals overdue
- Log of government engagement activities

---

### 6.8 Internal DFI Process Inefficiencies

**Problem:**
- DFIs themselves have internal bottlenecks
- Understaffing in key functions (legal, ESG, credit)
- Bureaucratic processes and multiple approval layers
- Siloed departments with poor communication
- Competing priorities (many deals competing for same resources)

**Impact:**
- Internal reviews take longer than planned
- Deals stall waiting for internal sign-offs
- Investment Officers frustrated
- Reputation risk (DFIs seen as slow and bureaucratic)

**Solutions:**

1. **Adequate Resourcing:**
   - Staff teams appropriately for deal volume
   - Hire specialists (ESG, legal, financial analysts)
   - Use external advisors to supplement capacity during peaks

2. **Clear Approval Authorities:**
   - Define who approves what at each stage
   - Delegate authority to lowest appropriate level
   - Avoid unnecessary escalations

3. **Process Mapping and Improvement:**
   - Map out end-to-end investment process
   - Identify bottlenecks and pain points
   - Implement process improvements (eliminate unnecessary steps, automate)
   - Lean / Six Sigma methodologies

4. **Cross-Functional Deal Teams:**
   - Assign cross-functional teams to each deal (Investment Officer, Credit, ESG, Legal)
   - Team works together from screening through monitoring
   - Reduces handoffs and miscommunication

5. **CRM / Deal Management System:**
   - Implement robust CRM system to track deals, tasks, documents
   - Visibility for management on pipeline and bottlenecks
   - Automated workflows and reminders
   - Reduces manual tracking and follow-ups

6. **Service Level Agreements (SLAs):**
   - Internal SLAs for each function (e.g., Legal reviews term sheet within 2 weeks of request)
   - Hold teams accountable to SLAs
   - Escalation if SLAs not met

7. **Continuous Improvement Culture:**
   - Regularly solicit feedback from investment teams on process pain points
   - Pilot new approaches
   - Share best practices across regions/sectors

**CRM Implication:**
- Workflow automation (automatic routing of tasks, approvals)
- SLA tracking and alerts
- Dashboards for management visibility

---

## 7. User Stories for CRM Development

User stories help translate operational needs into CRM features. They follow the format: **"As a [role], I need to [action], so that [benefit]."**

---

### 7.1 Deal Sourcing and Screening

**US-001:** As an **Investment Officer**, I need to **log new deal inquiries with source, sector, geography, and contact information**, so that I can track where deals are coming from and maintain a pipeline.

**US-002:** As an **Investment Officer**, I need to **assign a preliminary screening status (Screening, Declined, Proceeding to DD) and reason**, so that management can see pipeline conversion rates and understand why deals are declined.

**US-003:** As a **Head of Department**, I need to **view a dashboard of all deals by stage, sector, and region**, so that I can understand pipeline health and resource allocation needs.

**US-004:** As an **Investment Officer**, I need to **track referral partners and manage relationships**, so that I can nurture sources of deal flow.

**US-005:** As an **Investment Officer**, I need to **send automated acknowledgment emails to sponsors when a deal is logged**, so that sponsors know we received their inquiry and what next steps are.

---

### 7.2 Due Diligence Phase

**US-006:** As an **Investment Officer**, I need to **create and assign due diligence tasks to internal team members and external advisors**, so that DD activities are clearly defined and tracked.

**US-007:** As an **Investment Officer**, I need to **upload and organize due diligence documents in a central repository linked to the deal**, so that all team members and advisors can access documents easily.

**US-008:** As an **Investment Officer**, I need to **track document collection status against a checklist and send automated reminders to sponsors for missing documents**, so that document collection doesn't delay the deal.

**US-009:** As an **ESG Specialist**, I need to **conduct ESG screening and log ESG risks, gaps, and required actions**, so that ESG issues are identified early and tracked through to resolution.

**US-010:** As a **Credit Analyst**, I need to **log key financial assumptions, metrics, and sensitivities from the financial model**, so that credit assessments are documented and can be reviewed.

**US-011:** As a **Legal Counsel**, I need to **track legal due diligence findings and required legal actions**, so that legal risks are managed and legal close readiness is visible.

**US-012:** As an **Investment Officer**, I need to **view overall DD progress (% complete by workstream: financial, technical, legal, ESG, commercial)**, so that I can identify bottlenecks and manage timeline.

**US-013:** As a **Technical Specialist**, I need to **log findings from technical DD reports and flag any red flags or conditions**, so that technical risks are communicated to the deal team.

---

### 7.3 Investment Memo and IC Process

**US-014:** As an **Investment Officer**, I need to **compile an investment memo using a standardized template with inputs from all DD workstreams**, so that IC materials are complete and consistent.

**US-015:** As an **Investment Officer**, I need to **submit the deal for IC review and schedule on the IC calendar**, so that deals are queued for decision in an orderly manner.

**US-016:** As an **IC Member**, I need to **access IC memos and supporting documents in advance of the IC meeting**, so that I can review and come prepared for decision-making.

**US-017:** As an **Investment Officer**, I need to **log the IC decision (approved, approved with conditions, deferred, rejected) and any conditions or follow-up actions**, so that next steps are clear.

**US-018:** As a **Head of Investment Committee**, I need to **view upcoming IC pipeline and track decisions made**, so that I can manage IC workload and follow up on conditions.

**US-019:** As an **Investment Officer**, I need to **receive automated alerts if IC conditions are not addressed within a set timeframe**, so that deals don't stall post-IC approval.

---

### 7.4 Legal Documentation and Financial Close

**US-020:** As an **Investment Officer**, I need to **track legal documentation status (term sheet signed, loan agreement drafted, under negotiation, agreed, signed)**, so that legal close progress is visible.

**US-021:** As a **Legal Counsel**, I need to **maintain a list of conditions precedent with status and responsible party**, so that CP compliance is tracked and nothing is missed at close.

**US-022:** As an **Investment Officer**, I need to **be alerted when the long-stop date for financial close is approaching**, so that I can escalate issues and avoid deal expiry.

**US-023:** As a **Legal Counsel**, I need to **log and track negotiation points and their resolution**, so that there's an audit trail of legal negotiations.

**US-024:** As an **Investment Officer**, I need to **record financial close date and final deal terms (amount, rate, tenor, security)**, so that the deal record is complete and accurate.

**US-025:** As a **Finance Officer**, I need to **initiate disbursement workflows and track disbursement requests and approvals**, so that funds are transferred accurately and on time.

---

### 7.5 Portfolio Monitoring

**US-026:** As an **Investment Officer**, I need to **set up reporting schedules for each portfolio investment (quarterly financials, annual ESG reports, etc.)**, so that expected reports are tracked.

**US-027:** As an **Investment Officer**, I need to **receive automated reminders when reports are due from portfolio companies**, so that I can follow up with sponsors proactively.

**US-028:** As an **Investment Officer**, I need to **upload and review submitted reports (financial statements, operational KPIs, impact metrics, ESG reports)**, so that portfolio performance is monitored.

**US-029:** As an **Investment Officer**, I need to **calculate and track financial covenants (DSCR, Debt/Equity, etc.) and flag covenant breaches**, so that credit risk is monitored.

**US-030:** As an **Investment Officer**, I need to **log and track development impact metrics (jobs, GHG avoided, people served, etc.) over time**, so that impact performance is measured against targets.

**US-031:** As an **ESG Specialist**, I need to **track ESAP implementation progress and flag overdue actions**, so that ESG compliance is maintained.

**US-032:** As an **Investment Officer**, I need to **log incidents (environmental, health & safety, social) and track investigation and remediation**, so that incidents are documented and addressed.

**US-033:** As an **Investment Officer**, I need to **schedule and log site visits, including visit reports and action items**, so that on-site supervision is documented.

**US-034:** As a **Portfolio Manager**, I need to **view a portfolio dashboard with key metrics (DSCR, risk rating, ESG rating, impact metrics) across all investments**, so that I can identify problem investments and trends.

**US-035:** As an **Investment Officer**, I need to **escalate a portfolio investment to "watch list" status and assign corrective actions**, so that elevated risks are managed actively.

**US-036:** As an **Investment Officer**, I need to **generate automated portfolio reports for management and Board**, so that reporting is efficient and consistent.

---

### 7.6 Risk Management

**US-037:** As a **Credit Officer**, I need to **assign and update risk ratings for each investment**, so that portfolio risk is assessed consistently.

**US-038:** As a **Risk Manager**, I need to **view portfolio risk distribution (by risk rating, sector, geography)**, so that concentration risks are identified.

**US-039:** As an **Investment Officer**, I need to **log and track risk mitigation measures (insurance policies, guarantees, hedges)**, so that risk mitigations are monitored.

**US-040:** As a **Risk Manager**, I need to **be alerted when an investment is downgraded to a lower risk rating**, so that senior management is informed and actions are taken.

---

### 7.7 Stakeholder and Co-Financier Management

**US-041:** As an **Investment Officer**, I need to **log co-financiers for each deal with their roles, commitment amounts, and contact information**, so that co-financier coordination is organized.

**US-042:** As an **Investment Officer**, I need to **share selected documents with co-financiers via secure access**, so that information sharing is controlled and efficient.

**US-043:** As an **Investment Officer**, I need to **track co-financier approval milestones and flag if a co-financier is delayed**, so that coordination bottlenecks are visible.

**US-044:** As an **Investment Officer**, I need to **maintain a log of communication with sponsors, government, and co-financiers**, so that there's a record of key discussions and decisions.

---

### 7.8 Reporting and Analytics

**US-045:** As a **Head of Department**, I need to **generate reports on pipeline conversion rates (screening to IC, IC to close)**, so that I can assess team efficiency and identify improvement areas.

**US-046:** As a **Head of Department**, I need to **analyze time-to-close metrics (from screening to financial close) by sector and region**, so that I can identify bottlenecks and set benchmarks.

**US-047:** As a **CFO**, I need to **view committed vs disbursed capital and forecast future disbursements**, so that I can manage liquidity and funding needs.

**US-048:** As a **Chief Impact Officer**, I need to **aggregate impact metrics across the portfolio (total jobs, total GHG avoided, SDG contributions)**, so that I can report on DFI's development outcomes.

**US-049:** As a **Board Member**, I need to **access a dashboard with portfolio overview (size, sector, geography, risk profile, impact, financial performance)**, so that I can fulfill governance responsibilities.

**US-050:** As a **Communications Officer**, I need to **extract project information for public disclosure and annual reports**, so that transparency commitments are met.

---

### 7.9 Workflow Automation and Alerts

**US-051:** As an **Investment Officer**, I need to **receive automated alerts when a deal has been in a stage for longer than the expected timeline**, so that I can take action on stalled deals.

**US-052:** As an **Investment Officer**, I need to **automated escalation of overdue tasks to my manager**, so that accountability is maintained.

**US-053:** As an **Investment Officer**, I need to **automated routing of IC memos for review by Legal, ESG, Credit, and Finance departments**, so that reviews happen in parallel and efficiently.

**US-054:** As a **Legal Counsel**, I need to **be automatically notified when a deal enters the legal documentation stage**, so that I can allocate resources and begin work.

**US-055:** As an **Investment Officer**, I need to **receive automated reminders for upcoming disbursements and required approvals**, so that disbursements are not delayed.

---

### 7.10 Compliance and Audit Trail

**US-056:** As a **Compliance Officer**, I need to **conduct sanctions screening on all sponsors, shareholders, and counterparties and log results**, so that sanctions compliance is ensured.

**US-057:** As a **Compliance Officer**, I need to **track AML/KYC documentation for each sponsor**, so that compliance files are complete.

**US-058:** As an **Auditor**, I need to **access a complete audit trail of all decisions, approvals, and changes for any investment**, so that internal and external audits are supported.

**US-059:** As an **Investment Officer**, I need to **log rationale for key decisions (e.g., why a deal was declined, why a risk rating was assigned)**, so that decision-making is transparent and auditable.

---

### 7.11 User Management and Permissions

**US-060:** As an **Administrator**, I need to **create user accounts with role-based permissions (Investment Officer, ESG Specialist, Credit, Legal, Management, External Advisor)**, so that access to information is appropriate and secure.

**US-061:** As an **Administrator**, I need to **grant external advisors limited access to specific deals and documents**, so that they can perform their work without accessing unrelated information.

**US-062:** As a **User**, I need to **customize my dashboard to show deals and tasks most relevant to me**, so that I can work efficiently.

---

## Conclusion

This research documentation provides a comprehensive overview of DFI investment workflows, decision-making frameworks, and operational procedures. Key takeaways:

1. **Investment Process is Multi-Stage and Rigorous:** From deal sourcing through monitoring, each stage has clear objectives, timelines, and outputs. CRM systems must support this end-to-end process.

2. **Due Diligence is Multi-Dimensional:** Financial, technical, legal, ESG, political, and commercial due diligence occur in parallel. Coordination and tracking across these dimensions is critical.

3. **Decision Criteria are Multi-Faceted:** Financial returns, development impact, additionality, risk, and strategic fit all factor into IC decisions. The DFI "dual mandate" requires balancing commercial and development objectives.

4. **Reporting and Monitoring are Data-Intensive:** DFIs require extensive reporting on financial performance, impact metrics, and ESG compliance. Harmonized frameworks (HIPSO, IRIS+) are increasingly standard.

5. **Bottlenecks are Common and Addressable:** Document collection, compliance gaps, financial model iterations, IC scheduling, legal negotiations, co-financier coordination, government approvals, and internal inefficiencies all cause delays. Technology (CRM systems) and process improvements can mitigate many of these.

6. **User-Centric CRM Design is Essential:** The user stories highlight diverse needs across roles (Investment Officers, ESG Specialists, Legal Counsel, Management, etc.). A successful CRM must serve all stakeholders and support collaboration.

---

**Next Steps for CRM Development:**
- Translate these workflows and user stories into CRM requirements and design specifications
- Prioritize features based on impact and feasibility
- Develop prototypes and gather user feedback iteratively
- Ensure system is flexible to accommodate variations across DFIs and evolving standards

---

**Sources and References:**

- [Deal Flow Process & Best Practices - Carta](https://carta.com/learn/private-funds/management/deal-flow/)
- [Venture Capital Due Diligence Guide - Allvue Systems](https://www.allvuesystems.com/resources/venture-capital-due-diligence-guide/)
- [Investment Memos and Decision-Making - Addepar Research Brief (Stanford)](https://longterminvesting.stanford.edu/sites/g/files/sbiybj23856/files/media/file/addepar-investment-memos-and-decision-making.pdf)
- [Comparing Five Bilateral DFIs and IFC - Center for Global Development](https://www.cgdev.org/sites/default/files/comparing-five-bilateral-development-finance-institutions-and-ifc.pdf)
- [DFI Toolkit on Corporate Governance - IFC](https://www.ifc.org/wps/wcm/connect/topics_ext_content/ifc_external_corporate_site/ifc+cg/cg+development+framework/dfi+toolkit+on+corporate+governance)
- [BII ESG Toolkit - Due Diligence](https://toolkit.bii.co.uk/investment-cycle/due-diligence/)
- [ESG Due Diligence Checklist - Neotas](https://www.neotas.com/esg-due-diligence-checklist/)
- [What to Do When You Can't Prove DFI Additionality - CGD](https://www.cgdev.org/publication/what-do-when-you-cant-prove-dfi-additionality)
- [DFI Market Benchmarking Guidelines - EDFI](https://edfi-website-v1.s3.fr-par.scw.cloud/uploads/2021/04/210416-DFI-Market-Benchmarking-Guidelines-Final-1.pdf)
- [HIPSO - Harmonized Indicators for Private Sector Operations](https://indicators.ifipartnership.org/)
- [Joint Impact Indicators - HIPSO & IRIS+](https://edfi-website-v1.s3.fr-par.scw.cloud/uploads/2021/03/Joint-Impact-Indicators_final-release_3_12_2021.pdf)
- [IRIS+ and HIPSO - Global Impact Investing Network](https://iris.thegiin.org/document/iris-and-harmonized-indicators-for-private-sector-operations/)
- [DFI Transparency Tool - Publish What You Fund](https://www.publishwhatyoufund.org/app/uploads/dlm_uploads/2021/10/DFI-Transparency-Tool.pdf)
- [Four Views on How DFIs Must Invest Better - ODI](https://odi.org/en/insights/four-views-on-how-development-finance-institutions-must-invest-better/)
- [IFC Performance Standards](https://www.ifc.org/wps/wcm/connect/Topics_Ext_Content/IFC_External_Corporate_Site/Sustainability-At-IFC/Policies-Standards/Performance-Standards)
- [Conducting E&S Due Diligence Aligned with IFC - IFC Presentation](https://www.ifc.org/wps/wcm/connect/9975cfbc-6337-4f19-8935-d067a88b2899/PPT_ESDueDiligenceforFIs_June2017_external.pdf)
- [Debt Service Coverage Ratio - Corporate Finance Institute](https://corporatefinanceinstitute.com/resources/commercial-lending/debt-service-coverage-ratio/)
- [Investment Memo: How to Write - Carta](https://carta.com/learn/private-funds/management/portfolio-management/investment-memo/)
- [SDG Aligned Finance Framework - OECD-UNDP](https://sdgfinance.undp.org/sites/default/files/2024-04/Framework%20for%20SDG%20Aligned%20Finance%20OECD%20UNDP.pdf)
