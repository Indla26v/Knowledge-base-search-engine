# Knowledge-base Search Engine

A complete **RAG (Retrieval-Augmented Generation)** powered document search and question-answering system built with **Spring Boot**, **Spring AI**, and **React**.

Demo video: https://drive.google.com/file/d/1ukrYPc5fljmv3k72U447jG3HlAdp1zHK/view?usp=sharing

##  Features

- **Document Ingestion**: Upload and process PDF and TXT files
- **Intelligent Chunking**: Split documents into optimal chunks for better retrieval
- **Vector Search**: Use ONNX embeddings to find semantically similar content
- **RAG Pipeline**: Combine retrieval with LLM generation for accurate answers
- **RESTful API**: Clean Spring Boot REST endpoints for easy integration
- **React Frontend**: Full-featured web interface with upload, query, and stats views

##  Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Document      │    │   Text          │    │   Vector        │
│   Upload        │───▶│   Processing    │───▶│   Store         │
│   (PDF/TXT)     │    │   & Chunking    │    │ (SimpleVector)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Vector        │───▶│   LLM           │
│   & Response    │    │   Retrieval     │    │   (Anthropic)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

##  Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Spring Boot 3.3 (Java 17) |
| **AI/RAG Framework** | Spring AI 1.0.0-M1 |
| **LLM Provider** | Anthropic Claude (claude-haiku-4-5) |
| **Embeddings** | Spring AI Transformers (ONNX, all-MiniLM-L6-v2) |
| **Vector Store** | Spring AI SimpleVectorStore (file-backed) |
| **Document Parsing** | Spring AI PagePdfDocumentReader |
| **Frontend** | React 18 |
| **Build Tool** | Maven 3.9+ |

##  Quick Start

### Prerequisites

- Java 17+ (or use the portable JDK in `tools/`)
- Maven 3.9+ (or use the portable Maven in `tools/`)
- Node.js 16+ and npm
- Anthropic API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Indla26v/Knowledge-base-search-engine
   cd Knowledge-base-search-engine
   ```

2. **Configure your API key**

   Edit `spring-backend/src/main/resources/application.yml` and set your Anthropic API key:
   ```yaml
   spring:
     ai:
       anthropic:
         api-key: YOUR_ANTHROPIC_API_KEY
   ```

3. **Start the Spring Boot backend**
   ```bash
   # Option A: Use the convenience script (uses portable Java/Maven in tools/)
   .\run_spring_backend.bat

   # Option B: Use system Java/Maven
   cd spring-backend
   mvn spring-boot:run
   ```
   The backend API will be available at `http://localhost:8080`

4. **Start the React frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

##  API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload documents (PDF/TXT) |
| `POST` | `/query` | Ask questions and get RAG-generated answers |
| `GET` | `/stats` | Get database statistics |
| `DELETE` | `/clear-database` | Clear all documents from the vector store |

### Upload Documents

```bash
curl -X POST "http://localhost:8080/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@document1.pdf" \
  -F "files=@document2.txt"
```

**Response:**
```json
{
  "results": [
    {
      "filename": "document1.pdf",
      "status": "success",
      "chunks_created": 15,
      "message": "Successfully processed document1.pdf into 15 chunks"
    }
  ]
}
```

### Query Documents

```bash
curl -X POST "http://localhost:8080/query" \
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

##  Configuration

### application.yml

The main configuration file is located at `spring-backend/src/main/resources/application.yml`:

```yaml
spring:
  ai:
    anthropic:
      api-key: ${ANTHROPIC_API_KEY:your-key-here}
      chat:
        options:
          model: claude-haiku-4-5
          max-tokens: 2048
          temperature: 0.7
```

### Key Settings

- **Embedding Model**: `all-MiniLM-L6-v2` (ONNX, runs locally — no API calls needed)
- **LLM Model**: `claude-haiku-4-5` (fast and cost-effective)
- **Chunk Size**: 1000 characters with 200 character overlap
- **Server Port**: 8080

## 📁 Project Structure

```
Knowledge-base-search-engine/
├── spring-backend/
│   ├── pom.xml                                    # Maven dependencies
│   ├── src/main/java/com/example/rag/
│   │   ├── RagApplication.java                    # Spring Boot entry point
│   │   ├── config/
│   │   │   ├── AiConfig.java                      # VectorStore & ChatClient beans
│   │   │   └── CorsConfig.java                    # CORS configuration
│   │   ├── controller/
│   │   │   └── KnowledgeBaseController.java       # REST API endpoints
│   │   ├── dto/
│   │   │   ├── IngestionResponse.java             # Upload response DTO
│   │   │   ├── QueryResponse.java                 # Query response DTO
│   │   │   └── StatsResponse.java                 # Stats response DTO
│   │   └── service/
│   │       ├── DocumentIngestionService.java       # PDF/TXT parsing & chunking
│   │       └── RagPipelineService.java             # RAG orchestration
│   └── src/main/resources/
│       └── application.yml                         # App configuration
├── frontend/                                       # React frontend
│   ├── src/
│   │   ├── App.js                                 # Main app with tabs
│   │   └── components/
│   │       ├── FileUpload.js                      # Drag-and-drop upload
│   │       ├── QueryInterface.js                  # Question input form
│   │       ├── ResultsDisplay.js                  # Answer & citations display
│   │       └── StatsDisplay.js                    # Database statistics
│   └── package.json
├── tools/                                          # Portable JDK & Maven
├── run_spring_backend.bat                          # Convenience startup script
└── README.md
```

##  How It Works

### 1. Document Processing
- **Text Extraction**: PDFs are parsed with Spring AI's `PagePdfDocumentReader`; TXT files via standard Java I/O
- **Chunking**: Text is split into 1000-character chunks with 200-character overlap using `TokenTextSplitter`
- **Embedding Generation**: Each chunk is embedded locally using an ONNX model (all-MiniLM-L6-v2)
- **Storage**: Chunks and embeddings are stored in `SimpleVectorStore` (persisted to `vector_store.json`)

### 2. Query Processing
- **Query Embedding**: User question is embedded using the same ONNX model
- **Similarity Search**: Vector store finds the most similar chunks via cosine similarity
- **Context Assembly**: Top-K relevant chunks are combined into context
- **Answer Generation**: Anthropic Claude generates an answer using the retrieved context

### 3. RAG Pipeline (Java)
```java
public QueryResponse query(String question, int topK, boolean includeSources) {
    // 1. Retrieve relevant chunks
    List<Document> docs = vectorStore.similaritySearch(
        SearchRequest.query(question).withTopK(topK)
    );

    // 2. Build context from retrieved documents
    String context = docs.stream()
        .map(doc -> "Source: " + doc.getMetadata().get("filename") + "\n" + doc.getContent())
        .collect(Collectors.joining("\n\n"));

    // 3. Generate answer with Anthropic Claude
    String answer = chatClient.prompt()
        .system(s -> s.text(systemPrompt).param("context", context))
        .user(question)
        .call()
        .content();

    return new QueryResponse(answer, sources, sources.size(), question);
}
```

##  Frontend

The React frontend provides a full-featured interface:

```bash
cd frontend
npm install
npm start
```

Features:
- **Upload Documents** — Drag-and-drop file upload with progress indicators
- **Ask Questions** — Real-time query interface with configurable source count
- **Source Citations** — Answer display with chunk index and similarity score
- **Database Stats** — View total chunks, collection info, and clear the database

##  Example Usage

### cURL Examples

```bash
# Upload documents
curl -X POST "http://localhost:8080/upload" \
  -F "files=@document.pdf" \
  -F "files=@notes.txt"

# Query documents
curl -X POST "http://localhost:8080/query" \
  -d "question=What are the main benefits of renewable energy?" \
  -d "top_k=5" \
  -d "include_sources=true"

# Get stats
curl http://localhost:8080/stats

# Clear database
curl -X DELETE http://localhost:8080/clear-database
```

### JavaScript Client Example

```javascript
// Upload documents
const formData = new FormData();
formData.append('files', fileInput.files[0]);

fetch('http://localhost:8080/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Query documents
fetch('http://localhost:8080/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'question=What is artificial intelligence?&top_k=5&include_sources=true'
})
.then(response => response.json())
.then(data => console.log(data));
```

##  Performance Tips

1. **Chunk Size**: Adjust chunk size based on your documents (500–1000 characters recommended)
2. **Embedding Model**: The ONNX model runs locally with zero API latency
3. **Top-K**: Start with 3–5 chunks for good balance of context and speed
4. **Batch Processing**: Upload multiple documents at once for efficient processing

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

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
- [ ] Migrate to ChromaDB or pgvector for production use

---

**Built with Spring Boot, Spring AI, and React • Powered by RAG**
