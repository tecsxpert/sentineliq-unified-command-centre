package com.internship.tool.security;

import org.junit.jupiter.api.Test;
//import com.internship.tool.security.JwtUtil;
import static org.junit.jupiter.api.Assertions.*;
import com.internship.tool.config.JwtUtil;
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