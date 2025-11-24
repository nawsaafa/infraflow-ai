-- InfraFlow AI - Initial Database Schema
-- Migration: 001_initial_schema
-- Description: Creates core tables for projects, documents, financial models, and compliance checks

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Projects table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    sponsor TEXT,
    country TEXT,
    sector TEXT,
    total_value DECIMAL(15,2),
    dfi_partners JSONB,
    status TEXT,
    risk_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN ('draft', 'active', 'under_review', 'approved', 'rejected', 'completed'))
);

-- Create index on projects for faster queries
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_country ON projects(country);
CREATE INDEX idx_projects_sector ON projects(sector);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type TEXT,
    url TEXT,
    processed BOOLEAN DEFAULT FALSE,
    extracted_data JSONB,
    embeddings_id TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_document_type CHECK (type IN ('feasibility_study', 'financial_model', 'esg_report', 'legal_agreement', 'technical_specification', 'other'))
);

-- Create indexes on documents
CREATE INDEX idx_documents_project_id ON documents(project_id);
CREATE INDEX idx_documents_processed ON documents(processed);
CREATE INDEX idx_documents_type ON documents(type);

-- Financial models table
CREATE TABLE financial_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    model_type TEXT,
    assumptions JSONB,
    outputs JSONB,
    scenarios JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_model_type CHECK (model_type IN ('dcf', 'blended_finance', 'risk_analysis', 'carbon_credit', 'currency_risk', 'other'))
);

-- Create indexes on financial models
CREATE INDEX idx_financial_models_project_id ON financial_models(project_id);
CREATE INDEX idx_financial_models_type ON financial_models(model_type);

-- Compliance checks table
CREATE TABLE compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    standard TEXT,
    status TEXT,
    issues JSONB,
    recommendations JSONB,
    checked_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_compliance_standard CHECK (standard IN ('ebrd', 'ifc', 'eu_taxonomy', 'local_content', 'esg', 'other')),
    CONSTRAINT valid_compliance_status CHECK (status IN ('pending', 'compliant', 'non_compliant', 'requires_review'))
);

-- Create indexes on compliance checks
CREATE INDEX idx_compliance_checks_project_id ON compliance_checks(project_id);
CREATE INDEX idx_compliance_checks_standard ON compliance_checks(standard);
CREATE INDEX idx_compliance_checks_status ON compliance_checks(status);

-- Stakeholders table (for tracking project stakeholders)
CREATE TABLE stakeholders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    organization TEXT,
    role TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    status TEXT DEFAULT 'active',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_stakeholder_status CHECK (status IN ('active', 'inactive', 'pending'))
);

-- Create indexes on stakeholders
CREATE INDEX idx_stakeholders_project_id ON stakeholders(project_id);
CREATE INDEX idx_stakeholders_role ON stakeholders(role);

-- Project milestones table
CREATE TABLE project_milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    target_date DATE,
    completed_date DATE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_milestone_status CHECK (status IN ('pending', 'in_progress', 'completed', 'delayed', 'cancelled'))
);

-- Create indexes on milestones
CREATE INDEX idx_milestones_project_id ON project_milestones(project_id);
CREATE INDEX idx_milestones_status ON project_milestones(status);
CREATE INDEX idx_milestones_target_date ON project_milestones(target_date);

-- Users table (for authentication and authorization)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    organization TEXT,
    role TEXT DEFAULT 'user',
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_user_role CHECK (role IN ('admin', 'dfi_officer', 'sponsor', 'consultant', 'user'))
);

-- Create indexes on users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Project activity log table
CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes on activity log
CREATE INDEX idx_activity_log_project_id ON activity_log(project_id);
CREATE INDEX idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at DESC);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stakeholders_updated_at BEFORE UPDATE ON stakeholders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_milestones_updated_at BEFORE UPDATE ON project_milestones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE projects IS 'Core projects table storing infrastructure finance projects';
COMMENT ON TABLE documents IS 'Project documents with processing status and extracted data';
COMMENT ON TABLE financial_models IS 'Financial models and scenario analysis for projects';
COMMENT ON TABLE compliance_checks IS 'Compliance verification against various standards';
COMMENT ON TABLE stakeholders IS 'Project stakeholders and their contact information';
COMMENT ON TABLE project_milestones IS 'Project timeline and milestone tracking';
COMMENT ON TABLE users IS 'Platform users with role-based access';
COMMENT ON TABLE activity_log IS 'Audit trail of all project activities';
