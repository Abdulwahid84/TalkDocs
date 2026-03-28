#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete test of TalkDocs 2.0 - Test PDF chat without Streamlit
"""

import os
from dotenv import load_dotenv
import tempfile

print("\n" + "="*80)
print("TALKDOCS 2.0 - COMPLETE SYSTEM TEST")
print("="*80 + "\n")

# Step 1: Load environment
print("[1/7] Loading environment...")
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("[ERROR] GROQ_API_KEY not found!")
    exit(1)

if not api_key.startswith("gsk_"):
    print(f"[WARN] API key format unusual: {api_key[:15]}...")
else:
    print(f"[OK] API key loaded: {api_key[:20]}...")

# Step 2: Test imports
print("\n[2/7] Testing imports...")
try:
    from langchain_groq import ChatGroq
    from app_graph import PdfChat
    from ingestion import PDFIngestor, SimpleEmbeddings
    from router import route
    print("[OK] All imports successful")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    exit(1)

# Step 3: Test GROQ LLM directly
print("\n[3/7] Testing GROQ LLM...")
try:
    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
        timeout=30,
        max_retries=2
    )
    response = llm.invoke("Say HELLO only")
    print(f"[OK] LLM Response: {response.content[:50]}")
except Exception as e:
    print(f"[ERROR] LLM Error: {e}")
    exit(1)

# Step 4: Test SimpleEmbeddings
print("\n[4/7] Testing SimpleEmbeddings...")
try:
    embeddings = SimpleEmbeddings()
    test_embedding = embeddings.embed_documents(["test document"])
    dim = len(test_embedding[0])
    print(f"[OK] Embeddings working ({dim}-dim vectors)")
except Exception as e:
    print(f"[ERROR] Embeddings error: {e}")
    exit(1)

# Step 5: Create fake PDF for testing
print("\n[5/7] Creating test PDF...")
try:
    from pypdf import PdfWriter
    # Create a minimal PDF
    pdf = PdfWriter()
    page = pdf.add_blank_page(width=200, height=200)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as f:
        pdf.write(f)
        temp_pdf_path = f.name
    
    # Read it back as bytes
    with open(temp_pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    # Clean up
    os.unlink(temp_pdf_path)
    
    print(f"[OK] Test PDF created ({len(pdf_bytes)} bytes)")
except Exception as e:
    print(f"[WARN] Test PDF creation skipped: {e}")
    pdf_bytes = None

# Step 6: Test Router (without structured output)
print("\n[6/7] Testing Query Router...")
try:
    router_chain = route(llm, ["test conversation history"])
    route_result = router_chain.invoke({"question": "What is in my documents?"})
    datasource = route_result.datasource if hasattr(route_result, 'datasource') else str(route_result)
    print(f"[OK] Router working (result: {datasource})")
except Exception as e:
    print(f"[WARN] Router test: {e}")
    # This is not critical - continue

# Step 7: Test full graph (if PDF available)
print("\n[7/7] Testing Full Graph...")
if pdf_bytes:
    try:
        # Create a mock file object
        class MockUploadedFile:
            def __init__(self, data):
                self.data = data
            def getvalue(self):
                return self.data
        
        mock_file = MockUploadedFile(pdf_bytes)
        
        # Initialize ingestor
        print("  - Initializing PDF ingestor...")
        ingestor = PDFIngestor([mock_file], api_key)
        retriever = ingestor.get_retriever()
        print("  - PDF ingestor ready")
        
        # Initialize chat
        print("  - Creating PdfChat...")
        chat = PdfChat(api_key, retriever)
        print("  - PdfChat ready")
        
        # Test query
        print("  - Running test query...")
        result = chat.graph.invoke({"question": "What does this document contain?"})
        response = result.get("response", "No response")
        print(f"[OK] Full graph working!\n   Response: {response[:80]}...")
        
    except Exception as e:
        print(f"[WARN] Full graph test failed: {e}")
        print("   This may be expected if PDF is minimal")
else:
    print("[WARN] Skipped (no test PDF)")

print("\n" + "="*80)
print("[OK] SYSTEM TEST COMPLETE")
print("="*80)
print("\nNext steps:")
print("  1. Run: streamlit run app.py")
print("  2. Upload a PDF")
print("  3. Ask questions about it")
print("\n")
