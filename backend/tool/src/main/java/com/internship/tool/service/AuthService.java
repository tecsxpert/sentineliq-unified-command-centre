package com.internship.tool.service;

import com.internship.tool.entity.Role;
import com.internship.tool.entity.User;
import com.internship.tool.repository.RoleRepository;
import com.internship.tool.repository.UserRepository;
import com.internship.tool.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashSet;   // ✅ use HashSet (not ArrayList)
import java.util.Set;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RoleRepository roleRepository;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtil jwtUtil;

    // ✅ LOGIN
    public String login(String username, String password) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("Invalid password");
        }

        return jwtUtil.generateToken(username);
    }

    // ✅ REGISTER
    public void register(String username, String password) {
        User user = new User();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password));

        // ✅ FIX: Set<Role> → use HashSet
        Set<Role> roles = new HashSet<>();

        Role viewerRole = roleRepository.findByName("ROLE_VIEWER")
                .orElseThrow(() -> new RuntimeException("Role not found"));

        roles.add(viewerRole);
        user.setRoles(roles);

        userRepository.save(user);
    }

    // ✅ REFRESH TOKEN
    public String refresh(String token) {
        String username = jwtUtil.extractUsername(token);
        return jwtUtil.generateToken(username);
    }
}