package com.example.rag.controller;

import com.example.rag.dto.IngestionResponse;
import com.example.rag.dto.QueryResponse;
import com.example.rag.dto.StatsResponse;
import com.example.rag.service.DocumentIngestionService;
import com.example.rag.service.RagPipelineService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@CrossOrigin(origins = "*") // Allow all origins for the React frontend
public class KnowledgeBaseController {

    private static final Logger logger = LoggerFactory.getLogger(KnowledgeBaseController.class);

    private final DocumentIngestionService ingestionService;
    private final RagPipelineService ragPipelineService;

    @Value("${spring.ai.vectorstore.chroma.collection-name:default_collection}")
    private String collectionName;

    public KnowledgeBaseController(DocumentIngestionService ingestionService, RagPipelineService ragPipelineService) {
        this.ingestionService = ingestionService;
        this.ragPipelineService = ragPipelineService;
    }

    @GetMapping("/")
    public ResponseEntity<Map<String, String>> root() {
        Map<String, String> info = new HashMap<>();
        info.put("name", "Knowledge Base Search Engine API (Spring Boot)");
        info.put("version", "1.0");
        info.put("description", "RAG Backend using Spring Boot, Spring AI, ChromaDB, and Anthropic");
        return ResponseEntity.ok(info);
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "healthy");
        return ResponseEntity.ok(status);
    }

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<Map<String, Object>> upload(@RequestParam("files") MultipartFile[] files) {
        List<IngestionResponse> responses = new ArrayList<>();
        for (MultipartFile file : files) {
            try {
                int chunks = ingestionService.ingestFile(file);
                Map<String, Object> metadata = new HashMap<>();
                metadata.put("file_size", file.getSize());
                String message = "Successfully processed " + file.getOriginalFilename() + " into " + chunks + " chunks";
                responses.add(new IngestionResponse("success", file.getOriginalFilename(), chunks, message, metadata));
            } catch (IOException e) {
                logger.error("Error processing file {}", file.getOriginalFilename(), e);
                responses.add(new IngestionResponse("error", file.getOriginalFilename(), 0, e.getMessage(), Map.of("error", e.getMessage())));
            } catch (Exception e) {
                logger.error("Unexpected error processing file {}", file.getOriginalFilename(), e);
                responses.add(new IngestionResponse("error", file.getOriginalFilename(), 0, e.getMessage(), Map.of("error", e.getMessage())));
            }
        }
        return ResponseEntity.ok(Map.of("results", responses));
    }

    @PostMapping(value = "/query", consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.MULTIPART_FORM_DATA_VALUE})
    public ResponseEntity<QueryResponse> query(
            @RequestParam("question") String question,
            @RequestParam(value = "top_k", defaultValue = "3") int topK,
            @RequestParam(value = "include_sources", defaultValue = "true") boolean includeSources) {
        
        QueryResponse response = ragPipelineService.query(question, topK, includeSources);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/stats")
    public ResponseEntity<StatsResponse> stats() {
        long chunks = 0;
        try {
            java.io.File file = new java.io.File("vector_store.json");
            if (file.exists()) {
                String content = java.nio.file.Files.readString(file.toPath());
                com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
                com.fasterxml.jackson.databind.JsonNode root = mapper.readTree(content);
                chunks = root.size();
            }
        } catch (Exception e) {
            logger.error("Error reading vector store file for stats", e);
        }
        return ResponseEntity.ok(new StatsResponse(chunks, "SimpleVectorStore", "active"));
    }

    @DeleteMapping("/clear-database")
    public ResponseEntity<Map<String, String>> clearDatabase() {
        Map<String, String> response = new HashMap<>();
        try {
            java.io.File file = new java.io.File("vector_store.json");
            if (file.exists()) {
                file.delete();
            }
            response.put("status", "success");
            response.put("message", "Database cleared successfully. All documents have been removed.");
            logger.info("Database cleared successfully.");
        } catch (Exception e) {
            logger.error("Error clearing database", e);
            response.put("status", "error");
            response.put("message", "Failed to clear database: " + e.getMessage());
        }
        return ResponseEntity.ok(response);
    }
}
