# Knowledge-base Search Engine

A complete **RAG (Retrieval-Augmented Generation)** powered document search and question-answering system built with Python, FastAPI, and ChromaDB.
Demo video:https://drive.google.com/file/d/1ukrYPc5fljmv3k72U447jG3HlAdp1zHK/view?usp=sharing

## 🎯 Features

- **Document Ingestion**: Upload and process PDF and TXT files
- **Intelligent Chunking**: Split documents into optimal chunks for better retrieval
- **Vector Search**: Use embeddings to find semantically similar content
- **RAG Pipeline**: Combine retrieval with LLM generation for accurate answers
- **RESTful API**: Clean FastAPI endpoints for easy integration
- **Optional Frontend**: React-based web interface

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Document      │    │   Text          │    │   Vector        │
│   Upload        │───▶│   Processing    │───▶│   Database      │
│   (PDF/TXT)     │    │   & Chunking    │    │   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Vector        │───▶│   LLM           │
│   & Response    │    │   Retrieval     │    │   Generation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Claude API key (optional, for LLM generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <https://github.com/Indla26v/Knowledge-base-search-engine>
   cd knowledge-base-search-engine
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload documents (PDF/TXT) |
| `POST` | `/query` | Ask questions and get RAG-generated answers |
| `GET` | `/stats` | Get database statistics |

### Upload Documents

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@document1.pdf" \
  -F "files=@document2.txt"
```

**Response:**
```json
{
  "message": "Document processing completed",
  "results": [
    {
      "filename": "document1.pdf",
      "status": "success",
      "chunks_created": 15,
      "message": "Successfully processed 15 chunks"
    }
  ]
}
```

### Query Documents

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "question=What is machine learning?" \
  -d "top_k=5" \
  -d "include_sources=true"
```

**Response:**
```json
{
  "answer": "Machine learning is a subset of artificial intelligence...",
  "query": "What is machine learning?",
  "num_sources": 3,
  "sources": [
    {
      "text": "Machine learning algorithms can learn from data...",
      "filename": "ml_guide.pdf",
      "similarity_score": 0.89,
      "chunk_index": 2
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required for Anthropic integration
Claude_API_KEY=your_api_key_here
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### Model Settings

- **Embedding Model**: `all-MiniLM-L6-v2` (default, fast and efficient)
- **LLM Model**: `claude-3-haiku-20240307` (default, cost-effective)
- **Chunk Size**: 1000 characters with 200 character overlap

## 📁 Project Structure

```
knowledge-base-search-engine/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── ingestion.py           # Document processing pipeline
│   ├── retriever.py           # Vector search and retrieval
│   ├── rag_pipeline.py        # RAG orchestration
│   ├── requirements.txt       # Python dependencies
│   ├── env.example           # Environment variables template
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
├── frontend/                  # Optional React frontend
└── README.md
```

## 🧠 How It Works

### 1. Document Processing
- **Text Extraction**: PDFs and TXT files are parsed to extract text
- **Chunking**: Text is split into 1000-character chunks with 200-character overlap
- **Embedding Generation**: Each chunk is converted to a vector using sentence transformers
- **Storage**: Chunks and embeddings are stored in ChromaDB

### 2. Query Processing
- **Query Embedding**: User question is converted to a vector
- **Similarity Search**: Vector database finds most similar chunks
- **Context Assembly**: Relevant chunks are combined into context
- **Answer Generation**: LLM generates answer using retrieved context

### 3. RAG Pipeline
```python
def answer_query(question: str):
    # 1. Retrieve relevant chunks
    relevant_chunks = retriever.get_top_k(question, top_k=5)
    
    # 2. Combine chunks into context
    context = combine_documents(relevant_chunks)
    
    # 3. Generate answer with LLM
    answer = llm.generate(context, question)
    
    return answer
```

## 🎨 Optional Frontend

A React-based frontend is available for easy interaction:

```bash
cd frontend
npm install
npm start
```

Features:
- Drag-and-drop file upload
- Real-time query interface
- Answer display with source citations
- Document management

## 🔍 Example Usage

### Python Client Example

```python
import requests

# Upload documents
files = [
    ('files', open('document.pdf', 'rb')),
    ('files', open('notes.txt', 'rb'))
]
response = requests.post('http://localhost:8000/upload', files=files)
print(response.json())

# Query documents
query_data = {
    'question': 'What are the main benefits of renewable energy?',
    'top_k': 5,
    'include_sources': True
}
response = requests.post('http://localhost:8000/query', data=query_data)
print(response.json())
```

### JavaScript Client Example

```javascript
// Upload documents
const formData = new FormData();
formData.append('files', fileInput.files[0]);

fetch('http://localhost:8000/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Query documents
fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'question=What is artificial intelligence?&top_k=5&include_sources=true'
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🛠️ Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 📊 Performance Tips

1. **Chunk Size**: Adjust chunk size based on your documents (500-1000 characters recommended)
2. **Embedding Model**: Use `all-MiniLM-L6-v2` for speed or `all-mpnet-base-v2` for accuracy
3. **Top-K**: Start with 5-10 chunks for good balance of context and speed
4. **Batch Processing**: Process multiple documents in batches for better performance

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

##  Roadmap

- [ ] Support for more document formats (DOCX, HTML, etc.)
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Multi-language support
- [ ] Real-time document updates
- [ ] Advanced filtering and metadata search
- [ ] Integration with cloud storage (S3, GCS)
- [ ] Docker containerization
- [ ] Kubernetes deployment guides

---

**Built using FastAPI, ChromaDB, and Claude**

