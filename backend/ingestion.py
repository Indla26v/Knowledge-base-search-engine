"""
Document ingestion pipeline for processing PDF and text files.
Handles text extraction, chunking, and embedding generation.
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import hashlib

logger = logging.getLogger(__name__)

class DocumentIngestion:
    """Handles document processing, chunking, and embedding storage."""
    
    def __init__(self,
                 collection: chromadb.Collection,
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 embedding_model: str = "all-MiniLM-L6-v2"):
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        self.collection = collection
        
        logger.info("Document ingestion pipeline initialized with shared collection")
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            logger.info(f"Extracted text from PDF: {file_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting PDF text from {file_path}: {str(e)}")
            raise
    
    def extract_text_from_txt(self, file_path: str) -> str:
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            logger.info(f"Extracted text from TXT: {file_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error reading TXT file {file_path}: {str(e)}")
            raise
    
    def extract_text(self, file_path: str) -> str:
        
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    def create_chunks(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        # Split text into chunks
        text_chunks = self.text_splitter.split_text(text)
        
        chunks = []
        for i, chunk_text in enumerate(text_chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_index": i,
                "chunk_size": len(chunk_text),
                "total_chunks": len(text_chunks)
            })
            
            chunks.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })
        
        logger.info(f"Created {len(chunks)} chunks from document")
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def store_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Store chunks and embeddings in ChromaDB.
        
        Args:
            chunks: List of chunk dictionaries
            embeddings: List of embedding vectors
        """
        try:
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = hashlib.md5(
                    f"{chunk['metadata']['filename']}_{chunk['metadata']['chunk_index']}".encode()
                ).hexdigest()
                
                ids.append(chunk_id)
                documents.append(chunk["text"])
                metadatas.append(chunk["metadata"])
            
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
            
            logger.info(f"Stored {len(chunks)} chunks in ChromaDB")
            
        except Exception as e:
            logger.error(f"Error storing chunks: {str(e)}")
            raise
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        
        try:
            text = self.extract_text(file_path)
            
            if not text.strip():
                logger.warning(f"No text extracted from {file_path}")
                return []
            
            file_info = Path(file_path)
            metadata = {
                "filename": file_info.name,
                "file_path": str(file_path),
                "file_size": file_info.stat().st_size,
                "file_type": file_info.suffix.lower()
            }
            
            chunks = self.create_chunks(text, metadata)
            
            if not chunks:
                logger.warning(f"No chunks created from {file_path}")
                return []
            
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.generate_embeddings(texts)
            
            self.store_chunks(chunks, embeddings)
            
            logger.info(f"Successfully processed document: {file_path}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection.name,
                "status": "active"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}

