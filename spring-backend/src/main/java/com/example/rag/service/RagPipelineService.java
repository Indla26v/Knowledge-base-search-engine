package com.example.rag.service;

import com.example.rag.dto.QueryResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.SystemPromptTemplate;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class RagPipelineService {

    private static final Logger logger = LoggerFactory.getLogger(RagPipelineService.class);

    private final ChatClient chatClient;
    private final VectorStore vectorStore;

    @Value("${spring.ai.anthropic.api-key:}")
    private String anthropicApiKey;

    public RagPipelineService(ChatClient chatClient, VectorStore vectorStore) {
        this.chatClient = chatClient;
        this.vectorStore = vectorStore;
    }

    public QueryResponse query(String question, int topK, boolean includeSources) {
        // 1. Retrieve similar chunks
        List<Document> similarDocuments = vectorStore.similaritySearch(SearchRequest.query(question).withTopK(topK));

        // 2. Build context
        String context = similarDocuments.stream()
                .map(doc -> {
                    String filename = (String) doc.getMetadata().getOrDefault("filename", "unknown");
                    return "Source: " + filename + "\n" + doc.getContent();
                })
                .collect(Collectors.joining("\n\n"));

        // 3. System prompt
        String systemPromptText = "You are a helpful assistant that answers questions based on provided context. Be accurate and concise.\n\nContext:\n{context}";
        
        String answer;
        if (anthropicApiKey == null || anthropicApiKey.trim().isEmpty()) {
            logger.warn("ANTHROPIC_API_KEY is missing. Using fallback mock response.");
            answer = "This is a fallback response because the ANTHROPIC_API_KEY is not configured. Context retrieved: " + similarDocuments.size() + " chunks.";
        } else {
            try {
                answer = chatClient.prompt()
                        .system(s -> s.text(systemPromptText).param("context", context))
                        .user(question)
                        .call()
                        .content();
            } catch (Exception e) {
                logger.error("Error communicating with Anthropic API", e);
                answer = "Error generating answer: " + e.getMessage();
            }
        }

        // 4. Map sources
        List<QueryResponse.SourceCitation> sources = new ArrayList<>();
        if (includeSources) {
            sources = similarDocuments.stream()
                    .map(doc -> {
                        String filename = (String) doc.getMetadata().getOrDefault("filename", "unknown");
                        
                        int chunkIndex = 0;
                        if (doc.getMetadata().containsKey("chunk_index")) {
                            Object ci = doc.getMetadata().get("chunk_index");
                            if (ci instanceof Number) {
                                chunkIndex = ((Number) ci).intValue();
                            } else if (ci instanceof String) {
                                try { chunkIndex = Integer.parseInt((String) ci); } catch(Exception ignored){}
                            }
                        }
                        
                        double score = 0.95; // Default high match if SimpleVectorStore doesn't provide distance
                        if (doc.getMetadata().containsKey("distance")) {
                            Object dist = doc.getMetadata().get("distance");
                            if (dist instanceof Number) {
                                score = 1.0 - ((Number) dist).doubleValue();
                            }
                        }
                        
                        return new QueryResponse.SourceCitation(filename, doc.getContent(), chunkIndex, score);
                    })
                    .collect(Collectors.toList());
        }

        return new QueryResponse(answer, sources, sources.size(), question);
    }
}
