"""
Vector database retriever for finding relevant document chunks.
Handles similarity search and result ranking.
"""

import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class VectorRetriever:
    """Handles vector similarity search and document retrieval."""
    
    def __init__(self,
                 client: chromadb.Client,
                 collection: chromadb.Collection,
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector retriever with shared components.
        """
        self.embedding_model_name = embedding_model
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Use the shared client and collection from app.py
        self.chroma_client = client
        self.collection = collection
        
        logger.info(f"Vector retriever initialized with shared collection: {self.collection.name}")
    
    def get_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for query text.
        
        Args:
            query: Query text
            
        Returns:
            Query embedding vector
        """
        try:
            embedding = self.embedding_model.encode([query], convert_to_tensor=False)
            return embedding[0].tolist()
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise
    
    def search_similar_chunks(self, 
                            query: str, 
                            top_k: int = 5,
                            filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.
        
        Args:
            query: Query text
            top_k: Number of top results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of similar chunks with metadata
        """
        if not self.collection:
            logger.error("No collection available for search")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.get_query_embedding(query)
            
            # Perform similarity search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            similar_chunks = []
            
            if results["documents"] and results["documents"][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    similar_chunks.append({
                        "text": doc,
                        "metadata": metadata,
                        "similarity_score": 1 - distance,  # Convert distance to similarity
                        "rank": i + 1
                    })
            
            logger.info(f"Found {len(similar_chunks)} similar chunks for query")
            return similar_chunks
            
        except Exception as e:
            logger.error(f"Error searching similar chunks: {str(e)}")
            return []
    
    def get_top_k(self, 
                  query: str, 
                  top_k: int = 5,
                  min_similarity: float = 0.0,
                  filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get top-k most relevant chunks for a query.
        
        Args:
            query: Query text
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold
            filter_metadata: Optional metadata filters
            
        Returns:
            List of relevant chunks
        """
        try:
            # Get similar chunks
            similar_chunks = self.search_similar_chunks(
                query=query,
                top_k=top_k,
                filter_metadata=filter_metadata
            )
            
            # Filter by similarity threshold
            relevant_chunks = [
                chunk for chunk in similar_chunks 
                if chunk["similarity_score"] >= min_similarity
            ]
            
            logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks (threshold: {min_similarity})")
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Error getting top-k chunks: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        if not self.collection:
            return {"error": "No collection available"}
        
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection.name,
                "embedding_model": self.embedding_model_name,
                "status": "active"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}
    
    def search_by_metadata(self, 
                          metadata_filter: Dict[str, Any],
                          limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search chunks by metadata filters.
        
        Args:
            metadata_filter: Metadata conditions
            limit: Maximum number of results
            
        Returns:
            List of matching chunks
        """
        if not self.collection:
            logger.error("No collection available for metadata search")
            return []
        
        try:
            results = self.collection.get(
                where=metadata_filter,
                limit=limit,
                include=["documents", "metadatas"]
            )
            
            chunks = []
            if results["documents"]:
                for doc, metadata in zip(results["documents"], results["metadatas"]):
                    chunks.append({
                        "text": doc,
                        "metadata": metadata
                    })
            
            logger.info(f"Found {len(chunks)} chunks matching metadata filter")
            return chunks
            
        except Exception as e:
            logger.error(f"Error searching by metadata: {str(e)}")
            return []
    
    def clear_collection(self, ingestion_instance) -> Dict[str, Any]:
        """
        Delete the entire collection and update all relevant component references.
        
        Args:
            ingestion_instance: The DocumentIngestion instance to update.

        Returns:
            Dictionary with operation status
        """
        try:
            collection_name = self.collection.name
            logger.info(f"Clearing collection by deleting and recreating: {collection_name}")
            
            # Delete the entire collection
            self.chroma_client.delete_collection(name=collection_name)
            
            # Recreate the collection
            new_collection = self.chroma_client.get_or_create_collection(name=collection_name)
            
            # --- THIS IS THE CRITICAL FIX ---
            # Update the collection reference for both the retriever and the ingestion instances
            self.collection = new_collection
            ingestion_instance.collection = new_collection
            
            logger.info(f"Successfully cleared and synchronized collection: {collection_name}")
            return {"status": "success", "message": f"Collection '{collection_name}' cleared successfully."}
            
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            return {"error": str(e)}

