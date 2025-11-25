# InfraFlow AI - Data Aggregation Execution Guide

**Quick Reference Guide for Running the Data Aggregation System**

## 🚀 Quick Start (3 Steps)

### Step 1: Navigate to Backend Directory

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
```

### Step 2: Install Dependencies (First Time Only)

```bash
pip install -r requirements_aggregator.txt
```

### Step 3: Run the Orchestrator

```bash
python orchestrator.py
```

**Then select option 1** from the menu for the full pipeline.

---

## 📋 Complete Workflow

### Phase 1: Pre-Flight Checks

#### 1.1 Check Research Data Status

```bash
python check_research_status.py
```

**What it shows:**
- Available JSON files
- Record counts per file
- Missing expected files
- Completion percentage

**Expected output:**
```
📊 Status: X/10 expected files | Y total files
✅ Available Files:
  • dfi_projects.json                  17.4 KB     15 projects
  • green_hydrogen_projects.json       18.4 KB     10 hydrogen projects
  ...
```

#### 1.2 Test All Connections

```bash
python test_connections.py
```

**What it tests:**
- ✅ PostgreSQL database connection
- ✅ OpenAI API (for embeddings)
- ✅ Pinecone vector database

**Expected output:**
```
✅ PASS - PostgreSQL
✅ PASS - OpenAI
✅ PASS - Pinecone
✨ All connections successful!
```

---

### Phase 2: Run Aggregation

#### Option A: Interactive Mode (Recommended)

```bash
python orchestrator.py
```

**Menu:**
```
1. Run full pipeline (check → test → aggregate)    ← Choose this!
2. Check prerequisites only
3. Test connections only
4. Check research data status only
5. Run aggregation only (skip checks)
6. View summary report
7. Monitor aggregation (real-time)
0. Exit
```

#### Option B: Direct Execution

```bash
python aggregate_and_populate.py
```

This runs the aggregation directly without checks.

---

### Phase 3: Monitor Progress (Optional)

**In a separate terminal window:**

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
python monitor_aggregation.py
```

**What you'll see:**
```
================================================================================
                InfraFlow AI - Data Aggregation Monitor
================================================================================
Time: 2025-11-25 10:15:30
================================================================================

📊 STATISTICS
--------------------------------------------------------------------------------
Status:             Running
Projects Processed: 15
Embeddings Created: 12
Warnings:           0
Errors:             0
Last Project:       Morocco Solar Power Complex

📝 RECENT LOG ENTRIES
--------------------------------------------------------------------------------
🔵 INFO - Processing project 15/25: Morocco Solar Power Complex
🔵 INFO - Stored document in Pinecone
...
```

---

### Phase 4: View Results

#### 4.1 Check Summary Report

```bash
cat /home/claude-user/ai-consults-platform/00-pivot/research_data/POPULATION_REPORT.md
```

Or view with pagination:

```bash
less /home/claude-user/ai-consults-platform/00-pivot/research_data/POPULATION_REPORT.md
```

#### 4.2 Check Execution Log

```bash
tail -50 /home/claude-user/ai-consults-platform/00-pivot/research_data/population.log
```

Or watch in real-time:

```bash
tail -f /home/claude-user/ai-consults-platform/00-pivot/research_data/population.log
```

#### 4.3 Query Database

```bash
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db
```

**Useful queries:**

```sql
-- Count total projects
SELECT COUNT(*) FROM projects;

-- View recent projects
SELECT name, country, sector, total_value
FROM projects
ORDER BY created_at DESC
LIMIT 10;

-- Projects by sector
SELECT sector, COUNT(*)
FROM projects
GROUP BY sector
ORDER BY COUNT(*) DESC;

-- Projects by country
SELECT country, COUNT(*)
FROM projects
GROUP BY country
ORDER BY COUNT(*) DESC;

-- Compliance checks
SELECT COUNT(*) FROM compliance_checks;

-- Exit
\q
```

---

## 🎯 Common Scenarios

### Scenario 1: First Time Setup

```bash
# 1. Install dependencies
cd /home/claude-user/ai-consults-platform/00-pivot/backend
pip install -r requirements_aggregator.txt

# 2. Test everything
python test_connections.py

# 3. Check data
python check_research_status.py

# 4. Run full pipeline
python orchestrator.py
# Select option 1
```

### Scenario 2: New Research Data Arrived

```bash
# 1. Check what's new
python check_research_status.py

# 2. Run aggregation (deduplication handles existing data)
python aggregate_and_populate.py

# 3. View updated report
cat research_data/POPULATION_REPORT.md
```

### Scenario 3: Check Current Status

```bash
# Quick status check
python check_research_status.py

# Database check
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "SELECT COUNT(*) FROM projects;"
```

### Scenario 4: Troubleshooting

```bash
# Test connections
python test_connections.py

# Check logs
tail -100 research_data/population.log

# Check database
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "SELECT version();"
```

---

## ⚙️ Configuration

### Environment Variables

Located in: `/home/claude-user/ai-consults-platform/00-pivot/.env`

**Required variables:**

```bash
# Database
LOCAL_DATABASE_URL=postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db

# OpenAI (for embeddings)
OPENAI_API_KEY=sk-...

# Pinecone (for vector storage)
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=infraflow-documents
```

### Verify Configuration

```bash
cat /home/claude-user/ai-consults-platform/00-pivot/.env | grep -E "(DATABASE_URL|OPENAI|PINECONE)"
```

---

## 📊 Understanding the Output

### During Execution

**You'll see:**
- Loading research files
- Deduplicating projects
- Connecting to databases
- Processing each project:
  - Inserting into PostgreSQL
  - Generating embedding
  - Storing in Pinecone
- Creating summary report

### After Completion

**Check these files:**

1. **POPULATION_REPORT.md** - Executive summary
   - Total projects added
   - Data quality metrics
   - Recommendations

2. **population.log** - Detailed execution log
   - All operations performed
   - Any errors or warnings
   - Timing information

---

## 🔧 Troubleshooting

### Problem: "Database connection failed"

**Solution:**

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# If not running, start it
docker-compose up -d postgres

# Test connection
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db -c "SELECT 1"
```

### Problem: "OpenAI API key invalid"

**Solution:**

```bash
# Check if key is in .env
grep OPENAI_API_KEY /home/claude-user/ai-consults-platform/00-pivot/.env

# Verify key format (should start with sk-)
# Update .env if needed
```

### Problem: "Pinecone connection failed"

**Solution:**

```bash
# Check if key is in .env
grep PINECONE_API_KEY /home/claude-user/ai-consults-platform/00-pivot/.env

# Verify key format (should start with pcsk_)
# Check internet connection
```

### Problem: "No research files found"

**Solution:**

```bash
# Check if directory exists
ls -la /home/claude-user/ai-consults-platform/00-pivot/research_data/

# Check for JSON files
ls -la /home/claude-user/ai-consults-platform/00-pivot/research_data/*.json

# Wait for research agents to complete
python check_research_status.py
```

### Problem: "Import errors"

**Solution:**

```bash
# Reinstall dependencies
pip install -r requirements_aggregator.txt

# Or install individually
pip install psycopg2-binary pinecone-client openai python-dotenv
```

---

## 📈 Performance Tips

### Speed Up Embedding Generation

Embeddings are the slowest part. To optimize:

1. **Batch similar projects** (system handles this automatically)
2. **Check OpenAI rate limits** on your account
3. **Monitor progress** with `monitor_aggregation.py`

### Expected Duration

| Projects | Time | Rate |
|----------|------|------|
| 50 | ~3-5 min | 10-15/min |
| 100 | ~5-10 min | 10-20/min |
| 500 | ~20-30 min | 15-25/min |
| 1000 | ~60-90 min | 10-17/min |

---

## 🎓 Learning Resources

### Documentation Files

1. **README_AGGREGATOR.md** - Complete system documentation
2. **QUICKSTART.md** - Quick start guide
3. **AGGREGATOR_SETUP_COMPLETE.md** - System overview
4. **EXECUTION_GUIDE.md** - This file

### Code Files

- `aggregate_and_populate.py` - Main engine (well commented)
- `check_research_status.py` - Simple status checker
- `test_connections.py` - Connection testing
- `monitor_aggregation.py` - Real-time monitoring

---

## 🚀 Next Steps After Aggregation

1. **Verify Data Quality**
   ```bash
   # Check projects in database
   psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db
   \dt
   SELECT COUNT(*) FROM projects;
   ```

2. **Test Semantic Search**
   - Use Pinecone console
   - Query for similar projects
   - Verify metadata filtering

3. **Review Summary Report**
   ```bash
   less research_data/POPULATION_REPORT.md
   ```

4. **Set Up Incremental Updates**
   - Schedule periodic runs
   - Monitor for new research files
   - Automatic deduplication handles updates

---

## 📞 Quick Command Reference

```bash
# Status Check
python check_research_status.py

# Connection Test
python test_connections.py

# Full Pipeline (Interactive)
python orchestrator.py

# Direct Aggregation
python aggregate_and_populate.py

# Monitor Progress
python monitor_aggregation.py

# View Report
cat research_data/POPULATION_REPORT.md

# View Logs
tail -f research_data/population.log

# Database Query
psql postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db
```

---

**Ready to start?**

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
python orchestrator.py
```

**Select option 1 and let the system guide you!**

---

*InfraFlow AI Data Aggregation System v1.0.0*
