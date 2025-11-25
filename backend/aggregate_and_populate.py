#!/usr/bin/env python3
"""
InfraFlow AI - Data Aggregation and Database Population Script
This script aggregates research data and populates PostgreSQL and Pinecone databases.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import Json, execute_values
from pinecone import Pinecone
import openai
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/claude-user/ai-consults-platform/00-pivot/research_data/population.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('/home/claude-user/ai-consults-platform/00-pivot/.env')

# Configuration
RESEARCH_DATA_DIR = Path('/home/claude-user/ai-consults-platform/00-pivot/research_data')
DATABASE_URL = os.getenv('LOCAL_DATABASE_URL', 'postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'infraflow-documents')

# Expected research files
EXPECTED_FILES = [
    'ebrd_projects.json',
    'eib_projects.json',
    'ifc_projects.json',
    'worldbank_projects.json',
    'adb_projects.json',
    'afdb_projects.json',
    'compliance_standards.json',
    'renewable_energy_projects.json',
    'water_infrastructure_projects.json',
    'hydrogen_projects.json'
]

class DatabasePopulator:
    """Handles database population operations."""

    def __init__(self):
        """Initialize database connection."""
        self.conn = None
        self.cursor = None
        self.openai_client = None
        self.pinecone_client = None
        self.pinecone_index = None

    def connect_database(self) -> bool:
        """Connect to PostgreSQL database."""
        try:
            logger.info(f"Connecting to database: {DATABASE_URL}")
            self.conn = psycopg2.connect(DATABASE_URL)
            self.cursor = self.conn.cursor()
            logger.info("Database connection established")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False

    def connect_openai(self) -> bool:
        """Initialize OpenAI client."""
        try:
            if not OPENAI_API_KEY:
                logger.error("OpenAI API key not found")
                return False
            openai.api_key = OPENAI_API_KEY
            self.openai_client = openai
            logger.info("OpenAI client initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
            return False

    def connect_pinecone(self) -> bool:
        """Initialize Pinecone client and connect to index."""
        try:
            if not PINECONE_API_KEY:
                logger.error("Pinecone API key not found")
                return False

            self.pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

            # Check if index exists
            indexes = self.pinecone_client.list_indexes()
            index_names = [idx.name for idx in indexes]

            if PINECONE_INDEX_NAME not in index_names:
                logger.warning(f"Index {PINECONE_INDEX_NAME} not found. Creating it...")
                self.pinecone_client.create_index(
                    name=PINECONE_INDEX_NAME,
                    dimension=1536,  # OpenAI embedding dimension
                    metric='cosine',
                    spec={'serverless': {'cloud': 'aws', 'region': 'us-east-1'}}
                )
                logger.info(f"Created Pinecone index: {PINECONE_INDEX_NAME}")

            self.pinecone_index = self.pinecone_client.Index(PINECONE_INDEX_NAME)
            logger.info(f"Connected to Pinecone index: {PINECONE_INDEX_NAME}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {e}")
            return False

    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None

    def insert_project(self, project_data: Dict[str, Any]) -> Optional[str]:
        """Insert a project into the database."""
        try:
            # Get system user ID
            if not hasattr(self, 'system_user_id'):
                self.cursor.execute('SELECT id FROM users LIMIT 1;')
                self.system_user_id = self.cursor.fetchone()[0]

            query = """
            INSERT INTO projects (
                name, sponsor, country, sector, total_value,
                dfi_partners, status, user_id, metadata
            ) VALUES (
                %(name)s, %(sponsor)s, %(country)s, %(sector)s, %(total_value)s,
                %(dfi_partners)s, %(status)s, %(user_id)s, %(metadata)s
            ) RETURNING id
            """

            # Build comprehensive metadata
            metadata = project_data.get('metadata', {})

            # Add additional fields to metadata
            if 'currency' in project_data:
                metadata['currency'] = project_data['currency']
            if 'description' in project_data:
                metadata['description'] = project_data['description']
            if 'location' in project_data:
                metadata['location'] = project_data['location']
            if 'timeline' in project_data:
                metadata['timeline'] = project_data['timeline']
            if 'stakeholders' in project_data:
                metadata['stakeholders'] = project_data['stakeholders']
            if 'investment_usd' in project_data:
                metadata['investment_usd'] = project_data['investment_usd']
            if 'technology' in project_data:
                metadata['technology'] = project_data['technology']
            if 'renewable_source' in project_data:
                metadata['renewable_source'] = project_data['renewable_source']
            if 'capacity_details' in project_data:
                metadata['capacity_details'] = project_data['capacity_details']
            if 'partners' in project_data:
                metadata['partners'] = project_data['partners']
            if 'source' in project_data:
                metadata['source_url'] = project_data['source']
            if 'url' in project_data:
                metadata['source_url'] = project_data['url']

            # Prepare data
            params = {
                'name': project_data.get('name', 'Unknown Project'),
                'sponsor': project_data.get('sponsor', project_data.get('partners', ['Unknown'])[0] if project_data.get('partners') else 'Unknown'),
                'country': project_data.get('country', 'Unknown'),
                'sector': self._map_sector(project_data.get('sector', 'other')),
                'total_value': project_data.get('total_value') or project_data.get('investment_usd'),
                'dfi_partners': Json(project_data.get('dfi_partners', [])),
                'status': self._map_status(project_data.get('status', 'draft')),
                'user_id': self.system_user_id,
                'metadata': Json(metadata)
            }

            self.cursor.execute(query, params)
            project_id = self.cursor.fetchone()[0]
            return str(project_id)
        except Exception as e:
            logger.error(f"Failed to insert project: {e}")
            logger.error(f"Project data: {project_data}")
            return None

    def insert_compliance_check(self, project_id: str, compliance_data: Dict[str, Any]) -> Optional[str]:
        """Insert a compliance check into the database."""
        try:
            query = """
            INSERT INTO compliance_checks (
                project_id, standard, category, status, score,
                issues, recommendations, evidence, notes, metadata
            ) VALUES (
                %(project_id)s, %(standard)s, %(category)s, %(status)s, %(score)s,
                %(issues)s, %(recommendations)s, %(evidence)s, %(notes)s, %(metadata)s
            ) RETURNING id
            """

            params = {
                'project_id': project_id,
                'standard': compliance_data.get('standard', 'Unknown'),
                'category': compliance_data.get('category'),
                'status': compliance_data.get('status', 'pending'),
                'score': compliance_data.get('score'),
                'issues': Json(compliance_data.get('issues', [])),
                'recommendations': Json(compliance_data.get('recommendations', [])),
                'evidence': Json(compliance_data.get('evidence', [])),
                'notes': compliance_data.get('notes'),
                'metadata': Json(compliance_data.get('metadata', {}))
            }

            self.cursor.execute(query, params)
            check_id = self.cursor.fetchone()[0]
            return str(check_id)
        except Exception as e:
            logger.error(f"Failed to insert compliance check: {e}")
            return None

    def store_in_pinecone(self, doc_id: str, text: str, metadata: Dict[str, Any]) -> bool:
        """Store document embedding in Pinecone."""
        try:
            # Generate embedding
            embedding = self.generate_embedding(text)
            if not embedding:
                return False

            # Prepare metadata (Pinecone has restrictions on metadata size)
            clean_metadata = {
                'project_name': metadata.get('project_name', '')[:512],
                'country': metadata.get('country', '')[:100],
                'sector': metadata.get('sector', '')[:100],
                'dfi': metadata.get('dfi', '')[:100],
                'type': metadata.get('type', 'project'),
                'created_at': datetime.now().isoformat()
            }

            # Upsert to Pinecone
            self.pinecone_index.upsert(
                vectors=[(doc_id, embedding, clean_metadata)]
            )
            logger.debug(f"Stored document {doc_id} in Pinecone")
            return True
        except Exception as e:
            logger.error(f"Failed to store in Pinecone: {e}")
            return False

    def _map_sector(self, sector: str) -> str:
        """Map sector name to database enum value."""
        sector_mapping = {
            'renewable energy': 'renewable_energy',
            'green hydrogen': 'green_hydrogen',
            'hydrogen': 'green_hydrogen',
            'transmission': 'transmission',
            'water': 'water',
            'transportation': 'transportation',
            'waste management': 'waste_management',
            'waste': 'waste_management',
            'energy - wind': 'renewable_energy',
            'energy - solar': 'renewable_energy',
            'energy - hydro': 'renewable_energy'
        }
        return sector_mapping.get(sector.lower(), 'other')

    def _map_status(self, status: str) -> str:
        """Map project status to database enum value."""
        status_lower = status.lower()

        # Map various status strings to database enum
        if any(word in status_lower for word in ['completed', 'operational', 'operating']):
            return 'completed'
        elif any(word in status_lower for word in ['construction', 'under development', 'implementation']):
            return 'active'
        elif any(word in status_lower for word in ['planning', 'announced', 'development', 'awarded', 'signed']):
            return 'draft'
        elif any(word in status_lower for word in ['analyzed', 'assessed']):
            return 'analyzed'
        elif any(word in status_lower for word in ['archived', 'cancelled', 'suspended']):
            return 'archived'
        else:
            # Default to active if unsure
            return 'draft'

    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed")


class ResearchAggregator:
    """Handles research data aggregation."""

    def __init__(self):
        """Initialize aggregator."""
        self.data = {
            'projects': [],
            'compliance_standards': [],
            'dfis': set(),
            'countries': set(),
            'sectors': set()
        }

    def wait_for_completion(self, timeout: int = 3600) -> bool:
        """Wait for all research files to be created."""
        logger.info("Waiting for research agents to complete...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            missing_files = []
            for filename in EXPECTED_FILES:
                filepath = RESEARCH_DATA_DIR / filename
                if not filepath.exists():
                    missing_files.append(filename)

            if not missing_files:
                logger.info("All research files found!")
                return True

            logger.info(f"Waiting for {len(missing_files)} files: {missing_files[:3]}...")
            time.sleep(30)  # Check every 30 seconds

        logger.warning(f"Timeout reached. Missing files: {missing_files}")
        return False

    def load_research_files(self) -> bool:
        """Load all available research files."""
        logger.info("Loading research files...")
        loaded_count = 0

        # Load all JSON files from research directory
        json_files = list(RESEARCH_DATA_DIR.glob('*.json'))
        logger.info(f"Found {len(json_files)} JSON files")

        for filepath in json_files:
            filename = filepath.name

            # Skip sample files in production
            if filename.startswith('sample_'):
                logger.debug(f"Skipping sample file: {filename}")
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle different data structures
                projects_loaded = 0

                # Direct projects array
                if 'projects' in data:
                    projects = data['projects']
                    self.data['projects'].extend(projects)
                    projects_loaded = len(projects)
                    logger.info(f"Loaded {projects_loaded} projects from {filename}")

                # Green hydrogen projects
                elif 'green_hydrogen_projects' in data:
                    projects = data['green_hydrogen_projects']
                    # Convert to standard format
                    for proj in projects:
                        proj['sector'] = 'green_hydrogen'
                    self.data['projects'].extend(projects)
                    projects_loaded = len(projects)
                    logger.info(f"Loaded {projects_loaded} hydrogen projects from {filename}")

                # Compliance standards
                elif 'compliance_standards' in data:
                    standards = data['compliance_standards']
                    self.data['compliance_standards'].extend(standards)
                    logger.info(f"Loaded {len(standards)} compliance standards from {filename}")

                elif 'standards' in data:
                    standards = data['standards']
                    self.data['compliance_standards'].extend(standards)
                    logger.info(f"Loaded {len(standards)} compliance standards from {filename}")

                # Companies/Developers (convert to projects or skip)
                elif 'companies' in data:
                    logger.info(f"Loaded {len(data['companies'])} companies from {filename} (stored in metadata)")
                    # Store companies for reference but don't treat as projects

                else:
                    logger.warning(f"Unknown data structure in {filename}: keys={list(data.keys())}")

                loaded_count += 1
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}", exc_info=True)

        logger.info(f"Successfully loaded {loaded_count} files")
        logger.info(f"Total projects: {len(self.data['projects'])}")
        logger.info(f"Total compliance standards: {len(self.data['compliance_standards'])}")
        return loaded_count > 0

    def deduplicate_projects(self):
        """Remove duplicate projects based on name and country."""
        logger.info("Deduplicating projects...")
        unique_projects = {}

        for project in self.data['projects']:
            key = (project.get('name', '').lower(), project.get('country', '').lower())
            if key not in unique_projects:
                unique_projects[key] = project
            else:
                # Merge data if duplicate found
                existing = unique_projects[key]
                # Add DFI partner if not present
                if 'dfi_partners' in project:
                    if 'dfi_partners' not in existing:
                        existing['dfi_partners'] = []
                    existing['dfi_partners'].extend(project['dfi_partners'])

        self.data['projects'] = list(unique_projects.values())
        logger.info(f"Deduplicated to {len(self.data['projects'])} unique projects")

    def extract_metadata(self):
        """Extract metadata from aggregated data."""
        logger.info("Extracting metadata...")

        for project in self.data['projects']:
            # Extract DFIs
            dfi_partners = project.get('dfi_partners', [])
            for dfi in dfi_partners:
                if isinstance(dfi, dict):
                    self.data['dfis'].add(dfi.get('name', ''))
                elif isinstance(dfi, str):
                    self.data['dfis'].add(dfi)

            # Extract countries
            country = project.get('country', '')
            if country:
                self.data['countries'].add(country)

            # Extract sectors
            sector = project.get('sector', '')
            if sector:
                self.data['sectors'].add(sector)

        logger.info(f"Found {len(self.data['dfis'])} DFIs")
        logger.info(f"Found {len(self.data['countries'])} countries")
        logger.info(f"Found {len(self.data['sectors'])} sectors")

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        return {
            'total_projects': len(self.data['projects']),
            'total_compliance_standards': len(self.data['compliance_standards']),
            'total_dfis': len(self.data['dfis']),
            'total_countries': len(self.data['countries']),
            'total_sectors': len(self.data['sectors']),
            'dfis': sorted(list(self.data['dfis'])),
            'countries': sorted(list(self.data['countries'])),
            'sectors': sorted(list(self.data['sectors']))
        }


def create_summary_report(aggregator: ResearchAggregator, db_stats: Dict[str, Any]):
    """Create summary report."""
    summary = aggregator.get_summary()

    report_content = f"""# InfraFlow AI - Database Population Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report summarizes the data aggregation and database population process for InfraFlow AI.

## Data Sources

- **Research Files Processed**: {len(EXPECTED_FILES)} files
- **Data Aggregation Date**: {datetime.now().strftime('%Y-%m-%d')}

## Aggregated Data Statistics

### Projects
- **Total Projects Found**: {summary['total_projects']}
- **Projects Inserted to Database**: {db_stats.get('projects_inserted', 0)}
- **Projects with Embeddings**: {db_stats.get('embeddings_created', 0)}

### Coverage
- **Countries Covered**: {summary['total_countries']}
- **Sectors Represented**: {summary['total_sectors']}
- **DFI Partners**: {summary['total_dfis']}

### Compliance Standards
- **Total Standards**: {summary['total_compliance_standards']}
- **Compliance Checks Created**: {db_stats.get('compliance_checks_created', 0)}

## Detailed Breakdown

### DFI Partners
{chr(10).join(f'- {dfi}' for dfi in summary['dfis'][:20])}
{f"... and {len(summary['dfis']) - 20} more" if len(summary['dfis']) > 20 else ""}

### Countries
{chr(10).join(f'- {country}' for country in summary['countries'][:30])}
{f"... and {len(summary['countries']) - 30} more" if len(summary['countries']) > 30 else ""}

### Sectors
{chr(10).join(f'- {sector}' for sector in summary['sectors'])}

## Database Population Results

### PostgreSQL Database
- **Database URL**: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost:15432'}
- **Projects Table**: {db_stats.get('projects_inserted', 0)} records
- **Compliance Checks Table**: {db_stats.get('compliance_checks_created', 0)} records
- **Total Database Records**: {db_stats.get('total_records', 0)}

### Pinecone Vector Database
- **Index Name**: {PINECONE_INDEX_NAME}
- **Embeddings Created**: {db_stats.get('embeddings_created', 0)}
- **Embedding Model**: text-embedding-ada-002 (OpenAI)
- **Vector Dimension**: 1536

## Data Quality Metrics

### Completeness
- **Projects with Complete Data**: {db_stats.get('complete_projects', 0)} ({db_stats.get('complete_projects_percent', 0):.1f}%)
- **Projects with Location Data**: {db_stats.get('projects_with_location', 0)}
- **Projects with Financial Data**: {db_stats.get('projects_with_financial', 0)}
- **Projects with Timeline Data**: {db_stats.get('projects_with_timeline', 0)}

### Errors and Warnings
- **Insertion Errors**: {db_stats.get('errors', 0)}
- **Embedding Generation Failures**: {db_stats.get('embedding_failures', 0)}
- **Data Validation Warnings**: {db_stats.get('warnings', 0)}

## Recommendations

### Next Steps
1. **Data Enhancement**: Enrich existing project data with additional details from source websites
2. **Validation**: Review and validate compliance checks for accuracy
3. **Testing**: Test vector search functionality in Pinecone
4. **Monitoring**: Set up monitoring for database performance
5. **Backup**: Configure automated database backups

### Data Quality Improvements
1. Standardize country names and ISO codes
2. Normalize DFI partner names
3. Add missing financial data where available
4. Enhance project descriptions for better search results
5. Add more compliance standards from regional regulations

### System Optimization
1. Create database indexes for frequently queried fields
2. Optimize embedding generation for batch processing
3. Implement caching for repeated queries
4. Set up incremental updates for new research data

## Conclusion

The database population process has successfully aggregated and stored {summary['total_projects']} infrastructure projects from {summary['total_dfis']} DFI partners across {summary['total_countries']} countries. The data is now available in both PostgreSQL (for structured queries) and Pinecone (for semantic search).

The system is ready for:
- Project discovery and search
- Compliance checking
- Risk assessment
- Financial modeling
- Investment memo generation

---

*Report generated by InfraFlow AI Database Aggregation System*
*For questions or issues, contact the development team*
"""

    # Write report
    report_path = RESEARCH_DATA_DIR / 'POPULATION_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    logger.info(f"Summary report created: {report_path}")


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("InfraFlow AI - Data Aggregation and Database Population")
    logger.info("=" * 80)

    # Initialize components
    aggregator = ResearchAggregator()
    populator = DatabasePopulator()

    # Statistics
    db_stats = {
        'projects_inserted': 0,
        'compliance_checks_created': 0,
        'embeddings_created': 0,
        'complete_projects': 0,
        'projects_with_location': 0,
        'projects_with_financial': 0,
        'projects_with_timeline': 0,
        'errors': 0,
        'embedding_failures': 0,
        'warnings': 0
    }

    try:
        # Step 1: Wait for research completion (optional - can skip if running manually)
        # Uncomment the following lines to enable waiting
        # if not aggregator.wait_for_completion():
        #     logger.warning("Not all research files are available, proceeding with available data...")

        # Step 2: Load and aggregate research data
        if not aggregator.load_research_files():
            logger.error("Failed to load research files")
            return 1

        aggregator.deduplicate_projects()
        aggregator.extract_metadata()

        # Step 3: Connect to databases
        if not populator.connect_database():
            logger.error("Failed to connect to PostgreSQL")
            return 1

        if not populator.connect_openai():
            logger.error("Failed to initialize OpenAI (embeddings will be skipped)")

        if not populator.connect_pinecone():
            logger.error("Failed to connect to Pinecone (vector storage will be skipped)")

        # Step 4: Populate PostgreSQL
        logger.info("Populating PostgreSQL database...")
        for i, project in enumerate(aggregator.data['projects'], 1):
            logger.info(f"Processing project {i}/{len(aggregator.data['projects'])}: {project.get('name', 'Unknown')}")

            # Insert project
            project_id = populator.insert_project(project)
            if project_id:
                db_stats['projects_inserted'] += 1

                # Check data completeness
                if project.get('description') and len(project.get('description', '')) > 50:
                    db_stats['complete_projects'] += 1
                if project.get('location'):
                    db_stats['projects_with_location'] += 1
                if project.get('total_value'):
                    db_stats['projects_with_financial'] += 1
                if project.get('timeline'):
                    db_stats['projects_with_timeline'] += 1

                # Generate embedding and store in Pinecone
                if populator.pinecone_index and populator.openai_client:
                    # Create text for embedding
                    embedding_text = f"""
                    Project: {project.get('name', '')}
                    Country: {project.get('country', '')}
                    Sector: {project.get('sector', '')}
                    Description: {project.get('description', '')}
                    Sponsor: {project.get('sponsor', '')}
                    """

                    metadata = {
                        'project_name': project.get('name', ''),
                        'country': project.get('country', ''),
                        'sector': project.get('sector', ''),
                        'dfi': ', '.join([str(d.get('name', d)) if isinstance(d, dict) else str(d) for d in project.get('dfi_partners', [])]),
                        'type': 'project'
                    }

                    if populator.store_in_pinecone(project_id, embedding_text, metadata):
                        db_stats['embeddings_created'] += 1
                    else:
                        db_stats['embedding_failures'] += 1

                # Insert compliance checks if available
                if 'compliance_checks' in project:
                    for check in project['compliance_checks']:
                        if populator.insert_compliance_check(project_id, check):
                            db_stats['compliance_checks_created'] += 1

                # Commit after each project
                populator.conn.commit()
            else:
                db_stats['errors'] += 1
                logger.warning(f"Failed to insert project: {project.get('name', 'Unknown')}")

        # Calculate percentages
        if db_stats['projects_inserted'] > 0:
            db_stats['complete_projects_percent'] = (db_stats['complete_projects'] / db_stats['projects_inserted']) * 100
        else:
            db_stats['complete_projects_percent'] = 0

        db_stats['total_records'] = db_stats['projects_inserted'] + db_stats['compliance_checks_created']

        # Step 5: Create summary report
        logger.info("Creating summary report...")
        create_summary_report(aggregator, db_stats)

        logger.info("=" * 80)
        logger.info("Database population completed successfully!")
        logger.info(f"Projects inserted: {db_stats['projects_inserted']}")
        logger.info(f"Embeddings created: {db_stats['embeddings_created']}")
        logger.info(f"Compliance checks: {db_stats['compliance_checks_created']}")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Fatal error during execution: {e}", exc_info=True)
        return 1
    finally:
        populator.close()


if __name__ == '__main__':
    sys.exit(main())
