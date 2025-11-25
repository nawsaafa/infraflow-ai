-- ============================================================================
-- InfraFlow AI Platform - Complete Supabase Schema Setup
-- ============================================================================
--
-- INSTRUCTIONS:
-- 1. Go to Supabase Dashboard: https://supabase.com/dashboard/project/abhnlhbkmrozxtfoaxnv
-- 2. Click on "SQL Editor" in the left sidebar
-- 3. Click "New Query"
-- 4. Copy and paste this ENTIRE file
-- 5. Click "Run" button
-- 6. Wait for execution to complete (may take 30-60 seconds)
-- 7. You should see "Success. No rows returned" message
--
-- This script creates:
-- - 10 core tables (users, projects, documents, financial_models, compliance_checks,
--   risk_assessments, stakeholders, reports, audit_log, milestones)
-- - All indexes for performance
-- - Row Level Security policies
-- - Database functions and triggers
-- - Utility views for reporting
--
-- ============================================================================

-- InfraFlow AI Platform - Initial Database Schema
-- Migration: 20251123000001_initial_schema.sql
-- Description: Creates core tables for projects, documents, financial models, and compliance checks

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search optimization

-- Create custom types
CREATE TYPE project_status AS ENUM (
    'draft',
    'pipeline',
    'under_review',
    'approved',
    'rejected',
    'active',
    'completed',
    'cancelled'
);

CREATE TYPE document_type AS ENUM (
    'feasibility_study',
    'financial_model',
    'environmental_impact',
    'technical_specification',
    'legal_agreement',
    'compliance_report',
    'investment_memo',
    'due_diligence',
    'other'
);

CREATE TYPE compliance_status AS ENUM (
    'pending',
    'in_progress',
    'compliant',
    'non_compliant',
    'needs_review',
    'approved'
);

CREATE TYPE sector_type AS ENUM (
    'renewable_energy',
    'green_hydrogen',
    'transmission',
    'water',
    'transportation',
    'waste_management',
    'other'
);

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    sponsor TEXT,
    country TEXT NOT NULL,
    sector sector_type NOT NULL,
    total_value DECIMAL(15,2),
    currency TEXT DEFAULT 'USD',
    dfi_partners JSONB DEFAULT '[]'::jsonb,
    status project_status DEFAULT 'draft',
    risk_score FLOAT CHECK (risk_score >= 0 AND risk_score <= 100),
    description TEXT,
    location JSONB, -- {latitude, longitude, address}
    timeline JSONB, -- {start_date, completion_date, milestones}
    stakeholders JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    updated_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT projects_name_check CHECK (char_length(name) >= 3),
    CONSTRAINT projects_total_value_check CHECK (total_value >= 0)
);

COMMENT ON TABLE projects IS 'Core infrastructure projects tracked in the platform';
COMMENT ON COLUMN projects.dfi_partners IS 'Array of Development Finance Institutions involved: [{name, commitment, status}]';
COMMENT ON COLUMN projects.risk_score IS 'Overall risk score from 0-100, calculated by risk prediction model';
COMMENT ON COLUMN projects.stakeholders IS 'Array of project stakeholders: [{name, role, contact, organization}]';
COMMENT ON COLUMN projects.timeline IS 'Project timeline with milestones: {start_date, completion_date, milestones: [{name, date, status}]}';

-- ============================================================================
-- DOCUMENTS TABLE
-- ============================================================================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type document_type NOT NULL,
    url TEXT,
    file_path TEXT,
    file_size BIGINT,
    mime_type TEXT,
    processed BOOLEAN DEFAULT FALSE,
    processing_status TEXT DEFAULT 'pending',
    extracted_data JSONB DEFAULT '{}'::jsonb,
    embeddings_id TEXT,
    page_count INTEGER,
    language TEXT DEFAULT 'en',
    confidence_score FLOAT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    created_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT documents_name_check CHECK (char_length(name) >= 1),
    CONSTRAINT documents_file_size_check CHECK (file_size >= 0),
    CONSTRAINT documents_page_count_check CHECK (page_count >= 0),
    CONSTRAINT documents_confidence_check CHECK (confidence_score >= 0 AND confidence_score <= 1)
);

COMMENT ON TABLE documents IS 'Project documents uploaded and processed through the AI pipeline';
COMMENT ON COLUMN documents.extracted_data IS 'Structured data extracted from document: {summary, key_terms, entities, risks, financials}';
COMMENT ON COLUMN documents.embeddings_id IS 'Reference ID for vector embeddings in Pinecone/Weaviate';
COMMENT ON COLUMN documents.confidence_score IS 'AI extraction confidence score (0-1)';
COMMENT ON COLUMN documents.processing_status IS 'Current processing status: pending, processing, completed, failed';

-- ============================================================================
-- FINANCIAL_MODELS TABLE
-- ============================================================================
CREATE TABLE financial_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    model_type TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    assumptions JSONB NOT NULL DEFAULT '{}'::jsonb,
    outputs JSONB DEFAULT '{}'::jsonb,
    scenarios JSONB DEFAULT '[]'::jsonb,
    dcf_analysis JSONB,
    sensitivity_analysis JSONB,
    risk_metrics JSONB,
    currency TEXT DEFAULT 'USD',
    discount_rate FLOAT,
    project_life_years INTEGER,
    irr FLOAT,
    npv DECIMAL(15,2),
    payback_period FLOAT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT financial_models_version_check CHECK (version > 0),
    CONSTRAINT financial_models_project_life_check CHECK (project_life_years > 0)
);

COMMENT ON TABLE financial_models IS 'Financial models and DCF analyses for projects';
COMMENT ON COLUMN financial_models.assumptions IS 'Model assumptions: {revenue_growth, opex, capex, debt_terms, equity_terms}';
COMMENT ON COLUMN financial_models.outputs IS 'Model outputs: {revenue_projections, cost_projections, cash_flows}';
COMMENT ON COLUMN financial_models.scenarios IS 'Monte Carlo scenarios: [{name, probability, npv, irr, key_assumptions}]';
COMMENT ON COLUMN financial_models.dcf_analysis IS 'Detailed DCF breakdown: {cash_flows, terminal_value, enterprise_value}';
COMMENT ON COLUMN financial_models.irr IS 'Internal Rate of Return (percentage)';
COMMENT ON COLUMN financial_models.npv IS 'Net Present Value';

-- ============================================================================
-- COMPLIANCE_CHECKS TABLE
-- ============================================================================
CREATE TABLE compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    standard TEXT NOT NULL,
    category TEXT,
    status compliance_status DEFAULT 'pending',
    score FLOAT,
    issues JSONB DEFAULT '[]'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    evidence JSONB DEFAULT '[]'::jsonb,
    reviewer TEXT,
    notes TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT compliance_checks_score_check CHECK (score >= 0 AND score <= 100)
);

COMMENT ON TABLE compliance_checks IS 'Compliance checks against DFI and regulatory standards';
COMMENT ON COLUMN compliance_checks.standard IS 'Compliance standard: EBRD, IFC, EU Taxonomy, Local Regulations';
COMMENT ON COLUMN compliance_checks.issues IS 'Array of compliance issues: [{severity, description, requirement, gap}]';
COMMENT ON COLUMN compliance_checks.recommendations IS 'Array of remediation recommendations: [{priority, action, timeline, resources}]';
COMMENT ON COLUMN compliance_checks.evidence IS 'Supporting evidence: [{document_id, section, finding}]';

-- ============================================================================
-- RISK_ASSESSMENTS TABLE
-- ============================================================================
CREATE TABLE risk_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    assessment_type TEXT NOT NULL,
    overall_risk_score FLOAT CHECK (overall_risk_score >= 0 AND overall_risk_score <= 100),
    risk_categories JSONB DEFAULT '{}'::jsonb,
    identified_risks JSONB DEFAULT '[]'::jsonb,
    mitigation_strategies JSONB DEFAULT '[]'::jsonb,
    risk_matrix JSONB,
    country_risk JSONB,
    political_risk JSONB,
    financial_risk JSONB,
    technical_risk JSONB,
    environmental_risk JSONB,
    assessed_by TEXT,
    assessment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE
);

COMMENT ON TABLE risk_assessments IS 'Comprehensive risk assessments for projects';
COMMENT ON COLUMN risk_assessments.risk_categories IS 'Risk breakdown by category: {political, financial, technical, environmental, regulatory}';
COMMENT ON COLUMN risk_assessments.identified_risks IS 'Array of identified risks: [{category, description, likelihood, impact, severity}]';
COMMENT ON COLUMN risk_assessments.mitigation_strategies IS 'Array of mitigation strategies: [{risk_id, strategy, cost, effectiveness}]';

-- ============================================================================
-- STAKEHOLDERS TABLE
-- ============================================================================
CREATE TABLE stakeholders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    organization TEXT,
    role TEXT NOT NULL,
    contact_email TEXT,
    contact_phone TEXT,
    country TEXT,
    stakeholder_type TEXT,
    influence_level TEXT,
    engagement_status TEXT,
    notes TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT stakeholders_name_check CHECK (char_length(name) >= 2)
);

COMMENT ON TABLE stakeholders IS 'Project stakeholders and their roles';
COMMENT ON COLUMN stakeholders.influence_level IS 'Stakeholder influence: high, medium, low';
COMMENT ON COLUMN stakeholders.engagement_status IS 'Current engagement: active, pending, inactive';

-- ============================================================================
-- REPORTS TABLE
-- ============================================================================
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL,
    title TEXT NOT NULL,
    content JSONB NOT NULL,
    format TEXT DEFAULT 'json',
    file_url TEXT,
    generated_by TEXT,
    template_used TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE
);

COMMENT ON TABLE reports IS 'Generated reports: investment memos, compliance reports, risk matrices';
COMMENT ON COLUMN reports.report_type IS 'Type: investment_memo, compliance_report, risk_matrix, due_diligence, executive_summary';
COMMENT ON COLUMN reports.content IS 'Structured report content';

-- ============================================================================
-- AUDIT_LOG TABLE
-- ============================================================================
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by UUID,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

COMMENT ON TABLE audit_log IS 'Audit trail for all data changes';

-- ============================================================================
-- Create updated_at trigger function
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to all tables
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_financial_models_updated_at BEFORE UPDATE ON financial_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_compliance_checks_updated_at BEFORE UPDATE ON compliance_checks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_risk_assessments_updated_at BEFORE UPDATE ON risk_assessments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stakeholders_updated_at BEFORE UPDATE ON stakeholders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
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
-- InfraFlow AI Platform - Row Level Security Policies
-- Migration: 20251123000003_rls_policies.sql
-- Description: Implements RLS policies for multi-tenant data isolation and access control

-- ============================================================================
-- ENABLE ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_models ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_checks ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE stakeholders ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- CREATE HELPER FUNCTIONS FOR RLS
-- ============================================================================

-- Function to check if user has access to a project
CREATE OR REPLACE FUNCTION has_project_access(project_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
    -- Check if user is authenticated
    IF auth.uid() IS NULL THEN
        RETURN FALSE;
    END IF;

    -- Check if user is project owner, team member, or has admin role
    RETURN EXISTS (
        SELECT 1 FROM projects
        WHERE id = project_uuid
        AND (
            created_by = auth.uid()
            OR updated_by = auth.uid()
            OR auth.jwt() ->> 'role' = 'admin'
            OR auth.jwt() ->> 'role' = 'service_role'
        )
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check if user is admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        auth.jwt() ->> 'role' = 'admin' OR
        auth.jwt() ->> 'role' = 'service_role'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get user's organization
CREATE OR REPLACE FUNCTION get_user_organization()
RETURNS TEXT AS $$
BEGIN
    RETURN auth.jwt() ->> 'organization_id';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- PROJECTS TABLE RLS POLICIES
-- ============================================================================

-- Allow authenticated users to view projects they have access to
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

-- Allow authenticated users to create projects
CREATE POLICY "Users can create projects"
    ON projects FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND created_by = auth.uid()
    );

-- Allow project creators and admins to update projects
CREATE POLICY "Users can update their projects"
    ON projects FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND (
            created_by = auth.uid()
            OR is_admin()
        )
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND (
            created_by = auth.uid()
            OR is_admin()
        )
    );

-- Allow project creators and admins to soft delete projects
CREATE POLICY "Users can delete their projects"
    ON projects FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND (
            created_by = auth.uid()
            OR is_admin()
        )
    );

-- ============================================================================
-- DOCUMENTS TABLE RLS POLICIES
-- ============================================================================

-- Allow users to view documents for projects they have access to
CREATE POLICY "Users can view project documents"
    ON documents FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            has_project_access(project_id)
            OR is_admin()
        )
    );

-- Allow users to upload documents to their projects
CREATE POLICY "Users can upload documents to their projects"
    ON documents FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to update documents in their projects
CREATE POLICY "Users can update project documents"
    ON documents FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to delete documents from their projects
CREATE POLICY "Users can delete project documents"
    ON documents FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- ============================================================================
-- FINANCIAL_MODELS TABLE RLS POLICIES
-- ============================================================================

-- Allow users to view financial models for their projects
CREATE POLICY "Users can view project financial models"
    ON financial_models FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            has_project_access(project_id)
            OR is_admin()
        )
    );

-- Allow users to create financial models for their projects
CREATE POLICY "Users can create financial models"
    ON financial_models FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to update financial models for their projects
CREATE POLICY "Users can update financial models"
    ON financial_models FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to delete financial models from their projects
CREATE POLICY "Users can delete financial models"
    ON financial_models FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- ============================================================================
-- COMPLIANCE_CHECKS TABLE RLS POLICIES
-- ============================================================================

-- Allow users to view compliance checks for their projects
CREATE POLICY "Users can view project compliance checks"
    ON compliance_checks FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            has_project_access(project_id)
            OR is_admin()
        )
    );

-- Allow users to create compliance checks for their projects
CREATE POLICY "Users can create compliance checks"
    ON compliance_checks FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to update compliance checks for their projects
CREATE POLICY "Users can update compliance checks"
    ON compliance_checks FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to delete compliance checks from their projects
CREATE POLICY "Users can delete compliance checks"
    ON compliance_checks FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- ============================================================================
-- RISK_ASSESSMENTS TABLE RLS POLICIES
-- ============================================================================

-- Allow users to view risk assessments for their projects
CREATE POLICY "Users can view project risk assessments"
    ON risk_assessments FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            has_project_access(project_id)
            OR is_admin()
        )
    );

-- Allow users to create risk assessments for their projects
CREATE POLICY "Users can create risk assessments"
    ON risk_assessments FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to update risk assessments for their projects
CREATE POLICY "Users can update risk assessments"
    ON risk_assessments FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to delete risk assessments from their projects
CREATE POLICY "Users can delete risk assessments"
    ON risk_assessments FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- ============================================================================
-- STAKEHOLDERS TABLE RLS POLICIES
-- ============================================================================

-- Allow users to view stakeholders for their projects
CREATE POLICY "Users can view project stakeholders"
    ON stakeholders FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            has_project_access(project_id)
            OR is_admin()
        )
    );

-- Allow users to create stakeholders for their projects
CREATE POLICY "Users can create stakeholders"
    ON stakeholders FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to update stakeholders for their projects
CREATE POLICY "Users can update stakeholders"
    ON stakeholders FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to delete stakeholders from their projects
CREATE POLICY "Users can delete stakeholders"
    ON stakeholders FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- ============================================================================
-- REPORTS TABLE RLS POLICIES
-- ============================================================================

-- Allow users to view reports for their projects
CREATE POLICY "Users can view project reports"
    ON reports FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            has_project_access(project_id)
            OR is_admin()
        )
    );

-- Allow users to create reports for their projects
CREATE POLICY "Users can create reports"
    ON reports FOR INSERT
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to update reports for their projects
CREATE POLICY "Users can update reports"
    ON reports FOR UPDATE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    )
    WITH CHECK (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- Allow users to delete reports from their projects
CREATE POLICY "Users can delete reports"
    ON reports FOR DELETE
    USING (
        auth.uid() IS NOT NULL
        AND has_project_access(project_id)
    );

-- ============================================================================
-- AUDIT_LOG TABLE RLS POLICIES
-- ============================================================================

-- Only admins can view audit logs
CREATE POLICY "Admins can view audit logs"
    ON audit_log FOR SELECT
    USING (is_admin());

-- System can insert audit logs (service role)
CREATE POLICY "System can create audit logs"
    ON audit_log FOR INSERT
    WITH CHECK (
        auth.jwt() ->> 'role' = 'service_role'
        OR is_admin()
    );

-- No one can update or delete audit logs (immutable)
-- (No UPDATE or DELETE policies = denied)

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO service_role;

-- Grant table permissions to authenticated users
GRANT SELECT, INSERT, UPDATE, DELETE ON projects TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON documents TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON financial_models TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON compliance_checks TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON risk_assessments TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON stakeholders TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON reports TO authenticated;
GRANT SELECT ON audit_log TO authenticated;

-- Grant full access to service role
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON POLICY "Users can view their projects" ON projects IS
    'Users can view projects they created or have been granted access to';

COMMENT ON POLICY "Users can create projects" ON projects IS
    'Authenticated users can create new projects';

COMMENT ON FUNCTION has_project_access IS
    'Check if current user has access to specified project';

COMMENT ON FUNCTION is_admin IS
    'Check if current user has admin role';
-- InfraFlow AI Platform - Database Functions
-- Migration: 20251123000004_functions.sql
-- Description: Utility functions for common database operations

-- ============================================================================
-- PROJECT MANAGEMENT FUNCTIONS
-- ============================================================================

-- Function to calculate project risk score based on multiple factors
CREATE OR REPLACE FUNCTION calculate_project_risk_score(project_uuid UUID)
RETURNS FLOAT AS $$
DECLARE
    avg_compliance_score FLOAT;
    avg_risk_assessment FLOAT;
    final_risk_score FLOAT;
BEGIN
    -- Get average compliance score (lower is riskier)
    SELECT AVG(score) INTO avg_compliance_score
    FROM compliance_checks
    WHERE project_id = project_uuid
    AND status = 'compliant'
    AND deleted_at IS NULL;

    -- Get average risk assessment score
    SELECT AVG(overall_risk_score) INTO avg_risk_assessment
    FROM risk_assessments
    WHERE project_id = project_uuid
    AND deleted_at IS NULL;

    -- Calculate weighted risk score
    final_risk_score := COALESCE(
        (COALESCE(100 - avg_compliance_score, 50) * 0.4) +
        (COALESCE(avg_risk_assessment, 50) * 0.6),
        50
    );

    -- Update project table
    UPDATE projects
    SET risk_score = final_risk_score,
        updated_at = NOW()
    WHERE id = project_uuid;

    RETURN final_risk_score;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION calculate_project_risk_score IS
    'Calculates and updates project risk score based on compliance checks and risk assessments';

-- Function to get project summary statistics
CREATE OR REPLACE FUNCTION get_project_summary(project_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'project_id', p.id,
        'project_name', p.name,
        'status', p.status,
        'risk_score', p.risk_score,
        'total_value', p.total_value,
        'currency', p.currency,
        'document_count', (
            SELECT COUNT(*) FROM documents
            WHERE project_id = p.id AND deleted_at IS NULL
        ),
        'processed_documents', (
            SELECT COUNT(*) FROM documents
            WHERE project_id = p.id AND processed = TRUE AND deleted_at IS NULL
        ),
        'compliance_checks', (
            SELECT COUNT(*) FROM compliance_checks
            WHERE project_id = p.id AND deleted_at IS NULL
        ),
        'compliant_checks', (
            SELECT COUNT(*) FROM compliance_checks
            WHERE project_id = p.id AND status = 'compliant' AND deleted_at IS NULL
        ),
        'financial_models', (
            SELECT COUNT(*) FROM financial_models
            WHERE project_id = p.id AND deleted_at IS NULL
        ),
        'latest_irr', (
            SELECT irr FROM financial_models
            WHERE project_id = p.id AND deleted_at IS NULL
            ORDER BY version DESC LIMIT 1
        ),
        'stakeholder_count', (
            SELECT COUNT(*) FROM stakeholders
            WHERE project_id = p.id AND deleted_at IS NULL
        ),
        'risk_assessments', (
            SELECT COUNT(*) FROM risk_assessments
            WHERE project_id = p.id AND deleted_at IS NULL
        )
    ) INTO result
    FROM projects p
    WHERE p.id = project_uuid;

    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_project_summary IS
    'Returns comprehensive summary statistics for a project';

-- Function to get portfolio analytics
CREATE OR REPLACE FUNCTION get_portfolio_analytics()
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_projects', COUNT(*),
        'active_projects', COUNT(*) FILTER (WHERE status IN ('pipeline', 'under_review', 'approved', 'active')),
        'total_investment_value', SUM(total_value),
        'avg_risk_score', AVG(risk_score),
        'projects_by_status', (
            SELECT json_object_agg(status, count)
            FROM (
                SELECT status, COUNT(*) as count
                FROM projects
                WHERE deleted_at IS NULL
                GROUP BY status
            ) s
        ),
        'projects_by_sector', (
            SELECT json_object_agg(sector, count)
            FROM (
                SELECT sector, COUNT(*) as count
                FROM projects
                WHERE deleted_at IS NULL
                GROUP BY sector
            ) s
        ),
        'projects_by_country', (
            SELECT json_object_agg(country, count)
            FROM (
                SELECT country, COUNT(*) as count
                FROM projects
                WHERE deleted_at IS NULL
                GROUP BY country
            ) s
        )
    ) INTO result
    FROM projects
    WHERE deleted_at IS NULL;

    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_portfolio_analytics IS
    'Returns portfolio-wide analytics and statistics';

-- ============================================================================
-- DOCUMENT PROCESSING FUNCTIONS
-- ============================================================================

-- Function to mark document as processed and update project
CREATE OR REPLACE FUNCTION mark_document_processed(
    doc_uuid UUID,
    extracted JSON,
    embedding_id TEXT
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE documents
    SET processed = TRUE,
        processing_status = 'completed',
        processed_at = NOW(),
        extracted_data = extracted,
        embeddings_id = embedding_id,
        updated_at = NOW()
    WHERE id = doc_uuid;

    RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION mark_document_processed IS
    'Marks a document as processed and stores extracted data';

-- Function to get unprocessed documents
CREATE OR REPLACE FUNCTION get_unprocessed_documents(limit_count INT DEFAULT 10)
RETURNS TABLE (
    id UUID,
    project_id UUID,
    name TEXT,
    type document_type,
    url TEXT,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT d.id, d.project_id, d.name, d.type, d.url, d.created_at
    FROM documents d
    WHERE d.processed = FALSE
    AND d.deleted_at IS NULL
    ORDER BY d.created_at ASC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_unprocessed_documents IS
    'Returns list of documents pending processing';

-- ============================================================================
-- FINANCIAL MODELING FUNCTIONS
-- ============================================================================

-- Function to calculate NPV for a financial model
CREATE OR REPLACE FUNCTION calculate_npv(
    cash_flows JSONB,
    discount_rate FLOAT
)
RETURNS DECIMAL AS $$
DECLARE
    npv DECIMAL := 0;
    year_data JSONB;
    year_num INT;
    cash_flow DECIMAL;
BEGIN
    FOR year_data IN SELECT * FROM jsonb_array_elements(cash_flows)
    LOOP
        year_num := (year_data->>'year')::INT;
        cash_flow := (year_data->>'cash_flow')::DECIMAL;
        npv := npv + (cash_flow / POWER(1 + discount_rate, year_num));
    END LOOP;

    RETURN npv;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION calculate_npv IS
    'Calculates Net Present Value given cash flows and discount rate';

-- Function to get latest financial model for project
CREATE OR REPLACE FUNCTION get_latest_financial_model(project_uuid UUID)
RETURNS financial_models AS $$
DECLARE
    result financial_models;
BEGIN
    SELECT * INTO result
    FROM financial_models
    WHERE project_id = project_uuid
    AND deleted_at IS NULL
    ORDER BY version DESC
    LIMIT 1;

    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_latest_financial_model IS
    'Returns the latest version of financial model for a project';

-- ============================================================================
-- COMPLIANCE FUNCTIONS
-- ============================================================================

-- Function to check project compliance status
CREATE OR REPLACE FUNCTION get_compliance_status(project_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_checks', COUNT(*),
        'compliant', COUNT(*) FILTER (WHERE status = 'compliant'),
        'non_compliant', COUNT(*) FILTER (WHERE status = 'non_compliant'),
        'pending', COUNT(*) FILTER (WHERE status = 'pending'),
        'average_score', AVG(score),
        'standards_checked', json_agg(DISTINCT standard),
        'critical_issues', (
            SELECT json_agg(issue)
            FROM (
                SELECT jsonb_array_elements(issues) as issue
                FROM compliance_checks
                WHERE project_id = project_uuid
                AND status = 'non_compliant'
                AND deleted_at IS NULL
            ) i
            WHERE (issue->>'severity') = 'critical'
        )
    ) INTO result
    FROM compliance_checks
    WHERE project_id = project_uuid
    AND deleted_at IS NULL;

    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_compliance_status IS
    'Returns comprehensive compliance status for a project';

-- ============================================================================
-- SEARCH FUNCTIONS
-- ============================================================================

-- Function for full-text search across projects
CREATE OR REPLACE FUNCTION search_projects(search_query TEXT)
RETURNS TABLE (
    id UUID,
    name TEXT,
    country TEXT,
    sector sector_type,
    status project_status,
    risk_score FLOAT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.country,
        p.sector,
        p.status,
        p.risk_score,
        GREATEST(
            similarity(p.name, search_query),
            similarity(COALESCE(p.description, ''), search_query)
        ) as similarity
    FROM projects p
    WHERE p.deleted_at IS NULL
    AND (
        p.name ILIKE '%' || search_query || '%'
        OR p.description ILIKE '%' || search_query || '%'
        OR p.country ILIKE '%' || search_query || '%'
    )
    ORDER BY similarity DESC, p.created_at DESC
    LIMIT 50;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION search_projects IS
    'Full-text search across projects with relevance ranking';

-- ============================================================================
-- AUDIT FUNCTIONS
-- ============================================================================

-- Function to create audit log entry
CREATE OR REPLACE FUNCTION create_audit_log()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (
        table_name,
        record_id,
        action,
        old_data,
        new_data,
        changed_by,
        changed_at
    ) VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END,
        auth.uid(),
        NOW()
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION create_audit_log IS
    'Trigger function to create audit log entries for data changes';

-- Apply audit trigger to all main tables
CREATE TRIGGER audit_projects
    AFTER INSERT OR UPDATE OR DELETE ON projects
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

CREATE TRIGGER audit_documents
    AFTER INSERT OR UPDATE OR DELETE ON documents
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

CREATE TRIGGER audit_financial_models
    AFTER INSERT OR UPDATE OR DELETE ON financial_models
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

CREATE TRIGGER audit_compliance_checks
    AFTER INSERT OR UPDATE OR DELETE ON compliance_checks
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

CREATE TRIGGER audit_risk_assessments
    AFTER INSERT OR UPDATE OR DELETE ON risk_assessments
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

-- ============================================================================
-- REPORTING FUNCTIONS
-- ============================================================================

-- Function to generate investment memo data
CREATE OR REPLACE FUNCTION generate_investment_memo_data(project_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
    project_data projects;
    latest_model financial_models;
BEGIN
    -- Get project data
    SELECT * INTO project_data
    FROM projects
    WHERE id = project_uuid;

    -- Get latest financial model
    SELECT * INTO latest_model
    FROM financial_models
    WHERE project_id = project_uuid
    AND deleted_at IS NULL
    ORDER BY version DESC
    LIMIT 1;

    -- Build investment memo structure
    SELECT json_build_object(
        'project', json_build_object(
            'name', project_data.name,
            'sponsor', project_data.sponsor,
            'country', project_data.country,
            'sector', project_data.sector,
            'total_value', project_data.total_value,
            'currency', project_data.currency,
            'description', project_data.description,
            'status', project_data.status
        ),
        'financial_metrics', json_build_object(
            'irr', latest_model.irr,
            'npv', latest_model.npv,
            'payback_period', latest_model.payback_period,
            'discount_rate', latest_model.discount_rate,
            'project_life', latest_model.project_life_years
        ),
        'risk_summary', (
            SELECT json_build_object(
                'overall_score', project_data.risk_score,
                'assessments', json_agg(
                    json_build_object(
                        'type', assessment_type,
                        'score', overall_risk_score,
                        'date', assessment_date
                    )
                )
            )
            FROM risk_assessments
            WHERE project_id = project_uuid
            AND deleted_at IS NULL
        ),
        'compliance_summary', get_compliance_status(project_uuid),
        'stakeholders', (
            SELECT json_agg(
                json_build_object(
                    'name', name,
                    'organization', organization,
                    'role', role
                )
            )
            FROM stakeholders
            WHERE project_id = project_uuid
            AND deleted_at IS NULL
        ),
        'dfi_partners', project_data.dfi_partners
    ) INTO result;

    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION generate_investment_memo_data IS
    'Generates structured data for investment memo report';

-- ============================================================================
-- SOFT DELETE FUNCTION
-- ============================================================================

-- Function to soft delete records
CREATE OR REPLACE FUNCTION soft_delete(
    table_name TEXT,
    record_uuid UUID
)
RETURNS BOOLEAN AS $$
BEGIN
    EXECUTE format('UPDATE %I SET deleted_at = NOW() WHERE id = $1', table_name)
    USING record_uuid;

    RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION soft_delete IS
    'Soft deletes a record by setting deleted_at timestamp';

-- ============================================================================
-- CLEANUP FUNCTION
-- ============================================================================

-- Function to cleanup old audit logs (retain 90 days)
CREATE OR REPLACE FUNCTION cleanup_old_audit_logs()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM audit_log
    WHERE changed_at < NOW() - INTERVAL '90 days';

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION cleanup_old_audit_logs IS
    'Removes audit log entries older than 90 days';
-- InfraFlow AI Platform - Utility Views and Materialized Views
-- Migration: 20251123000005_utility_views.sql
-- Description: Creates useful views for common queries and reporting

-- ============================================================================
-- ACTIVE PROJECTS VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_active_projects AS
SELECT
    p.id,
    p.name,
    p.sponsor,
    p.country,
    p.sector,
    p.total_value,
    p.currency,
    p.status,
    p.risk_score,
    p.created_at,
    COUNT(DISTINCT d.id) as document_count,
    COUNT(DISTINCT d.id) FILTER (WHERE d.processed = TRUE) as processed_documents,
    COUNT(DISTINCT fm.id) as financial_model_count,
    COUNT(DISTINCT cc.id) as compliance_check_count,
    COUNT(DISTINCT cc.id) FILTER (WHERE cc.status = 'compliant') as compliant_checks,
    COUNT(DISTINCT ra.id) as risk_assessment_count,
    COUNT(DISTINCT s.id) as stakeholder_count,
    MAX(fm.irr) as latest_irr,
    MAX(fm.npv) as latest_npv
FROM projects p
LEFT JOIN documents d ON d.project_id = p.id AND d.deleted_at IS NULL
LEFT JOIN financial_models fm ON fm.project_id = p.id AND fm.deleted_at IS NULL
LEFT JOIN compliance_checks cc ON cc.project_id = p.id AND cc.deleted_at IS NULL
LEFT JOIN risk_assessments ra ON ra.project_id = p.id AND ra.deleted_at IS NULL
LEFT JOIN stakeholders s ON s.project_id = p.id AND s.deleted_at IS NULL
WHERE p.deleted_at IS NULL
AND p.status IN ('pipeline', 'under_review', 'approved', 'active')
GROUP BY p.id;

COMMENT ON VIEW v_active_projects IS 'Active projects with summary statistics';

-- ============================================================================
-- PROJECT DASHBOARD VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_project_dashboard AS
SELECT
    p.id,
    p.name,
    p.sponsor,
    p.country,
    p.sector,
    p.total_value,
    p.currency,
    p.status,
    p.risk_score,
    p.dfi_partners,
    p.created_at,

    -- Document metrics
    json_build_object(
        'total', COUNT(DISTINCT d.id),
        'processed', COUNT(DISTINCT d.id) FILTER (WHERE d.processed = TRUE),
        'pending', COUNT(DISTINCT d.id) FILTER (WHERE d.processed = FALSE)
    ) as documents,

    -- Financial metrics
    json_build_object(
        'irr', MAX(fm.irr),
        'npv', MAX(fm.npv),
        'payback_period', MAX(fm.payback_period),
        'models_count', COUNT(DISTINCT fm.id)
    ) as financial_metrics,

    -- Compliance metrics
    json_build_object(
        'total_checks', COUNT(DISTINCT cc.id),
        'compliant', COUNT(DISTINCT cc.id) FILTER (WHERE cc.status = 'compliant'),
        'non_compliant', COUNT(DISTINCT cc.id) FILTER (WHERE cc.status = 'non_compliant'),
        'average_score', AVG(cc.score)
    ) as compliance,

    -- Risk metrics
    json_build_object(
        'overall_score', p.risk_score,
        'assessments_count', COUNT(DISTINCT ra.id),
        'latest_assessment', MAX(ra.assessment_date)
    ) as risk,

    -- Stakeholder metrics
    json_build_object(
        'total', COUNT(DISTINCT s.id),
        'active', COUNT(DISTINCT s.id) FILTER (WHERE s.engagement_status = 'active')
    ) as stakeholders

FROM projects p
LEFT JOIN documents d ON d.project_id = p.id AND d.deleted_at IS NULL
LEFT JOIN financial_models fm ON fm.project_id = p.id AND fm.deleted_at IS NULL
LEFT JOIN compliance_checks cc ON cc.project_id = p.id AND cc.deleted_at IS NULL
LEFT JOIN risk_assessments ra ON ra.project_id = p.id AND ra.deleted_at IS NULL
LEFT JOIN stakeholders s ON s.project_id = p.id AND s.deleted_at IS NULL
WHERE p.deleted_at IS NULL
GROUP BY p.id;

COMMENT ON VIEW v_project_dashboard IS 'Comprehensive project dashboard with all metrics';

-- ============================================================================
-- PORTFOLIO OVERVIEW MATERIALIZED VIEW
-- ============================================================================

CREATE MATERIALIZED VIEW mv_portfolio_overview AS
SELECT
    COUNT(*) as total_projects,
    COUNT(*) FILTER (WHERE status IN ('pipeline', 'under_review', 'approved', 'active')) as active_projects,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_projects,
    SUM(total_value) as total_investment_value,
    AVG(risk_score) as average_risk_score,

    -- By status
    json_object_agg(status, status_count) as projects_by_status,

    -- By sector
    (SELECT json_object_agg(sector, sector_count)
     FROM (
         SELECT sector, COUNT(*) as sector_count
         FROM projects
         WHERE deleted_at IS NULL
         GROUP BY sector
     ) sector_data) as projects_by_sector,

    -- By country
    (SELECT json_object_agg(country, country_count)
     FROM (
         SELECT country, COUNT(*) as country_count
         FROM projects
         WHERE deleted_at IS NULL
         GROUP BY country
     ) country_data) as projects_by_country,

    -- Risk distribution
    json_build_object(
        'low_risk', COUNT(*) FILTER (WHERE risk_score < 40),
        'medium_risk', COUNT(*) FILTER (WHERE risk_score >= 40 AND risk_score < 70),
        'high_risk', COUNT(*) FILTER (WHERE risk_score >= 70)
    ) as risk_distribution,

    NOW() as last_updated

FROM (
    SELECT status, COUNT(*) as status_count
    FROM projects
    WHERE deleted_at IS NULL
    GROUP BY status
) status_data
CROSS JOIN projects p
WHERE p.deleted_at IS NULL;

CREATE UNIQUE INDEX ON mv_portfolio_overview ((1));

COMMENT ON MATERIALIZED VIEW mv_portfolio_overview IS 'Portfolio-wide statistics - refresh periodically';

-- ============================================================================
-- COMPLIANCE SUMMARY VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_compliance_summary AS
SELECT
    p.id as project_id,
    p.name as project_name,
    COUNT(cc.id) as total_checks,
    COUNT(cc.id) FILTER (WHERE cc.status = 'compliant') as compliant_count,
    COUNT(cc.id) FILTER (WHERE cc.status = 'non_compliant') as non_compliant_count,
    COUNT(cc.id) FILTER (WHERE cc.status = 'pending') as pending_count,
    AVG(cc.score) as average_score,
    array_agg(DISTINCT cc.standard) FILTER (WHERE cc.standard IS NOT NULL) as standards_checked,

    -- Critical issues count
    (SELECT COUNT(*)
     FROM compliance_checks cc2,
          jsonb_array_elements(cc2.issues) as issue
     WHERE cc2.project_id = p.id
     AND cc2.deleted_at IS NULL
     AND issue->>'severity' = 'critical') as critical_issues_count,

    MAX(cc.checked_at) as last_check_date

FROM projects p
LEFT JOIN compliance_checks cc ON cc.project_id = p.id AND cc.deleted_at IS NULL
WHERE p.deleted_at IS NULL
GROUP BY p.id;

COMMENT ON VIEW v_compliance_summary IS 'Compliance summary by project';

-- ============================================================================
-- DOCUMENT PROCESSING QUEUE VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_document_queue AS
SELECT
    d.id,
    d.name,
    d.type,
    d.project_id,
    p.name as project_name,
    d.file_size,
    d.page_count,
    d.processing_status,
    d.created_at,
    d.updated_at,
    EXTRACT(EPOCH FROM (NOW() - d.created_at))/3600 as hours_waiting
FROM documents d
JOIN projects p ON p.id = d.project_id
WHERE d.processed = FALSE
AND d.deleted_at IS NULL
AND p.deleted_at IS NULL
ORDER BY d.created_at ASC;

COMMENT ON VIEW v_document_queue IS 'Documents pending processing, oldest first';

-- ============================================================================
-- HIGH RISK PROJECTS VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_high_risk_projects AS
SELECT
    p.id,
    p.name,
    p.country,
    p.sector,
    p.total_value,
    p.risk_score,
    p.status,

    -- Risk breakdown
    (SELECT json_agg(
        json_build_object(
            'assessment_type', ra.assessment_type,
            'score', ra.overall_risk_score,
            'date', ra.assessment_date
        )
     )
     FROM risk_assessments ra
     WHERE ra.project_id = p.id
     AND ra.deleted_at IS NULL) as risk_assessments,

    -- Non-compliant checks
    (SELECT COUNT(*)
     FROM compliance_checks cc
     WHERE cc.project_id = p.id
     AND cc.status = 'non_compliant'
     AND cc.deleted_at IS NULL) as non_compliant_checks,

    -- Critical issues
    (SELECT json_agg(issue)
     FROM (
         SELECT jsonb_array_elements(cc.issues) as issue
         FROM compliance_checks cc
         WHERE cc.project_id = p.id
         AND cc.status = 'non_compliant'
         AND cc.deleted_at IS NULL
     ) issues
     WHERE (issue->>'severity') = 'critical') as critical_issues

FROM projects p
WHERE p.deleted_at IS NULL
AND p.risk_score >= 70
ORDER BY p.risk_score DESC;

COMMENT ON VIEW v_high_risk_projects IS 'Projects with risk score >= 70';

-- ============================================================================
-- FINANCIAL PERFORMANCE VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_financial_performance AS
SELECT
    p.id as project_id,
    p.name as project_name,
    p.sector,
    p.total_value,
    fm.id as model_id,
    fm.version,
    fm.irr,
    fm.npv,
    fm.payback_period,
    fm.discount_rate,
    fm.project_life_years,
    fm.assumptions,
    fm.created_at as model_created_at,

    -- Scenario analysis
    (SELECT json_agg(scenario ORDER BY (scenario->>'probability')::float DESC)
     FROM jsonb_array_elements(fm.scenarios) as scenario) as scenarios_ranked,

    -- Performance vs. threshold
    CASE
        WHEN fm.irr >= 15 THEN 'Excellent'
        WHEN fm.irr >= 12 THEN 'Good'
        WHEN fm.irr >= 10 THEN 'Acceptable'
        ELSE 'Below Target'
    END as performance_rating

FROM projects p
JOIN financial_models fm ON fm.project_id = p.id
WHERE p.deleted_at IS NULL
AND fm.deleted_at IS NULL
ORDER BY p.id, fm.version DESC;

COMMENT ON VIEW v_financial_performance IS 'Financial model performance metrics';

-- ============================================================================
-- STAKEHOLDER MATRIX VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_stakeholder_matrix AS
SELECT
    p.id as project_id,
    p.name as project_name,
    s.id as stakeholder_id,
    s.name as stakeholder_name,
    s.organization,
    s.role,
    s.stakeholder_type,
    s.influence_level,
    s.engagement_status,
    s.contact_email,

    -- Influence/Engagement matrix position
    CASE
        WHEN s.influence_level = 'high' AND s.engagement_status = 'active' THEN 'Key Stakeholder - Maintain'
        WHEN s.influence_level = 'high' AND s.engagement_status != 'active' THEN 'Important - Engage'
        WHEN s.influence_level = 'medium' AND s.engagement_status = 'active' THEN 'Monitor Closely'
        WHEN s.influence_level = 'low' THEN 'Keep Informed'
        ELSE 'Review Status'
    END as stakeholder_strategy

FROM projects p
JOIN stakeholders s ON s.project_id = p.id
WHERE p.deleted_at IS NULL
AND s.deleted_at IS NULL
ORDER BY
    CASE s.influence_level
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'low' THEN 3
    END,
    s.name;

COMMENT ON VIEW v_stakeholder_matrix IS 'Stakeholder influence/engagement matrix';

-- ============================================================================
-- AUDIT TRAIL VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_recent_changes AS
SELECT
    al.id,
    al.table_name,
    al.record_id,
    al.action,
    al.changed_by,
    al.changed_at,

    -- Record name (if available)
    CASE
        WHEN al.table_name = 'projects' THEN al.new_data->>'name'
        WHEN al.table_name = 'documents' THEN al.new_data->>'name'
        WHEN al.table_name = 'stakeholders' THEN al.new_data->>'name'
        ELSE NULL
    END as record_name,

    -- Changed fields
    (SELECT array_agg(key)
     FROM jsonb_object_keys(al.new_data) as key
     WHERE al.old_data IS NULL
     OR al.new_data->key != al.old_data->key) as changed_fields

FROM audit_log al
WHERE al.changed_at >= NOW() - INTERVAL '7 days'
ORDER BY al.changed_at DESC
LIMIT 100;

COMMENT ON VIEW v_recent_changes IS 'Recent database changes (last 7 days, max 100 records)';

-- ============================================================================
-- DFI PARTNERSHIP VIEW
-- ============================================================================

CREATE OR REPLACE VIEW v_dfi_partnerships AS
SELECT
    p.id as project_id,
    p.name as project_name,
    p.country,
    p.sector,
    p.total_value,
    dfi.partner->>'name' as dfi_name,
    (dfi.partner->>'commitment')::numeric as dfi_commitment,
    dfi.partner->>'status' as dfi_status,
    (dfi.partner->>'commitment')::numeric / p.total_value as commitment_ratio
FROM projects p,
     jsonb_array_elements(p.dfi_partners) as dfi(partner)
WHERE p.deleted_at IS NULL
AND p.dfi_partners IS NOT NULL
ORDER BY p.name, (dfi.partner->>'commitment')::numeric DESC;

COMMENT ON VIEW v_dfi_partnerships IS 'DFI partnerships with commitment ratios';

-- ============================================================================
-- FUNCTIONS TO REFRESH MATERIALIZED VIEWS
-- ============================================================================

-- Function to refresh portfolio overview
CREATE OR REPLACE FUNCTION refresh_portfolio_overview()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_portfolio_overview;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION refresh_portfolio_overview IS 'Refreshes portfolio overview materialized view';

-- ============================================================================
-- GRANT PERMISSIONS ON VIEWS
-- ============================================================================

GRANT SELECT ON v_active_projects TO authenticated;
GRANT SELECT ON v_project_dashboard TO authenticated;
GRANT SELECT ON mv_portfolio_overview TO authenticated;
GRANT SELECT ON v_compliance_summary TO authenticated;
GRANT SELECT ON v_document_queue TO authenticated;
GRANT SELECT ON v_high_risk_projects TO authenticated;
GRANT SELECT ON v_financial_performance TO authenticated;
GRANT SELECT ON v_stakeholder_matrix TO authenticated;
GRANT SELECT ON v_recent_changes TO authenticated;
GRANT SELECT ON v_dfi_partnerships TO authenticated;

-- Only admins can refresh materialized views
GRANT EXECUTE ON FUNCTION refresh_portfolio_overview() TO service_role;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON VIEW v_active_projects IS
    'Quick view of active projects with key metrics - use for dashboards';

COMMENT ON VIEW v_project_dashboard IS
    'Comprehensive project view with all metrics - use for detailed project pages';

COMMENT ON MATERIALIZED VIEW mv_portfolio_overview IS
    'Portfolio-wide statistics - refresh hourly or when needed for performance';

-- ============================================================================
-- ADDITIONAL TABLES
-- ============================================================================

-- ============================================================================
-- USERS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    organization TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('admin', 'analyst', 'user', 'viewer')),
    is_active BOOLEAN DEFAULT TRUE,
    preferences JSONB DEFAULT '{}'::jsonb,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view their own profile" ON users;
CREATE POLICY "Users can view their own profile"
    ON users FOR SELECT
    USING (auth.uid() = id OR is_admin());

DROP POLICY IF EXISTS "Users can update their own profile" ON users;
CREATE POLICY "Users can update their own profile"
    ON users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Admins can view all users" ON users;
CREATE POLICY "Admins can view all users"
    ON users FOR SELECT
    USING (is_admin());

DROP POLICY IF EXISTS "System can create users" ON users;
CREATE POLICY "System can create users"
    ON users FOR INSERT
    WITH CHECK (auth.jwt() ->> 'role' = 'service_role' OR is_admin());

GRANT SELECT, UPDATE ON users TO authenticated;
GRANT ALL ON users TO service_role;

COMMENT ON TABLE users IS 'Application users with roles and preferences';

-- ============================================================================
-- MILESTONES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    target_date DATE,
    completion_date DATE,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'delayed', 'cancelled')),
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    dependencies JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT milestones_name_check CHECK (char_length(name) >= 2)
);

CREATE INDEX IF NOT EXISTS idx_milestones_project_id ON milestones(project_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_milestones_status ON milestones(status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_milestones_target_date ON milestones(target_date);

DROP TRIGGER IF EXISTS update_milestones_updated_at ON milestones;
CREATE TRIGGER update_milestones_updated_at BEFORE UPDATE ON milestones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE milestones ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view project milestones" ON milestones;
CREATE POLICY "Users can view project milestones"
    ON milestones FOR SELECT
    USING (auth.uid() IS NOT NULL AND (has_project_access(project_id) OR is_admin()));

DROP POLICY IF EXISTS "Users can create milestones" ON milestones;
CREATE POLICY "Users can create milestones"
    ON milestones FOR INSERT
    WITH CHECK (auth.uid() IS NOT NULL AND has_project_access(project_id));

DROP POLICY IF EXISTS "Users can update milestones" ON milestones;
CREATE POLICY "Users can update milestones"
    ON milestones FOR UPDATE
    USING (auth.uid() IS NOT NULL AND has_project_access(project_id))
    WITH CHECK (auth.uid() IS NOT NULL AND has_project_access(project_id));

DROP POLICY IF EXISTS "Users can delete milestones" ON milestones;
CREATE POLICY "Users can delete milestones"
    ON milestones FOR DELETE
    USING (auth.uid() IS NOT NULL AND has_project_access(project_id));

GRANT SELECT, INSERT, UPDATE, DELETE ON milestones TO authenticated;
GRANT ALL ON milestones TO service_role;

COMMENT ON TABLE milestones IS 'Project milestones and deliverables tracking';

-- ============================================================================
-- ADD FOREIGN KEY CONSTRAINTS
-- ============================================================================

-- Add foreign key constraints for created_by/updated_by fields
DO $$ BEGIN
    ALTER TABLE projects ADD CONSTRAINT projects_created_by_fkey
        FOREIGN KEY (created_by) REFERENCES users(id);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    ALTER TABLE projects ADD CONSTRAINT projects_updated_by_fkey
        FOREIGN KEY (updated_by) REFERENCES users(id);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ============================================================================
-- FINAL SETUP
-- ============================================================================

-- Refresh materialized view
REFRESH MATERIALIZED VIEW mv_portfolio_overview;

-- Analyze all tables for query optimizer
ANALYZE;

-- ============================================================================
-- SETUP COMPLETE
-- ============================================================================

SELECT 'InfraFlow AI Platform schema setup completed successfully!' as status;
