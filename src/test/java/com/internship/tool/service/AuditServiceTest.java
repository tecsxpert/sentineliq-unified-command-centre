package com.internship.tool.service;

import org.junit.jupiter.api.Test;
import com.internship.tool.service.AuditService;
import static org.junit.jupiter.api.Assertions.*;

class AuditServiceTest {

    private AuditService service = new AuditService();

    @Test
    void testAuditLog() {
        assertDoesNotThrow(() -> service.log("User created"));
    }
}
