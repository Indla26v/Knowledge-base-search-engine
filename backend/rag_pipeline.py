"""
RAG (Retrieval-Augmented Generation) pipeline for question answering.
Combines document retrieval with LLM generation.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RAGPipeline:
    """RAG pipeline that combines retrieval and generation."""
    
    def __init__(self, retriever, model_name: str = "claude-3-haiku-20240307"):
        # ...
        self.retriever = retriever
        self.model_name = model_name

        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not found. Using mock responses.")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=api_key)
            logger.info(f"Initialized Anthropic client with model: {model_name}")
    
    def combine_documents(self, chunks: List[Dict[str, Any]], max_length: int = 4000) -> str:
        """
        Combine retrieved chunks into context.
        
        Args:
            chunks: List of retrieved chunks
            max_length: Maximum context length
            
        Returns:
            Combined context string
        """
        if not chunks:
            return ""
        
        context_parts = []
        current_length = 0
        
        for chunk in chunks:
            chunk_text = chunk["text"]
            chunk_length = len(chunk_text)
            
            # Check if adding this chunk would exceed max_length
            if current_length + chunk_length > max_length:
                break
            
            # Add source information
            source_info = f"[Source: {chunk['metadata'].get('filename', 'Unknown')}]"
            context_parts.append(f"{source_info}\n{chunk_text}")
            current_length += chunk_length + len(source_info) + 2
        
        return "\n\n".join(context_parts)
    
    def generate_answer(self, question: str, context: str) -> str:
    # ...
        if not self.client:
            # Mock response when Anthropic is not available
            return self._generate_mock_response(question, context)

        try:
            # Create prompt for the LLMcl
            prompt = self._create_prompt(question, context)

            # Generate response using Claude
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=500,
                temperature=0.1,
                system="You are a helpful assistant that answers questions based on provided context. Be accurate and concise.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = message.content[0].text.strip()
            logger.info("Generated answer using Claude")
            return answer

        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return f"Error generating answer: {str(e)}"
    
    def _create_prompt(self, question: str, context: str) -> str:
        """
        Create prompt for the LLM.
        
        Args:
            question: User's question
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        return f"""Using the following document context, answer the question succinctly and accurately.

Context:
{context}

Question: {question}

Answer:"""
    
    def _generate_mock_response(self, question: str, context: str) -> str:
        """
        Generate mock response when OpenAI is not available.
        
        Args:
            question: User's question
            context: Retrieved context
            
        Returns:
            Mock response
        """
        if not context:
            return "I don't have enough information to answer your question. Please upload some documents first."
        
        return f"Based on the provided context, here's what I found regarding your question '{question}':\n\n{context[:500]}..."
    
    def answer_query(self, 
                    question: str, 
                    top_k: int = 5,
                    min_similarity: float = 0.0,
                    include_sources: bool = True) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve relevant chunks and generate answer.
        
        Args:
            question: User's question
            top_k: Number of chunks to retrieve
            min_similarity: Minimum similarity threshold
            include_sources: Whether to include source chunks
            
        Returns:
            Dictionary with answer and optional sources
        """
        try:
            logger.info(f"Processing query: {question}")
            
            # Step 1: Retrieve relevant chunks
            relevant_chunks = self.retriever.get_top_k(
                query=question,
                top_k=top_k,
                min_similarity=min_similarity
            )
            
            if not relevant_chunks:
                return {
                    "answer": "I couldn't find any relevant information to answer your question. Please try uploading more documents or rephrasing your question.",
                    "sources": [],
                    "num_sources": 0,
                    "query": question
                }
            
            # Step 2: Combine chunks into context
            context = self.combine_documents(relevant_chunks)
            
            # Step 3: Generate answer
            answer = self.generate_answer(question, context)
            
            # Step 4: Prepare response
            response = {
                "answer": answer,
                "query": question,
                "num_sources": len(relevant_chunks)
            }
            
            # Include sources if requested
            if include_sources:
                sources = []
                for chunk in relevant_chunks:
                    sources.append({
                        "text": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                        "filename": chunk["metadata"].get("filename", "Unknown"),
                        "similarity_score": chunk["similarity_score"],
                        "chunk_index": chunk["metadata"].get("chunk_index", 0)
                    })
                response["sources"] = sources
            
            logger.info(f"Generated answer with {len(relevant_chunks)} sources")
            return response
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            return {
                "answer": f"Error processing your question: {str(e)}",
                "sources": [],
                "num_sources": 0,
                "query": question
            }
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available OpenAI models.
        
        Returns:
            List of model names
        """
        if not self.client:
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            logger.error(f"Error getting models: {str(e)}")
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

