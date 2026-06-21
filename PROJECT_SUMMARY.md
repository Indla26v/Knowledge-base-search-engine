# Knowledge-base Search Engine - Project Summary

## Project Overview

A complete **RAG (Retrieval-Augmented Generation)** powered document search and question-answering system built with **Spring Boot**, **Spring AI**, and **React**.

## Project Structure

```
Knowledge-base-search-engine/
├── spring-backend/                                  # Spring Boot backend
│   ├── pom.xml                                      # Maven dependencies
│   ├── src/main/java/com/example/rag/
│   │   ├── RagApplication.java                      # Spring Boot entry point
│   │   ├── config/
│   │   │   ├── AiConfig.java                        # VectorStore & ChatClient beans
│   │   │   └── CorsConfig.java                      # CORS configuration
│   │   ├── controller/
│   │   │   └── KnowledgeBaseController.java         # REST API endpoints
│   │   ├── dto/
│   │   │   ├── IngestionResponse.java               # Upload response DTO
│   │   │   ├── QueryResponse.java                   # Query response DTO
│   │   │   └── StatsResponse.java                   # Stats response DTO
│   │   └── service/
│   │       ├── DocumentIngestionService.java         # PDF/TXT parsing & chunking
│   │       └── RagPipelineService.java               # RAG orchestration
│   └── src/main/resources/
│       └── application.yml                           # App configuration
├── frontend/                                         # React frontend
│   ├── src/
│   │   ├── App.js                                   # Main app with tab navigation
│   │   └── components/
│   │       ├── FileUpload.js                        # Drag-and-drop upload
│   │       ├── QueryInterface.js                    # Question input form
│   │       ├── ResultsDisplay.js                    # Answer & citations display
│   │       └── StatsDisplay.js                      # Database statistics
│   └── package.json
├── tools/                                            # Portable JDK 17 & Maven 3.9
├── run_spring_backend.bat                            # Convenience startup script
├── README.md                                         # Main documentation
└── PROJECT_SUMMARY.md                                # This file
```

## Quick Start Guide

### 1. Backend Setup

```bash
# Option A: Use the convenience script (uses portable Java/Maven from tools/)
.\run_spring_backend.bat

# Option B: Use system Java/Maven
cd spring-backend
mvn spring-boot:run
```

Configure your Anthropic API key in `spring-backend/src/main/resources/application.yml`:
```yaml
spring:
  ai:
    anthropic:
      api-key: YOUR_ANTHROPIC_API_KEY
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

### 3. Access the Application

- **Backend API**: http://localhost:8080
- **Frontend UI**: http://localhost:3000

## Core Components

### Backend Architecture

1. **Document Ingestion (`DocumentIngestionService.java`)**
   - PDF parsing via Spring AI `PagePdfDocumentReader`
   - TXT file reading via standard Java I/O
   - Text chunking with `TokenTextSplitter` (1000 chars, 200 overlap)
   - Local ONNX embedding generation (all-MiniLM-L6-v2)
   - Persistence to `SimpleVectorStore` (file-backed JSON)

2. **RAG Pipeline (`RagPipelineService.java`)**
   - Semantic similarity search via `VectorStore.similaritySearch()`
   - Context assembly from top-K retrieved chunks
   - Answer generation via Anthropic Claude (claude-haiku-4-5)
   - Source citation extraction with chunk index and similarity score

3. **REST Controller (`KnowledgeBaseController.java`)**
   - RESTful API endpoints with Spring `@RestController`
   - Multipart file upload handling
   - CORS configuration for React frontend
   - Error handling and logging

4. **Configuration (`AiConfig.java`)**
   - `SimpleVectorStore` bean with file-backed persistence
   - `ChatClient` bean for Anthropic integration
   - Automatic vector store loading on startup

### Frontend Architecture

1. **React Components**
   - `FileUpload.js`: Drag & drop document upload with results display
   - `QueryInterface.js`: Question input with source count and options
   - `ResultsDisplay.js`: Answer display with source citations
   - `StatsDisplay.js`: Database statistics with clear database option

2. **Features**
   - Tab-based navigation (Upload, Query, Stats)
   - Real-time upload progress indicators
   - Copy-to-clipboard functionality
   - Source citation display with similarity percentages

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload documents (PDF/TXT) |
| `POST` | `/query` | Ask questions with RAG |
| `GET` | `/stats` | Database statistics |
| `DELETE` | `/clear-database` | Clear all documents |

## RAG Workflow

1. **Document Processing**
   ```
   PDF/TXT → Text Extraction → Chunking → ONNX Embeddings → SimpleVectorStore
   ```

2. **Query Processing**
   ```
   Question → ONNX Embedding → Similarity Search → Context → Anthropic Claude → Answer
   ```

3. **Answer Generation**
   ```
   Retrieved Chunks + Question → System Prompt → Claude API → Generated Answer + Sources
   ```

## Technical Stack

### Backend
- **Java 17**
- **Spring Boot 3.3**: Web framework
- **Spring AI 1.0.0-M1**: AI/RAG framework
- **Anthropic Claude**: LLM generation (claude-haiku-4-5)
- **Spring AI Transformers**: ONNX local embeddings (all-MiniLM-L6-v2)
- **SimpleVectorStore**: File-backed vector database
- **Spring AI PagePdfDocumentReader**: PDF processing

### Frontend
- **React 18**
- **Axios**: HTTP client
- **React Dropzone**: File upload
- **Lucide React**: Icons

## Performance Features

- **Local Embeddings**: ONNX model runs locally with zero API latency
- **Efficient Chunking**: 1000-character chunks with 200-character overlap
- **Semantic Search**: Cosine similarity for relevant retrieval
- **File Persistence**: Vector store persisted to `vector_store.json`
- **Batch Processing**: Multiple document upload in a single request
- **Error Handling**: Graceful failure recovery with detailed error messages

## Security Features

- **File Validation**: PDF/TXT only
- **Size Limits**: Configurable upload limits via Spring Boot
- **CORS Configuration**: Cross-origin request handling
- **Configuration**: API keys stored in `application.yml` (not committed to git)

## User Experience

- **Drag & Drop**: Intuitive file upload
- **Real-time Feedback**: Upload progress and status indicators
- **Source Citations**: Transparent answer sources with similarity scores
- **Chunk Navigation**: Chunk index displayed per citation
- **Copy Functionality**: Easy result sharing
- **Database Management**: View stats and clear database from the UI

## Deployment Options

### Backend
- **Local Development**: `.\run_spring_backend.bat` or `mvn spring-boot:run`
- **Production**: Package as JAR with `mvn package`, then `java -jar target/*.jar`
- **Docker**: Containerize with a standard Spring Boot Dockerfile

### Frontend
- **Development**: `npm start`
- **Production**: `npm run build`
- **Hosting**: Vercel, Netlify, AWS S3, or serve from Spring Boot static resources

## Future Enhancements

- [ ] Support for more document formats (DOCX, HTML)
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Multi-language support
- [ ] Real-time document updates
- [ ] Advanced search filters and metadata search
- [ ] Migrate to ChromaDB or pgvector for production use
- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, GCP, Azure)

## Metrics and Monitoring

- **Database Stats**: Chunk count, collection status, active/inactive indicator
- **Upload Tracking**: Per-file processing results with chunk count
- **Query Analytics**: Source count and similarity scores per query
- **Health Monitoring**: `/health` endpoint for status checks

## Use Cases

- **Document Q&A**: Ask questions about uploaded documents
- **Knowledge Management**: Organize and search company documents
- **Research Assistant**: Find relevant information quickly
- **Content Analysis**: Extract insights from documents
- **Educational Tool**: Interactive learning from course materials

## Key Features Delivered

- **Complete RAG Pipeline**: Retrieval + Generation with Anthropic Claude
- **Multi-format Support**: PDF and TXT documents
- **Local Embeddings**: ONNX model — no external embedding API needed
- **Vector Store**: SimpleVectorStore with file persistence
- **RESTful API**: Spring Boot REST endpoints
- **React Frontend**: Modern, responsive UI with tab navigation
- **Source Citations**: Transparent answer sources with similarity scores
- **Database Management**: Stats display and clear database functionality
- **Documentation**: Comprehensive README and project summary
- **Error Handling**: Robust error management across all endpoints

---

**Project Status: COMPLETE**

The Knowledge-base Search Engine has been fully migrated from Python (FastAPI, LangChain, ChromaDB) to Java (Spring Boot, Spring AI). The system provides a complete RAG-powered document search and question-answering solution with a Spring Boot backend API and React frontend.
