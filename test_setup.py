#!/usr/bin/env python3
"""
Test script to verify all imports and configuration are working
"""

print("=" * 60)
print("TalkDocs 2.0 - Testing Setup")
print("=" * 60)

# Test 1: Check environment variables
print("\n[1] Checking environment variables...")
import os
from dotenv import load_dotenv

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print("✅ GROQ_API_KEY found:", groq_key[:10] + "..." if len(groq_key) > 10 else groq_key)
else:
    print("❌ GROQ_API_KEY not found in .env file")
    exit(1)

# Test 2: Check imports
print("\n[2] Checking critical imports...")
try:
    from langchain_groq import ChatGroq
    print("✅ langchain_groq imported successfully")
except Exception as e:
    print(f"❌ Error importing langchain_groq: {e}")
    exit(1)

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("✅ HuggingFaceEmbeddings imported successfully")
except Exception as e:
    print(f"❌ Error importing HuggingFaceEmbeddings: {e}")
    exit(1)

try:
    from langgraph.graph import StateGraph
    print("✅ langgraph imported successfully")
except Exception as e:
    print(f"❌ Error importing langgraph: {e}")
    exit(1)

try:
    from langchain_community.vectorstores import FAISS
    print("✅ FAISS imported successfully")
except Exception as e:
    print(f"❌ Error importing FAISS: {e}")
    exit(1)

# Test 3: Test LLM initialization
print("\n[3] Testing GROQ LLM initialization...")
try:
    llm = ChatGroq(
        api_key=groq_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    print("✅ ChatGroq initialized successfully")
    print(f"   Model: llama-3.3-70b-versatile")
    print(f"   Temperature: 0")
except Exception as e:
    print(f"❌ Error initializing ChatGroq: {e}")
    exit(1)

# Test 4: Test simple LLM call
print("\n[4] Testing GROQ LLM call...")
try:
    response = llm.invoke("Say 'Setup test successful!' in one sentence only")
    print("✅ LLM call successful")
    print(f"   Response: {response.content}")
except Exception as e:
    print(f"❌ Error calling LLM: {e}")
    exit(1)

# Test 5: Test embeddings
print("\n[5] Testing HuggingFace embeddings...")
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder="./hf_cache"
    )
    test_embedding = embeddings.embed_query("Hello world")
    print("✅ HuggingFace embeddings initialized and working")
    print(f"   Embedding dimension: {len(test_embedding)}")
except Exception as e:
    print(f"❌ Error with embeddings: {e}")
    exit(1)

# Test 6: Check required files
print("\n[6] Checking required files...")
required_files = ["app.py", "app_graph.py", "ingestion.py", "router.py", "requirements.txt", ".env", "media/cover.jpg"]
for file in required_files:
    path = os.path.join(".", file)
    if os.path.exists(path):
        print(f"✅ {file} found")
    else:
        print(f"⚠️  {file} not found (may be needed)")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - System is ready to run!")
print("=" * 60)
print("\nTo run the application:")
print("  streamlit run app.py")
print("=" * 60)
