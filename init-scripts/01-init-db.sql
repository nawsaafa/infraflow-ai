-- ============================================================================
-- InfraFlow AI - Database Initialization Script
-- ============================================================================
-- This script creates the initial database schema for the InfraFlow AI platform
-- It is automatically run when PostgreSQL container starts for the first time
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    sponsor TEXT,
    country TEXT NOT NULL,
    sector TEXT NOT NULL,
    total_value DECIMAL(15,2),
    dfi_partners JSONB DEFAULT '[]'::jsonb,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'analyzed', 'completed', 'archived')),
    risk_score FLOAT CHECK (risk_score >= 0 AND risk_score <= 1),
    user_id UUID NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_country ON projects(country);
CREATE INDEX idx_projects_sector ON projects(sector);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- ============================================================================
-- DOCUMENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type TEXT,  -- e.g., 'ppa', 'feasibility_study', 'environmental_impact', etc.
    url TEXT,
    file_size BIGINT,
    mime_type TEXT,
    processed BOOLEAN DEFAULT FALSE,
    extracted_data JSONB DEFAULT '{}'::jsonb,
    embeddings_id TEXT,  -- Reference to vector database
    processing_status TEXT DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_documents_project_id ON documents(project_id);
CREATE INDEX idx_documents_processed ON documents(processed);
CREATE INDEX idx_documents_type ON documents(type);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);

-- ============================================================================
-- FINANCIAL MODELS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS financial_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    model_type TEXT NOT NULL CHECK (model_type IN ('dcf', 'irr', 'wacc', 'monte_carlo')),
    assumptions JSONB NOT NULL DEFAULT '{}'::jsonb,
    outputs JSONB NOT NULL DEFAULT '{}'::jsonb,
    scenarios JSONB DEFAULT '[]'::jsonb,
    num_simulations INTEGER,
    sensitivity_analysis JSONB,
    created_by UUID NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_financial_models_project_id ON financial_models(project_id);
CREATE INDEX idx_financial_models_type ON financial_models(model_type);
CREATE INDEX idx_financial_models_created_at ON financial_models(created_at DESC);

-- ============================================================================
-- COMPLIANCE CHECKS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    standard TEXT NOT NULL,  -- e.g., 'EBRD', 'IFC', 'EU_TAXONOMY'
    status TEXT NOT NULL CHECK (status IN ('compliant', 'non_compliant', 'partial', 'pending')),
    issues JSONB DEFAULT '[]'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    score FLOAT CHECK (score >= 0 AND score <= 100),
    checked_by UUID,
    checked_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_compliance_project_id ON compliance_checks(project_id);
CREATE INDEX idx_compliance_standard ON compliance_checks(standard);
CREATE INDEX idx_compliance_status ON compliance_checks(status);
CREATE INDEX idx_compliance_checked_at ON compliance_checks(checked_at DESC);

-- ============================================================================
-- RISK ASSESSMENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS risk_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    risk_type TEXT NOT NULL CHECK (risk_type IN ('financial', 'political', 'environmental', 'technical', 'regulatory', 'overall')),
    risk_level TEXT NOT NULL CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    risk_score FLOAT NOT NULL CHECK (risk_score >= 0 AND risk_score <= 1),
    description TEXT,
    mitigation_strategies JSONB DEFAULT '[]'::jsonb,
    impact_analysis JSONB,
    assessed_by UUID,
    assessed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_risk_assessments_project_id ON risk_assessments(project_id);
CREATE INDEX idx_risk_assessments_type ON risk_assessments(risk_type);
CREATE INDEX idx_risk_assessments_level ON risk_assessments(risk_level);

-- ============================================================================
-- STAKEHOLDERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS stakeholders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    organization TEXT,
    role TEXT NOT NULL,  -- e.g., 'sponsor', 'dfi', 'contractor', 'government', 'consultant'
    email TEXT,
    phone TEXT,
    contact_info JSONB DEFAULT '{}'::jsonb,
    involvement_level TEXT CHECK (involvement_level IN ('primary', 'secondary', 'tertiary')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_stakeholders_project_id ON stakeholders(project_id);
CREATE INDEX idx_stakeholders_role ON stakeholders(role);

-- ============================================================================
-- MILESTONES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    target_date DATE,
    completion_date DATE,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'delayed', 'cancelled')),
    owner_id UUID,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_milestones_project_id ON milestones(project_id);
CREATE INDEX idx_milestones_status ON milestones(status);
CREATE INDEX idx_milestones_target_date ON milestones(target_date);

-- ============================================================================
-- USERS TABLE (Simplified - integrate with Supabase Auth)
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    organization TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('admin', 'analyst', 'user', 'viewer')),
    is_active BOOLEAN DEFAULT TRUE,
    preferences JSONB DEFAULT '{}'::jsonb,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================================================
-- REPORTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL CHECK (report_type IN ('investment_memo', 'risk_matrix', 'compliance_report', 'financial_analysis', 'executive_summary')),
    title TEXT NOT NULL,
    content JSONB NOT NULL,
    file_url TEXT,
    generated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'final', 'archived')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_reports_project_id ON reports(project_id);
CREATE INDEX idx_reports_type ON reports(report_type);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_created_at ON reports(created_at DESC);

-- ============================================================================
-- AUDIT LOG TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,  -- e.g., 'create', 'update', 'delete', 'view'
    entity_type TEXT NOT NULL,  -- e.g., 'project', 'document', 'report'
    entity_id UUID,
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at DESC);

-- ============================================================================
-- n8n DATABASE (for workflow automation)
-- ============================================================================
CREATE DATABASE n8n_db;
GRANT ALL PRIVILEGES ON DATABASE n8n_db TO infraflow_user;

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_financial_models_updated_at BEFORE UPDATE ON financial_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stakeholders_updated_at BEFORE UPDATE ON stakeholders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_milestones_updated_at BEFORE UPDATE ON milestones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SEED DATA (Development Only)
-- ============================================================================

-- Insert a default admin user for development
INSERT INTO users (id, email, full_name, organization, role)
VALUES (
    uuid_generate_v4(),
    'admin@infraflow.ai',
    'Platform Administrator',
    'InfraFlow AI',
    'admin'
) ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- VIEWS (Optional - for common queries)
-- ============================================================================

-- View for project summary with related counts
CREATE OR REPLACE VIEW project_summary AS
SELECT
    p.id,
    p.name,
    p.country,
    p.sector,
    p.status,
    p.risk_score,
    COUNT(DISTINCT d.id) as document_count,
    COUNT(DISTINCT fm.id) as financial_model_count,
    COUNT(DISTINCT cc.id) as compliance_check_count,
    COUNT(DISTINCT ra.id) as risk_assessment_count,
    p.created_at,
    p.updated_at
FROM projects p
LEFT JOIN documents d ON p.id = d.project_id
LEFT JOIN financial_models fm ON p.id = fm.project_id
LEFT JOIN compliance_checks cc ON p.id = cc.project_id
LEFT JOIN risk_assessments ra ON p.id = ra.project_id
GROUP BY p.id;

-- ============================================================================
-- GRANTS & PERMISSIONS
-- ============================================================================

-- Grant permissions to infraflow_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO infraflow_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO infraflow_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO infraflow_user;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'InfraFlow AI Database Initialization Complete!';
    RAISE NOTICE 'Database: infraflow_db';
    RAISE NOTICE 'User: infraflow_user';
    RAISE NOTICE '============================================================================';
END $$;
