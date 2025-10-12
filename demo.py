#!/usr/bin/env python3
"""
Demo script for the Knowledge-base Search Engine.
Shows how to use the API endpoints for document upload and querying.
"""

import requests
import time
import json
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
DEMO_DOCUMENTS = [
    "sample_document.txt",  # We'll create this
    "sample_pdf.pdf"        # We'll create this
]

def create_sample_documents():
    """Create sample documents for demonstration."""
    print("📄 Creating sample documents...")
    
    # Create sample text document
    sample_text = """
    Artificial Intelligence and Machine Learning

    Artificial Intelligence (AI) is a broad field of computer science focused on creating 
    intelligent machines that can perform tasks that typically require human intelligence. 
    These tasks include learning, reasoning, problem-solving, perception, and language understanding.

    Machine Learning (ML) is a subset of AI that focuses on the development of algorithms 
    and statistical models that enable computer systems to improve their performance on a 
    specific task through experience, without being explicitly programmed.

    Key Concepts in Machine Learning:

    1. Supervised Learning: Learning with labeled training data
       - Classification: Predicting discrete categories
       - Regression: Predicting continuous values
       - Examples: Email spam detection, house price prediction

    2. Unsupervised Learning: Finding patterns in data without labels
       - Clustering: Grouping similar data points
       - Dimensionality reduction: Reducing data complexity
       - Examples: Customer segmentation, data visualization

    3. Deep Learning: Neural networks with multiple layers
       - Convolutional Neural Networks (CNNs): Image processing
       - Recurrent Neural Networks (RNNs): Sequence data
       - Transformers: Natural language processing

    Applications of AI and ML:

    - Healthcare: Medical diagnosis, drug discovery, personalized treatment
    - Finance: Fraud detection, algorithmic trading, risk assessment
    - Transportation: Autonomous vehicles, route optimization
    - Technology: Search engines, recommendation systems, virtual assistants
    - Manufacturing: Quality control, predictive maintenance, supply chain optimization

    Benefits of AI and ML:

    1. Automation: Reduces manual work and human error
    2. Scalability: Can process large amounts of data quickly
    3. Personalization: Provides tailored experiences and recommendations
    4. Efficiency: Optimizes processes and resource utilization
    5. Innovation: Enables new products and services

    Challenges and Considerations:

    - Data Quality: Requires clean, relevant, and sufficient data
    - Bias: Can perpetuate or amplify existing biases
    - Interpretability: Some models are "black boxes"
    - Privacy: Concerns about data collection and usage
    - Ethics: Ensuring fair and responsible AI deployment

    Future of AI and ML:

    The field continues to evolve rapidly with advances in:
    - Large Language Models (LLMs) like GPT and BERT
    - Computer Vision and image recognition
    - Reinforcement Learning for decision-making
    - Edge AI for real-time processing
    - Explainable AI for better transparency

    As AI and ML technologies become more sophisticated and accessible, 
    they will continue to transform industries and create new opportunities 
    for innovation and growth.
    """
    
    with open("sample_document.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print("✅ Created sample_document.txt")
    
    # Note: For PDF demo, you would need to create a PDF file
    # For this demo, we'll just show the text document upload
    print("ℹ️  Note: PDF demo requires a PDF file. Using text document for demo.")

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("💡 Make sure the backend is running: python backend/app.py")
        return False

def upload_documents():
    """Upload sample documents to the API."""
    print("\n📤 Uploading documents...")
    
    # Check if sample document exists
    if not Path("sample_document.txt").exists():
        print("❌ Sample document not found. Creating it first...")
        create_sample_documents()
    
    try:
        # Upload the text document
        with open("sample_document.txt", "rb") as f:
            files = [("files", ("sample_document.txt", f, "text/plain"))]
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document uploaded successfully!")
            for file_result in result["results"]:
                print(f"   📄 {file_result['filename']}: {file_result['message']}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def get_database_stats():
    """Get database statistics."""
    print("\n📊 Getting database statistics...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Database statistics:")
            print(f"   📄 Total chunks: {stats.get('total_chunks', 0)}")
            print(f"   🗄️  Collection: {stats.get('collection_name', 'N/A')}")
            print(f"   ✅ Status: {stats.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return False

def ask_questions():
    """Ask sample questions to demonstrate the RAG system."""
    print("\n❓ Asking questions to demonstrate RAG...")
    
    sample_questions = [
        "What is artificial intelligence?",
        "What are the different types of machine learning?",
        "What are the benefits of AI and ML?",
        "What challenges does AI face?",
        "What are some applications of machine learning?"
    ]
    
    for i, question in enumerate(sample_questions, 1):
        print(f"\n🔍 Question {i}: {question}")
        
        try:
            # Ask the question
            data = {
                "question": question,
                "top_k": 3,
                "include_sources": True
            }
            
            response = requests.post(f"{API_BASE_URL}/query", data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"🤖 Answer: {result['answer'][:200]}...")
                print(f"📚 Sources: {result['num_sources']} documents")
                
                if result.get('sources'):
                    print("   📄 Source files:")
                    for source in result['sources'][:2]:  # Show first 2 sources
                        print(f"      - {source['filename']} (similarity: {source['similarity_score']:.2f})")
            else:
                print(f"❌ Query failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Query error: {e}")
        
        # Small delay between questions
        time.sleep(1)

def cleanup():
    """Clean up demo files."""
    print("\n🧹 Cleaning up demo files...")
    try:
        if Path("sample_document.txt").exists():
            Path("sample_document.txt").unlink()
            print("✅ Removed sample_document.txt")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run the complete demo."""
    print("🚀 Knowledge-base Search Engine Demo")
    print("=" * 50)
    
    # Step 1: Check API health
    if not check_api_health():
        return
    
    # Step 2: Create sample documents
    create_sample_documents()
    
    # Step 3: Upload documents
    if not upload_documents():
        print("❌ Demo stopped due to upload failure")
        return
    
    # Step 4: Get database stats
    get_database_stats()
    
    # Step 5: Ask questions
    ask_questions()
    
    # Step 6: Cleanup
    cleanup()
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Next steps:")
    print("   - Try the React frontend: cd frontend && npm start")
    print("   - Upload your own documents via the API")
    print("   - Ask more specific questions about your content")

if __name__ == "__main__":
    main()



