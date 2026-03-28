#!/usr/bin/env python
"""
VS Code Python Interpreter Fix
Ensures VS Code is using the correct Python environment for Pylance
"""

import json
import os
import sys
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("  VS CODE PYTHON ENVIRONMENT SETUP")
    print("="*70 + "\n")
    
    # Get workspace root
    workspace_root = Path(__file__).parent.absolute()
    venv_python = workspace_root / ".venv" / "Scripts" / "python.exe"
    vscode_dir = workspace_root / ".vscode"
    
    print(f"📁 Workspace: {workspace_root}")
    print(f"🐍 venv Python: {venv_python}")
    print(f"⚙️  VS Code config: {vscode_dir}\n")
    
    # Check if venv exists
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print(f"   Expected at: {venv_python}")
        print("\n   To fix, run:")
        print("   python -m venv .venv")
        print("   .venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ Virtual environment found")
    
    # Check .vscode/settings.json
    settings_file = vscode_dir / "settings.json"
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                python_path = settings.get("python.defaultInterpreterPath", "")
                if "/.venv/" in python_path or "\\.venv\\" in python_path:
                    print("✅ VS Code settings.json configured correctly")
                else:
                    print("⚠️  VS Code settings.json exists but Python path may be incorrect")
        except json.JSONDecodeError:
            print("⚠️  VS Code settings.json is malformed")
    else:
        print("⚠️  VS Code settings.json not found")
    
    # Check launch.json
    launch_file = vscode_dir / "launch.json"
    if launch_file.exists():
        print("✅ VS Code launch.json configured")
    else:
        print("⚠️  VS Code launch.json not found")
    
    # Check required packages
    print("\n📦 Checking packages in venv...")
    required_packages = [
        'dotenv', 'langchain_groq', 'streamlit', 'faiss', 
        'langchain_core', 'langgraph', 'pypdf'
    ]
    
    all_present = True
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"   ✅ {pkg}")
        except ImportError:
            print(f"   ❌ {pkg} - MISSING")
            all_present = False
    
    if not all_present:
        print("\n❌ Some packages are missing!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Check .env file
    print("\n🔐 Checking environment variables...")
    env_file = workspace_root / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'GROQ_API_KEY=' in content:
                if 'gsk_' in content:
                    print("   ✅ .env file found with GROQ_API_KEY")
                else:
                    print("   ⚠️  .env file found but GROQ_API_KEY not set")
                    print("      Get a key from: https://console.groq.com")
    else:
        print("   ⚠️  .env file not found")
        print("      Copy .env.example to .env and add your GROQ_API_KEY")
    
    # Success message
    print("\n" + "="*70)
    print("  ✅ SETUP COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("  1. Reload VS Code (Ctrl+Shift+P → Developer: Reload Window)")
    print("  2. Select Python Interpreter (Ctrl+Shift+P → Python: Select Interpreter)")
    print("     → Choose: .venv/Scripts/python.exe")
    print("  3. Restart Pylance (Ctrl+Shift+P → Pylance: Restart Language Server)")
    print("  4. Run: streamlit run app.py\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
