-- InfraFlow AI Platform - Seed Data
-- File: seed_data.sql
-- Description: Comprehensive seed data for testing and development

-- ============================================================================
-- SEED PROJECTS
-- ============================================================================

-- Insert sample projects across different sectors and countries
INSERT INTO projects (
    id,
    name,
    sponsor,
    country,
    sector,
    total_value,
    currency,
    dfi_partners,
    status,
    risk_score,
    description,
    location,
    timeline,
    stakeholders
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440001',
    'Egypt Green Hydrogen Megaproject',
    'Green Energy International',
    'Egypt',
    'green_hydrogen',
    8500000000.00,
    'USD',
    '[
        {"name": "EBRD", "commitment": 2000000000, "status": "committed"},
        {"name": "EIB", "commitment": 1500000000, "status": "committed"},
        {"name": "AfDB", "commitment": 1000000000, "status": "pipeline"}
    ]'::jsonb,
    'under_review',
    45.5,
    'Large-scale green hydrogen production facility in Suez Canal Economic Zone with 4GW electrolysis capacity, targeting European export markets through GCC pipeline infrastructure.',
    '{"latitude": 30.0444, "longitude": 32.8973, "address": "Suez Canal Economic Zone, Egypt"}'::jsonb,
    '{
        "start_date": "2024-06-01",
        "completion_date": "2028-12-31",
        "milestones": [
            {"name": "Financial Close", "date": "2024-12-31", "status": "pending"},
            {"name": "Phase 1 Construction", "date": "2026-06-30", "status": "pending"},
            {"name": "Commercial Operation", "date": "2028-12-31", "status": "pending"}
        ]
    }'::jsonb,
    '[
        {"name": "Mohamed El-Khayat", "role": "Project Director", "organization": "Green Energy International"},
        {"name": "Sarah Williams", "role": "Investment Officer", "organization": "EBRD"},
        {"name": "Hans Mueller", "role": "Technical Advisor", "organization": "EIB"}
    ]'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440002',
    'Kenya Solar Power Plant - Phase II',
    'SunPower Africa Ltd',
    'Kenya',
    'renewable_energy',
    450000000.00,
    'USD',
    '[
        {"name": "AfDB", "commitment": 200000000, "status": "committed"},
        {"name": "BII", "commitment": 100000000, "status": "committed"}
    ]'::jsonb,
    'active',
    38.2,
    '350MW solar photovoltaic power plant with battery storage in Turkana County, connecting to national grid.',
    '{"latitude": 3.1167, "longitude": 35.6167, "address": "Turkana County, Kenya"}'::jsonb,
    '{
        "start_date": "2023-03-01",
        "completion_date": "2025-09-30",
        "milestones": [
            {"name": "Financial Close", "date": "2023-06-30", "status": "completed"},
            {"name": "Construction Start", "date": "2023-09-01", "status": "completed"},
            {"name": "Grid Connection", "date": "2025-09-30", "status": "in_progress"}
        ]
    }'::jsonb,
    '[
        {"name": "James Mwangi", "role": "CEO", "organization": "SunPower Africa Ltd"},
        {"name": "Patricia Omondi", "role": "Project Manager", "organization": "SunPower Africa Ltd"}
    ]'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440003',
    'Morocco Wind Farm Development',
    'Renewable Energy Corp Morocco',
    'Morocco',
    'renewable_energy',
    680000000.00,
    'EUR',
    '[
        {"name": "EIB", "commitment": 300000000, "status": "committed"},
        {"name": "EBRD", "commitment": 200000000, "status": "committed"}
    ]'::jsonb,
    'approved',
    42.0,
    '500MW onshore wind farm in Tangier-Tetouan-Al Hoceima region, contributing to Morocco\'s renewable energy targets.',
    '{"latitude": 35.7595, "longitude": -5.8340, "address": "Tangier-Tetouan-Al Hoceima, Morocco"}'::jsonb,
    '{
        "start_date": "2024-09-01",
        "completion_date": "2027-03-31",
        "milestones": [
            {"name": "Environmental Approval", "date": "2024-06-30", "status": "completed"},
            {"name": "Financial Close", "date": "2024-12-31", "status": "pending"},
            {"name": "Construction Complete", "date": "2027-03-31", "status": "pending"}
        ]
    }'::jsonb,
    '[]'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440004',
    'Nigeria Waste-to-Energy Facility',
    'Clean Cities Nigeria',
    'Nigeria',
    'waste_management',
    320000000.00,
    'USD',
    '[
        {"name": "AfDB", "commitment": 150000000, "status": "pipeline"},
        {"name": "IFC", "commitment": 100000000, "status": "pipeline"}
    ]'::jsonb,
    'pipeline',
    58.3,
    'Municipal solid waste processing facility with 80MW power generation capacity in Lagos metropolitan area.',
    '{"latitude": 6.5244, "longitude": 3.3792, "address": "Lagos, Nigeria"}'::jsonb,
    '{
        "start_date": "2025-06-01",
        "completion_date": "2028-12-31",
        "milestones": []
    }'::jsonb,
    '[]'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440005',
    'Chile Transmission Line Expansion',
    'TransGrid South America',
    'Chile',
    'transmission',
    580000000.00,
    'USD',
    '[
        {"name": "IDB", "commitment": 250000000, "status": "committed"}
    ]'::jsonb,
    'active',
    35.7,
    '1,200km high-voltage transmission line connecting renewable energy zones in Atacama Desert to central grid.',
    '{"latitude": -23.6345, "longitude": -70.3984, "address": "Atacama Region, Chile"}'::jsonb,
    '{
        "start_date": "2023-01-15",
        "completion_date": "2026-06-30",
        "milestones": [
            {"name": "Phase 1 Complete", "date": "2024-12-31", "status": "in_progress"}
        ]
    }'::jsonb,
    '[]'::jsonb
);

-- ============================================================================
-- SEED DOCUMENTS
-- ============================================================================

INSERT INTO documents (
    id,
    project_id,
    name,
    type,
    url,
    file_path,
    file_size,
    mime_type,
    processed,
    processing_status,
    extracted_data,
    page_count,
    language,
    confidence_score
) VALUES
(
    '650e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    'Egypt Green Hydrogen - Feasibility Study',
    'feasibility_study',
    'https://storage.example.com/docs/egh-feasibility-2024.pdf',
    '/documents/egh-feasibility-2024.pdf',
    15728640,
    'application/pdf',
    TRUE,
    'completed',
    '{
        "summary": "Comprehensive feasibility analysis for 4GW green hydrogen facility",
        "key_findings": ["Strong renewable resource potential", "Favorable logistics for export", "Competitive LCOH projections"],
        "technical_specs": {
            "capacity": "4GW electrolysis",
            "annual_production": "600,000 tonnes H2",
            "technology": "PEM electrolysis"
        },
        "risks": ["Water availability", "Grid connection timeline", "Offtake agreement finalization"]
    }'::jsonb,
    347,
    'en',
    0.94
),
(
    '650e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    'Environmental Impact Assessment - Egypt GH2',
    'environmental_impact',
    'https://storage.example.com/docs/egh-eia-2024.pdf',
    '/documents/egh-eia-2024.pdf',
    23456789,
    'application/pdf',
    TRUE,
    'completed',
    '{
        "environmental_rating": "Category A",
        "key_impacts": ["Water consumption", "Land use", "Marine environment"],
        "mitigation_measures": ["Desalination plant", "Habitat restoration", "Marine monitoring"],
        "compliance": ["IFC PS", "EBRD PRs", "Egyptian regulations"]
    }'::jsonb,
    512,
    'en',
    0.91
),
(
    '650e8400-e29b-41d4-a716-446655440003',
    '550e8400-e29b-41d4-a716-446655440002',
    'Kenya Solar - Financial Model v3',
    'financial_model',
    'https://storage.example.com/docs/kenya-solar-model.xlsx',
    '/documents/kenya-solar-model.xlsx',
    4567890,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    TRUE,
    'completed',
    '{
        "base_case_irr": 12.8,
        "npv_usd": 145000000,
        "payback_period": 7.2,
        "key_assumptions": {
            "capacity_factor": 0.28,
            "tariff": "0.087 USD/kWh",
            "opex_escalation": 0.025
        }
    }'::jsonb,
    1,
    'en',
    0.98
),
(
    '650e8400-e29b-41d4-a716-446655440004',
    '550e8400-e29b-41d4-a716-446655440003',
    'Morocco Wind - Technical Specification',
    'technical_specification',
    'https://storage.example.com/docs/morocco-wind-tech.pdf',
    '/documents/morocco-wind-tech.pdf',
    8765432,
    'application/pdf',
    FALSE,
    'pending',
    '{}'::jsonb,
    156,
    'en',
    NULL
);

-- ============================================================================
-- SEED FINANCIAL MODELS
-- ============================================================================

INSERT INTO financial_models (
    id,
    project_id,
    model_type,
    version,
    assumptions,
    outputs,
    scenarios,
    dcf_analysis,
    currency,
    discount_rate,
    project_life_years,
    irr,
    npv,
    payback_period
) VALUES
(
    '750e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    'Project Finance',
    1,
    '{
        "capex": 8500000000,
        "annual_production": 600000,
        "hydrogen_price": 4.5,
        "capacity_factor": 0.85,
        "opex_percentage": 0.03,
        "debt_ratio": 0.70,
        "debt_tenor": 18,
        "interest_rate": 0.065
    }'::jsonb,
    '{
        "revenue_year_1": 2295000000,
        "revenue_year_10": 2754000000,
        "ebitda_year_5": 2106000000,
        "debt_service_coverage": 1.45
    }'::jsonb,
    '[
        {"name": "Base Case", "probability": 0.50, "npv": 2450000000, "irr": 11.2},
        {"name": "Upside", "probability": 0.25, "npv": 3680000000, "irr": 14.8},
        {"name": "Downside", "probability": 0.25, "npv": 1420000000, "irr": 8.3}
    ]'::jsonb,
    '{
        "enterprise_value": 12450000000,
        "terminal_value": 8900000000,
        "wacc": 0.087
    }'::jsonb,
    'USD',
    0.087,
    25,
    11.2,
    2450000000.00,
    8.7
),
(
    '750e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440002',
    'Project Finance',
    2,
    '{
        "capex": 450000000,
        "capacity_mw": 350,
        "capacity_factor": 0.28,
        "ppa_tariff": 0.087,
        "opex_per_mw": 25000,
        "debt_ratio": 0.75,
        "debt_tenor": 15
    }'::jsonb,
    '{
        "annual_generation_gwh": 858,
        "revenue_year_1": 74646000,
        "lcoe": 0.062
    }'::jsonb,
    '[
        {"name": "Base Case", "probability": 0.60, "npv": 145000000, "irr": 12.8}
    ]'::jsonb,
    '{}'::jsonb,
    'USD',
    0.095,
    20,
    12.8,
    145000000.00,
    7.2
);

-- ============================================================================
-- SEED COMPLIANCE CHECKS
-- ============================================================================

INSERT INTO compliance_checks (
    id,
    project_id,
    standard,
    category,
    status,
    score,
    issues,
    recommendations,
    evidence
) VALUES
(
    '850e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    'EBRD Environmental and Social Policy',
    'Environmental',
    'needs_review',
    78.5,
    '[
        {
            "severity": "medium",
            "description": "Water consumption exceeds local availability",
            "requirement": "PR3 - Resource Efficiency",
            "gap": "Need alternative water source assessment"
        },
        {
            "severity": "low",
            "description": "Limited biodiversity baseline data",
            "requirement": "PR6 - Biodiversity",
            "gap": "Additional surveys required for marine environment"
        }
    ]'::jsonb,
    '[
        {
            "priority": "high",
            "action": "Commission desalination feasibility study",
            "timeline": "30 days",
            "resources": "External consultant"
        },
        {
            "priority": "medium",
            "action": "Conduct marine biodiversity surveys",
            "timeline": "60 days",
            "resources": "Marine biology team"
        }
    ]'::jsonb,
    '[
        {"document_id": "650e8400-e29b-41d4-a716-446655440002", "section": "Section 4.2", "finding": "Water usage calculations"}
    ]'::jsonb
),
(
    '850e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    'IFC Performance Standards',
    'Social',
    'compliant',
    88.0,
    '[]'::jsonb,
    '[]'::jsonb,
    '[
        {"document_id": "650e8400-e29b-41d4-a716-446655440002", "section": "Section 6", "finding": "Stakeholder engagement plan"}
    ]'::jsonb
),
(
    '850e8400-e29b-41d4-a716-446655440003',
    '550e8400-e29b-41d4-a716-446655440002',
    'IFC Performance Standards',
    'Environmental',
    'compliant',
    92.0,
    '[]'::jsonb,
    '[]'::jsonb,
    '[]'::jsonb
);

-- ============================================================================
-- SEED RISK ASSESSMENTS
-- ============================================================================

INSERT INTO risk_assessments (
    id,
    project_id,
    assessment_type,
    overall_risk_score,
    risk_categories,
    identified_risks,
    mitigation_strategies,
    country_risk,
    political_risk,
    financial_risk,
    technical_risk
) VALUES
(
    '950e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    'Comprehensive Risk Assessment',
    45.5,
    '{
        "political": 38,
        "financial": 42,
        "technical": 35,
        "environmental": 48,
        "regulatory": 52
    }'::jsonb,
    '[
        {
            "category": "political",
            "description": "Currency convertibility restrictions",
            "likelihood": "medium",
            "impact": "high",
            "severity": "high"
        },
        {
            "category": "technical",
            "description": "Green hydrogen technology scale-up risk",
            "likelihood": "medium",
            "impact": "medium",
            "severity": "medium"
        },
        {
            "category": "financial",
            "description": "Offtaker credit risk",
            "likelihood": "low",
            "impact": "high",
            "severity": "medium"
        }
    ]'::jsonb,
    '[
        {
            "risk_id": "POL-001",
            "strategy": "EBRD political risk guarantee",
            "cost": 45000000,
            "effectiveness": "high"
        },
        {
            "risk_id": "TECH-001",
            "strategy": "Technology provider performance guarantee",
            "cost": 15000000,
            "effectiveness": "medium"
        }
    ]'::jsonb,
    '{
        "score": 42,
        "factors": ["Currency controls", "Regulatory changes", "Political transitions"]
    }'::jsonb,
    '{
        "score": 38,
        "factors": ["Government stability", "Policy consistency"]
    }'::jsonb,
    '{
        "score": 42,
        "factors": ["FX volatility", "Interest rate risk", "Refinancing risk"]
    }'::jsonb,
    '{
        "score": 35,
        "factors": ["Technology maturity", "Supply chain", "Construction risk"]
    }'::jsonb
),
(
    '950e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440002',
    'Comprehensive Risk Assessment',
    38.2,
    '{
        "political": 35,
        "financial": 40,
        "technical": 32,
        "environmental": 42,
        "regulatory": 38
    }'::jsonb,
    '[
        {
            "category": "environmental",
            "description": "Resource intermittency",
            "likelihood": "high",
            "impact": "medium",
            "severity": "medium"
        }
    ]'::jsonb,
    '[
        {
            "risk_id": "ENV-001",
            "strategy": "Battery storage system",
            "cost": 80000000,
            "effectiveness": "high"
        }
    ]'::jsonb,
    '{"score": 35}'::jsonb,
    '{"score": 35}'::jsonb,
    '{"score": 40}'::jsonb,
    '{"score": 32}'::jsonb
);

-- ============================================================================
-- SEED STAKEHOLDERS
-- ============================================================================

INSERT INTO stakeholders (
    id,
    project_id,
    name,
    organization,
    role,
    contact_email,
    stakeholder_type,
    influence_level,
    engagement_status
) VALUES
(
    'a50e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    'Sarah Williams',
    'EBRD',
    'Senior Investment Officer',
    's.williams@ebrd.com',
    'DFI',
    'high',
    'active'
),
(
    'a50e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    'Mohamed El-Khayat',
    'Green Energy International',
    'Project Director',
    'm.elkhayat@gei.com',
    'Sponsor',
    'high',
    'active'
),
(
    'a50e8400-e29b-41d4-a716-446655440003',
    '550e8400-e29b-41d4-a716-446655440001',
    'Dr. Ahmed Hassan',
    'Egyptian Ministry of Electricity',
    'Undersecretary',
    'a.hassan@moee.gov.eg',
    'Government',
    'high',
    'active'
),
(
    'a50e8400-e29b-41d4-a716-446655440004',
    '550e8400-e29b-41d4-a716-446655440002',
    'James Mwangi',
    'SunPower Africa Ltd',
    'CEO',
    'j.mwangi@sunpower-africa.com',
    'Sponsor',
    'high',
    'active'
);

-- ============================================================================
-- SEED REPORTS
-- ============================================================================

INSERT INTO reports (
    id,
    project_id,
    report_type,
    title,
    content,
    format,
    generated_by
) VALUES
(
    'b50e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    'executive_summary',
    'Egypt Green Hydrogen - Executive Summary',
    '{
        "project_name": "Egypt Green Hydrogen Megaproject",
        "total_investment": 8500000000,
        "key_highlights": [
            "4GW electrolysis capacity targeting European markets",
            "Strong DFI support with $4.5B committed",
            "Favorable location in Suez Canal Economic Zone",
            "Competitive LCOH of $4.50/kg"
        ],
        "investment_rationale": "Strategic project aligned with global green hydrogen demand",
        "risk_rating": "Medium",
        "recommendation": "Proceed to due diligence"
    }'::jsonb,
    'json',
    'InfraFlow AI'
);

-- Update project statistics after seeding
SELECT calculate_project_risk_score('550e8400-e29b-41d4-a716-446655440001');
SELECT calculate_project_risk_score('550e8400-e29b-41d4-a716-446655440002');

-- Verify seed data
SELECT 'Projects seeded: ' || COUNT(*)::TEXT FROM projects;
SELECT 'Documents seeded: ' || COUNT(*)::TEXT FROM documents;
SELECT 'Financial models seeded: ' || COUNT(*)::TEXT FROM financial_models;
SELECT 'Compliance checks seeded: ' || COUNT(*)::TEXT FROM compliance_checks;
SELECT 'Risk assessments seeded: ' || COUNT(*)::TEXT FROM risk_assessments;
SELECT 'Stakeholders seeded: ' || COUNT(*)::TEXT FROM stakeholders;
SELECT 'Reports seeded: ' || COUNT(*)::TEXT FROM reports;
