#!/usr/bin/env python
"""Quick check if packages are installed"""
import sys

packages = ['dotenv', 'langchain_groq', 'streamlit', 'faiss', 'langchain_core', 'langgraph']
missing = []

for pkg in packages:
    try:
        __import__(pkg)
        print(f"[OK] {pkg}")
    except ImportError:
        print(f"[MISSING] {pkg}")
        missing.append(pkg)

if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)
else:
    print("\n[SUCCESS] All packages installed!")
    sys.exit(0)
