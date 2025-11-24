"""
Database models using SQLAlchemy ORM
"""

from sqlalchemy import Column, String, Float, DateTime, Boolean, Text, ForeignKey, DECIMAL, Date, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Project(Base):
    """Project model"""
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    sponsor = Column(Text)
    country = Column(Text)
    sector = Column(Text)
    total_value = Column(DECIMAL(15, 2))
    dfi_partners = Column(JSONB)
    status = Column(Text)
    risk_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    financial_models = relationship("FinancialModel", back_populates="project", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="project", cascade="all, delete-orphan")
    stakeholders = relationship("Stakeholder", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("ProjectMilestone", back_populates="project", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="project", cascade="all, delete-orphan")


class Document(Base):
    """Document model"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(Text, nullable=False)
    type = Column(Text)
    url = Column(Text)
    processed = Column(Boolean, default=False)
    extracted_data = Column(JSONB)
    embeddings_id = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="documents")


class FinancialModel(Base):
    """Financial model"""
    __tablename__ = "financial_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    model_type = Column(Text)
    assumptions = Column(JSONB)
    outputs = Column(JSONB)
    scenarios = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="financial_models")


class ComplianceCheck(Base):
    """Compliance check model"""
    __tablename__ = "compliance_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    standard = Column(Text)
    status = Column(Text)
    issues = Column(JSONB)
    recommendations = Column(JSONB)
    checked_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="compliance_checks")


class Stakeholder(Base):
    """Stakeholder model"""
    __tablename__ = "stakeholders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(Text, nullable=False)
    organization = Column(Text)
    role = Column(Text)
    contact_email = Column(Text)
    contact_phone = Column(Text)
    status = Column(Text, default="active")
    metadata = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="stakeholders")


class ProjectMilestone(Base):
    """Project milestone model"""
    __tablename__ = "project_milestones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(Text, nullable=False)
    description = Column(Text)
    target_date = Column(Date)
    completed_date = Column(Date)
    status = Column(Text, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="milestones")


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text, unique=True, nullable=False)
    name = Column(Text)
    organization = Column(Text)
    role = Column(Text, default="user")
    avatar_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activity_logs = relationship("ActivityLog", back_populates="user")


class ActivityLog(Base):
    """Activity log model"""
    __tablename__ = "activity_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(Text, nullable=False)
    details = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="activity_logs")
    user = relationship("User", back_populates="activity_logs")
