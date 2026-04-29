package com.internship.tool.service;

import com.internship.tool.entity.Item;
import com.internship.tool.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ItemService {

    @Autowired
    private ItemRepository itemRepository;

    public Page<Item> getAll(int page, int size, String sortBy, String sortDir) {
        Sort sort = sortDir.equalsIgnoreCase("desc")
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();
        Pageable pageable = PageRequest.of(page, size, sort);
        return itemRepository.findByDeletedFalse(pageable);
    }

    public Item getById(Long id) {
        return itemRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Item not found"));
    }

    public Item create(Item item) {
        return itemRepository.save(item);
    }

    public Item update(Long id, Item item) {
        Item existing = getById(id);
        existing.setName(item.getName());
        existing.setDescription(item.getDescription());
        return itemRepository.save(existing);
    }

    public void softDelete(Long id) {
        Item item = getById(id);
        item.setDeleted(true);
        itemRepository.save(item);
    }

    public Page<Item> search(String q, int page, int size, String sortBy, String sortDir) {
        Sort sort = sortDir.equalsIgnoreCase("desc")
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();
        Pageable pageable = PageRequest.of(page, size, sort);
        return itemRepository.findByNameContainingIgnoreCaseAndDeletedFalse(q, pageable);
    }

    public List<Item> getAllForExport() {
        return itemRepository.findAll()
                .stream()
                .filter(i -> !i.isDeleted())
                .toList();
    }
}