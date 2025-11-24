"""
InfraFlow AI - Main FastAPI Application
Infrastructure Finance Intelligence Platform Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import sentry_sdk
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import projects, documents, financial_models, compliance, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("🚀 Starting InfraFlow AI Platform...")

    # Initialize Sentry if DSN is provided
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

    yield

    # Shutdown
    print("👋 Shutting down InfraFlow AI Platform...")


# Create FastAPI application
app = FastAPI(
    title="InfraFlow AI API",
    description="Infrastructure Finance Intelligence Platform - API for DFIs and Project Sponsors",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "InfraFlow AI API",
        "version": "0.1.0"
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "InfraFlow AI - Infrastructure Finance Intelligence Platform",
        "version": "0.1.0",
        "docs": "/api/docs",
        "status": "operational"
    }


# Include routers
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(financial_models.router, prefix="/api/v1/financial-models", tags=["Financial Models"])
app.include_router(compliance.router, prefix="/api/v1/compliance", tags=["Compliance"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
