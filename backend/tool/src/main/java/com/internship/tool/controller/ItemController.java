package com.internship.tool.controller;

import com.internship.tool.entity.Item;
import com.internship.tool.service.ItemService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/items")
public class ItemController {

    private final ItemService itemService;

    public ItemController(ItemService itemService) {
        this.itemService = itemService;
    }

    @PutMapping("/{id}")
    public ResponseEntity<Item> update(@PathVariable Long id, @RequestBody Item item) {
        return ResponseEntity.ok(itemService.update(id, item));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        itemService.softDelete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    public ResponseEntity<List<Item>> search(@RequestParam String q) {
        return ResponseEntity.ok(itemService.search(q));
    }

    @GetMapping("/stats")
    public ResponseEntity<List<Object[]>> stats() {
        return ResponseEntity.ok(itemService.getStats());
    }
}