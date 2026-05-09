package com.internship.tool.controller;

import com.internship.tool.dto.LoginRequest;
import com.internship.tool.dto.RegisterRequest;
import com.internship.tool.dto.AuthResponse;
import com.internship.tool.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request) {
        String token = authService.login(request.getUsername(), request.getPassword());
        return ResponseEntity.ok(new AuthResponse(token));
    }

    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody RegisterRequest request) {
        authService.register(request.getUsername(), request.getPassword());
        return ResponseEntity.status(201).body("User registered successfully");
    }

    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refresh(@RequestHeader("Authorization") String token) {
        String newToken = authService.refresh(token.replace("Bearer ", ""));
        return ResponseEntity.ok(new AuthResponse(newToken));
    }
}