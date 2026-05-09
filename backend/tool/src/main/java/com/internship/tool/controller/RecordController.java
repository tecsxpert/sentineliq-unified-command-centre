package com.internship.tool.controller;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/records")
@CrossOrigin(origins = "http://localhost:5173")
public class RecordController {

    @GetMapping
    public List<Map<String, Object>> getAll() {
        List<Map<String, Object>> list = new ArrayList<>();

        Map<String, Object> r1 = new HashMap<>();
        r1.put("id", 1);
        r1.put("title", "Fix bug");
        r1.put("status", "Completed");
        r1.put("category", "Bug");
        r1.put("score", 80);

        list.add(r1);

        return list;
    }

    @GetMapping("/stats")
    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("total", 1);
        stats.put("completed", 1);
        stats.put("inProgress", 0);
        stats.put("notStarted", 0);
        return stats;
    }
}