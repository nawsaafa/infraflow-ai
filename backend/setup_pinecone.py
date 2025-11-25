#!/usr/bin/env python3
"""
Pinecone Setup Script for InfraFlow AI
Initializes Pinecone indexes for document embeddings and semantic search
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import time

# Load environment variables
load_dotenv('../.env')

def initialize_pinecone():
    """Initialize Pinecone client with API key from environment"""
    api_key = os.getenv('PINECONE_API_KEY')

    if not api_key or api_key == 'your-pinecone-api-key-here':
        raise ValueError(
            "❌ PINECONE_API_KEY not found or is placeholder!\n"
            "Please add your Pinecone API key to .env file.\n"
            "Get your key at: https://app.pinecone.io/"
        )

    print("✅ Pinecone API key found")
    print(f"🔑 Key preview: {api_key[:20]}...")

    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    print("✅ Pinecone client initialized successfully")

    return pc

def create_document_index(pc, index_name="infraflow-documents"):
    """
    Create Pinecone index for document embeddings

    Specifications:
    - Dimension: 1536 (OpenAI Ada-002 embeddings)
    - Metric: Cosine similarity (best for semantic search)
    - Cloud: AWS (us-east-1 for low latency)
    """

    print(f"\n📊 Creating index: {index_name}")

    # Check if index already exists
    existing_indexes = pc.list_indexes()
    index_names = [idx.name for idx in existing_indexes.indexes]

    if index_name in index_names:
        print(f"⚠️  Index '{index_name}' already exists")
        response = input("Do you want to delete and recreate it? (yes/no): ")

        if response.lower() in ['yes', 'y']:
            print(f"🗑️  Deleting existing index '{index_name}'...")
            pc.delete_index(index_name)
            print("✅ Index deleted")
            time.sleep(5)  # Wait for deletion to complete
        else:
            print("✅ Using existing index")
            return pc.Index(index_name)

    # Create index with serverless specification
    print(f"🚀 Creating new index '{index_name}'...")

    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI Ada-002 embedding dimension
        metric='cosine',  # Cosine similarity for semantic search
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'  # Change to your preferred region
        )
    )

    print("⏳ Waiting for index to be ready...")

    # Wait for index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

    print(f"✅ Index '{index_name}' created and ready!")

    # Get index stats
    index = pc.Index(index_name)
    stats = index.describe_index_stats()
    print(f"📊 Index stats: {stats}")

    return index

def create_financial_index(pc, index_name="infraflow-financial"):
    """
    Create Pinecone index for financial model embeddings

    Specifications:
    - Dimension: 768 (smaller, optimized for financial data)
    - Metric: Euclidean (better for numerical similarity)
    """

    print(f"\n📊 Creating index: {index_name}")

    # Check if index already exists
    existing_indexes = pc.list_indexes()
    index_names = [idx.name for idx in existing_indexes.indexes]

    if index_name in index_names:
        print(f"⚠️  Index '{index_name}' already exists")
        response = input("Do you want to delete and recreate it? (yes/no): ")

        if response.lower() in ['yes', 'y']:
            print(f"🗑️  Deleting existing index '{index_name}'...")
            pc.delete_index(index_name)
            print("✅ Index deleted")
            time.sleep(5)
        else:
            print("✅ Using existing index")
            return pc.Index(index_name)

    print(f"🚀 Creating new index '{index_name}'...")

    pc.create_index(
        name=index_name,
        dimension=768,  # Smaller dimension for financial data
        metric='euclidean',  # Better for numerical similarity
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

    print("⏳ Waiting for index to be ready...")

    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

    print(f"✅ Index '{index_name}' created and ready!")

    index = pc.Index(index_name)
    stats = index.describe_index_stats()
    print(f"📊 Index stats: {stats}")

    return index

def test_index(index, index_name):
    """Test the index with a sample vector"""

    print(f"\n🧪 Testing index: {index_name}")

    # Create a test vector
    import random
    dimension = index.describe_index_stats()['dimension']
    test_vector = [random.random() for _ in range(dimension)]

    # Upsert test vector
    print("📤 Upserting test vector...")
    index.upsert(
        vectors=[
            {
                "id": "test-vector-1",
                "values": test_vector,
                "metadata": {
                    "text": "Test document for InfraFlow AI",
                    "project_id": "test-project-001",
                    "document_type": "test",
                    "created_at": "2024-01-01T00:00:00Z"
                }
            }
        ]
    )

    print("⏳ Waiting for vector to be indexed...")
    time.sleep(2)

    # Query the index
    print("🔍 Querying index...")
    results = index.query(
        vector=test_vector,
        top_k=1,
        include_metadata=True
    )

    if results['matches']:
        print("✅ Index is working correctly!")
        print(f"📊 Query results: {results}")

        # Clean up test vector
        print("🗑️  Cleaning up test vector...")
        index.delete(ids=["test-vector-1"])
        print("✅ Test vector deleted")
    else:
        print("❌ Index test failed - no results returned")

def display_summary(pc):
    """Display summary of Pinecone setup"""

    print("\n" + "="*60)
    print("📊 PINECONE SETUP SUMMARY")
    print("="*60)

    indexes = pc.list_indexes()

    print(f"\n✅ Total indexes: {len(indexes.indexes)}")

    for idx in indexes.indexes:
        print(f"\n📊 Index: {idx.name}")
        print(f"   - Dimension: {idx.dimension}")
        print(f"   - Metric: {idx.metric}")
        print(f"   - Cloud: {idx.spec.serverless.cloud}")
        print(f"   - Region: {idx.spec.serverless.region}")
        print(f"   - Status: Ready ✅")

    print("\n" + "="*60)
    print("🎉 Pinecone setup complete!")
    print("="*60)

    print("\n📝 Next steps:")
    print("1. Update PINECONE_INDEX_NAME in .env (default: infraflow-documents)")
    print("2. Start the backend: cd backend && uvicorn app.main:app --reload")
    print("3. Upload documents to test embeddings")
    print("4. Monitor usage at: https://app.pinecone.io/")

def main():
    """Main setup function"""

    print("="*60)
    print("🌲 INFRAFLOW AI - PINECONE SETUP")
    print("="*60)

    try:
        # Step 1: Initialize Pinecone
        print("\n📍 Step 1: Initialize Pinecone client")
        pc = initialize_pinecone()

        # Step 2: Create document embeddings index
        print("\n📍 Step 2: Create document embeddings index")
        doc_index = create_document_index(pc, "infraflow-documents")

        # Step 3: Test document index
        test_index(doc_index, "infraflow-documents")

        # Step 4: Create financial models index (optional)
        print("\n📍 Step 3: Create financial models index (optional)")
        create_financial = input("Create financial models index? (yes/no): ")

        if create_financial.lower() in ['yes', 'y']:
            fin_index = create_financial_index(pc, "infraflow-financial")
            test_index(fin_index, "infraflow-financial")
        else:
            print("⏭️  Skipping financial index creation")

        # Step 5: Display summary
        display_summary(pc)

        print("\n✅ All done! Pinecone is ready to use.")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Check your PINECONE_API_KEY in .env")
        print("2. Ensure you have an active Pinecone account")
        print("3. Visit https://docs.pinecone.io/ for help")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
