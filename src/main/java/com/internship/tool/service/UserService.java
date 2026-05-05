package com.internship.tool.service;

import com.internship.tool.entity.User;
import com.internship.tool.exception.InvalidInputException;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.UserRepository;
import com.internship.tool.service.AiAnalysisService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.List;

@Slf4j
@Service
public class UserService {

    private final UserRepository userRepository;
    private final AiAnalysisService aiAnalysisService;

    public UserService(UserRepository userRepository, AiAnalysisService aiAnalysisService) {
        this.userRepository = userRepository;
        this.aiAnalysisService = aiAnalysisService;
    }

    // CREATE USER
    public User createUser(User user) {

        if (user.getName() == null || user.getName().isEmpty()) {
            throw new InvalidInputException("Name is required");
        }

        if (user.getEmail() == null || user.getEmail().isEmpty()) {
            throw new InvalidInputException("Email is required");
        }

        // Initialize AI analysis status
        user.setAiAnalysisStatus(User.AiAnalysisStatus.PENDING);
        user.setAiAnalysis(null);

        // Save user first
        User savedUser = userRepository.save(user);

        // Trigger async AI analysis
        try {
            log.info("Triggering AI analysis for new user: {}", savedUser.getId());
            aiAnalysisService.analyzeUserAsync(savedUser.getId());
        } catch (Exception e) {
            log.error("Failed to trigger AI analysis for user {}: {}", savedUser.getId(), e.getMessage());
            // Don't fail user creation if AI analysis fails
            // Status remains PENDING, will be retried or marked as failed
        }

        return savedUser;
    }

    // GET ALL USERS
    public Page<User> getAllUsers(Pageable pageable) {
        return userRepository.findAll(pageable);
    }

    // GET USER BY ID
    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found with id: " + id));
    }

    // DELETE USER
    public void deleteUser(Long id) {
        User user = getUserById(id);
        userRepository.delete(user);
    }

    // GET AI ANALYSIS FOR USER
    public String getUserAiAnalysis(Long id) {
        User user = getUserById(id);
        return user.getAiAnalysis(); // Returns null gracefully if not available
    }

    // GET AI ANALYSIS STATUS FOR USER
    public User.AiAnalysisStatus getUserAiAnalysisStatus(Long id) {
        User user = getUserById(id);
        return user.getAiAnalysisStatus();
    }

    // RETRY AI ANALYSIS FOR USER
    public void retryAiAnalysis(Long id) {
        User user = getUserById(id);

        // Reset status to PENDING
        user.setAiAnalysisStatus(User.AiAnalysisStatus.PENDING);
        user.setAiAnalysis(null);
        user.setAiAnalysisCompletedAt(null);
        userRepository.save(user);

        // Trigger analysis again
        try {
            log.info("Retrying AI analysis for user: {}", id);
            aiAnalysisService.analyzeUserAsync(id);
        } catch (Exception e) {
            log.error("Failed to retry AI analysis for user {}: {}", id, e.getMessage());
        }
    }
}
