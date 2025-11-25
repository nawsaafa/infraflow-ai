# Supabase Quick Start Guide

## 📋 Overview

All 24 projects have been successfully migrated to Supabase cloud database. This guide will help you integrate Supabase into your application.

---

## 🔑 Credentials

Add these to your `.env` file (already configured):

```env
SUPABASE_URL=https://abhnlhbkmrozxtfoaxnv.supabase.co
SUPABASE_SERVICE_KEY=sb_secret_sKMOGxOH23E9hlYz_v6wag_ToX2vpVI
SUPABASE_PUBLIC_ANON=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🚀 Using the Python Client

### Installation

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
source venv/bin/activate
# Dependencies already installed: requests, python-dotenv
```

### Basic Usage

```python
from supabase_config import SupabaseClient

# Initialize client
client = SupabaseClient()

# Get all projects
result = client.table('projects').select('*').execute()
projects = result['data']

# Get specific project
result = client.table('projects').select('*').eq('id', project_id).execute()
project = result['data'][0] if result['data'] else None

# Filter by country
result = client.table('projects').select('*').eq('country', 'Egypt').execute()
egypt_projects = result['data']

# Search by name (case-insensitive)
result = client.table('projects').select('*').ilike('name', '%Hydrogen%').execute()
hydrogen_projects = result['data']

# Create new project
new_project = {
    'name': 'My New Project',
    'country': 'USA',
    'sector': 'renewable_energy',
    'status': 'draft'
}
result = client.table('projects').insert(new_project).execute()

# Update project
updates = {'status': 'active'}
result = client.table('projects').eq('id', project_id).update(updates).execute()

# Delete project
result = client.table('projects').eq('id', project_id).delete().execute()
```

### Helper Functions

```python
from supabase_config import (
    get_all_projects,
    get_project_by_id,
    get_projects_by_country,
    get_projects_by_sector,
    search_projects,
    create_project,
    update_project,
    delete_project,
    get_projects_count
)

# Get all projects
projects = get_all_projects()

# Get by country
egypt_projects = get_projects_by_country('Egypt')

# Search
results = search_projects('Hydrogen')

# Get count
total = get_projects_count()
```

---

## 🖥️ CLI Usage

The `supabase_config.py` script includes a CLI:

```bash
# Get project count
python3 supabase_config.py count

# List all projects
python3 supabase_config.py list

# Get projects by country
python3 supabase_config.py country Egypt

# Get projects by sector
python3 supabase_config.py sector renewable_energy

# Search projects
python3 supabase_config.py search Hydrogen
```

---

## 🌐 REST API Usage

### Direct API Calls

```bash
# Get all projects
curl -X GET 'https://abhnlhbkmrozxtfoaxnv.supabase.co/rest/v1/projects?select=*' \
  -H "apikey: YOUR_SERVICE_KEY" \
  -H "Authorization: Bearer YOUR_SERVICE_KEY"

# Get specific project
curl -X GET 'https://abhnlhbkmrozxtfoaxnv.supabase.co/rest/v1/projects?id=eq.PROJECT_ID' \
  -H "apikey: YOUR_SERVICE_KEY" \
  -H "Authorization: Bearer YOUR_SERVICE_KEY"

# Filter by country
curl -X GET 'https://abhnlhbkmrozxtfoaxnv.supabase.co/rest/v1/projects?country=eq.Egypt' \
  -H "apikey: YOUR_SERVICE_KEY" \
  -H "Authorization: Bearer YOUR_SERVICE_KEY"

# Create project
curl -X POST 'https://abhnlhbkmrozxtfoaxnv.supabase.co/rest/v1/projects' \
  -H "apikey: YOUR_SERVICE_KEY" \
  -H "Authorization: Bearer YOUR_SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "name": "New Project",
    "country": "USA",
    "sector": "renewable_energy",
    "status": "draft"
  }'
```

---

## 📊 Current Data Stats

**Total Projects:** 24

**By Sector:**
- Other: 18
- Renewable Energy: 6

**By Status:**
- Draft: 19
- Active: 3
- Completed: 2

**By Country (Top 5):**
1. Egypt: 3 projects
2. Poland: 3 projects
3. Oman: 2 projects
4. Romania: 2 projects
5. Saudi Arabia: 1 project

**Data Completeness:**
- With metadata: 24/24 (100%)
- With financial data: 22/24 (92%)

---

## 🔍 Query Operators

### Comparison Operators

```python
# Equal
.eq('country', 'Egypt')

# Not equal
.neq('status', 'archived')

# Greater than
.gt('total_value', 1000000)

# Greater than or equal
.gte('total_value', 1000000)

# Less than
.lt('risk_score', 0.5)

# Less than or equal
.lte('risk_score', 0.5)

# In list
.in_('country', ['Egypt', 'Saudi Arabia', 'UAE'])
```

### Pattern Matching

```python
# Case-sensitive LIKE
.like('name', '%Solar%')

# Case-insensitive LIKE
.ilike('name', '%solar%')
```

### Sorting and Pagination

```python
# Sort ascending
.order('created_at', ascending=True)

# Sort descending
.order('created_at', ascending=False)

# Limit results
.limit(10)

# Offset (pagination)
.offset(20)

# Get count
.count('exact')
```

---

## 🔐 Authentication (Future)

When Supabase Auth is configured:

```python
# For backend (admin operations)
client = SupabaseClient(use_service_key=True)

# For frontend (user operations)
client = SupabaseClient(use_service_key=False)

# With user JWT token
client = SupabaseClient(use_service_key=False)
client.headers['Authorization'] = f'Bearer {user_jwt_token}'
```

---

## 🎯 Integration with Lovable

### Option 1: Use Supabase JavaScript SDK

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_PUBLIC_ANON
)

// Get projects
const { data: projects, error } = await supabase
  .from('projects')
  .select('*')

// Filter
const { data, error } = await supabase
  .from('projects')
  .select('*')
  .eq('country', 'Egypt')
  .order('created_at', { ascending: false })

// Insert
const { data, error } = await supabase
  .from('projects')
  .insert([
    { name: 'New Project', country: 'USA', sector: 'renewable_energy' }
  ])

// Update
const { data, error } = await supabase
  .from('projects')
  .update({ status: 'active' })
  .eq('id', projectId)

// Delete
const { data, error } = await supabase
  .from('projects')
  .delete()
  .eq('id', projectId)
```

### Option 2: Create Backend API Endpoints

Create FastAPI endpoints that use the Python Supabase client:

```python
from fastapi import FastAPI, HTTPException
from supabase_config import (
    get_all_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project
)

app = FastAPI()

@app.get("/api/projects")
def list_projects():
    return get_all_projects()

@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/api/projects")
def create_project_endpoint(project_data: dict):
    return create_project(project_data)

@app.patch("/api/projects/{project_id}")
def update_project_endpoint(project_id: str, updates: dict):
    return update_project(project_id, updates)

@app.delete("/api/projects/{project_id}")
def delete_project_endpoint(project_id: str):
    success = delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True}
```

---

## 📝 Schema Reference

### Projects Table

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    sponsor TEXT,
    country TEXT NOT NULL,
    sector TEXT NOT NULL,
    total_value NUMERIC(15,2),
    dfi_partners JSONB DEFAULT '[]',
    status TEXT DEFAULT 'draft'
        CHECK (status IN ('draft', 'active', 'analyzed', 'completed', 'archived')),
    risk_score DOUBLE PRECISION CHECK (risk_score >= 0 AND risk_score <= 1),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Status Values
- `draft` - Initial state, project being planned
- `active` - Project is in progress
- `analyzed` - Project has been analyzed
- `completed` - Project is finished
- `archived` - Project is archived/inactive

### Sector Values (Current)
- `renewable_energy` - Solar, wind, hydro projects
- `green_hydrogen` - Hydrogen production projects
- `transmission` - Grid and transmission projects
- `water` - Water infrastructure
- `transportation` - Transport infrastructure
- `waste_management` - Waste and recycling
- `other` - Other infrastructure types

---

## 🧪 Testing

### Test Connection

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
source venv/bin/activate
python3 supabase_config.py count
```

Expected output: `Total projects: 24`

### Test Query

```bash
python3 supabase_config.py search Hydrogen
```

Expected output: 7 hydrogen-related projects

### Test Python Import

```python
from supabase_config import get_all_projects, get_projects_count

count = get_projects_count()
print(f"Total: {count}")

projects = get_all_projects()
print(f"First project: {projects[0]['name']}")
```

---

## 🐛 Troubleshooting

### Connection Issues

1. **Check credentials:**
   ```bash
   cd /home/claude-user/ai-consults-platform/00-pivot
   cat .env | grep SUPABASE
   ```

2. **Test API directly:**
   ```bash
   curl -X GET 'https://abhnlhbkmrozxtfoaxnv.supabase.co/rest/v1/projects?select=count' \
     -H "apikey: YOUR_SERVICE_KEY"
   ```

3. **Check Supabase dashboard:**
   - Visit: https://supabase.com/dashboard/project/abhnlhbkmrozxtfoaxnv
   - Check if projects table exists
   - Verify RLS policies (if enabled)

### Common Errors

**404 - Table not found:**
- Check table name spelling
- Verify table exists in Supabase dashboard

**401 - Unauthorized:**
- Check API key is correct
- Ensure using Service Key for admin operations

**400 - Bad request:**
- Check data types match schema
- Verify required fields are provided

---

## 📚 Resources

- **Supabase Dashboard:** https://supabase.com/dashboard/project/abhnlhbkmrozxtfoaxnv
- **Supabase Docs:** https://supabase.com/docs
- **PostgREST API Docs:** https://postgrest.org/
- **Python Client Code:** `/home/claude-user/ai-consults-platform/00-pivot/backend/supabase_config.py`
- **Migration Summary:** `/home/claude-user/ai-consults-platform/00-pivot/MIGRATION_SUMMARY.md`

---

## ✅ Next Steps

1. **Configure Supabase Auth** (for user management)
2. **Set up Row Level Security (RLS)** policies
3. **Update frontend** to use Supabase SDK
4. **Create API endpoints** in FastAPI
5. **Add real-time subscriptions** (if needed)
6. **Set up database backups** in Supabase dashboard
7. **Configure monitoring** and alerts

---

**All 24 projects are live on Supabase! 🎉**

For questions or issues, refer to the migration log:
`/home/claude-user/ai-consults-platform/00-pivot/migration.log`
