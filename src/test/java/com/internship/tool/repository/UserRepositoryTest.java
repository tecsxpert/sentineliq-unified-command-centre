package com.internship.tool.repository;

import com.internship.tool.entity.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository repo;

    @Test
    void testSaveUser() {
        User user = new User(null, "Akhila", "test@gmail.com", "1234", null, null);

        User saved = repo.save(user);

        assertNotNull(saved.getId());
    }

    @Test
    void testFindById() {
        User user = repo.save(new User(null, "Akhila", "test@gmail.com", "1234", null, null));

        Optional<User> found = repo.findById(user.getId());

        assertTrue(found.isPresent());
    }
}