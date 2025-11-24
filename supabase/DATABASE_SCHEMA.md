# InfraFlow AI - Database Schema Documentation

## Overview

This document provides comprehensive documentation for the InfraFlow AI PostgreSQL database schema. The database is designed to support infrastructure project finance intelligence, document processing, financial modeling, compliance checking, and risk assessment.

**Database Version:** PostgreSQL 14+
**Schema Version:** 1.0.0
**Last Updated:** 2025-11-23

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Tables](#core-tables)
3. [Indexes](#indexes)
4. [Row Level Security](#row-level-security)
5. [Database Functions](#database-functions)
6. [Migrations](#migrations)
7. [Data Types](#data-types)
8. [Best Practices](#best-practices)

---

## Architecture Overview

### Database Design Principles

- **Multi-tenant Architecture**: RLS policies ensure data isolation
- **Soft Deletes**: All tables support soft deletion via `deleted_at` timestamp
- **JSONB for Flexibility**: Complex data structures stored as JSONB for flexibility
- **Audit Trail**: Comprehensive audit logging for all data changes
- **Performance Optimized**: Strategic indexes including GIN and trigram indexes
- **Timestamped Records**: All tables include `created_at` and `updated_at`

### Entity Relationship Diagram

```
projects (1) ──< (N) documents
         │
         ├──< (N) financial_models
         │
         ├──< (N) compliance_checks
         │
         ├──< (N) risk_assessments
         │
         ├──< (N) stakeholders
         │
         └──< (N) reports

audit_log (tracks all changes)
```

---

## Core Tables

### 1. Projects Table

**Purpose**: Stores core infrastructure project information.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique project identifier |
| name | TEXT | NOT NULL, CHECK (length >= 3) | Project name |
| sponsor | TEXT | | Project sponsor organization |
| country | TEXT | NOT NULL | Project country |
| sector | sector_type | NOT NULL | Project sector (enum) |
| total_value | DECIMAL(15,2) | CHECK (>= 0) | Total project value |
| currency | TEXT | DEFAULT 'USD' | Currency code |
| dfi_partners | JSONB | DEFAULT '[]' | DFI partnerships array |
| status | project_status | DEFAULT 'draft' | Current project status |
| risk_score | FLOAT | CHECK (0-100) | Overall risk score |
| description | TEXT | | Project description |
| location | JSONB | | Geographic coordinates and address |
| timeline | JSONB | | Project timeline and milestones |
| stakeholders | JSONB | DEFAULT '[]' | Stakeholders array |
| metadata | JSONB | DEFAULT '{}' | Additional metadata |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Last update timestamp |
| created_by | UUID | | User who created record |
| updated_by | UUID | | User who last updated record |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

**Enums**:

- `project_status`: draft, pipeline, under_review, approved, rejected, active, completed, cancelled
- `sector_type`: renewable_energy, green_hydrogen, transmission, water, transportation, waste_management, other

**JSONB Structures**:

```json
// dfi_partners
[
  {
    "name": "EBRD",
    "commitment": 2000000000,
    "status": "committed"
  }
]

// location
{
  "latitude": 30.0444,
  "longitude": 32.8973,
  "address": "Suez Canal Economic Zone, Egypt"
}

// timeline
{
  "start_date": "2024-06-01",
  "completion_date": "2028-12-31",
  "milestones": [
    {
      "name": "Financial Close",
      "date": "2024-12-31",
      "status": "pending"
    }
  ]
}

// stakeholders
[
  {
    "name": "John Doe",
    "role": "Project Director",
    "organization": "Green Energy International",
    "contact": "john@example.com"
  }
]
```

**Indexes**:

- `idx_projects_status` - Fast filtering by status
- `idx_projects_country` - Country lookup
- `idx_projects_sector` - Sector filtering
- `idx_projects_country_sector` - Composite index
- `idx_projects_risk_score` - Risk-based sorting
- `idx_projects_dfi_partners` - GIN index for JSONB queries
- `idx_projects_name_trgm` - Trigram index for fuzzy search

---

### 2. Documents Table

**Purpose**: Stores project documents and their processing status.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique document identifier |
| project_id | UUID | NOT NULL, FK(projects) | Associated project |
| name | TEXT | NOT NULL | Document name |
| type | document_type | NOT NULL | Document type (enum) |
| url | TEXT | | Public URL |
| file_path | TEXT | | Storage path |
| file_size | BIGINT | CHECK (>= 0) | File size in bytes |
| mime_type | TEXT | | MIME type |
| processed | BOOLEAN | DEFAULT FALSE | Processing status |
| processing_status | TEXT | DEFAULT 'pending' | Current processing state |
| extracted_data | JSONB | DEFAULT '{}' | Extracted structured data |
| embeddings_id | TEXT | | Vector database reference |
| page_count | INTEGER | CHECK (>= 0) | Number of pages |
| language | TEXT | DEFAULT 'en' | Document language |
| confidence_score | FLOAT | CHECK (0-1) | AI extraction confidence |
| metadata | JSONB | DEFAULT '{}' | Additional metadata |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Upload timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Last update |
| processed_at | TIMESTAMPTZ | | Processing completion time |
| created_by | UUID | | Uploader user ID |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

**Enums**:

- `document_type`: feasibility_study, financial_model, environmental_impact, technical_specification, legal_agreement, compliance_report, investment_memo, due_diligence, other

**JSONB Structures**:

```json
// extracted_data
{
  "summary": "Executive summary text",
  "key_terms": ["term1", "term2"],
  "entities": {
    "organizations": ["EBRD", "Company X"],
    "locations": ["Egypt", "Suez"],
    "dates": ["2024-06-01"]
  },
  "risks": ["risk1", "risk2"],
  "financials": {
    "capex": 8500000000,
    "revenue": 2000000000
  }
}
```

**Indexes**:

- `idx_documents_project_id` - Fast project lookup
- `idx_documents_type` - Filter by document type
- `idx_documents_processed` - Find unprocessed documents
- `idx_documents_project_type` - Composite index
- `idx_documents_extracted_data` - GIN index for JSONB
- `idx_documents_embeddings_id` - Vector lookup

---

### 3. Financial Models Table

**Purpose**: Stores financial models and DCF analyses.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Model identifier |
| project_id | UUID | NOT NULL, FK(projects) | Associated project |
| model_type | TEXT | NOT NULL | Model type |
| version | INTEGER | DEFAULT 1, CHECK (> 0) | Model version |
| assumptions | JSONB | NOT NULL | Model assumptions |
| outputs | JSONB | DEFAULT '{}' | Calculated outputs |
| scenarios | JSONB | DEFAULT '[]' | Scenario analyses |
| dcf_analysis | JSONB | | DCF breakdown |
| sensitivity_analysis | JSONB | | Sensitivity data |
| risk_metrics | JSONB | | Risk metrics |
| currency | TEXT | DEFAULT 'USD' | Currency |
| discount_rate | FLOAT | | Discount rate (WACC) |
| project_life_years | INTEGER | CHECK (> 0) | Project lifetime |
| irr | FLOAT | | Internal Rate of Return |
| npv | DECIMAL(15,2) | | Net Present Value |
| payback_period | FLOAT | | Payback period in years |
| metadata | JSONB | DEFAULT '{}' | Additional metadata |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Update timestamp |
| created_by | UUID | | Creator user ID |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

**JSONB Structures**:

```json
// assumptions
{
  "capex": 8500000000,
  "annual_production": 600000,
  "price": 4.5,
  "capacity_factor": 0.85,
  "opex_percentage": 0.03,
  "debt_ratio": 0.70,
  "debt_tenor": 18,
  "interest_rate": 0.065
}

// scenarios
[
  {
    "name": "Base Case",
    "probability": 0.50,
    "npv": 2450000000,
    "irr": 11.2,
    "key_assumptions": {}
  },
  {
    "name": "Upside",
    "probability": 0.25,
    "npv": 3680000000,
    "irr": 14.8
  }
]
```

**Indexes**:

- `idx_financial_models_project_id` - Project lookup
- `idx_financial_models_version` - Version sorting
- `idx_financial_models_irr` - Performance ranking
- `idx_financial_models_npv` - Value sorting
- `idx_financial_models_assumptions` - GIN index

---

### 4. Compliance Checks Table

**Purpose**: Tracks compliance against DFI and regulatory standards.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Check identifier |
| project_id | UUID | NOT NULL, FK(projects) | Associated project |
| standard | TEXT | NOT NULL | Compliance standard name |
| category | TEXT | | Check category |
| status | compliance_status | DEFAULT 'pending' | Check status |
| score | FLOAT | CHECK (0-100) | Compliance score |
| issues | JSONB | DEFAULT '[]' | Identified issues |
| recommendations | JSONB | DEFAULT '[]' | Recommendations |
| evidence | JSONB | DEFAULT '[]' | Supporting evidence |
| reviewer | TEXT | | Reviewer name |
| notes | TEXT | | Additional notes |
| metadata | JSONB | DEFAULT '{}' | Additional data |
| checked_at | TIMESTAMPTZ | DEFAULT NOW() | Check timestamp |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Update timestamp |
| created_by | UUID | | Creator user ID |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

**Enums**:

- `compliance_status`: pending, in_progress, compliant, non_compliant, needs_review, approved

**JSONB Structures**:

```json
// issues
[
  {
    "severity": "high",
    "description": "Issue description",
    "requirement": "Standard requirement reference",
    "gap": "Gap analysis"
  }
]

// recommendations
[
  {
    "priority": "high",
    "action": "Recommended action",
    "timeline": "30 days",
    "resources": "Required resources"
  }
]
```

**Indexes**:

- `idx_compliance_checks_project_id` - Project lookup
- `idx_compliance_checks_standard` - Standard filtering
- `idx_compliance_checks_status` - Status filtering
- `idx_compliance_project_standard` - Composite index
- `idx_compliance_issues` - GIN index

---

### 5. Risk Assessments Table

**Purpose**: Stores comprehensive risk assessments.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Assessment identifier |
| project_id | UUID | NOT NULL, FK(projects) | Associated project |
| assessment_type | TEXT | NOT NULL | Type of assessment |
| overall_risk_score | FLOAT | CHECK (0-100) | Overall risk score |
| risk_categories | JSONB | DEFAULT '{}' | Risk by category |
| identified_risks | JSONB | DEFAULT '[]' | Identified risks |
| mitigation_strategies | JSONB | DEFAULT '[]' | Mitigation plans |
| risk_matrix | JSONB | | Risk matrix data |
| country_risk | JSONB | | Country-specific risks |
| political_risk | JSONB | | Political risks |
| financial_risk | JSONB | | Financial risks |
| technical_risk | JSONB | | Technical risks |
| environmental_risk | JSONB | | Environmental risks |
| assessed_by | TEXT | | Assessor name |
| assessment_date | TIMESTAMPTZ | DEFAULT NOW() | Assessment date |
| metadata | JSONB | DEFAULT '{}' | Additional data |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Update timestamp |
| created_by | UUID | | Creator user ID |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

**JSONB Structures**:

```json
// risk_categories
{
  "political": 38,
  "financial": 42,
  "technical": 35,
  "environmental": 48,
  "regulatory": 52
}

// identified_risks
[
  {
    "category": "political",
    "description": "Risk description",
    "likelihood": "medium",
    "impact": "high",
    "severity": "high"
  }
]

// mitigation_strategies
[
  {
    "risk_id": "POL-001",
    "strategy": "Mitigation approach",
    "cost": 45000000,
    "effectiveness": "high"
  }
]
```

---

### 6. Stakeholders Table

**Purpose**: Tracks project stakeholders.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Stakeholder identifier |
| project_id | UUID | NOT NULL, FK(projects) | Associated project |
| name | TEXT | NOT NULL, CHECK (length >= 2) | Stakeholder name |
| organization | TEXT | | Organization name |
| role | TEXT | NOT NULL | Stakeholder role |
| contact_email | TEXT | | Email address |
| contact_phone | TEXT | | Phone number |
| country | TEXT | | Country |
| stakeholder_type | TEXT | | Type (DFI, Sponsor, etc.) |
| influence_level | TEXT | | Influence: high/medium/low |
| engagement_status | TEXT | | Status: active/pending/inactive |
| notes | TEXT | | Additional notes |
| metadata | JSONB | DEFAULT '{}' | Additional data |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Update timestamp |
| created_by | UUID | | Creator user ID |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

---

### 7. Reports Table

**Purpose**: Stores generated reports.

**Schema**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Report identifier |
| project_id | UUID | NOT NULL, FK(projects) | Associated project |
| report_type | TEXT | NOT NULL | Report type |
| title | TEXT | NOT NULL | Report title |
| content | JSONB | NOT NULL | Report content |
| format | TEXT | DEFAULT 'json' | Output format |
| file_url | TEXT | | Generated file URL |
| generated_by | TEXT | | Generator (AI/User) |
| template_used | TEXT | | Template reference |
| metadata | JSONB | DEFAULT '{}' | Additional data |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Update timestamp |
| created_by | UUID | | Creator user ID |
| deleted_at | TIMESTAMPTZ | | Soft delete timestamp |

**Report Types**:
- investment_memo
- compliance_report
- risk_matrix
- due_diligence
- executive_summary

---

### 8. Audit Log Table

**Purpose**: Immutable audit trail of all data changes.

**Schema**:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Audit entry identifier |
| table_name | TEXT | Affected table |
| record_id | UUID | Affected record |
| action | TEXT | INSERT/UPDATE/DELETE |
| old_data | JSONB | Previous state |
| new_data | JSONB | New state |
| changed_by | UUID | User who made change |
| changed_at | TIMESTAMPTZ | Change timestamp |
| ip_address | INET | User IP address |
| user_agent | TEXT | User agent string |
| metadata | JSONB | Additional context |

**Note**: Audit log is immutable (no UPDATE or DELETE policies).

---

## Indexes

### Index Strategy

The database uses multiple index types for optimal performance:

1. **B-tree Indexes**: Standard indexes for equality and range queries
2. **GIN Indexes**: For JSONB columns and full-text search
3. **Trigram Indexes**: For fuzzy text search (pg_trgm extension)
4. **Composite Indexes**: For common multi-column queries
5. **Partial Indexes**: For frequently filtered subsets

### Key Indexes

**Full-text Search**:
- `idx_projects_name_trgm` - Fuzzy project name search
- `idx_documents_name_trgm` - Fuzzy document search
- `idx_stakeholders_name_trgm` - Stakeholder search

**JSONB Queries**:
- `idx_projects_dfi_partners` - Query DFI partnerships
- `idx_documents_extracted_data` - Search extracted data
- `idx_financial_models_assumptions` - Query model assumptions
- `idx_compliance_issues` - Search compliance issues

**Performance Indexes**:
- `idx_active_projects` - Partial index for active projects
- `idx_unprocessed_documents` - Partial index for pending documents
- `idx_high_risk_projects` - Partial index for high-risk projects

---

## Row Level Security

### RLS Architecture

All tables have RLS enabled with policies based on:

1. **User Authentication**: via `auth.uid()`
2. **Project Ownership**: `created_by = auth.uid()`
3. **Admin Role**: `auth.jwt() ->> 'role' = 'admin'`
4. **Project Access**: `has_project_access()` helper function

### Key RLS Functions

**`has_project_access(project_uuid UUID)`**
- Checks if current user can access a project
- Returns TRUE for project creators, team members, or admins

**`is_admin()`**
- Checks if current user has admin role
- Returns TRUE for admin or service_role

**`get_user_organization()`**
- Returns current user's organization ID
- Used for multi-tenant data isolation

### Policy Examples

```sql
-- Users can view their projects
CREATE POLICY "Users can view their projects" ON projects FOR SELECT
USING (
    auth.uid() IS NOT NULL AND
    (created_by = auth.uid() OR is_admin())
);

-- Users can create projects
CREATE POLICY "Users can create projects" ON projects FOR INSERT
WITH CHECK (
    auth.uid() IS NOT NULL AND
    created_by = auth.uid()
);
```

---

## Database Functions

### Project Management

**`calculate_project_risk_score(project_uuid UUID)`**
- Calculates overall project risk based on compliance and risk assessments
- Updates project.risk_score automatically
- Returns: FLOAT (0-100)

**`get_project_summary(project_uuid UUID)`**
- Returns comprehensive project statistics
- Returns: JSON with document counts, compliance status, financial metrics

**`get_portfolio_analytics()`**
- Portfolio-wide analytics and statistics
- Returns: JSON with aggregated metrics

### Document Processing

**`mark_document_processed(doc_uuid UUID, extracted JSON, embedding_id TEXT)`**
- Marks document as processed
- Stores extracted data and embeddings reference
- Returns: BOOLEAN

**`get_unprocessed_documents(limit_count INT)`**
- Returns list of documents pending processing
- Returns: TABLE

### Financial Modeling

**`calculate_npv(cash_flows JSONB, discount_rate FLOAT)`**
- Calculates Net Present Value
- Returns: DECIMAL

**`get_latest_financial_model(project_uuid UUID)`**
- Returns latest version of financial model
- Returns: financial_models record

### Compliance

**`get_compliance_status(project_uuid UUID)`**
- Comprehensive compliance status summary
- Returns: JSON with checks, scores, issues

### Reporting

**`generate_investment_memo_data(project_uuid UUID)`**
- Generates structured data for investment memo
- Aggregates project, financial, risk, and compliance data
- Returns: JSON

### Search

**`search_projects(search_query TEXT)`**
- Full-text search across projects with relevance ranking
- Returns: TABLE with similarity scores

### Utilities

**`soft_delete(table_name TEXT, record_uuid UUID)`**
- Soft deletes any record
- Returns: BOOLEAN

**`cleanup_old_audit_logs()`**
- Removes audit logs older than 90 days
- Returns: INTEGER (count deleted)

---

## Migrations

### Migration Files

Migrations are located in `/supabase/migrations/` and should be applied in order:

1. **20251123000001_initial_schema.sql** - Core tables and types
2. **20251123000002_indexes.sql** - Performance indexes
3. **20251123000003_rls_policies.sql** - Row Level Security
4. **20251123000004_functions.sql** - Database functions

### Running Migrations

```bash
# Using Supabase CLI
supabase db reset
supabase migration up

# Or apply manually
psql -U postgres -d infraflow -f migrations/20251123000001_initial_schema.sql
psql -U postgres -d infraflow -f migrations/20251123000002_indexes.sql
psql -U postgres -d infraflow -f migrations/20251123000003_rls_policies.sql
psql -U postgres -d infraflow -f migrations/20251123000004_functions.sql
```

### Seed Data

Load test data:

```bash
psql -U postgres -d infraflow -f seed/seed_data.sql
```

---

## Data Types

### Custom ENUMs

```sql
-- Project status lifecycle
CREATE TYPE project_status AS ENUM (
    'draft', 'pipeline', 'under_review',
    'approved', 'rejected', 'active',
    'completed', 'cancelled'
);

-- Document categories
CREATE TYPE document_type AS ENUM (
    'feasibility_study', 'financial_model',
    'environmental_impact', 'technical_specification',
    'legal_agreement', 'compliance_report',
    'investment_memo', 'due_diligence', 'other'
);

-- Compliance status
CREATE TYPE compliance_status AS ENUM (
    'pending', 'in_progress', 'compliant',
    'non_compliant', 'needs_review', 'approved'
);

-- Infrastructure sectors
CREATE TYPE sector_type AS ENUM (
    'renewable_energy', 'green_hydrogen',
    'transmission', 'water', 'transportation',
    'waste_management', 'other'
);
```

---

## Best Practices

### 1. JSONB Usage

**DO**:
- Use JSONB for flexible, semi-structured data
- Create GIN indexes for frequently queried JSONB columns
- Use JSONB for arrays and nested objects

**DON'T**:
- Store large text blobs in JSONB
- Use JSONB for data that should be normalized
- Skip indexing frequently queried JSONB fields

### 2. Soft Deletes

Always use soft deletes:

```sql
UPDATE projects SET deleted_at = NOW() WHERE id = 'uuid';
```

Query active records:

```sql
SELECT * FROM projects WHERE deleted_at IS NULL;
```

### 3. Audit Trail

All changes are automatically logged. Access audit logs:

```sql
SELECT * FROM audit_log
WHERE table_name = 'projects'
AND record_id = 'project-uuid'
ORDER BY changed_at DESC;
```

### 4. Performance

- Use indexes for WHERE clauses
- Leverage partial indexes for common filters
- Use `EXPLAIN ANALYZE` to optimize queries
- Regularly `ANALYZE` tables after bulk inserts

### 5. Transactions

Use transactions for multi-table operations:

```sql
BEGIN;
  INSERT INTO projects (...) VALUES (...);
  INSERT INTO documents (...) VALUES (...);
COMMIT;
```

### 6. Query Patterns

**Good**:
```sql
-- Use indexes
SELECT * FROM projects WHERE status = 'active' AND deleted_at IS NULL;

-- Use JSONB operators
SELECT * FROM projects WHERE dfi_partners @> '[{"name": "EBRD"}]';
```

**Bad**:
```sql
-- Avoid functions on indexed columns
SELECT * FROM projects WHERE UPPER(name) = 'PROJECT';

-- Avoid SELECT *
SELECT * FROM projects; -- specify columns instead
```

---

## Schema Maintenance

### Regular Tasks

1. **Analyze Tables** (Weekly):
```sql
ANALYZE projects;
ANALYZE documents;
ANALYZE financial_models;
```

2. **Cleanup Old Audit Logs** (Monthly):
```sql
SELECT cleanup_old_audit_logs();
```

3. **Reindex** (As needed):
```sql
REINDEX TABLE projects;
```

4. **Vacuum** (Automatic, but can force):
```sql
VACUUM ANALYZE projects;
```

---

## Support

For issues or questions:

- **Database Engineer**: Contact system architect
- **Migration Issues**: Check Supabase logs
- **Performance**: Use `EXPLAIN ANALYZE` and consult indexes
- **RLS Issues**: Verify user authentication and roles

---

**Document Version**: 1.0.0
**Database Schema Version**: 1.0.0
**Last Updated**: 2025-11-23
