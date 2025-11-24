"""
InfraFlow AI - FastAPI Backend
Main application with all API endpoints for infrastructure finance intelligence platform
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from datetime import datetime
import asyncio

from models import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    DocumentUploadResponse,
    AnalysisResponse,
    FinancialModelRequest,
    FinancialModelResponse,
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    RiskAssessmentResponse,
    ErrorResponse
)
from database import Database
from document_processor import DocumentProcessor
from financial_engine import FinancialEngine
from compliance_checker import ComplianceChecker
from auth import get_current_user, User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="InfraFlow AI API",
    description="Infrastructure Finance Intelligence Platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://infraflow-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = Database()
document_processor = DocumentProcessor()
financial_engine = FinancialEngine()
compliance_checker = ComplianceChecker()


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@app.post(
    "/api/projects/create",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Projects"]
)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new infrastructure project

    Args:
        project: Project details including name, country, sector, etc.
        current_user: Authenticated user from JWT token

    Returns:
        Created project with generated ID and metadata
    """
    try:
        logger.info(f"Creating project: {project.name} for user: {current_user.id}")

        # Create project in database
        project_data = {
            "name": project.name,
            "sponsor": project.sponsor,
            "country": project.country,
            "sector": project.sector,
            "total_value": project.total_value,
            "dfi_partners": project.dfi_partners,
            "status": "draft",
            "risk_score": None,
            "user_id": current_user.id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        project_id = await db.create_project(project_data)
        created_project = await db.get_project(project_id)

        logger.info(f"Project created successfully: {project_id}")
        return ProjectResponse(**created_project)

    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )


@app.get(
    "/api/projects",
    response_model=List[ProjectResponse],
    tags=["Projects"]
)
async def list_projects(
    status_filter: Optional[str] = None,
    country: Optional[str] = None,
    sector: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
):
    """
    List all projects with optional filters

    Args:
        status_filter: Filter by project status (draft, active, completed)
        country: Filter by country
        sector: Filter by sector
        limit: Maximum number of results
        offset: Pagination offset
        current_user: Authenticated user

    Returns:
        List of projects matching filters
    """
    try:
        filters = {}
        if status_filter:
            filters["status"] = status_filter
        if country:
            filters["country"] = country
        if sector:
            filters["sector"] = sector

        projects = await db.list_projects(
            user_id=current_user.id,
            filters=filters,
            limit=limit,
            offset=offset
        )

        return [ProjectResponse(**p) for p in projects]

    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list projects: {str(e)}"
        )


@app.get(
    "/api/projects/{project_id}",
    response_model=ProjectResponse,
    tags=["Projects"]
)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get project details by ID"""
    try:
        project = await db.get_project(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        # Verify user has access to this project
        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        return ProjectResponse(**project)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve project: {str(e)}"
        )


@app.patch(
    "/api/projects/{project_id}",
    response_model=ProjectResponse,
    tags=["Projects"]
)
async def update_project(
    project_id: str,
    updates: ProjectUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update project details"""
    try:
        # Verify project exists and user has access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        # Update project
        update_data = updates.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        await db.update_project(project_id, update_data)
        updated_project = await db.get_project(project_id)

        return ProjectResponse(**updated_project)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update project: {str(e)}"
        )


@app.delete(
    "/api/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Projects"]
)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a project"""
    try:
        # Verify project exists and user has access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        await db.delete_project(project_id)
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete project: {str(e)}"
        )


# ============================================================================
# DOCUMENT ENDPOINTS
# ============================================================================

@app.post(
    "/api/documents/upload",
    response_model=List[DocumentUploadResponse],
    tags=["Documents"]
)
async def upload_documents(
    project_id: str,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload and process multiple documents for a project

    Args:
        project_id: Project ID to associate documents with
        files: List of uploaded files
        current_user: Authenticated user

    Returns:
        List of processed document metadata
    """
    try:
        # Verify project exists and user has access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        logger.info(f"Processing {len(files)} documents for project {project_id}")

        # Process all documents concurrently
        tasks = []
        for file in files:
            tasks.append(
                document_processor.process_document(
                    file=file,
                    project_id=project_id
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle results and errors
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing {files[i].filename}: {str(result)}")
                responses.append(
                    DocumentUploadResponse(
                        id=None,
                        name=files[i].filename,
                        status="error",
                        message=str(result)
                    )
                )
            else:
                responses.append(
                    DocumentUploadResponse(
                        id=result["id"],
                        name=result["name"],
                        type=result["type"],
                        status="processed",
                        url=result["url"],
                        extracted_data=result.get("extracted_data"),
                        message="Document processed successfully"
                    )
                )

        logger.info(f"Completed processing {len(files)} documents")
        return responses

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload documents: {str(e)}"
        )


@app.get(
    "/api/documents/{document_id}",
    tags=["Documents"]
)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get document details and extracted data"""
    try:
        document = await db.get_document(document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document {document_id} not found"
            )

        # Verify user has access via project
        project = await db.get_project(document["project_id"])
        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this document"
            )

        return document

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document: {str(e)}"
        )


@app.get(
    "/api/projects/{project_id}/documents",
    tags=["Documents"]
)
async def list_project_documents(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """List all documents for a project"""
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        documents = await db.list_project_documents(project_id)
        return documents

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}"
        )


# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================

@app.get(
    "/api/projects/{project_id}/analyze",
    response_model=AnalysisResponse,
    tags=["Analysis"]
)
async def analyze_project(
    project_id: str,
    include_financial: bool = True,
    include_compliance: bool = True,
    include_risk: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Run comprehensive analysis on a project

    Performs document analysis, financial modeling, compliance checking,
    and risk assessment based on processed documents.

    Args:
        project_id: Project ID to analyze
        include_financial: Include financial analysis
        include_compliance: Include compliance checking
        include_risk: Include risk assessment
        current_user: Authenticated user

    Returns:
        Comprehensive analysis results
    """
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        logger.info(f"Starting comprehensive analysis for project {project_id}")

        # Get all project documents
        documents = await db.list_project_documents(project_id)

        if not documents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No documents found for analysis. Please upload documents first."
            )

        # Run analysis tasks concurrently
        tasks = []

        # Document summary
        tasks.append(
            document_processor.generate_project_summary(project_id, documents)
        )

        # Financial analysis
        if include_financial:
            tasks.append(
                financial_engine.analyze_project(project_id, documents)
            )

        # Compliance checking
        if include_compliance:
            tasks.append(
                compliance_checker.check_project(project_id, documents)
            )

        # Risk assessment
        if include_risk:
            tasks.append(
                financial_engine.assess_risks(project_id, documents)
            )

        results = await asyncio.gather(*tasks)

        # Compile results
        analysis_result = {
            "project_id": project_id,
            "analyzed_at": datetime.utcnow().isoformat(),
            "document_summary": results[0],
            "financial_analysis": results[1] if include_financial else None,
            "compliance_check": results[2] if include_compliance else None,
            "risk_assessment": results[3] if include_risk else None,
            "recommendations": await _generate_recommendations(results)
        }

        # Update project with analysis results
        await db.update_project(project_id, {
            "status": "analyzed",
            "risk_score": analysis_result.get("risk_assessment", {}).get("overall_score"),
            "updated_at": datetime.utcnow()
        })

        logger.info(f"Analysis completed for project {project_id}")
        return AnalysisResponse(**analysis_result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze project: {str(e)}"
        )


# ============================================================================
# FINANCIAL MODELING ENDPOINTS
# ============================================================================

@app.post(
    "/api/projects/{project_id}/financial-model",
    response_model=FinancialModelResponse,
    tags=["Financial Modeling"]
)
async def create_financial_model(
    project_id: str,
    model_request: FinancialModelRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate financial model with DCF analysis and scenario modeling

    Args:
        project_id: Project ID
        model_request: Model parameters and assumptions
        current_user: Authenticated user

    Returns:
        Financial model with DCF, scenarios, and sensitivity analysis
    """
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        logger.info(f"Creating financial model for project {project_id}")

        # Generate financial model
        model_result = await financial_engine.create_model(
            project_id=project_id,
            model_type=model_request.model_type,
            assumptions=model_request.assumptions,
            scenarios=model_request.scenarios,
            num_simulations=model_request.num_simulations
        )

        # Save model to database
        model_id = await db.create_financial_model({
            "project_id": project_id,
            "model_type": model_request.model_type,
            "assumptions": model_request.assumptions,
            "outputs": model_result,
            "scenarios": model_request.scenarios,
            "created_at": datetime.utcnow()
        })

        model_result["id"] = model_id
        logger.info(f"Financial model created: {model_id}")

        return FinancialModelResponse(**model_result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating financial model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create financial model: {str(e)}"
        )


@app.get(
    "/api/projects/{project_id}/financial-models",
    tags=["Financial Modeling"]
)
async def list_financial_models(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """List all financial models for a project"""
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        models = await db.list_financial_models(project_id)
        return models

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing financial models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list financial models: {str(e)}"
        )


# ============================================================================
# COMPLIANCE CHECKING ENDPOINTS
# ============================================================================

@app.post(
    "/api/projects/{project_id}/compliance-check",
    response_model=ComplianceCheckResponse,
    tags=["Compliance"]
)
async def run_compliance_check(
    project_id: str,
    check_request: ComplianceCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Run compliance check against specified standards

    Args:
        project_id: Project ID
        check_request: Compliance standards to check against
        current_user: Authenticated user

    Returns:
        Compliance check results with issues and recommendations
    """
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        logger.info(f"Running compliance check for project {project_id}")

        # Get project documents
        documents = await db.list_project_documents(project_id)

        # Run compliance checks
        compliance_results = await compliance_checker.check_standards(
            project_id=project_id,
            documents=documents,
            standards=check_request.standards
        )

        # Save compliance check to database
        check_id = await db.create_compliance_check({
            "project_id": project_id,
            "standard": ", ".join(check_request.standards),
            "status": compliance_results["overall_status"],
            "issues": compliance_results["issues"],
            "recommendations": compliance_results["recommendations"],
            "checked_at": datetime.utcnow()
        })

        compliance_results["id"] = check_id
        logger.info(f"Compliance check completed: {check_id}")

        return ComplianceCheckResponse(**compliance_results)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running compliance check: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run compliance check: {str(e)}"
        )


@app.get(
    "/api/projects/{project_id}/compliance-checks",
    tags=["Compliance"]
)
async def list_compliance_checks(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """List all compliance checks for a project"""
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        checks = await db.list_compliance_checks(project_id)
        return checks

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing compliance checks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list compliance checks: {str(e)}"
        )


# ============================================================================
# RISK ASSESSMENT ENDPOINTS
# ============================================================================

@app.get(
    "/api/projects/{project_id}/risk-assessment",
    response_model=RiskAssessmentResponse,
    tags=["Risk Assessment"]
)
async def get_risk_assessment(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive risk assessment for a project

    Analyzes financial, political, environmental, and technical risks
    """
    try:
        # Verify project access
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        if project.get("user_id") != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        logger.info(f"Generating risk assessment for project {project_id}")

        # Get project documents
        documents = await db.list_project_documents(project_id)

        # Perform risk assessment
        risk_assessment = await financial_engine.assess_risks(project_id, documents)

        logger.info(f"Risk assessment completed for project {project_id}")
        return RiskAssessmentResponse(**risk_assessment)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating risk assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate risk assessment: {str(e)}"
        )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def _generate_recommendations(analysis_results: List[Dict[str, Any]]) -> List[str]:
    """
    Generate actionable recommendations based on analysis results

    Args:
        analysis_results: List of analysis outputs

    Returns:
        List of recommendations
    """
    recommendations = []

    # Extract insights from each analysis component
    for result in analysis_results:
        if isinstance(result, dict):
            if "recommendations" in result:
                recommendations.extend(result["recommendations"])

    # Add general recommendations based on patterns
    if recommendations:
        recommendations.insert(0, "Review all identified issues before proceeding")
    else:
        recommendations.append("No critical issues identified - project appears viable")

    return recommendations


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting InfraFlow AI API...")
    await db.connect()
    logger.info("Database connected")
    logger.info("InfraFlow AI API is ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down InfraFlow AI API...")
    await db.disconnect()
    logger.info("Database disconnected")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
