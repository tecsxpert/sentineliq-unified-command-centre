package com.internship.tool.controller;

import com.internship.tool.config.JwtUtil;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class AuthControllerTest {

    @Test
    void testLogin() throws Exception {

        JwtUtil jwtUtil = new JwtUtil();
        AuthController controller = new AuthController(jwtUtil);

        MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build();

        mockMvc.perform(post("/auth/login")
                        .param("id", "1"))
                .andExpect(status().isOk());
    }
}