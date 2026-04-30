package com.internship.tool.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class IncidentAiService {

    private final AiServiceClient aiServiceClient;

    @Async
    public CompletableFuture<String> getIncidentAnalysisAsync(String incidentData) {
        log.info("Processing incident analysis asynchronously...");
        String description = aiServiceClient.describe(incidentData);
        return CompletableFuture.completedFuture(description);
    }

    public String getCategorization(String incidentData) {
        return aiServiceClient.categorise(incidentData);
    }
}
