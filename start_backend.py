#!/usr/bin/env python3
"""
Startup script for the Knowledge-base Search Engine backend.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10+."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        print(f"   Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import chromadb
        import sentence_transformers
        import openai
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install dependencies with: pip install -r backend/requirements.txt")
        return False

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = [
        "backend/uploads",
        "backend/chroma_db",
        "backend/logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created {directory}")

def start_server():
    """Start the FastAPI server."""
    print("🚀 Starting Knowledge-base Search Engine...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir("backend")
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    except FileNotFoundError:
        print("❌ uvicorn not found. Install with: pip install uvicorn")
        return False
    
    return True

def main():
    """Main startup function."""
    print("🎯 Knowledge-base Search Engine Startup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create directories
    create_directories()
    
    # Start server
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    start_server()

if __name__ == "__main__":
    main()



