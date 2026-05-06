package com.internship.tool;

import com.internship.tool.entity.Item;
import com.internship.tool.repository.ItemRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Testcontainers
class ItemIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:15");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private ItemRepository itemRepository;

    @Test
    void fullCrudFlow() {
        // 1. CREATE
        Item item = new Item();
        item.setTitle("Test Item");
        item.setStatus("ACTIVE");
        item.setScore(85);
        Item saved = itemRepository.save(item);
        assertNotNull(saved.getId());

        // 2. READ
        Item found = itemRepository.findById(saved.getId()).orElse(null);
        assertNotNull(found);
        assertEquals("Test Item", found.getTitle());

        // 3. UPDATE
        found.setTitle("Updated Item");
        Item updated = itemRepository.save(found);
        assertEquals("Updated Item", updated.getTitle());

        // 4. DELETE
        itemRepository.deleteById(updated.getId());

        // 5. VERIFY DELETED
        assertFalse(itemRepository.findById(updated.getId()).isPresent());
    }
}