package com.internship.tool.service;

import com.internship.tool.entity.User;
import com.internship.tool.exception.InvalidInputException;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.CacheEvict;

import java.util.List;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final EmailService emailService;

    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
    // CREATE USER
    @CacheEvict(value = "users", allEntries = true)
    public User createUser(User user) {

        if (user.getName() == null || user.getName().isEmpty()) {
            throw new InvalidInputException("Name is required");
        }

        if (user.getEmail() == null || user.getEmail().isEmpty()) {
            throw new InvalidInputException("Email is required");
        }

        User saved = userRepository.save(user);

        // 📧 Send email
        emailService.sendUserCreatedEmail(saved.getEmail(), saved.getName());

        return saved;
    }

    // GET ALL USERS
    @Cacheable(value = "users")
    public Page<User> getAllUsers(Pageable pageable) {
        System.out.println("🔥 Fetching from DB...");
        return userRepository.findAll(pageable);
    }

    // GET USER BY ID
    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found with id: " + id));
    }

    // DELETE USER
    @CacheEvict(value = "users", allEntries = true)

    public void deleteUser(Long id) {
        User user = getUserById(id);
        userRepository.delete(user);
    }
    @Cacheable(value = "users")
    public List<User> getAll() {
        System.out.println("🔥 Fetching from DB...");
        return userRepository.findAll();
    }


}
