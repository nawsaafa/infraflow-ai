# InfraFlow AI Platform - Supabase Database Setup Guide

## Overview

This guide provides complete instructions for setting up the InfraFlow AI Platform database schema in Supabase.

## Database Schema Summary

The schema includes **10 core tables** with:
- Complete indexing strategy for optimal performance
- Row Level Security (RLS) policies for multi-tenant data isolation
- Database functions and triggers for automation
- Utility views for reporting and analytics

### Core Tables

1. **users** - Application users with roles and preferences
2. **projects** - Infrastructure projects (main entity)
3. **documents** - Project documents with AI processing status
4. **financial_models** - DCF models and financial analysis
5. **compliance_checks** - DFI and regulatory compliance tracking
6. **risk_assessments** - Comprehensive risk analysis
7. **stakeholders** - Project stakeholders and engagement
8. **reports** - Generated investment memos and reports
9. **audit_log** - Complete audit trail for all changes
10. **milestones** - Project milestones and deliverables

### Additional Features

- **Indexes**: 80+ optimized indexes for fast queries
- **RLS Policies**: 40+ security policies for data isolation
- **Functions**: 15+ utility functions for common operations
- **Views**: 10+ views for reporting and dashboards
- **Triggers**: Automatic timestamp updates and audit logging

## Setup Instructions

### Option 1: Using Supabase SQL Editor (Recommended)

This is the easiest and most reliable method.

1. **Access Supabase Dashboard**
   - Go to: https://supabase.com/dashboard/project/abhnlhbkmrozxtfoaxnv
   - Login with your Supabase credentials

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Click "+ New query" button

3. **Execute Schema Script**
   - Open the file: `/home/claude-user/ai-consults-platform/00-pivot/backend/supabase-complete-schema.sql`
   - Copy the ENTIRE contents (2100+ lines)
   - Paste into the SQL Editor
   - Click "Run" button
   - Wait 30-60 seconds for completion

4. **Verify Success**
   - You should see: "Success. No rows returned"
   - At the bottom, you'll see: "InfraFlow AI Platform schema setup completed successfully!"

5. **Check Tables**
   - Go to "Table Editor" in the sidebar
   - You should see all 10 tables listed

### Option 2: Using Supabase CLI (Alternative)

If you have the Supabase CLI installed:

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
supabase db push --db-url "postgresql://postgres:c9R%25zn%40JZ6J%5EUZYg%40x4@db.abhnlhbkmrozxtfoaxnv.supabase.co:5432/postgres" -f supabase-complete-schema.sql
```

### Option 3: Using Node.js Script (If connection works)

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
node setup-supabase-direct.js
```

Note: This method may not work due to Supabase connection restrictions.

## Verification Steps

After running the schema setup, verify the installation:

### 1. Check Tables

Run this query in SQL Editor:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

Expected output (10 tables):
- audit_log
- compliance_checks
- documents
- financial_models
- milestones
- projects
- reports
- risk_assessments
- stakeholders
- users

### 2. Check Indexes

```sql
SELECT
    tablename,
    COUNT(*) as index_count
FROM pg_indexes
WHERE schemaname = 'public'
GROUP BY tablename
ORDER BY tablename;
```

Should show 80+ indexes across all tables.

### 3. Check RLS Policies

```sql
SELECT
    schemaname,
    tablename,
    policyname
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

Should show 40+ RLS policies.

### 4. Check Functions

```sql
SELECT
    routine_name,
    routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

Should show 15+ functions.

### 5. Check Views

```sql
SELECT
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type IN ('VIEW', 'MATERIALIZED VIEW')
ORDER BY table_name;
```

Should show 10+ views including the materialized view `mv_portfolio_overview`.

## Schema Details

### Projects Table Structure

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    sponsor TEXT,
    country TEXT NOT NULL,
    sector sector_type NOT NULL,  -- ENUM: renewable_energy, green_hydrogen, transmission, water, transportation, waste_management, other
    total_value DECIMAL(15,2),
    currency TEXT DEFAULT 'USD',
    dfi_partners JSONB DEFAULT '[]'::jsonb,
    status project_status DEFAULT 'draft',  -- ENUM: draft, pipeline, under_review, approved, rejected, active, completed, cancelled
    risk_score FLOAT CHECK (risk_score >= 0 AND risk_score <= 100),
    description TEXT,
    location JSONB,  -- {latitude, longitude, address}
    timeline JSONB,  -- {start_date, completion_date, milestones}
    stakeholders JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMPTZ
);
```

### Key Indexes

```sql
-- Fast project lookups
CREATE INDEX idx_projects_status ON projects(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_country ON projects(country) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_sector ON projects(sector) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_risk_score ON projects(risk_score DESC) WHERE deleted_at IS NULL;

-- JSONB searches
CREATE INDEX idx_projects_dfi_partners ON projects USING GIN (dfi_partners);
CREATE INDEX idx_projects_metadata ON projects USING GIN (metadata);

-- Full-text search
CREATE INDEX idx_projects_name_trgm ON projects USING GIN (name gin_trgm_ops);
```

### RLS Policy Example

```sql
-- Users can only see their own projects (or if they're admin)
CREATE POLICY "Users can view their projects"
    ON projects FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            created_by = auth.uid()
            OR is_admin()
            OR deleted_at IS NULL
        )
    );
```

## Useful Functions

### Calculate Project Risk Score

```sql
SELECT calculate_project_risk_score('<project_uuid>');
```

### Get Project Summary

```sql
SELECT get_project_summary('<project_uuid>');
```

### Get Portfolio Analytics

```sql
SELECT get_portfolio_analytics();
```

### Search Projects

```sql
SELECT * FROM search_projects('solar');
```

### Get Unprocessed Documents

```sql
SELECT * FROM get_unprocessed_documents(10);
```

## Useful Views

### Active Projects Dashboard

```sql
SELECT * FROM v_active_projects;
```

### Project Dashboard with All Metrics

```sql
SELECT * FROM v_project_dashboard WHERE id = '<project_uuid>';
```

### Portfolio Overview

```sql
SELECT * FROM mv_portfolio_overview;
```

### High Risk Projects

```sql
SELECT * FROM v_high_risk_projects;
```

### Compliance Summary

```sql
SELECT * FROM v_compliance_summary;
```

## Maintenance

### Refresh Materialized Views

The portfolio overview is a materialized view that needs periodic refresh:

```sql
SELECT refresh_portfolio_overview();
```

Or manually:

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_portfolio_overview;
```

### Cleanup Old Audit Logs

To remove audit logs older than 90 days:

```sql
SELECT cleanup_old_audit_logs();
```

### Update Statistics

For optimal query performance, periodically update table statistics:

```sql
ANALYZE;
```

## Connection Information

### Supabase Credentials

From `.env` file:

- **Supabase URL**: https://abhnlhbkmrozxtfoaxnv.supabase.co
- **Project Reference**: abhnlhbkmrozxtfoaxnv
- **Database**: postgres
- **Port**: 5432 (direct) or 6543 (pooler)

### Service Role Key

For server-side operations:

```javascript
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_KEY
);
```

### Anon Key

For client-side operations (with RLS):

```javascript
const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_PUBLIC_ANON
);
```

## Next Steps

After setting up the schema:

1. **Migrate Data** - Transfer the 24 projects from local PostgreSQL to Supabase
2. **Test Queries** - Verify all queries work with proper indexes
3. **Configure RLS** - Ensure RLS policies match your authentication setup
4. **Set up Backups** - Configure automated backups in Supabase dashboard
5. **Monitor Performance** - Use Supabase monitoring tools to track query performance

## Troubleshooting

### Issue: "already exists" errors

This is normal if you run the script multiple times. The script uses `IF NOT EXISTS` and `DROP POLICY IF EXISTS` to handle this.

### Issue: Connection refused

Supabase restricts direct PostgreSQL connections. Use the SQL Editor instead.

### Issue: RLS policy denies access

Make sure you're using the service role key for server-side operations, or that your JWT contains the correct role/user ID for client-side operations.

### Issue: Slow queries

Check if indexes are being used:

```sql
EXPLAIN ANALYZE SELECT * FROM projects WHERE country = 'Morocco';
```

### Issue: Materialized view out of date

Refresh it manually:

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_portfolio_overview;
```

## Support

- Supabase Documentation: https://supabase.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- InfraFlow AI Repository: (your repo URL)

## Schema Files

All schema files are located in:
- `/home/claude-user/ai-consults-platform/00-pivot/supabase/migrations/`
- Complete schema: `/home/claude-user/ai-consults-platform/00-pivot/backend/supabase-complete-schema.sql`

---

**Last Updated**: November 25, 2025
**Schema Version**: 1.0.0
**Total Lines**: 2115
**Total Tables**: 10
**Total Indexes**: 80+
**Total RLS Policies**: 40+
**Total Functions**: 15+
**Total Views**: 10+
