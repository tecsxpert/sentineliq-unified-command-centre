package com.internship.tool.config;

import com.internship.tool.entity.User;
import com.internship.tool.repository.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadData(UserRepository userRepository) {
        return args -> {

            // Don't add again if data already exists
            if (userRepository.count() > 0) {
                return;
            }

            for (int i = 1; i <= 30; i++) {
                User user = new User();

                user.setName("User" + i);
                user.setEmail("user" + i + "@gmail.com");
                user.setPassword("1234");
                //user.setRole(i % 2 == 0 ? "ADMIN" : "USER");

                userRepository.save(user);
            }

            System.out.println("✅ 30 users added");
        };
    }
}
