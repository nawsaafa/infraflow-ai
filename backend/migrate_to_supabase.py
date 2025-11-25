#!/usr/bin/env python3
"""
Migrate projects from local PostgreSQL to Supabase
"""

import os
import sys
import json
import logging
from datetime import datetime
from urllib.parse import quote_plus
import psycopg2
from psycopg2.extras import Json, RealDictCursor
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/claude-user/ai-consults-platform/00-pivot/migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('/home/claude-user/ai-consults-platform/00-pivot/.env')

# Configuration
LOCAL_DATABASE_URL = os.getenv('LOCAL_DATABASE_URL')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_DB_PASSWORD = os.getenv('SUPABASE_DB_PASSWORD')

# Construct Supabase direct database connection string
# Format: postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
project_ref = SUPABASE_URL.replace('https://', '').split('.')[0]
# URL encode the password to handle special characters
encoded_password = quote_plus(SUPABASE_DB_PASSWORD)
SUPABASE_DATABASE_URL = f"postgresql://postgres:{encoded_password}@db.{project_ref}.supabase.co:5432/postgres"

logger.info(f"Using Supabase project: {project_ref}")

class DatabaseMigrator:
    """Handles database migration from local PostgreSQL to Supabase."""

    def __init__(self):
        self.local_conn = None
        self.supabase_conn = None
        self.stats = {
            'projects_exported': 0,
            'projects_imported': 0,
            'users_created': 0,
            'errors': 0,
            'skipped': 0
        }
        self.user_mapping = {}  # Map local user IDs to Supabase user IDs

    def connect_local(self) -> bool:
        """Connect to local PostgreSQL database."""
        try:
            logger.info(f"Connecting to local PostgreSQL...")
            self.local_conn = psycopg2.connect(LOCAL_DATABASE_URL)
            logger.info("✓ Local PostgreSQL connected")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to connect to local PostgreSQL: {e}")
            return False

    def connect_supabase(self) -> bool:
        """Connect to Supabase PostgreSQL database."""
        try:
            logger.info(f"Connecting to Supabase...")
            self.supabase_conn = psycopg2.connect(SUPABASE_DATABASE_URL)
            logger.info("✓ Supabase connected")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to connect to Supabase: {e}")
            logger.error(f"Connection string format: postgresql://postgres.{project_ref}:****@aws-0-us-east-1.pooler.supabase.com:6543/postgres")
            return False

    def verify_supabase_schema(self) -> bool:
        """Verify that Supabase has the required schema."""
        try:
            cursor = self.supabase_conn.cursor()

            # Check if projects table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'projects'
                );
            """)

            projects_exists = cursor.fetchone()[0]

            if not projects_exists:
                logger.error("✗ Projects table does not exist in Supabase")
                logger.error("Please run the schema migration first")
                return False

            logger.info("✓ Supabase schema verified")
            cursor.close()
            return True

        except Exception as e:
            logger.error(f"✗ Failed to verify Supabase schema: {e}")
            return False

    def create_or_get_system_user(self) -> str:
        """Create or get system user in Supabase."""
        try:
            cursor = self.supabase_conn.cursor(cursor_factory=RealDictCursor)

            # Check if system user exists
            cursor.execute("""
                SELECT id FROM users
                WHERE email = 'system@infraflow.ai'
                LIMIT 1;
            """)

            result = cursor.fetchone()

            if result:
                user_id = result['id']
                logger.info(f"✓ Using existing system user: {user_id}")
            else:
                # Create system user
                cursor.execute("""
                    INSERT INTO users (email, name, role)
                    VALUES ('system@infraflow.ai', 'System User', 'admin')
                    RETURNING id;
                """)
                user_id = cursor.fetchone()['id']
                self.supabase_conn.commit()
                self.stats['users_created'] += 1
                logger.info(f"✓ Created system user: {user_id}")

            cursor.close()
            return user_id

        except Exception as e:
            logger.error(f"✗ Failed to create/get system user: {e}")
            return None

    def export_projects(self) -> list:
        """Export all projects from local PostgreSQL."""
        try:
            cursor = self.local_conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id, name, sponsor, country, sector,
                    total_value, dfi_partners, status,
                    risk_score, user_id, metadata,
                    created_at, updated_at
                FROM projects
                ORDER BY created_at;
            """)

            projects = cursor.fetchall()
            self.stats['projects_exported'] = len(projects)

            logger.info(f"✓ Exported {len(projects)} projects from local PostgreSQL")
            cursor.close()
            return projects

        except Exception as e:
            logger.error(f"✗ Failed to export projects: {e}")
            return []

    def import_project(self, project: dict, system_user_id: str) -> bool:
        """Import a single project into Supabase."""
        try:
            cursor = self.supabase_conn.cursor()

            # Check if project already exists (by name and country)
            cursor.execute("""
                SELECT id FROM projects
                WHERE name = %s AND country = %s
                LIMIT 1;
            """, (project['name'], project['country']))

            existing = cursor.fetchone()

            if existing:
                logger.debug(f"⊘ Project already exists: {project['name']} ({project['country']})")
                self.stats['skipped'] += 1
                cursor.close()
                return True

            # Insert project
            cursor.execute("""
                INSERT INTO projects (
                    id, name, sponsor, country, sector,
                    total_value, dfi_partners, status,
                    risk_score, user_id, metadata,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s
                );
            """, (
                project['id'],
                project['name'],
                project['sponsor'],
                project['country'],
                project['sector'],
                project['total_value'],
                Json(project['dfi_partners']) if project['dfi_partners'] else Json([]),
                project['status'],
                project['risk_score'],
                system_user_id,  # Use system user for all projects
                Json(project['metadata']) if project['metadata'] else Json({}),
                project['created_at'],
                project['updated_at']
            ))

            self.supabase_conn.commit()
            self.stats['projects_imported'] += 1

            logger.info(f"✓ Imported: {project['name']} ({project['country']})")
            cursor.close()
            return True

        except Exception as e:
            logger.error(f"✗ Failed to import project {project.get('name', 'Unknown')}: {e}")
            self.stats['errors'] += 1
            self.supabase_conn.rollback()
            return False

    def verify_migration(self) -> bool:
        """Verify that all projects were migrated correctly."""
        try:
            local_cursor = self.local_conn.cursor()
            supabase_cursor = self.supabase_conn.cursor()

            # Count projects in local database
            local_cursor.execute("SELECT COUNT(*) FROM projects;")
            local_count = local_cursor.fetchone()[0]

            # Count projects in Supabase
            supabase_cursor.execute("SELECT COUNT(*) FROM projects;")
            supabase_count = supabase_cursor.fetchone()[0]

            logger.info(f"\n{'='*60}")
            logger.info("MIGRATION VERIFICATION")
            logger.info(f"{'='*60}")
            logger.info(f"Local PostgreSQL projects: {local_count}")
            logger.info(f"Supabase projects: {supabase_count}")
            logger.info(f"Projects imported: {self.stats['projects_imported']}")
            logger.info(f"Projects skipped (duplicates): {self.stats['skipped']}")
            logger.info(f"Errors: {self.stats['errors']}")
            logger.info(f"{'='*60}\n")

            local_cursor.close()
            supabase_cursor.close()

            if supabase_count >= local_count:
                logger.info("✓ Migration verification passed")
                return True
            else:
                logger.warning("⚠ Supabase has fewer projects than local PostgreSQL")
                return False

        except Exception as e:
            logger.error(f"✗ Failed to verify migration: {e}")
            return False

    def sample_data_comparison(self):
        """Compare sample data between local and Supabase."""
        try:
            local_cursor = self.local_conn.cursor(cursor_factory=RealDictCursor)
            supabase_cursor = self.supabase_conn.cursor(cursor_factory=RealDictCursor)

            # Get 3 random projects from local
            local_cursor.execute("""
                SELECT id, name, country, sector, status, total_value
                FROM projects
                ORDER BY RANDOM()
                LIMIT 3;
            """)
            local_samples = local_cursor.fetchall()

            logger.info("\nSAMPLE DATA COMPARISON:")
            logger.info(f"{'='*60}")

            for sample in local_samples:
                logger.info(f"\nProject: {sample['name']}")
                logger.info(f"  Local: {sample['country']}, {sample['sector']}, {sample['status']}")

                # Find same project in Supabase
                supabase_cursor.execute("""
                    SELECT id, name, country, sector, status, total_value
                    FROM projects
                    WHERE id = %s;
                """, (sample['id'],))

                supabase_sample = supabase_cursor.fetchone()

                if supabase_sample:
                    logger.info(f"  Supabase: {supabase_sample['country']}, {supabase_sample['sector']}, {supabase_sample['status']}")

                    # Check if data matches
                    if (sample['country'] == supabase_sample['country'] and
                        sample['sector'] == supabase_sample['sector'] and
                        sample['status'] == supabase_sample['status']):
                        logger.info("  ✓ Data matches")
                    else:
                        logger.warning("  ⚠ Data mismatch detected")
                else:
                    logger.error("  ✗ Project not found in Supabase")

            logger.info(f"{'='*60}\n")

            local_cursor.close()
            supabase_cursor.close()

        except Exception as e:
            logger.error(f"✗ Failed to compare sample data: {e}")

    def close(self):
        """Close database connections."""
        if self.local_conn:
            self.local_conn.close()
            logger.info("✓ Local PostgreSQL connection closed")

        if self.supabase_conn:
            self.supabase_conn.close()
            logger.info("✓ Supabase connection closed")


def main():
    """Main migration function."""
    logger.info("="*60)
    logger.info("INFRAFLOW AI - DATABASE MIGRATION TO SUPABASE")
    logger.info("="*60)
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    migrator = DatabaseMigrator()

    try:
        # Step 1: Connect to databases
        if not migrator.connect_local():
            logger.error("Cannot proceed without local database connection")
            return 1

        if not migrator.connect_supabase():
            logger.error("Cannot proceed without Supabase connection")
            return 1

        # Step 2: Verify Supabase schema
        if not migrator.verify_supabase_schema():
            logger.error("Cannot proceed without proper Supabase schema")
            return 1

        # Step 3: Create or get system user
        system_user_id = migrator.create_or_get_system_user()
        if not system_user_id:
            logger.error("Cannot proceed without system user")
            return 1

        # Step 4: Export projects from local PostgreSQL
        projects = migrator.export_projects()
        if not projects:
            logger.error("No projects to migrate")
            return 1

        # Step 5: Import projects to Supabase
        logger.info(f"\nImporting {len(projects)} projects to Supabase...")
        for i, project in enumerate(projects, 1):
            logger.info(f"[{i}/{len(projects)}] Processing: {project['name']}")
            migrator.import_project(project, system_user_id)

        # Step 6: Verify migration
        migrator.verify_migration()

        # Step 7: Compare sample data
        migrator.sample_data_comparison()

        # Final summary
        logger.info("\n" + "="*60)
        logger.info("MIGRATION SUMMARY")
        logger.info("="*60)
        logger.info(f"Projects exported: {migrator.stats['projects_exported']}")
        logger.info(f"Projects imported: {migrator.stats['projects_imported']}")
        logger.info(f"Projects skipped: {migrator.stats['skipped']}")
        logger.info(f"Users created: {migrator.stats['users_created']}")
        logger.info(f"Errors: {migrator.stats['errors']}")
        logger.info("="*60)
        logger.info(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60 + "\n")

        if migrator.stats['errors'] == 0:
            logger.info("✓ Migration completed successfully!")
            return 0
        else:
            logger.warning(f"⚠ Migration completed with {migrator.stats['errors']} errors")
            return 1

    except Exception as e:
        logger.error(f"✗ Fatal error during migration: {e}", exc_info=True)
        return 1
    finally:
        migrator.close()


if __name__ == '__main__':
    sys.exit(main())
