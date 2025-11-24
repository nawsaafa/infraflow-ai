"""
Pydantic schemas for Project entities
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=500)
    sponsor: Optional[str] = None
    country: Optional[str] = None
    sector: Optional[str] = None
    total_value: Optional[Decimal] = None
    dfi_partners: Optional[Dict[str, Any]] = None
    status: Optional[str] = "draft"


class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    sponsor: Optional[str] = None
    country: Optional[str] = None
    sector: Optional[str] = None
    total_value: Optional[Decimal] = None
    dfi_partners: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    risk_score: Optional[float] = None


class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: UUID
    risk_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for paginated project list"""
    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProjectDetailResponse(ProjectResponse):
    """Detailed project response with related data"""
    documents_count: int = 0
    financial_models_count: int = 0
    compliance_checks_count: int = 0
    stakeholders_count: int = 0
