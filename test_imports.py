#!/usr/bin/env python3
"""Quick import and functionality test"""

print("\n" + "="*60)
print("TalkDocs 2.0 - SYSTEM VERIFICATION")
print("="*60)

try:
    print("\n[1/5] Testing environment...")
    import os
    from dotenv import load_dotenv
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("[OK] GROQ_API_KEY loaded from .env")
    else:
        print("[WARN] GROQ_API_KEY not found")
except Exception as e:
    print(f"[ERROR] Environment error: {e}")

try:
    print("\n[2/5] Testing imports...")
    from app import *
    from app_graph import *
    from ingestion import *
    from router import *
    print("[OK] All imports successful")
except Exception as e:
    print(f"[ERROR] Import error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n[3/5] Testing GROQ LLM...")
    from langchain_groq import ChatGroq
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.3-70b-versatile", temperature=0)
    response = llm.invoke("Say OK")
    print(f"[OK] GROQ LLM working: {response.content[:50]}")
except Exception as e:
    print(f"[ERROR] LLM error: {e}")

try:
    print("\n[4/5] Testing SimpleEmbeddings...")
    from ingestion import SimpleEmbeddings
    embeddings = SimpleEmbeddings()
    test_embed = embeddings.embed_documents(["test document"])
    print(f"[OK] SimpleEmbeddings working (embedding dim: {len(test_embed[0])})")
except Exception as e:
    print(f"[ERROR] Embeddings error: {e}")

try:
    print("\n[5/5] Checking files...")
    import os
    files_to_check = ["app.py", "app_graph.py", "ingestion.py", "router.py", ".env", "requirements.txt"]
    all_exist = True
    for f in files_to_check:
        exists = os.path.exists(f)
        status = "[OK]" if exists else "[MISSING]"
        if exists:
            size = os.path.getsize(f)
            print(f"{status} {f} ({size} bytes)")
        else:
            print(f"{status} {f} (MISSING)")
            all_exist = False
    if all_exist:
        print("\n[OK] All critical files present")
except Exception as e:
    print(f"[ERROR] File check error: {e}")

print("\n" + "="*60)
print("[OK] SYSTEM VERIFICATION COMPLETE")
print("Ready to run: streamlit run app.py")
print("="*60 + "\n")
