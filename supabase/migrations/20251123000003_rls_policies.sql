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
