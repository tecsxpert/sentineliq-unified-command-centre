package com.internship.tool.controller;

import com.internship.tool.entity.Item;
import com.internship.tool.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

@RestController
@RequestMapping("/api/items")
public class ItemController {

    @Autowired
    private ItemRepository itemRepository;

    // GET /all with pagination
    @GetMapping("/all")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public ResponseEntity<Page<Item>> getAll(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "createdAt") String sortBy,
            @RequestParam(defaultValue = "desc") String sortDir) {

        Sort sort = sortDir.equalsIgnoreCase("asc")
                ? Sort.by(sortBy).ascending()
                : Sort.by(sortBy).descending();

        Pageable pageable = PageRequest.of(page, size, sort);
        return ResponseEntity.ok(itemRepository.findAll(pageable));
    }

    // GET /export CSV
    @GetMapping("/export")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public void exportCsv(HttpServletResponse response) throws IOException {
        response.setContentType("text/csv");
        response.setHeader("Content-Disposition",
                "attachment; filename=items.csv");

        PrintWriter writer = response.getWriter();
        writer.println("id,title,description,status,score,createdAt");

        List<Item> items = itemRepository.findAll();
        for (Item item : items) {
            writer.println(
                    item.getId() + "," +
                            item.getTitle() + "," +
                            item.getDescription() + "," +
                            item.getStatus() + "," +
                            item.getScore() + "," +
                            item.getCreatedAt()
            );
        }
    }

    // POST /create
    @PostMapping("/create")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public ResponseEntity<Item> create(@RequestBody Item item) {
        return ResponseEntity.status(201).body(itemRepository.save(item));
    }

    // PUT /{id}
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public ResponseEntity<Item> update(@PathVariable Long id,
                                       @RequestBody Item item) {
        item.setId(id);
        return ResponseEntity.ok(itemRepository.save(item));
    }

    // DELETE /{id}
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        itemRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}