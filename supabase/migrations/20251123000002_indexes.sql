-- InfraFlow AI Platform - Performance Indexes
-- Migration: 20251123000002_indexes.sql
-- Description: Creates indexes for optimal query performance

-- ============================================================================
-- PROJECTS TABLE INDEXES
-- ============================================================================

-- Primary lookup indexes
CREATE INDEX idx_projects_status ON projects(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_country ON projects(country) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_sector ON projects(sector) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
CREATE INDEX idx_projects_risk_score ON projects(risk_score DESC) WHERE deleted_at IS NULL;

-- Composite indexes for common queries
CREATE INDEX idx_projects_country_sector ON projects(country, sector) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_status_risk ON projects(status, risk_score DESC) WHERE deleted_at IS NULL;

-- JSONB GIN indexes for flexible queries
CREATE INDEX idx_projects_dfi_partners ON projects USING GIN (dfi_partners);
CREATE INDEX idx_projects_stakeholders ON projects USING GIN (stakeholders);
CREATE INDEX idx_projects_metadata ON projects USING GIN (metadata);

-- Full-text search on project name and description
CREATE INDEX idx_projects_name_trgm ON projects USING GIN (name gin_trgm_ops);
CREATE INDEX idx_projects_description_trgm ON projects USING GIN (description gin_trgm_ops);

-- Soft delete support
CREATE INDEX idx_projects_deleted_at ON projects(deleted_at) WHERE deleted_at IS NOT NULL;

COMMENT ON INDEX idx_projects_status IS 'Fast filtering by project status';
COMMENT ON INDEX idx_projects_country_sector IS 'Composite index for country-sector queries';
COMMENT ON INDEX idx_projects_name_trgm IS 'Trigram index for fuzzy name search';

-- ============================================================================
-- DOCUMENTS TABLE INDEXES
-- ============================================================================

-- Foreign key and lookup indexes
CREATE INDEX idx_documents_project_id ON documents(project_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_type ON documents(type) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_processed ON documents(processed) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_processing_status ON documents(processing_status);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);

-- Composite indexes
CREATE INDEX idx_documents_project_type ON documents(project_id, type) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_project_processed ON documents(project_id, processed) WHERE deleted_at IS NULL;

-- JSONB indexes
CREATE INDEX idx_documents_extracted_data ON documents USING GIN (extracted_data);
CREATE INDEX idx_documents_metadata ON documents USING GIN (metadata);

-- Full-text search
CREATE INDEX idx_documents_name_trgm ON documents USING GIN (name gin_trgm_ops);

-- Embeddings lookup
CREATE INDEX idx_documents_embeddings_id ON documents(embeddings_id) WHERE embeddings_id IS NOT NULL;

COMMENT ON INDEX idx_documents_project_id IS 'Fast lookup of documents by project';
COMMENT ON INDEX idx_documents_embeddings_id IS 'Quick access to vector embeddings';

-- ============================================================================
-- FINANCIAL_MODELS TABLE INDEXES
-- ============================================================================

-- Foreign key and lookup indexes
CREATE INDEX idx_financial_models_project_id ON financial_models(project_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_financial_models_type ON financial_models(model_type) WHERE deleted_at IS NULL;
CREATE INDEX idx_financial_models_version ON financial_models(project_id, version DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_financial_models_created_at ON financial_models(created_at DESC);

-- Performance metrics indexes
CREATE INDEX idx_financial_models_irr ON financial_models(irr DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_financial_models_npv ON financial_models(npv DESC) WHERE deleted_at IS NULL;

-- JSONB indexes
CREATE INDEX idx_financial_models_assumptions ON financial_models USING GIN (assumptions);
CREATE INDEX idx_financial_models_outputs ON financial_models USING GIN (outputs);
CREATE INDEX idx_financial_models_scenarios ON financial_models USING GIN (scenarios);

COMMENT ON INDEX idx_financial_models_version IS 'Retrieve latest version of financial model';
COMMENT ON INDEX idx_financial_models_irr IS 'Sort and filter by IRR performance';

-- ============================================================================
-- COMPLIANCE_CHECKS TABLE INDEXES
-- ============================================================================

-- Foreign key and lookup indexes
CREATE INDEX idx_compliance_checks_project_id ON compliance_checks(project_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_compliance_checks_standard ON compliance_checks(standard) WHERE deleted_at IS NULL;
CREATE INDEX idx_compliance_checks_status ON compliance_checks(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_compliance_checks_category ON compliance_checks(category) WHERE deleted_at IS NULL;
CREATE INDEX idx_compliance_checks_score ON compliance_checks(score DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_compliance_checks_checked_at ON compliance_checks(checked_at DESC);

-- Composite indexes
CREATE INDEX idx_compliance_project_standard ON compliance_checks(project_id, standard) WHERE deleted_at IS NULL;
CREATE INDEX idx_compliance_status_score ON compliance_checks(status, score DESC) WHERE deleted_at IS NULL;

-- JSONB indexes
CREATE INDEX idx_compliance_issues ON compliance_checks USING GIN (issues);
CREATE INDEX idx_compliance_recommendations ON compliance_checks USING GIN (recommendations);
CREATE INDEX idx_compliance_evidence ON compliance_checks USING GIN (evidence);

COMMENT ON INDEX idx_compliance_project_standard IS 'Fast lookup of compliance checks by project and standard';

-- ============================================================================
-- RISK_ASSESSMENTS TABLE INDEXES
-- ============================================================================

-- Foreign key and lookup indexes
CREATE INDEX idx_risk_assessments_project_id ON risk_assessments(project_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_risk_assessments_type ON risk_assessments(assessment_type) WHERE deleted_at IS NULL;
CREATE INDEX idx_risk_assessments_score ON risk_assessments(overall_risk_score DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_risk_assessments_date ON risk_assessments(assessment_date DESC);

-- JSONB indexes for complex risk analysis
CREATE INDEX idx_risk_categories ON risk_assessments USING GIN (risk_categories);
CREATE INDEX idx_identified_risks ON risk_assessments USING GIN (identified_risks);
CREATE INDEX idx_mitigation_strategies ON risk_assessments USING GIN (mitigation_strategies);
CREATE INDEX idx_country_risk ON risk_assessments USING GIN (country_risk);
CREATE INDEX idx_political_risk ON risk_assessments USING GIN (political_risk);

COMMENT ON INDEX idx_risk_assessments_score IS 'Filter and sort projects by risk score';

-- ============================================================================
-- STAKEHOLDERS TABLE INDEXES
-- ============================================================================

-- Foreign key and lookup indexes
CREATE INDEX idx_stakeholders_project_id ON stakeholders(project_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_stakeholders_role ON stakeholders(role) WHERE deleted_at IS NULL;
CREATE INDEX idx_stakeholders_type ON stakeholders(stakeholder_type) WHERE deleted_at IS NULL;
CREATE INDEX idx_stakeholders_influence ON stakeholders(influence_level) WHERE deleted_at IS NULL;
CREATE INDEX idx_stakeholders_engagement ON stakeholders(engagement_status) WHERE deleted_at IS NULL;

-- Full-text search
CREATE INDEX idx_stakeholders_name_trgm ON stakeholders USING GIN (name gin_trgm_ops);
CREATE INDEX idx_stakeholders_organization_trgm ON stakeholders USING GIN (organization gin_trgm_ops);

-- Composite indexes
CREATE INDEX idx_stakeholders_project_role ON stakeholders(project_id, role) WHERE deleted_at IS NULL;

COMMENT ON INDEX idx_stakeholders_project_id IS 'Fast lookup of stakeholders by project';

-- ============================================================================
-- REPORTS TABLE INDEXES
-- ============================================================================

-- Foreign key and lookup indexes
CREATE INDEX idx_reports_project_id ON reports(project_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_reports_type ON reports(report_type) WHERE deleted_at IS NULL;
CREATE INDEX idx_reports_created_at ON reports(created_at DESC);

-- JSONB indexes
CREATE INDEX idx_reports_content ON reports USING GIN (content);
CREATE INDEX idx_reports_metadata ON reports USING GIN (metadata);

-- Full-text search
CREATE INDEX idx_reports_title_trgm ON reports USING GIN (title gin_trgm_ops);

COMMENT ON INDEX idx_reports_project_id IS 'Fast lookup of reports by project';

-- ============================================================================
-- AUDIT_LOG TABLE INDEXES
-- ============================================================================

-- High-performance indexes for audit queries
CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_changed_at ON audit_log(changed_at DESC);
CREATE INDEX idx_audit_log_changed_by ON audit_log(changed_by);
CREATE INDEX idx_audit_log_action ON audit_log(action);

-- Composite index for common audit queries
CREATE INDEX idx_audit_log_table_action ON audit_log(table_name, action, changed_at DESC);

COMMENT ON INDEX idx_audit_log_table_record IS 'Fast lookup of audit history for specific records';

-- ============================================================================
-- PARTIAL INDEXES FOR COMMON FILTERS
-- ============================================================================

-- Active projects only
CREATE INDEX idx_active_projects ON projects(created_at DESC)
    WHERE status IN ('pipeline', 'under_review', 'approved', 'active') AND deleted_at IS NULL;

-- Unprocessed documents
CREATE INDEX idx_unprocessed_documents ON documents(created_at DESC)
    WHERE processed = FALSE AND deleted_at IS NULL;

-- High-risk projects
CREATE INDEX idx_high_risk_projects ON projects(risk_score DESC)
    WHERE risk_score > 70 AND deleted_at IS NULL;

-- Non-compliant checks
CREATE INDEX idx_non_compliant_checks ON compliance_checks(checked_at DESC)
    WHERE status = 'non_compliant' AND deleted_at IS NULL;

COMMENT ON INDEX idx_active_projects IS 'Optimized index for active projects dashboard';
COMMENT ON INDEX idx_unprocessed_documents IS 'Fast access to documents pending processing';

-- ============================================================================
-- ANALYZE TABLES
-- ============================================================================

-- Update statistics for query planner
ANALYZE projects;
ANALYZE documents;
ANALYZE financial_models;
ANALYZE compliance_checks;
ANALYZE risk_assessments;
ANALYZE stakeholders;
ANALYZE reports;
ANALYZE audit_log;
