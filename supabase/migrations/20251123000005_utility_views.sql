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
