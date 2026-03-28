#!/usr/bin/env python3
"""
Quick verification that TalkDocs 2.0 is ready to run
"""
import sys

print("\n" + "="*60)
print("TalkDocs 2.0 - Quick Verification")
print("="*60 + "\n")

# Test 1: Environment
print("[✓] Step 1: Checking Environment...")
import os
from dotenv import load_dotenv
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print(f"    GROQ API Key: Found ✅")
else:
    print(f"    GROQ API Key: NOT FOUND ❌")
    sys.exit(1)

# Test 2: Core imports
print("\n[✓] Step 2: Checking Core Imports...")
try:
    from langchain_groq import ChatGroq
    print("    langchain_groq: OK ✅")
    from langgraph.graph import StateGraph
    print("    langgraph: OK ✅")
    from langchain_community.vectorstores import FAISS
    print("    FAISS: OK ✅")
    from langchain.prompts import PromptTemplate
    print("    langchain: OK ✅")
except Exception as e:
    print(f"    Import Error: {e} ❌")
    sys.exit(1)

# Test 3: GROQ Connection
print("\n[✓] Step 3: Testing GROQ Connection...")
try:
    llm = ChatGroq(api_key=groq_key, model="llama-3.3-70b-versatile", temperature=0)
    response = llm.invoke("Say 'Ready!' in one word only")
    print(f"    LLM Response: {response.content} ✅")
except Exception as e:
    print(f"    GROQ Error: {e} ❌")
    sys.exit(1)

# Test 4: File check
print("\n[✓] Step 4: Checking Required Files...")
files_ok = True
required = ["app.py", "app_graph.py", "ingestion.py", "router.py", ".env"]
for f in required:
    if os.path.exists(f):
        print(f"    {f}: Found ✅")
    else:
        print(f"    {f}: MISSING ❌")
        files_ok = False

if not files_ok:
    sys.exit(1)

# Final verdict
print("\n" + "="*60)
print("✅ ALL CHECKS PASSED - READY TO RUN!")
print("="*60)
print("\nRun: streamlit run app.py")
print("="*60 + "\n")
