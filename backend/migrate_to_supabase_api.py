#!/usr/bin/env python3
"""
Migrate projects from local PostgreSQL to Supabase using REST API
"""

import os
import sys
import json
import logging
from datetime import datetime
from decimal import Decimal
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
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
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Supabase API endpoints
SUPABASE_API_URL = f"{SUPABASE_URL}/rest/v1"
HEADERS = {
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

class SupabaseAPIError(Exception):
    """Custom exception for Supabase API errors."""
    pass

class DatabaseMigrator:
    """Handles database migration from local PostgreSQL to Supabase using REST API."""

    def __init__(self):
        self.local_conn = None
        self.stats = {
            'projects_exported': 0,
            'projects_imported': 0,
            'users_created': 0,
            'errors': 0,
            'skipped': 0
        }
        self.system_user_id = None

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

    def test_supabase_connection(self) -> bool:
        """Test Supabase API connection."""
        try:
            logger.info("Testing Supabase API connection...")
            # Test with projects table instead
            response = requests.get(
                f"{SUPABASE_API_URL}/projects?limit=1",
                headers=HEADERS,
                timeout=10
            )

            if response.status_code in [200, 206]:
                logger.info("✓ Supabase API connected")
                return True
            else:
                logger.error(f"✗ Supabase API error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"✗ Failed to connect to Supabase API: {e}")
            return False

    def create_or_get_system_user(self) -> str:
        """Create or get system user in Supabase via API."""
        try:
            # For now, use a dummy UUID as the system user
            # The projects table in Supabase may not have FK constraints yet
            import uuid
            system_user_uuid = str(uuid.UUID('00000000-0000-0000-0000-000000000001'))
            logger.info(f"✓ Using system user UUID: {system_user_uuid}")
            logger.info("  (User management table will be created separately)")
            return system_user_uuid

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

    def convert_to_json_serializable(self, obj):
        """Convert objects to JSON serializable format."""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self.convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_to_json_serializable(item) for item in obj]
        else:
            return obj

    def import_project(self, project: dict) -> bool:
        """Import a single project into Supabase via API."""
        try:
            # Check if project already exists (by name and country)
            response = requests.get(
                f"{SUPABASE_API_URL}/projects?name=eq.{requests.utils.quote(project['name'])}&country=eq.{requests.utils.quote(project['country'])}&select=id",
                headers=HEADERS,
                timeout=10
            )

            if response.status_code == 200:
                existing = response.json()
                if existing:
                    logger.debug(f"⊘ Project already exists: {project['name']} ({project['country']})")
                    self.stats['skipped'] += 1
                    return True

            # Prepare project data (excluding user_id if not in schema)
            project_data = {
                'id': str(project['id']),
                'name': project['name'],
                'sponsor': project['sponsor'],
                'country': project['country'],
                'sector': project['sector'],
                'total_value': float(project['total_value']) if project['total_value'] else None,
                'dfi_partners': self.convert_to_json_serializable(project['dfi_partners']) if project['dfi_partners'] else [],
                'status': project['status'],
                'risk_score': float(project['risk_score']) if project['risk_score'] else None,
                # 'user_id': self.system_user_id,  # Excluded - not in Supabase schema yet
                'metadata': self.convert_to_json_serializable(project['metadata']) if project['metadata'] else {},
                'created_at': project['created_at'].isoformat() if project['created_at'] else None,
                'updated_at': project['updated_at'].isoformat() if project['updated_at'] else None
            }

            # Insert project
            response = requests.post(
                f"{SUPABASE_API_URL}/projects",
                headers=HEADERS,
                json=project_data,
                timeout=10
            )

            if response.status_code in [200, 201]:
                self.stats['projects_imported'] += 1
                logger.info(f"✓ Imported: {project['name']} ({project['country']})")
                return True
            else:
                logger.error(f"✗ Failed to import project {project['name']}: {response.status_code} - {response.text}")
                self.stats['errors'] += 1
                return False

        except Exception as e:
            logger.error(f"✗ Failed to import project {project.get('name', 'Unknown')}: {e}")
            self.stats['errors'] += 1
            return False

    def verify_migration(self) -> bool:
        """Verify that all projects were migrated correctly."""
        try:
            local_cursor = self.local_conn.cursor()

            # Count projects in local database
            local_cursor.execute("SELECT COUNT(*) FROM projects;")
            local_count = local_cursor.fetchone()[0]

            # Count projects in Supabase via API
            response = requests.get(
                f"{SUPABASE_API_URL}/projects?select=count",
                headers={**HEADERS, 'Prefer': 'count=exact'},
                timeout=10
            )

            if response.status_code == 206:
                supabase_count = int(response.headers.get('Content-Range', '0/0').split('/')[1])
            else:
                logger.warning("Could not get exact count from Supabase")
                supabase_count = 0

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
                response = requests.get(
                    f"{SUPABASE_API_URL}/projects?id=eq.{sample['id']}&select=id,name,country,sector,status,total_value",
                    headers=HEADERS,
                    timeout=10
                )

                if response.status_code == 200:
                    supabase_samples = response.json()
                    if supabase_samples:
                        supabase_sample = supabase_samples[0]
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
                else:
                    logger.error(f"  ✗ Error querying Supabase: {response.status_code}")

            logger.info(f"{'='*60}\n")

            local_cursor.close()

        except Exception as e:
            logger.error(f"✗ Failed to compare sample data: {e}")

    def close(self):
        """Close database connection."""
        if self.local_conn:
            self.local_conn.close()
            logger.info("✓ Local PostgreSQL connection closed")


def main():
    """Main migration function."""
    logger.info("="*60)
    logger.info("INFRAFLOW AI - DATABASE MIGRATION TO SUPABASE (REST API)")
    logger.info("="*60)
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    migrator = DatabaseMigrator()

    try:
        # Step 1: Connect to databases
        if not migrator.connect_local():
            logger.error("Cannot proceed without local database connection")
            return 1

        if not migrator.test_supabase_connection():
            logger.error("Cannot proceed without Supabase API connection")
            return 1

        # Step 2: Create or get system user
        migrator.system_user_id = migrator.create_or_get_system_user()
        if not migrator.system_user_id:
            logger.error("Cannot proceed without system user")
            return 1

        # Step 3: Export projects from local PostgreSQL
        projects = migrator.export_projects()
        if not projects:
            logger.error("No projects to migrate")
            return 1

        # Step 4: Import projects to Supabase
        logger.info(f"\nImporting {len(projects)} projects to Supabase...")
        for i, project in enumerate(projects, 1):
            logger.info(f"[{i}/{len(projects)}] Processing: {project['name']}")
            migrator.import_project(project)

        # Step 5: Verify migration
        migrator.verify_migration()

        # Step 6: Compare sample data
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
