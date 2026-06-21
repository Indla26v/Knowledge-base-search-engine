package com.example.rag.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record QueryResponse(
    String answer, 
    List<SourceCitation> sources,
    @JsonProperty("num_sources") int numSources,
    String query
) {
    public record SourceCitation(
        String filename, 
        String text, 
        @JsonProperty("chunk_index") int chunkIndex,
        @JsonProperty("similarity_score") double similarityScore
    ) {}
}
