"""
FastAPI application for Knowledge-base Search Engine with RAG capabilities.
"""
import chromadb
from chromadb.config import Settings
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import logging
from pathlib import Path

from ingestion import DocumentIngestion
from retriever import VectorRetriever
from rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Knowledge-base Search Engine",
    description="RAG-powered document search and question answering system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW COMPONENT INITIALIZATION LOGIC ---

# 1. Create a single, shared ChromaDB client
logger.info("Initializing shared ChromaDB client...")
chroma_client = chromadb.PersistentClient(
    path="./chroma_db", 
    settings=Settings(anonymized_telemetry=False)
)

# 2. Get or create the shared collection
collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    metadata={"description": "Document chunks for RAG system"}
)
logger.info(f"Connected to collection: {collection.name}")

# 3. Initialize components, passing the shared objects to them
ingestion = DocumentIngestion(collection=collection)
retriever = VectorRetriever(client=chroma_client, collection=collection)
rag_pipeline = RAGPipeline(retriever)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Knowledge-base Search Engine API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "query": "/query",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload and ingest multiple documents (PDF/TXT).
    
    Args:
        files: List of uploaded files
        
    Returns:
        JSON response with ingestion status
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        results = []
        
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.txt')):
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": "Only PDF and TXT files are supported"
                })
                continue
            
            try:
                # Save uploaded file
                file_path = UPLOAD_DIR / file.filename
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                # Ingest document
                logger.info(f"Processing file: {file.filename}")
                chunks = ingestion.process_document(str(file_path))
                
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "chunks_created": len(chunks),
                    "message": f"Successfully processed {len(chunks)} chunks"
                })
                
                # Clean up uploaded file
                os.remove(file_path)
                
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {str(e)}")
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": str(e)
                })
        
        return JSONResponse(content={
            "message": "Document processing completed",
            "results": results
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/query")
async def query_documents(
    question: str = Form(...),
    top_k: int = Form(5),
    include_sources: bool = Form(True)
):
    """
    Query the knowledge base and get RAG-generated answers.
    
    Args:
        question: User's question
        top_k: Number of top relevant chunks to retrieve
        include_sources: Whether to include source chunks
        
    Returns:
        JSON response with answer and optional sources
    """
    try:
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing query: {question}")
        
        # Get RAG response
        response = rag_pipeline.answer_query(
            question=question,
            top_k=top_k,
            include_sources=include_sources
        )
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get database statistics."""
    try:
        stats = retriever.get_collection_stats()
        return JSONResponse(content=stats)
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.delete("/clear-database")
async def clear_database():
    """Clear all data from the database."""
    try:
        # Pass the 'ingestion' instance to the clear_collection method
        result = retriever.clear_collection(ingestion_instance=ingestion)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Clear database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

