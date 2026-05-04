package com.internship.tool.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;
import java.util.Map;

@Service
@Slf4j
public class AiServiceClient {

    private final RestTemplate restTemplate;

    @Value("${ai.service.url:http://localhost:5000}")
    private String aiServiceUrl;

    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String describe(String text) {
        return callAiService("/describe", text);
    }

    public String recommend(String text) {
        return callAiService("/recommend", text);
    }

    public String categorise(String text) {
        return callAiService("/categorise", text);
    }

    public String generateReport(String text) {
        return callAiService("/generate-report", text);
    }

    private String callAiService(String endpoint, String text) {
        try {
            Map<String, String> request = new HashMap<>();
            request.put("text", text);
            
            log.info("Calling AI service at {}{} with text: {}", aiServiceUrl, endpoint, text);
            
            Map<String, Object> response = restTemplate.postForObject(aiServiceUrl + endpoint, request, Map.class);
            
            if (response != null && response.containsKey("result")) {
                return String.valueOf(response.get("result"));
            }
            
            return null;
        } catch (Exception e) {
            log.error("Error calling AI service at {}: {}", endpoint, e.getMessage());
            return "Fallback: AI service unavailable";
        }
    }
}
