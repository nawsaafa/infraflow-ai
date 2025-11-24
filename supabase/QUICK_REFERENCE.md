# InfraFlow AI Database - Quick Reference Guide

## Installation Checklist

- [ ] PostgreSQL 14+ installed
- [ ] Extensions enabled: `uuid-ossp`, `pg_trgm`
- [ ] Run migration 1: `20251123000001_initial_schema.sql`
- [ ] Run migration 2: `20251123000002_indexes.sql`
- [ ] Run migration 3: `20251123000003_rls_policies.sql`
- [ ] Run migration 4: `20251123000004_functions.sql`
- [ ] Run migration 5: `20251123000005_utility_views.sql`
- [ ] Load seed data: `seed/seed_data.sql` (optional)
- [ ] Verify installation (see below)

## Verification Commands

```sql
-- Check tables (should return 8)
SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';

-- Check data (if seed loaded)
SELECT COUNT(*) FROM projects; -- Should return 5
SELECT COUNT(*) FROM documents; -- Should return 4

-- Test a function
SELECT get_portfolio_analytics();

-- Test a view
SELECT * FROM v_active_projects;
```

## Common Queries

### Projects

```sql
-- Get all active projects
SELECT * FROM v_active_projects;

-- Search projects
SELECT * FROM search_projects('green hydrogen');

-- Get project summary
SELECT get_project_summary('project-uuid');

-- Calculate risk score
SELECT calculate_project_risk_score('project-uuid');

-- Create new project
INSERT INTO projects (name, country, sector, total_value, status)
VALUES ('My Project', 'Kenya', 'renewable_energy', 500000000, 'draft')
RETURNING *;
```

### Documents

```sql
-- Get unprocessed documents
SELECT * FROM v_document_queue;
SELECT * FROM get_unprocessed_documents(10);

-- Mark document as processed
SELECT mark_document_processed(
    'doc-uuid',
    '{"summary": "Document summary"}'::json,
    'pinecone-id-123'
);

-- Upload new document
INSERT INTO documents (project_id, name, type, url)
VALUES ('project-uuid', 'Feasibility Study', 'feasibility_study', 'https://...')
RETURNING *;
```

### Financial Models

```sql
-- Get latest financial model
SELECT get_latest_financial_model('project-uuid');

-- Get all financial performance
SELECT * FROM v_financial_performance;

-- Calculate NPV
SELECT calculate_npv(
    '[{"year": 1, "cash_flow": 1000000}, {"year": 2, "cash_flow": 1200000}]'::jsonb,
    0.10
);

-- Create financial model
INSERT INTO financial_models (
    project_id, model_type, assumptions, irr, npv
) VALUES (
    'project-uuid',
    'Project Finance',
    '{"capex": 500000000, "opex": 15000000}'::jsonb,
    12.5,
    145000000
) RETURNING *;
```

### Compliance

```sql
-- Get compliance status
SELECT get_compliance_status('project-uuid');

-- View compliance summary
SELECT * FROM v_compliance_summary;

-- Create compliance check
INSERT INTO compliance_checks (
    project_id, standard, status, score
) VALUES (
    'project-uuid',
    'IFC Performance Standards',
    'compliant',
    88.5
) RETURNING *;
```

### Risk Assessment

```sql
-- View high risk projects
SELECT * FROM v_high_risk_projects;

-- Create risk assessment
INSERT INTO risk_assessments (
    project_id,
    assessment_type,
    overall_risk_score,
    risk_categories
) VALUES (
    'project-uuid',
    'Comprehensive Risk Assessment',
    45.0,
    '{"political": 40, "financial": 45, "technical": 35}'::jsonb
) RETURNING *;
```

### Analytics & Reporting

```sql
-- Portfolio overview
SELECT * FROM mv_portfolio_overview;

-- Refresh portfolio stats
SELECT refresh_portfolio_overview();

-- Project dashboard
SELECT * FROM v_project_dashboard WHERE id = 'project-uuid';

-- DFI partnerships
SELECT * FROM v_dfi_partnerships;

-- Recent changes
SELECT * FROM v_recent_changes;

-- Generate investment memo data
SELECT generate_investment_memo_data('project-uuid');
```

### Stakeholders

```sql
-- Stakeholder matrix
SELECT * FROM v_stakeholder_matrix WHERE project_id = 'project-uuid';

-- Add stakeholder
INSERT INTO stakeholders (
    project_id, name, organization, role, influence_level
) VALUES (
    'project-uuid',
    'John Doe',
    'EBRD',
    'Investment Officer',
    'high'
) RETURNING *;
```

## Useful Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `calculate_project_risk_score(uuid)` | Calculate risk score | FLOAT |
| `get_project_summary(uuid)` | Project statistics | JSON |
| `get_portfolio_analytics()` | Portfolio stats | JSON |
| `mark_document_processed(uuid, json, text)` | Mark doc processed | BOOLEAN |
| `get_unprocessed_documents(int)` | Pending docs | TABLE |
| `calculate_npv(jsonb, float)` | Calculate NPV | DECIMAL |
| `get_latest_financial_model(uuid)` | Latest model | RECORD |
| `get_compliance_status(uuid)` | Compliance summary | JSON |
| `search_projects(text)` | Search projects | TABLE |
| `generate_investment_memo_data(uuid)` | Memo data | JSON |
| `soft_delete(text, uuid)` | Soft delete record | BOOLEAN |
| `cleanup_old_audit_logs()` | Clean old logs | INTEGER |

## Useful Views

| View | Purpose |
|------|---------|
| `v_active_projects` | Active projects with metrics |
| `v_project_dashboard` | Full project dashboard |
| `mv_portfolio_overview` | Portfolio statistics (cached) |
| `v_compliance_summary` | Compliance by project |
| `v_document_queue` | Pending documents |
| `v_high_risk_projects` | Projects with risk >= 70 |
| `v_financial_performance` | Financial metrics |
| `v_stakeholder_matrix` | Stakeholder analysis |
| `v_recent_changes` | Recent changes (7 days) |
| `v_dfi_partnerships` | DFI commitments |

## Index Overview

### Performance Indexes
- B-tree indexes on frequently queried columns
- GIN indexes on all JSONB columns
- Trigram indexes for fuzzy text search
- Partial indexes for common filters

### Key Indexes
```sql
-- Projects
idx_projects_status              -- Fast status filtering
idx_projects_country_sector      -- Composite search
idx_projects_name_trgm           -- Fuzzy name search
idx_projects_dfi_partners        -- JSONB queries

-- Documents
idx_documents_project_id         -- Fast project lookup
idx_documents_processed          -- Find unprocessed
idx_documents_extracted_data     -- JSONB queries

-- Financial Models
idx_financial_models_version     -- Latest version
idx_financial_models_irr         -- Performance ranking

-- Compliance
idx_compliance_project_standard  -- Composite lookup
idx_compliance_issues            -- JSONB search
```

## JSONB Query Examples

```sql
-- Query DFI partners
SELECT * FROM projects
WHERE dfi_partners @> '[{"name": "EBRD"}]';

-- Extract specific JSONB field
SELECT
    name,
    dfi_partners->0->>'name' as lead_dfi,
    dfi_partners->0->>'commitment' as commitment
FROM projects;

-- Search in JSONB array
SELECT * FROM risk_assessments
WHERE identified_risks @> '[{"category": "political"}]';

-- Get array length
SELECT name, jsonb_array_length(dfi_partners) as partner_count
FROM projects;

-- Aggregate JSONB data
SELECT
    country,
    SUM((dfi_partners->0->>'commitment')::numeric) as total_commitment
FROM projects
WHERE jsonb_array_length(dfi_partners) > 0
GROUP BY country;
```

## Performance Tips

### Query Optimization
```sql
-- Always filter deleted records
WHERE deleted_at IS NULL

-- Use indexes
WHERE status = 'active' AND deleted_at IS NULL

-- Avoid function on indexed columns (bad)
WHERE UPPER(name) = 'PROJECT'

-- Use trigram search instead (good)
WHERE name ILIKE '%project%'
```

### Maintenance
```sql
-- Analyze tables weekly
ANALYZE projects;
ANALYZE documents;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan;

-- Vacuum if needed
VACUUM ANALYZE projects;
```

## Environment Setup

### Local Development
```bash
# PostgreSQL with Docker
docker run -d \
  --name infraflow-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=infraflow \
  -p 5432:5432 \
  postgres:14

# Apply migrations
psql -h localhost -U postgres -d infraflow -f migrations/20251123000001_initial_schema.sql
# ... repeat for all migrations

# Load seed data
psql -h localhost -U postgres -d infraflow -f seed/seed_data.sql
```

### Supabase
```bash
# Link project
supabase link --project-ref your-project-ref

# Apply migrations
supabase db reset

# Or incrementally
supabase migration up
```

## Troubleshooting

### Migration Fails
```sql
-- Check PostgreSQL version (need 14+)
SELECT version();

-- Check extensions
SELECT * FROM pg_extension WHERE extname IN ('uuid-ossp', 'pg_trgm');

-- Install missing extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### RLS Issues
```sql
-- Check current user
SELECT auth.uid();

-- Check role
SELECT auth.jwt() ->> 'role';

-- Disable RLS temporarily (development only!)
ALTER TABLE projects DISABLE ROW LEVEL SECURITY;
```

### Performance Issues
```sql
-- Find slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Explain query
EXPLAIN ANALYZE
SELECT * FROM projects WHERE status = 'active';
```

## Security Reminders

- **Always use RLS**: Keep policies enabled in production
- **Soft deletes**: Never hard delete, use `deleted_at`
- **Audit trail**: All changes are logged automatically
- **Service role**: Use only for backend operations
- **Authenticated role**: For user-facing operations

## Database Stats

- **Tables**: 8 core tables
- **Custom Types**: 4 enums
- **Indexes**: 50+ optimized indexes
- **Functions**: 15+ helper functions
- **Views**: 10 utility views
- **Policies**: 40+ RLS policies
- **Total SQL Lines**: 2,600+ lines

## Next Steps

1. **Test the setup**: Run verification commands
2. **Explore seed data**: Query the sample projects
3. **Try functions**: Test utility functions
4. **Check views**: Explore dashboard views
5. **Read docs**: See DATABASE_SCHEMA.md for details

## Support Resources

- **Full Documentation**: `DATABASE_SCHEMA.md`
- **Setup Guide**: `README.md`
- **SPARC Spec**: `../SPARC_INFRAFLOW.md`
- **PostgreSQL Docs**: https://www.postgresql.org/docs/14/
- **Supabase Docs**: https://supabase.com/docs

---

**Version**: 1.0.0
**Last Updated**: 2025-11-23
