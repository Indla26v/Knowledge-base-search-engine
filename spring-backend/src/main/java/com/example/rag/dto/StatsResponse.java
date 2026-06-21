package com.example.rag.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record StatsResponse(
    @JsonProperty("total_chunks") long totalChunks,
    @JsonProperty("collection_name") String collectionName,
    @JsonProperty("status") String status
) {
}
