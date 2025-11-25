# InfraFlow AI - Data Aggregation & Database Population System

This system aggregates research data from multiple agents and populates the InfraFlow AI databases (PostgreSQL and Pinecone).

## Overview

The data aggregation system consists of:

1. **Research Data Collection**: Multiple research agents collect data from DFIs and create JSON files
2. **Data Aggregation**: Combines, deduplicates, and validates all research data
3. **Database Population**: Inserts data into PostgreSQL and creates vector embeddings in Pinecone
4. **Reporting**: Generates comprehensive summary reports

## Files

- `aggregate_and_populate.py` - Main aggregation and population script
- `check_research_status.py` - Check status of research data files
- `requirements_aggregator.txt` - Python dependencies
- `README_AGGREGATOR.md` - This file

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements_aggregator.txt
```

### 2. Verify Environment Configuration

Ensure the following environment variables are set in `/home/claude-user/ai-consults-platform/00-pivot/.env`:

```bash
# Database
LOCAL_DATABASE_URL=postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db

# OpenAI (for embeddings)
OPENAI_API_KEY=your-openai-api-key

# Pinecone (for vector storage)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=infraflow-documents
```

### 3. Start Required Services

Make sure PostgreSQL is running:

```bash
# Check if database is accessible
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "SELECT version();"
```

## Usage

### Check Research Data Status

Before running the aggregation, check which research files are available:

```bash
python check_research_status.py
```

This will show:
- Which files are ready
- File sizes and record counts
- Completion percentage
- Missing files

### Run Data Aggregation

Once research data is available, run the aggregation script:

```bash
python aggregate_and_populate.py
```

The script will:
1. Load all available research JSON files
2. Deduplicate projects
3. Extract metadata
4. Connect to PostgreSQL and Pinecone
5. Insert projects into database
6. Generate embeddings and store in Pinecone
7. Create compliance checks
8. Generate summary report

### View Results

After completion, check:

1. **Summary Report**: `/home/claude-user/ai-consults-platform/00-pivot/research_data/POPULATION_REPORT.md`
2. **Log File**: `/home/claude-user/ai-consults-platform/00-pivot/research_data/population.log`
3. **Database**: Query PostgreSQL to verify data

```bash
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db

-- Check inserted projects
SELECT COUNT(*) FROM projects;
SELECT name, country, sector FROM projects LIMIT 10;

-- Check compliance checks
SELECT COUNT(*) FROM compliance_checks;
```

## Expected Research Files

The system expects these JSON files in `/home/claude-user/ai-consults-platform/00-pivot/research_data/`:

1. `ebrd_projects.json` - EBRD projects
2. `eib_projects.json` - EIB projects
3. `ifc_projects.json` - IFC/World Bank projects
4. `worldbank_projects.json` - World Bank projects
5. `adb_projects.json` - Asian Development Bank projects
6. `afdb_projects.json` - African Development Bank projects
7. `compliance_standards.json` - Compliance standards
8. `renewable_energy_projects.json` - Renewable energy projects
9. `water_infrastructure_projects.json` - Water infrastructure projects
10. `hydrogen_projects.json` - Green hydrogen projects

## JSON File Format

### Projects File Format

```json
{
  "source": "Data source name",
  "collected_at": "2025-11-25T00:00:00Z",
  "projects": [
    {
      "name": "Project Name",
      "sponsor": "Sponsor Company",
      "country": "Country Name",
      "sector": "renewable_energy",
      "total_value": 1000000000,
      "currency": "USD",
      "dfi_partners": [
        {
          "name": "DFI Name",
          "commitment": 200000000,
          "status": "approved"
        }
      ],
      "status": "active",
      "description": "Project description...",
      "location": {
        "latitude": 0.0,
        "longitude": 0.0,
        "address": "Location"
      },
      "timeline": {
        "start_date": "2023-01-01",
        "completion_date": "2026-12-31",
        "milestones": []
      },
      "stakeholders": [],
      "metadata": {}
    }
  ]
}
```

### Compliance Standards Format

```json
{
  "source": "Source name",
  "collected_at": "2025-11-25T00:00:00Z",
  "standards": [
    {
      "name": "Standard Name",
      "category": "Category",
      "issuing_body": "Organization",
      "version": "2024",
      "description": "Description...",
      "key_requirements": [],
      "applicability": "Scope",
      "url": "https://..."
    }
  ]
}
```

## Data Processing Flow

```
Research Agents
       ↓
JSON Files (research_data/)
       ↓
Load & Aggregate
       ↓
Deduplicate
       ↓
Validate
       ↓
    ┌──────┴──────┐
    ↓             ↓
PostgreSQL    Pinecone
(Structured)  (Vectors)
    ↓             ↓
Summary Report
```

## Database Schema

### Projects Table

- **id**: UUID (primary key)
- **name**: Project name
- **sponsor**: Sponsor organization
- **country**: Country location
- **sector**: Project sector (enum)
- **total_value**: Project value in currency
- **currency**: Currency code (default USD)
- **dfi_partners**: JSON array of DFI partners
- **status**: Project status (enum)
- **description**: Project description
- **location**: JSON with lat/long
- **timeline**: JSON with dates and milestones
- **stakeholders**: JSON array
- **metadata**: Additional JSON data

### Compliance Checks Table

- **id**: UUID (primary key)
- **project_id**: Foreign key to projects
- **standard**: Compliance standard name
- **category**: Standard category
- **status**: Check status (enum)
- **score**: Compliance score (0-100)
- **issues**: JSON array of issues
- **recommendations**: JSON array
- **evidence**: JSON array

## Vector Embeddings

Each project is converted to a text representation and embedded using OpenAI's `text-embedding-ada-002` model (1536 dimensions). The embeddings are stored in Pinecone with metadata:

- **project_name**: Project name
- **country**: Country
- **sector**: Sector
- **dfi**: DFI partners (comma-separated)
- **type**: "project"

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "SELECT 1"

# Check if database is running
docker ps | grep postgres

# View database logs
docker logs infraflow-postgres
```

### OpenAI API Issues

- Verify API key is valid
- Check API quota and billing
- Monitor rate limits

### Pinecone Issues

- Verify API key and index name
- Check if index exists: Go to Pinecone console
- Ensure index dimensions match (1536 for text-embedding-ada-002)

### Missing Research Files

If files are missing:
1. Check if research agents completed successfully
2. Verify file permissions on research_data directory
3. Review agent logs for errors

## Performance

- **Projects/minute**: ~20-30 (with embeddings)
- **Embedding generation**: ~2-3 seconds per project
- **Database insertion**: <0.1 seconds per project
- **Total time for 1000 projects**: ~60-90 minutes

## Monitoring

Monitor the process:

```bash
# Watch log file in real-time
tail -f /home/claude-user/ai-consults-platform/00-pivot/research_data/population.log

# Check database size
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "
  SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
  FROM pg_tables
  WHERE schemaname = 'public'
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

## Next Steps

After successful population:

1. **Verify Data Quality**: Review sample projects in database
2. **Test Search**: Query Pinecone for semantic search
3. **Run Compliance Checks**: Test compliance checking system
4. **Generate Reports**: Create investment memos from projects
5. **Setup Incremental Updates**: Configure system for ongoing data updates

## Support

For issues or questions:
- Check logs: `population.log`
- Review summary report: `POPULATION_REPORT.md`
- Verify database schema: `supabase/migrations/`

---

*Part of InfraFlow AI Platform - Database Aggregation System*
