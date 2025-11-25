#!/usr/bin/env python3
"""
Test database and API connections for InfraFlow AI aggregation system.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv('/home/claude-user/ai-consults-platform/00-pivot/.env')

def test_postgresql():
    """Test PostgreSQL connection."""
    print("\n" + "=" * 80)
    print("Testing PostgreSQL Connection")
    print("=" * 80)

    try:
        import psycopg2
        database_url = os.getenv('LOCAL_DATABASE_URL', 'postgresql://infraflow_user:infraflow_dev_password_change_me@localhost:15432/infraflow_db')

        print(f"Database URL: {database_url.split('@')[1] if '@' in database_url else database_url}")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {version.split(',')[0]}")

        # Check tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\n📊 Available tables: {len(tables)}")
        for table in tables[:10]:
            print(f"   • {table[0]}")
        if len(tables) > 10:
            print(f"   ... and {len(tables) - 10} more")

        # Check record counts
        cursor.execute("SELECT COUNT(*) FROM projects;")
        project_count = cursor.fetchone()[0]
        print(f"\n📈 Current data:")
        print(f"   • Projects: {project_count}")

        cursor.close()
        conn.close()
        return True

    except ImportError:
        print("❌ psycopg2 not installed")
        print("   Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if PostgreSQL is running (docker ps)")
        print("   2. Verify DATABASE_URL in .env")
        print("   3. Check port 15432 is accessible")
        return False


def test_openai():
    """Test OpenAI API connection."""
    print("\n" + "=" * 80)
    print("Testing OpenAI API Connection")
    print("=" * 80)

    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False

        print(f"API Key: {api_key[:10]}...{api_key[-5:]}")

        # Test embedding generation
        openai.api_key = api_key
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input="Test embedding"
        )

        embedding = response.data[0].embedding
        print(f"✅ Connected successfully!")
        print(f"Embedding dimension: {len(embedding)}")
        print(f"Model: text-embedding-ada-002")
        return True

    except ImportError:
        print("❌ openai library not installed")
        print("   Install with: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Verify OPENAI_API_KEY in .env")
        print("   2. Check API key is valid and has credits")
        print("   3. Check internet connectivity")
        return False


def test_pinecone():
    """Test Pinecone connection."""
    print("\n" + "=" * 80)
    print("Testing Pinecone Connection")
    print("=" * 80)

    try:
        from pinecone import Pinecone
        api_key = os.getenv('PINECONE_API_KEY')
        index_name = os.getenv('PINECONE_INDEX_NAME', 'infraflow-documents')

        if not api_key:
            print("❌ PINECONE_API_KEY not found in environment")
            return False

        print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
        print(f"Index Name: {index_name}")

        pc = Pinecone(api_key=api_key)

        # List indexes
        indexes = pc.list_indexes()
        index_names = [idx.name for idx in indexes]

        print(f"✅ Connected successfully!")
        print(f"Available indexes: {len(index_names)}")
        for idx_name in index_names:
            print(f"   • {idx_name}")

        # Check if target index exists
        if index_name in index_names:
            print(f"\n✅ Target index '{index_name}' exists")

            # Get index stats
            index = pc.Index(index_name)
            stats = index.describe_index_stats()
            print(f"   • Total vectors: {stats.total_vector_count}")
            print(f"   • Dimension: {stats.dimension}")
        else:
            print(f"\n⚠️  Target index '{index_name}' not found")
            print("   It will be created automatically when needed")

        return True

    except ImportError:
        print("❌ pinecone library not installed")
        print("   Install with: pip install pinecone-client")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Verify PINECONE_API_KEY in .env")
        print("   2. Check API key is valid")
        print("   3. Check internet connectivity")
        return False


def main():
    """Run all connection tests."""
    print("\n" + "=" * 80)
    print("InfraFlow AI - Connection Tests")
    print("=" * 80)

    results = {
        'PostgreSQL': test_postgresql(),
        'OpenAI': test_openai(),
        'Pinecone': test_pinecone()
    }

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    all_passed = all(results.values())

    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {service}")

    if all_passed:
        print("\n✨ All connections successful! Ready to run aggregation.")
        print("\n💡 Next steps:")
        print("   1. Check research data: python check_research_status.py")
        print("   2. Run aggregation: python aggregate_and_populate.py")
    else:
        print("\n⚠️  Some connections failed. Please fix issues before running aggregation.")

    print("=" * 80)

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
