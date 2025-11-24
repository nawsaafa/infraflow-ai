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
