"""
InfraFlow AI - Pydantic Models
Data models for request/response validation and serialization
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class ProjectStatus(str, Enum):
    """Project status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class ProjectSector(str, Enum):
    """Project sector enumeration"""
    RENEWABLE_ENERGY = "renewable_energy"
    INFRASTRUCTURE = "infrastructure"
    TRANSPORT = "transport"
    WATER = "water"
    TELECOMMUNICATIONS = "telecommunications"
    MANUFACTURING = "manufacturing"
    AGRICULTURE = "agriculture"
    OTHER = "other"


class DocumentType(str, Enum):
    """Document type enumeration"""
    FEASIBILITY_STUDY = "feasibility_study"
    FINANCIAL_MODEL = "financial_model"
    ENVIRONMENTAL_IMPACT = "environmental_impact"
    TECHNICAL_SPECS = "technical_specs"
    LEGAL_AGREEMENT = "legal_agreement"
    COMPLIANCE_REPORT = "compliance_report"
    OTHER = "other"


class ComplianceStandard(str, Enum):
    """Compliance standards enumeration"""
    EBRD_ENVIRONMENTAL = "ebrd_environmental"
    IFC_PERFORMANCE = "ifc_performance"
    EU_TAXONOMY = "eu_taxonomy"
    LOCAL_CONTENT = "local_content"
    ESG_SCORING = "esg_scoring"
    EQUATOR_PRINCIPLES = "equator_principles"


class ModelType(str, Enum):
    """Financial model type enumeration"""
    DCF = "dcf"
    BLENDED_FINANCE = "blended_finance"
    PROJECT_FINANCE = "project_finance"
    MONTE_CARLO = "monte_carlo"


# ============================================================================
# USER MODELS
# ============================================================================

class User(BaseModel):
    """User model for authentication"""
    id: str
    email: str
    name: Optional[str] = None
    organization: Optional[str] = None
    role: str = "user"
    is_admin: bool = False

    class Config:
        from_attributes = True


# ============================================================================
# PROJECT MODELS
# ============================================================================

class ProjectCreate(BaseModel):
    """Request model for creating a new project"""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    sponsor: Optional[str] = Field(None, max_length=255, description="Project sponsor")
    country: str = Field(..., min_length=2, max_length=100, description="Project country")
    sector: ProjectSector = Field(..., description="Project sector")
    total_value: Optional[float] = Field(None, ge=0, description="Total project value in USD")
    dfi_partners: Optional[List[str]] = Field(default_factory=list, description="DFI partners")
    description: Optional[str] = Field(None, description="Project description")
    technology: Optional[str] = Field(None, description="Technology type")
    capacity: Optional[str] = Field(None, description="Project capacity")

    @validator('total_value')
    def validate_total_value(cls, v):
        if v is not None and v < 0:
            raise ValueError('Total value must be non-negative')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Egypt Green Hydrogen Project",
                "sponsor": "Scatec ASA",
                "country": "Egypt",
                "sector": "renewable_energy",
                "total_value": 5000000000,
                "dfi_partners": ["EBRD", "EIB", "AfDB"],
                "description": "Large-scale green hydrogen production facility",
                "technology": "PEM Electrolysis",
                "capacity": "100 MW"
            }
        }


class ProjectUpdate(BaseModel):
    """Request model for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sponsor: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    sector: Optional[ProjectSector] = None
    total_value: Optional[float] = Field(None, ge=0)
    dfi_partners: Optional[List[str]] = None
    status: Optional[ProjectStatus] = None
    description: Optional[str] = None
    technology: Optional[str] = None
    capacity: Optional[str] = None
    risk_score: Optional[float] = Field(None, ge=0, le=100)


class ProjectResponse(BaseModel):
    """Response model for project data"""
    id: str
    name: str
    sponsor: Optional[str]
    country: str
    sector: str
    total_value: Optional[float]
    dfi_partners: Optional[List[str]]
    status: str
    risk_score: Optional[float]
    description: Optional[str]
    technology: Optional[str]
    capacity: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Egypt Green Hydrogen Project",
                "sponsor": "Scatec ASA",
                "country": "Egypt",
                "sector": "renewable_energy",
                "total_value": 5000000000,
                "dfi_partners": ["EBRD", "EIB", "AfDB"],
                "status": "active",
                "risk_score": 45.5,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            }
        }


# ============================================================================
# DOCUMENT MODELS
# ============================================================================

class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""
    id: Optional[str] = None
    name: str
    type: Optional[str] = None
    status: str
    url: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "name": "feasibility_study.pdf",
                "type": "feasibility_study",
                "status": "processed",
                "url": "https://storage.example.com/documents/660e8400.pdf",
                "extracted_data": {
                    "project_name": "Egypt Green Hydrogen",
                    "total_investment": 5000000000,
                    "technology": "PEM Electrolysis"
                },
                "message": "Document processed successfully"
            }
        }


class DocumentMetadata(BaseModel):
    """Document metadata model"""
    id: str
    project_id: str
    name: str
    type: Optional[str]
    url: str
    processed: bool
    extracted_data: Optional[Dict[str, Any]]
    embeddings_id: Optional[str]
    created_at: datetime


# ============================================================================
# ANALYSIS MODELS
# ============================================================================

class AnalysisResponse(BaseModel):
    """Response model for comprehensive project analysis"""
    project_id: str
    analyzed_at: str
    document_summary: Dict[str, Any]
    financial_analysis: Optional[Dict[str, Any]]
    compliance_check: Optional[Dict[str, Any]]
    risk_assessment: Optional[Dict[str, Any]]
    recommendations: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "550e8400-e29b-41d4-a716-446655440000",
                "analyzed_at": "2024-01-15T10:30:00Z",
                "document_summary": {
                    "total_documents": 5,
                    "key_findings": ["Strong technical feasibility", "Clear financial structure"],
                    "stakeholders": ["Scatec ASA", "Egyptian Government", "EBRD"]
                },
                "financial_analysis": {
                    "npv": 450000000,
                    "irr": 12.5,
                    "payback_period": 8.5
                },
                "compliance_check": {
                    "overall_status": "compliant",
                    "issues_count": 2
                },
                "risk_assessment": {
                    "overall_score": 45.5,
                    "critical_risks": 1
                },
                "recommendations": [
                    "Review currency hedging strategy",
                    "Strengthen local content requirements"
                ]
            }
        }


# ============================================================================
# FINANCIAL MODELING MODELS
# ============================================================================

class FinancialAssumptions(BaseModel):
    """Financial model assumptions"""
    discount_rate: float = Field(..., ge=0, le=1, description="Discount rate (decimal)")
    project_lifetime: int = Field(..., ge=1, le=50, description="Project lifetime in years")
    revenue_growth_rate: Optional[float] = Field(None, ge=-1, le=1)
    inflation_rate: Optional[float] = Field(None, ge=0, le=1)
    tax_rate: Optional[float] = Field(None, ge=0, le=1)
    currency: str = Field(default="USD", max_length=3)
    custom_assumptions: Optional[Dict[str, Any]] = None


class Scenario(BaseModel):
    """Scenario definition for financial modeling"""
    name: str
    probability: float = Field(..., ge=0, le=1)
    assumptions_override: Dict[str, Any]


class FinancialModelRequest(BaseModel):
    """Request model for creating a financial model"""
    model_type: ModelType
    assumptions: FinancialAssumptions
    scenarios: Optional[List[Scenario]] = Field(default_factory=list)
    num_simulations: int = Field(default=1000, ge=100, le=100000, description="Number of Monte Carlo simulations")

    class Config:
        json_schema_extra = {
            "example": {
                "model_type": "dcf",
                "assumptions": {
                    "discount_rate": 0.10,
                    "project_lifetime": 25,
                    "revenue_growth_rate": 0.03,
                    "inflation_rate": 0.025,
                    "tax_rate": 0.20,
                    "currency": "USD"
                },
                "scenarios": [
                    {
                        "name": "Base Case",
                        "probability": 0.6,
                        "assumptions_override": {}
                    },
                    {
                        "name": "Optimistic",
                        "probability": 0.2,
                        "assumptions_override": {"revenue_growth_rate": 0.05}
                    }
                ],
                "num_simulations": 10000
            }
        }


class FinancialModelResponse(BaseModel):
    """Response model for financial model results"""
    id: Optional[str] = None
    project_id: str
    model_type: str
    npv: Optional[float]
    irr: Optional[float]
    payback_period: Optional[float]
    scenarios_results: Optional[List[Dict[str, Any]]]
    sensitivity_analysis: Optional[Dict[str, Any]]
    monte_carlo_results: Optional[Dict[str, Any]]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "770e8400-e29b-41d4-a716-446655440000",
                "project_id": "550e8400-e29b-41d4-a716-446655440000",
                "model_type": "dcf",
                "npv": 450000000,
                "irr": 0.125,
                "payback_period": 8.5,
                "scenarios_results": [
                    {"name": "Base Case", "npv": 450000000, "irr": 0.125},
                    {"name": "Optimistic", "npv": 650000000, "irr": 0.158}
                ],
                "sensitivity_analysis": {
                    "discount_rate": [-100000000, 0, 100000000],
                    "revenue_growth": [-50000000, 0, 80000000]
                },
                "created_at": "2024-01-15T11:00:00Z"
            }
        }


# ============================================================================
# COMPLIANCE MODELS
# ============================================================================

class ComplianceCheckRequest(BaseModel):
    """Request model for compliance checking"""
    standards: List[ComplianceStandard] = Field(..., min_items=1, description="Compliance standards to check")

    class Config:
        json_schema_extra = {
            "example": {
                "standards": ["ebrd_environmental", "ifc_performance", "eu_taxonomy"]
            }
        }


class ComplianceIssue(BaseModel):
    """Compliance issue model"""
    standard: str
    severity: str  # critical, high, medium, low
    description: str
    reference: Optional[str]
    recommendation: Optional[str]


class ComplianceCheckResponse(BaseModel):
    """Response model for compliance check results"""
    id: Optional[str] = None
    project_id: str
    overall_status: str  # compliant, partial, non_compliant
    standards_checked: List[str]
    issues: List[ComplianceIssue]
    recommendations: List[str]
    checked_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "880e8400-e29b-41d4-a716-446655440000",
                "project_id": "550e8400-e29b-41d4-a716-446655440000",
                "overall_status": "partial",
                "standards_checked": ["ebrd_environmental", "ifc_performance"],
                "issues": [
                    {
                        "standard": "ebrd_environmental",
                        "severity": "medium",
                        "description": "Incomplete biodiversity assessment",
                        "reference": "EBRD PR6",
                        "recommendation": "Complete comprehensive biodiversity survey"
                    }
                ],
                "recommendations": [
                    "Address biodiversity assessment gaps",
                    "Update stakeholder engagement plan"
                ],
                "checked_at": "2024-01-15T12:00:00Z"
            }
        }


# ============================================================================
# RISK ASSESSMENT MODELS
# ============================================================================

class RiskFactor(BaseModel):
    """Individual risk factor model"""
    category: str  # financial, political, environmental, technical, regulatory
    name: str
    description: str
    likelihood: float = Field(..., ge=0, le=100)
    impact: float = Field(..., ge=0, le=100)
    risk_score: float = Field(..., ge=0, le=100)
    mitigation_strategies: List[str]


class RiskAssessmentResponse(BaseModel):
    """Response model for risk assessment"""
    project_id: str
    overall_score: float = Field(..., ge=0, le=100)
    risk_level: str  # low, medium, high, critical
    risk_factors: List[RiskFactor]
    critical_risks: List[str]
    mitigation_plan: List[str]
    assessed_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "550e8400-e29b-41d4-a716-446655440000",
                "overall_score": 45.5,
                "risk_level": "medium",
                "risk_factors": [
                    {
                        "category": "political",
                        "name": "Regulatory Change Risk",
                        "description": "Risk of changes in renewable energy policy",
                        "likelihood": 40,
                        "impact": 70,
                        "risk_score": 55,
                        "mitigation_strategies": [
                            "Secure long-term power purchase agreements",
                            "Diversify offtaker base"
                        ]
                    }
                ],
                "critical_risks": ["Currency devaluation", "Political instability"],
                "mitigation_plan": [
                    "Implement currency hedging strategy",
                    "Obtain political risk insurance"
                ],
                "assessed_at": "2024-01-15T13:00:00Z"
            }
        }


# ============================================================================
# ERROR MODELS
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: Optional[str] = None
    status_code: int
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Project not found",
                "message": "Project with ID 550e8400-e29b-41d4-a716-446655440000 does not exist",
                "status_code": 404,
                "timestamp": "2024-01-15T14:00:00Z"
            }
        }


# ============================================================================
# STAKEHOLDER MODELS
# ============================================================================

class Stakeholder(BaseModel):
    """Stakeholder model"""
    name: str
    role: str
    organization: str
    contact_info: Optional[Dict[str, str]]
    engagement_level: str  # high, medium, low


class StakeholderUpdate(BaseModel):
    """Stakeholder status update"""
    stakeholder_id: str
    update_type: str  # milestone, issue, communication
    description: str
    timestamp: datetime
