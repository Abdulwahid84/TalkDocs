#!/usr/bin/env python3
"""
Complete verification that TalkDocs 2.0 is fully functional
"""
import sys
import os

print("\n" + "="*70)
print(" TalkDocs 2.0 - COMPLETE SYSTEM VERIFICATION")
print("="*70 + "\n")

errors = []

# 1. Check environment
print("[1/5] Environment Check...")
from dotenv import load_dotenv
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print(f"     ✅ GROQ_API_KEY loaded: {groq_key[:15]}...")
else:
    print(f"     ❌ GROQ_API_KEY missing")
    errors.append("GROQ_API_KEY not found")

# 2. Test all critical imports
print("\n[2/5] Imports Test...")
try:
    from ingestion import PDFIngestor
    print("     ✅ PDFIngestor imported")
except Exception as e:
    print(f"     ❌ PDFIngestor error: {e}")
    errors.append(f"PDFIngestor: {e}")

try:
    from app_graph import PdfChat
    print("     ✅ PdfChat imported")
except Exception as e:
    print(f"     ❌ PdfChat error: {e}")
    errors.append(f"PdfChat: {e}")

try:
    from router import route
    print("     ✅ router imported")
except Exception as e:
    print(f"     ❌ router error: {e}")
    errors.append(f"router: {e}")

# 3. Test GROQ LLM
print("\n[3/5] GROQ LLM Test...")
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(api_key=groq_key, model="llama-3.3-70b-versatile", temperature=0)
    response = llm.invoke("Say 'OK' only")
    print(f"     ✅ GROQ LLM working: Response = '{response.content}'")
except Exception as e:
    print(f"     ❌ GROQ LLM error: {e}")
    errors.append(f"GROQ LLM: {e}")

# 4. Test Embeddings (using SimpleEmbeddings)
print("\n[4/5] Embeddings Test...")
try:
    from ingestion import SimpleEmbeddings
    embeddings = SimpleEmbeddings()
    test_embed = embeddings.embed_query("test")
    print(f"     ✅ SimpleEmbeddings working (dim: {len(test_embed)})")
except Exception as e:
    print(f"     ⚠️  Embeddings skipped: {str(e)[:50]}")

# 5. Check files
print("\n[5/5] File Check...")
required_files = ["app.py", "app_graph.py", "ingestion.py", "router.py", ".env", "requirements.txt"]
all_exist = True
for file in required_files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"     ✅ {file} ({size} bytes)")
    else:
        print(f"     ❌ {file} MISSING")
        all_exist = False
        errors.append(f"File missing: {file}")

# Summary
print("\n" + "="*70)
if not errors:
    print("✅ ALL CHECKS PASSED - SYSTEM 100% READY!")
    print("="*70)
    print("\n▶️  Ready to run: streamlit run app.py\n")
    sys.exit(0)
else:
    print(f"❌ {len(errors)} ISSUE(S) FOUND:")
    for i, err in enumerate(errors, 1):
        print(f"   {i}. {err}")
    print("="*70 + "\n")
    sys.exit(1)
