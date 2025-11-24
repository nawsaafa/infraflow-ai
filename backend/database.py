"""
InfraFlow AI - Database Layer
Supabase/PostgreSQL connection and data access layer
"""

from typing import Optional, List, Dict, Any
import os
import logging
from datetime import datetime
import asyncpg
from supabase import create_client, Client
import json

logger = logging.getLogger(__name__)


class Database:
    """Database connection and operations handler"""

    def __init__(self):
        """Initialize database connection"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.db_url = os.getenv("DATABASE_URL")

        # Supabase client for storage and auth
        if self.supabase_url and self.supabase_key:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            logger.warning("Supabase credentials not configured")

        # PostgreSQL connection pool
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Establish database connection pool"""
        try:
            if self.db_url:
                self.pool = await asyncpg.create_pool(
                    self.db_url,
                    min_size=2,
                    max_size=10,
                    command_timeout=60
                )
                logger.info("Database pool created successfully")

                # Run migrations if needed
                await self._ensure_tables_exist()
            else:
                logger.warning("DATABASE_URL not configured")

        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise

    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database pool closed")

    async def _ensure_tables_exist(self):
        """Ensure all required tables exist"""
        async with self.pool.acquire() as conn:
            # Check if projects table exists
            exists = await conn.fetchval("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'projects'
                )
            """)

            if not exists:
                logger.info("Creating database schema...")
                await self._create_schema(conn)

    async def _create_schema(self, conn):
        """Create database schema"""
        schema_sql = """
        -- Enable UUID extension
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        -- Projects table
        CREATE TABLE IF NOT EXISTS projects (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name TEXT NOT NULL,
            sponsor TEXT,
            country TEXT NOT NULL,
            sector TEXT NOT NULL,
            total_value DECIMAL(15,2),
            dfi_partners JSONB DEFAULT '[]'::jsonb,
            status TEXT DEFAULT 'draft',
            risk_score FLOAT,
            description TEXT,
            technology TEXT,
            capacity TEXT,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Documents table
        CREATE TABLE IF NOT EXISTS documents (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            type TEXT,
            url TEXT NOT NULL,
            processed BOOLEAN DEFAULT FALSE,
            extracted_data JSONB,
            embeddings_id TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );

        -- Financial models table
        CREATE TABLE IF NOT EXISTS financial_models (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
            model_type TEXT NOT NULL,
            assumptions JSONB NOT NULL,
            outputs JSONB,
            scenarios JSONB DEFAULT '[]'::jsonb,
            created_at TIMESTAMP DEFAULT NOW()
        );

        -- Compliance checks table
        CREATE TABLE IF NOT EXISTS compliance_checks (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
            standard TEXT NOT NULL,
            status TEXT NOT NULL,
            issues JSONB DEFAULT '[]'::jsonb,
            recommendations JSONB DEFAULT '[]'::jsonb,
            checked_at TIMESTAMP DEFAULT NOW()
        );

        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
        CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
        CREATE INDEX IF NOT EXISTS idx_projects_country ON projects(country);
        CREATE INDEX IF NOT EXISTS idx_documents_project_id ON documents(project_id);
        CREATE INDEX IF NOT EXISTS idx_financial_models_project_id ON financial_models(project_id);
        CREATE INDEX IF NOT EXISTS idx_compliance_checks_project_id ON compliance_checks(project_id);
        """

        await conn.execute(schema_sql)
        logger.info("Database schema created successfully")

    # ========================================================================
    # PROJECT OPERATIONS
    # ========================================================================

    async def create_project(self, project_data: Dict[str, Any]) -> str:
        """
        Create a new project

        Args:
            project_data: Project data dictionary

        Returns:
            Created project ID
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO projects (
                    name, sponsor, country, sector, total_value,
                    dfi_partners, status, description, technology,
                    capacity, user_id, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                RETURNING id
            """,
                project_data["name"],
                project_data.get("sponsor"),
                project_data["country"],
                project_data["sector"],
                project_data.get("total_value"),
                json.dumps(project_data.get("dfi_partners", [])),
                project_data.get("status", "draft"),
                project_data.get("description"),
                project_data.get("technology"),
                project_data.get("capacity"),
                project_data["user_id"],
                project_data.get("created_at", datetime.utcnow()),
                project_data.get("updated_at", datetime.utcnow())
            )

            return str(row["id"])

    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get project by ID

        Args:
            project_id: Project UUID

        Returns:
            Project data or None if not found
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM projects WHERE id = $1
            """, project_id)

            if row:
                return dict(row)
            return None

    async def list_projects(
        self,
        user_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List projects with filters

        Args:
            user_id: User ID to filter by
            filters: Additional filters (status, country, sector)
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of projects
        """
        query = "SELECT * FROM projects WHERE user_id = $1"
        params = [user_id]
        param_idx = 2

        if filters:
            if "status" in filters:
                query += f" AND status = ${param_idx}"
                params.append(filters["status"])
                param_idx += 1

            if "country" in filters:
                query += f" AND country = ${param_idx}"
                params.append(filters["country"])
                param_idx += 1

            if "sector" in filters:
                query += f" AND sector = ${param_idx}"
                params.append(filters["sector"])
                param_idx += 1

        query += f" ORDER BY created_at DESC LIMIT ${param_idx} OFFSET ${param_idx + 1}"
        params.extend([limit, offset])

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(row) for row in rows]

    async def update_project(self, project_id: str, updates: Dict[str, Any]):
        """
        Update project

        Args:
            project_id: Project UUID
            updates: Fields to update
        """
        # Build dynamic UPDATE query
        set_clauses = []
        params = []
        param_idx = 1

        for key, value in updates.items():
            if key in ["dfi_partners", "description", "technology", "capacity"]:
                set_clauses.append(f"{key} = ${param_idx}")
                params.append(json.dumps(value) if key == "dfi_partners" else value)
                param_idx += 1
            elif key in ["name", "sponsor", "country", "sector", "total_value", "status", "risk_score"]:
                set_clauses.append(f"{key} = ${param_idx}")
                params.append(value)
                param_idx += 1

        if not set_clauses:
            return

        params.append(project_id)
        query = f"""
            UPDATE projects
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = ${param_idx}
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, *params)

    async def delete_project(self, project_id: str):
        """
        Delete project (cascades to related data)

        Args:
            project_id: Project UUID
        """
        async with self.pool.acquire() as conn:
            await conn.execute("""
                DELETE FROM projects WHERE id = $1
            """, project_id)

    # ========================================================================
    # DOCUMENT OPERATIONS
    # ========================================================================

    async def create_document(self, document_data: Dict[str, Any]) -> str:
        """
        Create a new document record

        Args:
            document_data: Document data

        Returns:
            Created document ID
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO documents (
                    project_id, name, type, url, processed,
                    extracted_data, embeddings_id, created_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id
            """,
                document_data["project_id"],
                document_data["name"],
                document_data.get("type"),
                document_data["url"],
                document_data.get("processed", False),
                json.dumps(document_data.get("extracted_data")) if document_data.get("extracted_data") else None,
                document_data.get("embeddings_id"),
                document_data.get("created_at", datetime.utcnow())
            )

            return str(row["id"])

    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document by ID

        Args:
            document_id: Document UUID

        Returns:
            Document data or None
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM documents WHERE id = $1
            """, document_id)

            if row:
                return dict(row)
            return None

    async def list_project_documents(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List all documents for a project

        Args:
            project_id: Project UUID

        Returns:
            List of documents
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM documents
                WHERE project_id = $1
                ORDER BY created_at DESC
            """, project_id)

            return [dict(row) for row in rows]

    async def update_document(self, document_id: str, updates: Dict[str, Any]):
        """
        Update document

        Args:
            document_id: Document UUID
            updates: Fields to update
        """
        set_clauses = []
        params = []
        param_idx = 1

        for key, value in updates.items():
            if key in ["name", "type", "url", "processed", "extracted_data", "embeddings_id"]:
                set_clauses.append(f"{key} = ${param_idx}")
                if key == "extracted_data":
                    params.append(json.dumps(value) if value else None)
                else:
                    params.append(value)
                param_idx += 1

        if not set_clauses:
            return

        params.append(document_id)
        query = f"""
            UPDATE documents
            SET {', '.join(set_clauses)}
            WHERE id = ${param_idx}
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, *params)

    # ========================================================================
    # FINANCIAL MODEL OPERATIONS
    # ========================================================================

    async def create_financial_model(self, model_data: Dict[str, Any]) -> str:
        """
        Create a new financial model

        Args:
            model_data: Model data

        Returns:
            Created model ID
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO financial_models (
                    project_id, model_type, assumptions, outputs, scenarios, created_at
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
            """,
                model_data["project_id"],
                model_data["model_type"],
                json.dumps(model_data["assumptions"]),
                json.dumps(model_data.get("outputs")),
                json.dumps(model_data.get("scenarios", [])),
                model_data.get("created_at", datetime.utcnow())
            )

            return str(row["id"])

    async def list_financial_models(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List all financial models for a project

        Args:
            project_id: Project UUID

        Returns:
            List of financial models
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM financial_models
                WHERE project_id = $1
                ORDER BY created_at DESC
            """, project_id)

            return [dict(row) for row in rows]

    # ========================================================================
    # COMPLIANCE CHECK OPERATIONS
    # ========================================================================

    async def create_compliance_check(self, check_data: Dict[str, Any]) -> str:
        """
        Create a new compliance check record

        Args:
            check_data: Compliance check data

        Returns:
            Created check ID
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO compliance_checks (
                    project_id, standard, status, issues, recommendations, checked_at
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
            """,
                check_data["project_id"],
                check_data["standard"],
                check_data["status"],
                json.dumps(check_data.get("issues", [])),
                json.dumps(check_data.get("recommendations", [])),
                check_data.get("checked_at", datetime.utcnow())
            )

            return str(row["id"])

    async def list_compliance_checks(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List all compliance checks for a project

        Args:
            project_id: Project UUID

        Returns:
            List of compliance checks
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM compliance_checks
                WHERE project_id = $1
                ORDER BY checked_at DESC
            """, project_id)

            return [dict(row) for row in rows]

    # ========================================================================
    # SUPABASE STORAGE OPERATIONS
    # ========================================================================

    def upload_file(self, bucket: str, file_path: str, file_data: bytes) -> str:
        """
        Upload file to Supabase Storage

        Args:
            bucket: Storage bucket name
            file_path: Path within bucket
            file_data: File content as bytes

        Returns:
            Public URL of uploaded file
        """
        if not self.supabase:
            raise ValueError("Supabase not configured")

        try:
            # Upload file
            self.supabase.storage.from_(bucket).upload(
                file_path,
                file_data,
                file_options={"content-type": "application/octet-stream"}
            )

            # Get public URL
            url = self.supabase.storage.from_(bucket).get_public_url(file_path)
            return url

        except Exception as e:
            logger.error(f"Error uploading file to Supabase: {str(e)}")
            raise

    def download_file(self, bucket: str, file_path: str) -> bytes:
        """
        Download file from Supabase Storage

        Args:
            bucket: Storage bucket name
            file_path: Path within bucket

        Returns:
            File content as bytes
        """
        if not self.supabase:
            raise ValueError("Supabase not configured")

        try:
            return self.supabase.storage.from_(bucket).download(file_path)
        except Exception as e:
            logger.error(f"Error downloading file from Supabase: {str(e)}")
            raise

    def delete_file(self, bucket: str, file_path: str):
        """
        Delete file from Supabase Storage

        Args:
            bucket: Storage bucket name
            file_path: Path within bucket
        """
        if not self.supabase:
            raise ValueError("Supabase not configured")

        try:
            self.supabase.storage.from_(bucket).remove([file_path])
        except Exception as e:
            logger.error(f"Error deleting file from Supabase: {str(e)}")
            raise
