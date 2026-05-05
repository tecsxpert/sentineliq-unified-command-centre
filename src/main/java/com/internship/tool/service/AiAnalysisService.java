package com.internship.tool.service;

import com.internship.tool.entity.User;
import com.internship.tool.config.AiServiceClient;
import com.internship.tool.repository.UserRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.Optional;

/**
 * Service for handling AI analysis operations asynchronously
 * Processes user analysis without blocking the main request thread
 */
@Slf4j
@Service
public class AiAnalysisService {

    private final AiServiceClient aiServiceClient;
    private final UserRepository userRepository;

    public AiAnalysisService(AiServiceClient aiServiceClient, UserRepository userRepository) {
        this.aiServiceClient = aiServiceClient;
        this.userRepository = userRepository;
    }

    /**
     * Generate AI analysis for user asynchronously
     * Runs in a separate thread and updates the user entity when complete
     *
     * @param userId User ID to analyze
     */
    @Async
    public void analyzeUserAsync(Long userId) {
        log.info("Starting async AI analysis for user: {}", userId);
        
        try {
            // Retrieve the user
            Optional<User> userOptional = userRepository.findById(userId);
            if (userOptional.isEmpty()) {
                log.warn("User not found for AI analysis: {}", userId);
                return;
            }

            User user = userOptional.get();
            
            // Mark analysis as PENDING
            user.setAiAnalysisStatus(User.AiAnalysisStatus.PENDING);
            userRepository.save(user);

            // Build context from user data
            String userContext = buildUserContext(user);
            
            // Check if AI service is available
            if (!aiServiceClient.isAvailable()) {
                log.warn("AI service is not available for user: {}", userId);
                user.setAiAnalysisStatus(User.AiAnalysisStatus.SKIPPED);
                user.setAiAnalysis("AI service unavailable");
                userRepository.save(user);
                return;
            }

            // Generate report from AI service
            String topic = "User Profile Analysis: " + user.getName();
            Optional<String> analysisResult = aiServiceClient.generateReport(topic, userContext);

            if (analysisResult.isPresent()) {
                // Analysis succeeded
                user.setAiAnalysis(analysisResult.get());
                user.setAiAnalysisStatus(User.AiAnalysisStatus.COMPLETED);
                user.setAiAnalysisCompletedAt(LocalDateTime.now());
                log.info("AI analysis completed successfully for user: {}", userId);
            } else {
                // Analysis failed gracefully
                user.setAiAnalysisStatus(User.AiAnalysisStatus.FAILED);
                user.setAiAnalysis(null);
                log.warn("AI analysis failed for user: {}", userId);
            }

            // Save the updated user
            userRepository.save(user);
            log.info("User analysis status updated: {} -> {}", userId, user.getAiAnalysisStatus());

        } catch (Exception e) {
            log.error("Unexpected error during AI analysis for user {}: {}", userId, e.getMessage(), e);
            
            try {
                // Attempt to update user with error status
                Optional<User> userOptional = userRepository.findById(userId);
                if (userOptional.isPresent()) {
                    User user = userOptional.get();
                    user.setAiAnalysisStatus(User.AiAnalysisStatus.FAILED);
                    user.setAiAnalysis("Analysis error: " + e.getMessage());
                    userRepository.save(user);
                }
            } catch (Exception updateError) {
                log.error("Failed to update user status after error: {}", updateError.getMessage());
            }
        }
    }

    /**
     * Generate AI description for user asynchronously
     *
     * @param userId User ID to describe
     */
    @Async
    public void describeUserAsync(Long userId) {
        log.info("Starting async AI description for user: {}", userId);
        
        try {
            Optional<User> userOptional = userRepository.findById(userId);
            if (userOptional.isEmpty()) {
                log.warn("User not found for AI description: {}", userId);
                return;
            }

            User user = userOptional.get();
            String profileDescription = user.getName() + " (" + user.getEmail() + ")";

            Optional<String> description = aiServiceClient.describeUser(profileDescription);
            
            if (description.isPresent()) {
                log.info("AI description generated for user: {}", userId);
                // You could store this in a separate field if needed
            } else {
                log.warn("AI description generation failed for user: {}", userId);
            }
        } catch (Exception e) {
            log.error("Error generating AI description for user {}: {}", userId, e.getMessage(), e);
        }
    }

    /**
     * Categorize user asynchronously
     *
     * @param userId User ID to categorize
     */
    @Async
    public void categorizeUserAsync(Long userId) {
        log.info("Starting async user categorization: {}", userId);
        
        try {
            Optional<User> userOptional = userRepository.findById(userId);
            if (userOptional.isEmpty()) {
                log.warn("User not found for categorization: {}", userId);
                return;
            }

            User user = userOptional.get();
            String profileData = buildUserContext(user);

            Optional<String> category = aiServiceClient.categorizeUser(profileData);
            
            if (category.isPresent()) {
                log.info("User categorized successfully: {} -> {}", userId, category.get());
                // You could store this in a separate field if needed
            } else {
                log.warn("User categorization failed for user: {}", userId);
            }
        } catch (Exception e) {
            log.error("Error categorizing user {}: {}", userId, e.getMessage(), e);
        }
    }

    /**
     * Build context string from user information
     * Gracefully handles null values
     *
     * @param user User entity
     * @return Context string for AI analysis
     */
    private String buildUserContext(User user) {
        StringBuilder context = new StringBuilder();
        
        if (user != null) {
            if (user.getName() != null && !user.getName().isEmpty()) {
                context.append("Name: ").append(user.getName()).append("\n");
            }
            
            if (user.getEmail() != null && !user.getEmail().isEmpty()) {
                context.append("Email: ").append(user.getEmail()).append("\n");
            }
            
            if (user.getCreatedAt() != null) {
                context.append("Member since: ").append(user.getCreatedAt()).append("\n");
            }
        }
        
        return context.toString().isEmpty() ? "No user data available" : context.toString();
    }

    /**
     * Get AI analysis for user
     * Returns null gracefully if not available
     *
     * @param userId User ID
     * @return Optional containing AI analysis or empty
     */
    public Optional<String> getAiAnalysis(Long userId) {
        try {
            Optional<User> user = userRepository.findById(userId);
            if (user.isPresent() && user.get().getAiAnalysis() != null) {
                return Optional.of(user.get().getAiAnalysis());
            }
            return Optional.empty();
        } catch (Exception e) {
            log.error("Error retrieving AI analysis for user {}: {}", userId, e.getMessage());
            return Optional.empty();
        }
    }

    /**
     * Get AI analysis status for user
     *
     * @param userId User ID
     * @return Optional containing status or empty
     */
    public Optional<User.AiAnalysisStatus> getAnalysisStatus(Long userId) {
        try {
            Optional<User> user = userRepository.findById(userId);
            if (user.isPresent() && user.get().getAiAnalysisStatus() != null) {
                return Optional.of(user.get().getAiAnalysisStatus());
            }
            return Optional.empty();
        } catch (Exception e) {
            log.error("Error retrieving analysis status for user {}: {}", userId, e.getMessage());
            return Optional.empty();
        }
    }
}
