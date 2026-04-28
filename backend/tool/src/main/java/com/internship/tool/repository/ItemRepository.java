package com.internship.tool.repository;

import com.internship.tool.entity.Item;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ItemRepository extends JpaRepository<Item, Long> {
    List<Item> findByDeletedFalse();
    List<Item> findByNameContainingIgnoreCaseAndDeletedFalse(String name);
}