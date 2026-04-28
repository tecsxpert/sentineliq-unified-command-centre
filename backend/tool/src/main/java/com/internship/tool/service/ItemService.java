package com.internship.tool.service;

import com.internship.tool.entity.Item;
import com.internship.tool.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ItemService {

    @Autowired
    private ItemRepository itemRepository;

    public List<Item> getAll() {
        return itemRepository.findByDeletedFalse();
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

    public List<Item> search(String q) {
        return itemRepository.findByNameContainingIgnoreCaseAndDeletedFalse(q);
    }
}