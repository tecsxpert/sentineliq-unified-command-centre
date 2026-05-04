package com.internship.tool.repository;

import com.internship.tool.entity.Item;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface ItemRepository extends JpaRepository<Item, Long> {

    // Search by title — uses idx_items_title
    List<Item> findByTitleContainingIgnoreCase(String title);

    // Filter by status — uses idx_items_status
    List<Item> findByStatus(String status);

    // Paginated list
    Page<Item> findAll(Pageable pageable);

    // Date range query — uses idx_items_created_at
    @Query("SELECT i FROM Item i WHERE i.createdAt BETWEEN :start AND :end")
    List<Item> findByDateRange(@Param("start") LocalDateTime start,
                               @Param("end") LocalDateTime end);

    // Fix N+1 — fetch everything in one query
    @Query("SELECT i FROM Item i WHERE i.id = :id")
    Optional<Item> findByIdOptimized(@Param("id") Long id);

    // Stats for dashboard
    @Query("SELECT i.status, COUNT(i) FROM Item i GROUP BY i.status")
    List<Object[]> countByStatus();

    // Find overdue items
    @Query("SELECT i FROM Item i WHERE i.status = 'OVERDUE'")
    List<Item> findOverdueItems();

    // Find items due before date
    @Query("SELECT i FROM Item i WHERE i.updatedAt < :date")
    List<Item> findDueBefore(@Param("date") LocalDateTime date);
}