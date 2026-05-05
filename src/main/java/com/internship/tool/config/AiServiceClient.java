package com.internship.tool.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.extern.slf4j.Slf4j;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Client for communicating with AI Service
 * Handles REST requests to the Flask AI microservice
 * Provides methods for querying, categorizing, and generating reports
 */
@Slf4j
@Component
public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    @Value("${ai-service.url:http://localhost:5000}")
    private String aiServiceUrl;

    @Value("${ai-service.timeout:10000}")
    private long timeout;

    @Value("${ai-service.enabled:true}")
    private boolean aiServiceEnabled;

    public AiServiceClient(RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    /**
     * Check if AI service is available
     */
    public boolean isAvailable() {
        if (!aiServiceEnabled) {
            log.debug("AI service is disabled in configuration");
            return false;
        }

        try {
            String url = aiServiceUrl + "/api/ai/health";
            log.debug("Checking AI service availability at: {}", url);
            
            String response = restTemplate.getForObject(url, String.class);
            JsonNode json = objectMapper.readTree(response);
            
            boolean available = "running".equalsIgnoreCase(json.get("status").asText());
            log.debug("AI service availability check: {}", available);
            return available;
        } catch (Exception e) {
            log.warn("AI service availability check failed: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Query user information for analysis
     *
     * @param query Search query about the user
     * @param context Additional context about the user
     * @return Optional containing analysis result or empty if failed
     */
    public Optional<String> queryUser(String query, String context) {
        if (!aiServiceEnabled) {
            log.debug("AI service is disabled, skipping query");
            return Optional.empty();
        }

        if (query == null || query.trim().isEmpty()) {
            log.warn("Query is empty, skipping AI query");
            return Optional.empty();
        }

        try {
            String url = aiServiceUrl + "/api/ai/query";
            
            Map<String, String> payload = new HashMap<>();
            payload.put("query", query);
            if (context != null && !context.isEmpty()) {
                payload.put("context", context);
            }

            log.debug("Sending query to AI service: {}", query);
            
            JsonNode response = restTemplate.postForObject(url, payload, JsonNode.class);
            
            if (response != null && "success".equalsIgnoreCase(response.get("status").asText())) {
                String result = response.get("data").asText();
                log.debug("AI query successful");
                return Optional.of(result);
            }
            
            log.warn("AI query returned non-success status: {}", response);
            return Optional.empty();
        } catch (RestClientException e) {
            log.error("AI service query failed: {}", e.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            log.error("Unexpected error during AI query: {}", e.getMessage(), e);
            return Optional.empty();
        }
    }

    /**
     * Categorize user based on profile information
     *
     * @param profileData User profile data to categorize
     * @return Optional containing category or empty if failed
     */
    public Optional<String> categorizeUser(String profileData) {
        if (!aiServiceEnabled) {
            log.debug("AI service is disabled, skipping categorization");
            return Optional.empty();
        }

        if (profileData == null || profileData.trim().isEmpty()) {
            log.warn("Profile data is empty, skipping categorization");
            return Optional.empty();
        }

        try {
            String url = aiServiceUrl + "/api/ai/categorise";
            
            Map<String, String> payload = new HashMap<>();
            payload.put("text", profileData);

            log.debug("Sending categorization request to AI service");
            
            JsonNode response = restTemplate.postForObject(url, payload, JsonNode.class);
            
            if (response != null && "success".equalsIgnoreCase(response.get("status").asText())) {
                String category = response.get("data").get("category").asText();
                log.debug("AI categorization successful: {}", category);
                return Optional.of(category);
            }
            
            log.warn("AI categorization returned non-success status: {}", response);
            return Optional.empty();
        } catch (RestClientException e) {
            log.error("AI service categorization failed: {}", e.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            log.error("Unexpected error during AI categorization: {}", e.getMessage(), e);
            return Optional.empty();
        }
    }

    /**
     * Generate analysis report for user
     *
     * @param topic Analysis topic
     * @param context Context information
     * @return Optional containing report data or empty if failed
     */
    public Optional<String> generateReport(String topic, String context) {
        if (!aiServiceEnabled) {
            log.debug("AI service is disabled, skipping report generation");
            return Optional.empty();
        }

        if (topic == null || topic.trim().isEmpty()) {
            log.warn("Topic is empty, skipping report generation");
            return Optional.empty();
        }

        try {
            String url = aiServiceUrl + "/api/ai/generate-report";
            
            Map<String, Object> payload = new HashMap<>();
            payload.put("topic", topic);
            payload.put("report_type", "general");
            payload.put("use_rag", false);
            if (context != null && !context.isEmpty()) {
                payload.put("custom_context", context);
            }
            payload.put("top_items_count", 3);

            log.debug("Sending report generation request to AI service for topic: {}", topic);
            
            JsonNode response = restTemplate.postForObject(url, payload, JsonNode.class);
            
            if (response != null && "success".equalsIgnoreCase(response.get("status").asText())) {
                // Serialize the entire report data for storage
                String reportData = objectMapper.writeValueAsString(response.get("data"));
                log.debug("AI report generation successful");
                return Optional.of(reportData);
            }
            
            log.warn("AI report generation returned non-success status: {}", response);
            return Optional.empty();
        } catch (RestClientException e) {
            log.error("AI service report generation failed: {}", e.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            log.error("Unexpected error during AI report generation: {}", e.getMessage(), e);
            return Optional.empty();
        }
    }

    /**
     * Describe user based on profile
     *
     * @param profileDescription Description of the user
     * @return Optional containing AI description or empty if failed
     */
    public Optional<String> describeUser(String profileDescription) {
        if (!aiServiceEnabled) {
            log.debug("AI service is disabled, skipping description");
            return Optional.empty();
        }

        if (profileDescription == null || profileDescription.trim().isEmpty()) {
            log.warn("Profile description is empty, skipping description request");
            return Optional.empty();
        }

        try {
            String url = aiServiceUrl + "/api/ai/describe";
            
            Map<String, String> payload = new HashMap<>();
            payload.put("text", profileDescription);

            log.debug("Sending description request to AI service");
            
            JsonNode response = restTemplate.postForObject(url, payload, JsonNode.class);
            
            if (response != null && "success".equalsIgnoreCase(response.get("status").asText())) {
                String description = response.get("data").asText();
                log.debug("AI description generation successful");
                return Optional.of(description);
            }
            
            log.warn("AI description returned non-success status: {}", response);
            return Optional.empty();
        } catch (RestClientException e) {
            log.error("AI service description failed: {}", e.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            log.error("Unexpected error during AI description: {}", e.getMessage(), e);
            return Optional.empty();
        }
    }

    /**
     * Get service URL
     */
    public String getServiceUrl() {
        return aiServiceUrl;
    }

    /**
     * Get timeout configuration
     */
    public long getTimeout() {
        return timeout;
    }

    /**
     * Check if service is enabled
     */
    public boolean isEnabled() {
        return aiServiceEnabled;
    }
}
