#!/usr/bin/env python
"""Test GROQ API connection directly"""

import os
from dotenv import load_dotenv

print("\n" + "="*70)
print("GROQ API CONNECTION DIAGNOSTIC")
print("="*70 + "\n")

# Load environment
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

print(f"[1/5] Checking API key...")
if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)

if not api_key.startswith("gsk_"):
    print(f"⚠️  API key format suspicious: {api_key[:10]}...")
else:
    print(f"✅ API key found: {api_key[:20]}...")

try:
    print(f"\n[2/5] Importing ChatGroq...")
    from langchain_groq import ChatGroq
    print("✅ ChatGroq imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

try:
    print(f"\n[3/5] Creating ChatGroq instance...")
    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
        timeout=30,  # 30 second timeout
        max_retries=2
    )
    print("✅ ChatGroq instance created")
except Exception as e:
    print(f"❌ Error creating instance: {e}")
    exit(1)

try:
    print(f"\n[4/5] Testing API call (simple message)...")
    response = llm.invoke("Say 'HELLO' only")
    result = response.content if hasattr(response, 'content') else str(response)
    print(f"✅ API Response: {result[:100]}")
except Exception as e:
    print(f"❌ API call failed: {type(e).__name__}: {str(e)}")
    print(f"\nFull error: {e}")
    
    # More diagnostics
    print(f"\n[!] Checking internet connection...")
    try:
        import urllib.request
        urllib.request.urlopen("https://api.groq.com", timeout=5)
        print("✅ Can reach API endpoint")
    except Exception as net_e:
        print(f"❌ Cannot reach API: {net_e}")
    
    exit(1)

try:
    print(f"\n[5/5] Testing with question routing...")
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    prompt = ChatPromptTemplate.from_template("Answer briefly: {question}")
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"question": "What is 2+2?"})
    print(f"✅ Chain works: {result[:100]}")
except Exception as e:
    print(f"❌ Chain test failed: {e}")
    exit(1)

print("\n" + "="*70)
print("✅ ALL TESTS PASSED - GROQ API IS WORKING!")
print("="*70 + "\n")
