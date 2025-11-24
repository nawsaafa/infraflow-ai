# InfraFlow AI - Database Architecture

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INFRAFLOW AI DATABASE                            │
│                      Infrastructure Finance Platform                     │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│      PROJECTS        │◄─────────────────────────────────────────┐
├──────────────────────┤                                          │
│ • id (PK)           │                                          │
│ • name              │                                          │
│ • sponsor           │                                          │
│ • country           │                                          │
│ • sector            │                                          │
│ • total_value       │                                          │
│ • dfi_partners      │                                          │
│ • status            │                                          │
│ • risk_score        │                                          │
│ • timeline          │                                          │
│ • stakeholders      │                                          │
└──────┬───────────────┘                                          │
       │                                                          │
       │ 1:N                                                      │
       ├────────────────────────┬──────────────────┬──────────────┤
       │                        │                  │              │
       ▼                        ▼                  ▼              ▼
┌─────────────────┐   ┌──────────────────┐   ┌────────────┐   ┌─────────────┐
│   DOCUMENTS     │   │ FINANCIAL_MODELS │   │COMPLIANCE_ │   │    RISK_    │
├─────────────────┤   ├──────────────────┤   │  CHECKS    │   │ASSESSMENTS  │
│ • id (PK)      │   │ • id (PK)       │   ├────────────┤   ├─────────────┤
│ • project_id   │   │ • project_id    │   │ • id (PK)  │   │ • id (PK)   │
│ • name         │   │ • model_type    │   │ • proj_id  │   │ • proj_id   │
│ • type         │   │ • version       │   │ • standard │   │ • type      │
│ • url          │   │ • assumptions   │   │ • status   │   │ • score     │
│ • processed    │   │ • outputs       │   │ • score    │   │ • risks     │
│ • extracted_   │   │ • scenarios     │   │ • issues   │   │ • mitigat.  │
│   data         │   │ • dcf_analysis  │   │ • recomm.  │   │ • political │
│ • embeddings_id│   │ • irr, npv      │   └────────────┘   │ • financial │
└─────────────────┘   │ • payback       │                    │ • technical │
                      └──────────────────┘                    └─────────────┘
       │                                                             │
       │ 1:N                                                    1:N  │
       ▼                                                             ▼
┌─────────────────┐                                          ┌─────────────┐
│  STAKEHOLDERS   │                                          │   REPORTS   │
├─────────────────┤                                          ├─────────────┤
│ • id (PK)      │                                          │ • id (PK)   │
│ • project_id   │                                          │ • proj_id   │
│ • name         │                                          │ • type      │
│ • organization │                                          │ • title     │
│ • role         │                                          │ • content   │
│ • influence    │                                          │ • format    │
│ • engagement   │                                          │ • file_url  │
└─────────────────┘                                          └─────────────┘

                        ┌──────────────────┐
                        │    AUDIT_LOG     │
                        ├──────────────────┤
                        │ • id (PK)       │
                        │ • table_name    │
                        │ • record_id     │
                        │ • action        │
                        │ • old_data      │
                        │ • new_data      │
                        │ • changed_by    │
                        │ • changed_at    │
                        └──────────────────┘
                        (Tracks all changes)
```

## Table Relationships

### Primary Relationships

```
projects (1) ──< (N) documents
projects (1) ──< (N) financial_models
projects (1) ──< (N) compliance_checks
projects (1) ──< (N) risk_assessments
projects (1) ──< (N) stakeholders
projects (1) ──< (N) reports
```

### Foreign Keys

- All child tables have `project_id` FK referencing `projects.id`
- Cascade delete: When project deleted, all related records deleted
- Soft delete pattern: Use `deleted_at` instead of hard delete

## Data Flow Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW PIPELINE                           │
└────────────────────────────────────────────────────────────────────┘

1. PROJECT CREATION
   ┌─────────┐
   │ Frontend│──► INSERT INTO projects
   └─────────┘    └─► Trigger: set created_at, updated_at
                  └─► Audit: Log creation

2. DOCUMENT UPLOAD
   ┌─────────┐
   │ Frontend│──► INSERT INTO documents (processed=false)
   └─────────┘    └─► View: v_document_queue
                  └─► Function: get_unprocessed_documents()

3. AI PROCESSING
   ┌─────────┐
   │ Backend │──► Process document
   │   AI    │    └─► Extract data
   └─────────┘    └─► Generate embeddings
                  └─► Function: mark_document_processed()
                  └─► UPDATE documents SET processed=true

4. RISK CALCULATION
   ┌─────────┐
   │ Backend │──► INSERT risk_assessments
   │  Risk   │    INSERT compliance_checks
   │ Engine  │    └─► Function: calculate_project_risk_score()
   └─────────┘    └─► UPDATE projects SET risk_score

5. FINANCIAL MODELING
   ┌─────────┐
   │ Backend │──► INSERT financial_models
   │Financial│    └─► Function: calculate_npv()
   │ Engine  │    └─► Store scenarios, DCF analysis
   └─────────┘

6. REPORTING
   ┌─────────┐
   │ Backend │──► Function: generate_investment_memo_data()
   │ Report  │    └─► Aggregates from all tables
   │Generator│    └─► INSERT INTO reports
   └─────────┘

7. ANALYTICS
   ┌─────────┐
   │Dashboard│──► View: v_project_dashboard
   │Frontend │    View: v_portfolio_overview
   └─────────┘    Function: get_portfolio_analytics()
```

## Security Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    ROW LEVEL SECURITY (RLS)                        │
└────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│     USER     │
│ (auth.uid()) │
└──────┬───────┘
       │
       ├─── Is Admin? ──► Full Access (via is_admin())
       │
       ├─── Project Owner? ──► Access to project and children
       │                       (via has_project_access())
       │
       └─── Team Member? ──► Access to organization projects
                             (via get_user_organization())

Policy Enforcement:
┌─────────────┐
│   SELECT    │ ──► Can view owned/assigned projects
├─────────────┤
│   INSERT    │ ──► Can create with self as owner
├─────────────┤
│   UPDATE    │ ──► Can update owned projects
├─────────────┤
│   DELETE    │ ──► Can delete owned projects
└─────────────┘

Audit Trail:
ALL operations ──► Trigger: create_audit_log()
                   └─► INSERT INTO audit_log (immutable)
```

## Index Strategy

```
┌────────────────────────────────────────────────────────────────────┐
│                       INDEX ARCHITECTURE                            │
└────────────────────────────────────────────────────────────────────┘

B-TREE INDEXES (Fast Lookups)
├─► status, country, sector (WHERE clauses)
├─► created_at, updated_at (ORDER BY, time ranges)
├─► Foreign keys (JOINs)
└─► Composite indexes (Multi-column queries)

GIN INDEXES (JSONB Queries)
├─► dfi_partners (projects)
├─► extracted_data (documents)
├─► assumptions, outputs (financial_models)
├─► issues, recommendations (compliance_checks)
└─► risk_categories, identified_risks (risk_assessments)

TRIGRAM INDEXES (Fuzzy Search)
├─► name (projects)
├─► name (documents)
├─► name (stakeholders)
└─► organization (stakeholders)

PARTIAL INDEXES (Common Filters)
├─► Active projects (status IN (...) AND deleted_at IS NULL)
├─► Unprocessed documents (processed = false)
├─► High risk projects (risk_score > 70)
└─► Non-compliant checks (status = 'non_compliant')
```

## Function Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                     FUNCTION CATEGORIES                             │
└────────────────────────────────────────────────────────────────────┘

PROJECT MANAGEMENT
├─► calculate_project_risk_score(uuid) ──► Updates risk_score
├─► get_project_summary(uuid) ──► Returns JSON stats
└─► get_portfolio_analytics() ──► Portfolio-wide metrics

DOCUMENT PROCESSING
├─► mark_document_processed(uuid, json, text) ──► Update status
└─► get_unprocessed_documents(int) ──► Queue management

FINANCIAL MODELING
├─► calculate_npv(jsonb, float) ──► NPV calculation
└─► get_latest_financial_model(uuid) ──► Version control

COMPLIANCE & RISK
└─► get_compliance_status(uuid) ──► Compliance summary

SEARCH & DISCOVERY
└─► search_projects(text) ──► Fuzzy search with ranking

REPORTING
└─► generate_investment_memo_data(uuid) ──► Report aggregation

UTILITIES
├─► soft_delete(text, uuid) ──► Soft delete any record
└─► cleanup_old_audit_logs() ──► Maintenance
```

## View Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                      VIEW CATEGORIES                                │
└────────────────────────────────────────────────────────────────────┘

DASHBOARD VIEWS (Real-time)
├─► v_active_projects ──► Active projects + metrics
├─► v_project_dashboard ──► Full project detail
└─► v_recent_changes ──► Audit trail (7 days)

ANALYTICS VIEWS (Cached)
└─► mv_portfolio_overview ──► Portfolio stats (materialized)

OPERATIONAL VIEWS
├─► v_document_queue ──► Processing queue
├─► v_high_risk_projects ──► Risk monitoring
└─► v_compliance_summary ──► Compliance status

BUSINESS INTELLIGENCE
├─► v_financial_performance ──► Financial metrics
├─► v_stakeholder_matrix ──► Stakeholder analysis
└─► v_dfi_partnerships ──► DFI tracking
```

## Performance Optimization Strategy

```
┌────────────────────────────────────────────────────────────────────┐
│                  PERFORMANCE ARCHITECTURE                           │
└────────────────────────────────────────────────────────────────────┘

QUERY OPTIMIZATION
├─► Use indexes for WHERE clauses
├─► Partial indexes for common filters
├─► Avoid functions on indexed columns
└─► Use EXPLAIN ANALYZE for tuning

CACHING STRATEGY
├─► Materialized views for heavy aggregations
├─► Refresh on-demand or scheduled
└─► Use regular views for real-time data

DATA MANAGEMENT
├─► Soft deletes (prevent hard deletes)
├─► Audit log cleanup (retain 90 days)
├─► Regular ANALYZE for statistics
└─► Periodic VACUUM for space recovery

JSONB OPTIMIZATION
├─► GIN indexes for all queried JSONB
├─► Specific path extraction for performance
└─► Avoid deep nesting where possible
```

## Scalability Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                     SCALE STRATEGY                                  │
└────────────────────────────────────────────────────────────────────┘

HORIZONTAL SCALING
├─► Read replicas for analytics
├─► Connection pooling (PgBouncer)
└─► Materialized views reduce load

VERTICAL SCALING
├─► Optimized indexes reduce memory needs
├─► Efficient queries via views
└─► Periodic maintenance

DATA GROWTH MANAGEMENT
├─► Audit log cleanup (automatic)
├─► Document archival strategy
├─► Historical data partitioning (future)
└─► Soft delete cleanup (manual)

EXPECTED CAPACITY
├─► Projects: 10,000+ (indexed)
├─► Documents: 100,000+ (partitioned)
├─► Models: 50,000+ (versioned)
└─► Audit logs: 90 days retention
```

## Integration Points

```
┌────────────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                         │
└────────────────────────────────────────────────────────────────────┘

BACKEND API (FastAPI)
├─► Use functions for business logic
├─► RLS enforces security automatically
├─► JSONB for flexible data structures
└─► Audit trail for compliance

FRONTEND (Next.js)
├─► Use views for dashboard queries
├─► Real-time subscriptions via Supabase
├─► Optimized queries via indexes
└─► Client-side caching

AI/ML PIPELINE
├─► Store embeddings references
├─► JSONB for extracted data
├─► Batch processing via functions
└─► Link to vector database (Pinecone)

VECTOR DATABASE (Pinecone)
├─► embeddings_id links to vectors
├─► Hybrid search (SQL + Vector)
└─► Document retrieval

EXTERNAL SYSTEMS
├─► DFI APIs (future integration)
├─► Data export via views
└─► Webhook triggers (Supabase)
```

## Deployment Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT STRATEGY                               │
└────────────────────────────────────────────────────────────────────┘

MIGRATION-BASED DEPLOYMENT
├─► Version-controlled migrations
├─► Sequential application
├─► Rollback capability
└─► Zero-downtime updates

ENVIRONMENTS
├─► Development: Full seed data
├─► Staging: Subset of production
└─► Production: Migrations only

BACKUP STRATEGY
├─► Daily automated backups
├─► Point-in-time recovery
├─► Audit log archival
└─► Disaster recovery plan

MONITORING
├─► Query performance (pg_stat_statements)
├─► Index usage (pg_stat_user_indexes)
├─► Table statistics (pg_stat_user_tables)
└─► Audit log size
```

---

**Architecture Version**: 1.0.0
**Last Updated**: 2025-11-23
**Database Engine**: PostgreSQL 14+
**Schema Version**: 1.0.0
