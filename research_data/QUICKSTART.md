# InfraFlow AI - Data Aggregation Quick Start Guide

This guide helps you quickly set up and run the data aggregation system.

## Prerequisites

- Python 3.8+
- PostgreSQL database running (localhost:15432)
- OpenAI API key
- Pinecone API key
- Research data files (JSON format)

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
pip install -r requirements_aggregator.txt
```

### 2. Verify Environment

Make sure your `.env` file has these settings:

```bash
# Check .env file
cat /home/claude-user/ai-consults-platform/00-pivot/.env | grep -E "(DATABASE_URL|OPENAI|PINECONE)"
```

Required variables:
- `LOCAL_DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key for embeddings
- `PINECONE_API_KEY` - Pinecone API key
- `PINECONE_INDEX_NAME` - Pinecone index name (default: infraflow-documents)

### 3. Test Connections

```bash
python test_connections.py
```

This will verify:
- ✅ PostgreSQL is accessible
- ✅ OpenAI API is working
- ✅ Pinecone is accessible

### 4. Check Research Data

```bash
python check_research_status.py
```

This shows which research files are available and ready for aggregation.

## Running Aggregation

### Option 1: Interactive Orchestrator (Recommended)

```bash
python orchestrator.py
```

This provides an interactive menu:
1. Run full pipeline
2. Check prerequisites
3. Test connections
4. Check research data
5. Run aggregation
6. View report
7. Monitor real-time

### Option 2: Direct Execution

```bash
python aggregate_and_populate.py
```

### Option 3: Monitor Progress

In a separate terminal, monitor the aggregation in real-time:

```bash
python monitor_aggregation.py
```

## What Happens During Aggregation?

1. **Load Research Files** - Reads all JSON files from research_data/
2. **Deduplicate** - Removes duplicate projects
3. **Validate** - Checks data quality
4. **Database Insert** - Adds projects to PostgreSQL
5. **Generate Embeddings** - Creates vectors using OpenAI
6. **Store Vectors** - Saves embeddings to Pinecone
7. **Create Report** - Generates summary report

## Viewing Results

### Check Database

```bash
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db

-- Count projects
SELECT COUNT(*) FROM projects;

-- View sample projects
SELECT name, country, sector FROM projects LIMIT 10;
```

### View Report

```bash
cat /home/claude-user/ai-consults-platform/00-pivot/research_data/POPULATION_REPORT.md
```

### Check Logs

```bash
tail -f /home/claude-user/ai-consults-platform/00-pivot/research_data/population.log
```

## Expected Duration

- **Small dataset** (< 100 projects): ~5-10 minutes
- **Medium dataset** (100-500 projects): ~20-30 minutes
- **Large dataset** (500+ projects): ~60-90 minutes

*Time varies based on embedding generation speed*

## Troubleshooting

### Database Connection Failed

```bash
# Check if database is running
docker ps | grep postgres

# Test connection manually
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "SELECT 1"
```

### OpenAI API Errors

- Verify API key is valid
- Check you have credits available
- Rate limit: The script includes automatic retry logic

### Pinecone Connection Issues

- Verify API key
- Check if index exists (will be created automatically if not)
- Ensure index dimensions match (1536 for text-embedding-ada-002)

### Missing Research Files

If research agents haven't completed:

```bash
# Check what files exist
ls -la /home/claude-user/ai-consults-platform/00-pivot/research_data/

# Run status check
python check_research_status.py
```

## File Structure

```
backend/
├── aggregate_and_populate.py    # Main aggregation script
├── orchestrator.py              # Interactive menu
├── check_research_status.py     # Status checker
├── test_connections.py          # Connection tester
├── monitor_aggregation.py       # Real-time monitor
└── requirements_aggregator.txt  # Dependencies

research_data/
├── ebrd_projects.json           # EBRD projects
├── eib_projects.json            # EIB projects
├── ifc_projects.json            # IFC projects
├── compliance_standards.json    # Standards
├── ...                          # Other research files
├── population.log               # Execution log
└── POPULATION_REPORT.md         # Summary report
```

## Next Steps After Aggregation

1. ✅ Verify data in database
2. ✅ Test semantic search in Pinecone
3. ✅ Review summary report
4. ✅ Run compliance checks on projects
5. ✅ Generate investment memos
6. ✅ Set up incremental updates

## Getting Help

- **Logs**: Check `population.log` for detailed execution logs
- **Report**: Review `POPULATION_REPORT.md` for statistics
- **Database**: Query PostgreSQL for data verification
- **Status**: Run `check_research_status.py` anytime

## Common Commands

```bash
# Full workflow
python orchestrator.py

# Check status
python check_research_status.py

# Test connections
python test_connections.py

# Run aggregation
python aggregate_and_populate.py

# Monitor progress
python monitor_aggregation.py

# View report
cat research_data/POPULATION_REPORT.md

# Check logs
tail -f research_data/population.log
```

---

**Ready to start?** Run `python orchestrator.py` and select option 1 for the full pipeline!
