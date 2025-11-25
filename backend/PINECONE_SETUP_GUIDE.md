# Pinecone Setup Guide for InfraFlow AI

## ❌ Current Issue: Invalid API Key

The Pinecone API key in your `.env` file appears to be invalid or expired.

```
Error: (401) Unauthorized - Invalid API Key
```

## 🔑 Getting a Valid Pinecone API Key

### Step 1: Sign Up / Log In to Pinecone

1. Visit: https://app.pinecone.io/
2. Sign up for a free account or log in
3. Pinecone offers a **generous free tier**:
   - 1 serverless index
   - 100K vectors
   - Perfect for development and testing

### Step 2: Create an API Key

1. Once logged in, go to **API Keys** section
2. Click **"Create API Key"**
3. Give it a name: `infraflow-ai-dev`
4. Copy the key (starts with something like `pcsk_...`)

### Step 3: Update Your .env File

Edit `/home/claude-user/ai-consults-platform/00-pivot/.env`:

```bash
# Replace the current key with your new key
PINECONE_API_KEY=pcsk_YOUR_NEW_API_KEY_HERE
```

**Important:** Make sure there are no spaces before or after the key!

### Step 4: Run Setup Script

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
source venv/bin/activate
python setup_pinecone.py
```

---

## 📊 What the Setup Script Does

The `setup_pinecone.py` script will:

1. **Initialize Pinecone Client** - Connect using your API key
2. **Create Document Index** - For document embeddings (1536 dimensions)
   - Index name: `infraflow-documents`
   - Metric: Cosine similarity
   - Cloud: AWS (us-east-1)

3. **Optional: Create Financial Index** - For financial model embeddings (768 dimensions)
   - Index name: `infraflow-financial`
   - Metric: Euclidean distance

4. **Test Indexes** - Upload and query test vectors to verify everything works

---

## 🔧 Alternative: Manual Setup via Pinecone Console

If you prefer to create indexes manually:

### 1. Create Document Embeddings Index

In Pinecone console:
- Click **"Create Index"**
- Name: `infraflow-documents`
- Dimensions: `1536`
- Metric: `cosine`
- Pod Type: Serverless (AWS, us-east-1)

### 2. Update .env with Index Name

```bash
PINECONE_INDEX_NAME=infraflow-documents
```

---

## 📝 Pinecone Configuration in .env

After setup, your `.env` should have:

```bash
# Pinecone Vector Database
PINECONE_API_KEY=pcsk_YOUR_ACTUAL_KEY_HERE
PINECONE_ENVIRONMENT=your-environment  # Not needed for serverless
PINECONE_INDEX_NAME=infraflow-documents
```

**Note:** For serverless indexes, you don't need `PINECONE_ENVIRONMENT`. It's only for pod-based indexes.

---

## 🧪 Testing Pinecone Connection

After updating your API key, test the connection:

```bash
cd /home/claude-user/ai-consults-platform/00-pivot/backend
source venv/bin/activate
python -c "
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv('../.env')
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
print('✅ Pinecone connection successful!')
print(f'📊 Indexes: {[idx.name for idx in pc.list_indexes().indexes]}')
"
```

---

## 📚 Pinecone Resources

- **Dashboard:** https://app.pinecone.io/
- **Documentation:** https://docs.pinecone.io/
- **Python SDK:** https://docs.pinecone.io/guides/get-started/quickstart
- **Pricing:** https://www.pinecone.io/pricing/ (Free tier available!)

---

## 🔄 What Happens Next

Once Pinecone is set up, InfraFlow AI will use it for:

1. **Document Embeddings** - Store vector representations of uploaded documents
2. **Semantic Search** - Find relevant documents using natural language queries
3. **Similar Projects** - Find projects similar to a given project
4. **Compliance Matching** - Match projects to compliance requirements

---

## 💡 Pro Tips

### Use Environment-Specific Keys

For production, create separate API keys:

```bash
# .env.development
PINECONE_API_KEY=pcsk_dev_key_here

# .env.production
PINECONE_API_KEY=pcsk_prod_key_here
```

### Monitor Usage

Check your Pinecone dashboard regularly:
- Vector count
- Query performance
- API usage
- Stay within free tier limits

### Index Naming Convention

Use descriptive names:
- `infraflow-dev-documents` (development)
- `infraflow-prod-documents` (production)
- `infraflow-staging-documents` (staging)

---

## 🐛 Troubleshooting

### Error: "Invalid API Key"

**Solution:**
1. Verify the key in Pinecone dashboard
2. Copy-paste carefully (no extra spaces)
3. Try generating a new key
4. Check if your account is active

### Error: "Quota Exceeded"

**Solution:**
1. Check your usage in Pinecone dashboard
2. Delete unused indexes
3. Upgrade to paid plan if needed

### Error: "Index Already Exists"

**Solution:**
1. The setup script will ask if you want to recreate it
2. Or use the existing index (choose "no" when prompted)
3. Or manually delete in Pinecone console

---

## ✅ Quick Start Commands

```bash
# 1. Navigate to backend
cd /home/claude-user/ai-consults-platform/00-pivot/backend

# 2. Activate virtual environment
source venv/bin/activate

# 3. Update API key in ../.env
nano ../.env  # Add your real Pinecone API key

# 4. Run setup
python setup_pinecone.py

# 5. Verify setup
python -c "from pinecone import Pinecone; import os; from dotenv import load_dotenv; load_dotenv('../.env'); pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY')); print('Indexes:', [i.name for i in pc.list_indexes().indexes])"
```

---

## 📞 Need Help?

- **Pinecone Support:** https://support.pinecone.io/
- **InfraFlow AI Issues:** https://github.com/nawsaafa/infraflow-ai/issues
- **Documentation:** See `README.md` in backend directory

---

**Once you have a valid API key, run the setup script again!**
