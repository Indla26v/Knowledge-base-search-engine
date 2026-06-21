package com.example.rag.service;

import org.springframework.ai.document.Document;
import org.springframework.ai.reader.pdf.PagePdfDocumentReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DocumentIngestionService {

    private final VectorStore vectorStore;
    private final TokenTextSplitter textSplitter;

    public DocumentIngestionService(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
        // TokenTextSplitter with chunk size 1000 and overlap 200
        this.textSplitter = new TokenTextSplitter(1000, 1000, 200, 10000, true);
    }

    public int ingestFile(MultipartFile file) throws IOException {
        String filename = file.getOriginalFilename();
        if (filename == null) {
            filename = "unknown";
        }

        List<Document> documents = new ArrayList<>();
        String contentType = file.getContentType();
        long fileSize = file.getSize();

        if (filename.toLowerCase().endsWith(".pdf") || "application/pdf".equals(contentType)) {
            Resource resource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
            PagePdfDocumentReader pdfReader = new PagePdfDocumentReader(resource);
            documents = pdfReader.get();
        } else if (filename.toLowerCase().endsWith(".txt") || "text/plain".equals(contentType)) {
            String content = new String(file.getBytes(), StandardCharsets.UTF_8);
            Document doc = new Document(content);
            documents.add(doc);
        } else {
            throw new IllegalArgumentException("Unsupported file type: " + filename);
        }

        // Apply chunking
        List<Document> chunkedDocs = textSplitter.apply(documents);

        // Add metadata
        for (int i = 0; i < chunkedDocs.size(); i++) {
            Document chunk = chunkedDocs.get(i);
            Map<String, Object> metadata = new HashMap<>(chunk.getMetadata());
            metadata.put("filename", filename);
            metadata.put("file_type", filename.toLowerCase().endsWith(".pdf") ? "pdf" : "txt");
            metadata.put("file_size", fileSize);
            metadata.put("chunk_index", i);
            chunkedDocs.set(i, new Document(chunk.getId(), chunk.getContent(), metadata));
        }

        // Persist to SimpleVectorStore
        vectorStore.add(chunkedDocs);
        if (vectorStore instanceof org.springframework.ai.vectorstore.SimpleVectorStore simpleStore) {
            simpleStore.save(new java.io.File("vector_store.json"));
        }

        return chunkedDocs.size();
    }
}
