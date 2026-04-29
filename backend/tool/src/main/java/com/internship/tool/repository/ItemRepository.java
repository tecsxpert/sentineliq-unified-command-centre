package com.internship.tool.repository;

import com.internship.tool.entity.Item;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemRepository extends JpaRepository<Item, Long> {
    Page<Item> findByDeletedFalse(Pageable pageable);
    Page<Item> findByNameContainingIgnoreCaseAndDeletedFalse(String name, Pageable pageable);
}