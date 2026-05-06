package com.internship.tool.security;

import com.internship.tool.config.JwtUtil;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class JwtUtilTest {

    JwtUtil jwtUtil = new JwtUtil();

    @Test
    void testGenerateToken() {
        String token = jwtUtil.generateToken(1L);

        assertNotNull(token);
    }

    @Test
    void testExtractUsername() {
        String token = jwtUtil.generateToken(1L);

        Long userId = jwtUtil.extractUserId(token);
        assertEquals(1L, userId);

    }
}