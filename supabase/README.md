# InfraFlow AI - Database Setup

This directory contains all database migrations, seed data, and documentation for the InfraFlow AI platform.

## Quick Start

### Prerequisites

- PostgreSQL 14 or higher
- Supabase CLI (optional but recommended)
- psql command-line tool

### Option 1: Using Supabase CLI (Recommended)

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize Supabase (if not already done)
supabase init

# Link to your Supabase project
supabase link --project-ref your-project-ref

# Apply all migrations
supabase db reset

# Or apply migrations incrementally
supabase migration up
```

### Option 2: Manual Setup with psql

```bash
# Apply migrations in order
psql -U postgres -d your_database -f migrations/20251123000001_initial_schema.sql
psql -U postgres -d your_database -f migrations/20251123000002_indexes.sql
psql -U postgres -d your_database -f migrations/20251123000003_rls_policies.sql
psql -U postgres -d your_database -f migrations/20251123000004_functions.sql

# Load seed data (optional)
psql -U postgres -d your_database -f seed/seed_data.sql
```

### Option 3: Docker

```bash
# Start PostgreSQL with Docker
docker run -d \
  --name infraflow-db \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=infraflow \
  -p 5432:5432 \
  postgres:14

# Apply migrations
docker exec -i infraflow-db psql -U postgres -d infraflow < migrations/20251123000001_initial_schema.sql
docker exec -i infraflow-db psql -U postgres -d infraflow < migrations/20251123000002_indexes.sql
docker exec -i infraflow-db psql -U postgres -d infraflow < migrations/20251123000003_rls_policies.sql
docker exec -i infraflow-db psql -U postgres -d infraflow < migrations/20251123000004_functions.sql
```

## Directory Structure

```
supabase/
├── README.md                           # This file
├── DATABASE_SCHEMA.md                  # Comprehensive schema documentation
├── migrations/                         # Database migrations
│   ├── 20251123000001_initial_schema.sql    # Core tables and types
│   ├── 20251123000002_indexes.sql           # Performance indexes
│   ├── 20251123000003_rls_policies.sql      # Row Level Security
│   └── 20251123000004_functions.sql         # Database functions
└── seed/                               # Seed data
    └── seed_data.sql                   # Test data for development
```

## What Gets Created

### Tables

1. **projects** - Core infrastructure projects
2. **documents** - Project documents and processing status
3. **financial_models** - Financial models and DCF analyses
4. **compliance_checks** - DFI compliance assessments
5. **risk_assessments** - Risk analysis and scoring
6. **stakeholders** - Project stakeholders
7. **reports** - Generated reports
8. **audit_log** - Complete audit trail

### Custom Types

- `project_status` - Project lifecycle states
- `document_type` - Document categories
- `compliance_status` - Compliance states
- `sector_type` - Infrastructure sectors

### Indexes

- 50+ optimized indexes including:
  - B-tree indexes for fast lookups
  - GIN indexes for JSONB queries
  - Trigram indexes for fuzzy search
  - Partial indexes for common filters

### Functions

- `calculate_project_risk_score()` - Calculate risk scores
- `get_project_summary()` - Project statistics
- `get_portfolio_analytics()` - Portfolio analytics
- `mark_document_processed()` - Document processing
- `get_compliance_status()` - Compliance summary
- `search_projects()` - Full-text search
- And more...

### Security

- Row Level Security (RLS) policies on all tables
- Multi-tenant data isolation
- Audit logging for all changes
- Helper functions for access control

## Seed Data

The seed data includes:

- **5 sample projects** across different sectors and countries:
  - Egypt Green Hydrogen Megaproject
  - Kenya Solar Power Plant
  - Morocco Wind Farm
  - Nigeria Waste-to-Energy Facility
  - Chile Transmission Line

- **4 sample documents** with processing status
- **2 financial models** with DCF analysis
- **3 compliance checks** with issues and recommendations
- **2 risk assessments** with mitigation strategies
- **4 stakeholders** across different organizations
- **1 sample report** (executive summary)

### Loading Seed Data

```bash
# With Supabase CLI
supabase db reset --with-seed

# With psql
psql -U postgres -d your_database -f seed/seed_data.sql
```

## Verification

After setup, verify the installation:

```sql
-- Check tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check data
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM documents;
SELECT COUNT(*) FROM financial_models;

-- Test a function
SELECT get_portfolio_analytics();

-- Test search
SELECT * FROM search_projects('green hydrogen');
```

## Environment Variables

Set these environment variables in your application:

```env
DATABASE_URL=postgresql://user:password@host:5432/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Common Operations

### Create a New Project

```sql
INSERT INTO projects (name, country, sector, total_value, status)
VALUES ('My New Project', 'Kenya', 'renewable_energy', 500000000, 'draft');
```

### Upload a Document

```sql
INSERT INTO documents (project_id, name, type, url)
VALUES (
    'project-uuid',
    'Feasibility Study',
    'feasibility_study',
    'https://storage.example.com/doc.pdf'
);
```

### Check Compliance Status

```sql
SELECT get_compliance_status('project-uuid');
```

### Calculate Risk Score

```sql
SELECT calculate_project_risk_score('project-uuid');
```

### Search Projects

```sql
SELECT * FROM search_projects('solar');
```

## Backup and Restore

### Backup

```bash
# Full database backup
pg_dump -U postgres -d infraflow > backup.sql

# Backup specific tables
pg_dump -U postgres -d infraflow -t projects -t documents > tables_backup.sql
```

### Restore

```bash
# Restore full database
psql -U postgres -d infraflow < backup.sql

# Restore specific tables
psql -U postgres -d infraflow < tables_backup.sql
```

## Performance Tuning

### Analyze Tables

```sql
ANALYZE projects;
ANALYZE documents;
ANALYZE financial_models;
```

### Check Index Usage

```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;
```

### Query Performance

```sql
EXPLAIN ANALYZE
SELECT * FROM projects
WHERE status = 'active' AND deleted_at IS NULL;
```

## Troubleshooting

### Migration Errors

If migrations fail:

1. Check PostgreSQL version: `SELECT version();`
2. Verify extensions: `SELECT * FROM pg_extension;`
3. Check permissions: `\du` in psql
4. Review error logs

### RLS Issues

If queries return empty results:

1. Check authentication: `SELECT auth.uid();`
2. Verify RLS policies: `SELECT * FROM pg_policies;`
3. Check user role: `SELECT auth.jwt() ->> 'role';`

### Performance Issues

1. Run `ANALYZE` on affected tables
2. Check slow queries: `SELECT * FROM pg_stat_statements;`
3. Review index usage
4. Consider adding indexes for common queries

## Maintenance

### Weekly Tasks

```sql
-- Analyze tables
ANALYZE projects;
ANALYZE documents;
ANALYZE financial_models;
ANALYZE compliance_checks;
ANALYZE risk_assessments;
```

### Monthly Tasks

```sql
-- Cleanup old audit logs (retains 90 days)
SELECT cleanup_old_audit_logs();

-- Vacuum analyze
VACUUM ANALYZE;
```

### As Needed

```sql
-- Reindex tables if needed
REINDEX TABLE projects;

-- Update table statistics
ANALYZE;
```

## Development Workflow

1. **Create Migration**: Add new .sql file in `migrations/`
2. **Test Locally**: Apply migration to local database
3. **Version Control**: Commit migration file
4. **Apply to Dev**: Run migration on development environment
5. **Test**: Verify changes work as expected
6. **Apply to Prod**: Run migration on production (with backup!)

## Additional Resources

- **Full Documentation**: See `DATABASE_SCHEMA.md`
- **SPARC Specification**: See `../SPARC_INFRAFLOW.md`
- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## Support

For issues or questions:

- Check `DATABASE_SCHEMA.md` for detailed schema information
- Review migration files for implementation details
- Contact the Database Engineer or System Architect

---

**Last Updated**: 2025-11-23
**Schema Version**: 1.0.0
**PostgreSQL Version**: 14+
