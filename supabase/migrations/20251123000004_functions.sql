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
