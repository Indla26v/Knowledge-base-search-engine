"""
Utility functions for the Knowledge-base Search Engine.
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def validate_file_type(filename: str, allowed_extensions: List[str] = ['.pdf', '.txt']) -> bool:
    """
    Validate if file has allowed extension.
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed file extensions
        
    Returns:
        True if file type is allowed
    """
    file_extension = Path(filename).suffix.lower()
    return file_extension in allowed_extensions

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception as e:
        logger.error(f"Error getting file size: {str(e)}")
        return 0.0

def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove special characters but keep basic punctuation
    import re
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    return text.strip()

def format_chunk_metadata(chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format chunk metadata for display.
    
    Args:
        chunk: Chunk dictionary
        
    Returns:
        Formatted metadata
    """
    metadata = chunk.get("metadata", {})
    
    return {
        "filename": metadata.get("filename", "Unknown"),
        "chunk_index": metadata.get("chunk_index", 0),
        "file_type": metadata.get("file_type", "unknown"),
        "similarity_score": chunk.get("similarity_score", 0.0),
        "text_preview": chunk.get("text", "")[:100] + "..." if len(chunk.get("text", "")) > 100 else chunk.get("text", "")
    }

def create_upload_directory(upload_dir: str = "uploads") -> str:
    """
    Create upload directory if it doesn't exist.
    
    Args:
        upload_dir: Directory path
        
    Returns:
        Created directory path
    """
    try:
        Path(upload_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created upload directory: {upload_dir}")
        return upload_dir
    except Exception as e:
        logger.error(f"Error creating upload directory: {str(e)}")
        raise

def get_supported_file_types() -> List[str]:
    """
    Get list of supported file types.
    
    Returns:
        List of supported file extensions
    """
    return ['.pdf', '.txt']

def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

