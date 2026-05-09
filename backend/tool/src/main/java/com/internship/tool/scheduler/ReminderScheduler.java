package com.internship.tool.scheduler;

import com.internship.tool.entity.Item;
import com.internship.tool.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;
import java.util.List;

@Component
public class ReminderScheduler {

    @Autowired
    private ItemRepository itemRepository;

    // Every day at 8am — overdue items
    @Scheduled(cron = "0 0 8 * * *")
    public void sendOverdueReminders() {
        List<Item> allItems = itemRepository.findAll();
        allItems.stream()
                .filter(item -> "OVERDUE".equals(item.getStatus()))
                .forEach(item ->
                        System.out.println("OVERDUE REMINDER: " + item.getTitle())
                );
    }

    // Every day at 9am — due in 7 days
    @Scheduled(cron = "0 0 9 * * *")
    public void sendDeadlineAlerts() {
        LocalDateTime in7Days = LocalDateTime.now().plusDays(7);
        System.out.println("Checking items due before: " + in7Days);
        List<Item> allItems = itemRepository.findAll();
        allItems.stream()
                .filter(item -> item.getUpdatedAt() != null
                        && item.getUpdatedAt().isBefore(in7Days))
                .forEach(item ->
                        System.out.println("DEADLINE ALERT: " + item.getTitle())
                );
    }

    // Every Monday at 7am — weekly summary
    @Scheduled(cron = "0 0 7 * * MON")
    public void sendWeeklySummary() {
        List<Item> allItems = itemRepository.findAll();
        System.out.println("WEEKLY SUMMARY — Total items: "
                + allItems.size());
        long active = allItems.stream()
                .filter(i -> "ACTIVE".equals(i.getStatus()))
                .count();
        System.out.println("Active items: " + active);
    }
}