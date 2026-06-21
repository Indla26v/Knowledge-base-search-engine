package com.example.rag.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

public record IngestionResponse(
    String status, 
    String filename, 
    @JsonProperty("chunks_created") int chunksCreated,
    String message,
    Map<String, Object> metadata
) {
}
