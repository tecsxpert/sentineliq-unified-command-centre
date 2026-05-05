package com.internship.tool.config;

import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Collections;
@Component
public class JwtAuthFilter implements Filter {

    private final JwtUtil jwtUtil;

    public JwtAuthFilter(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {


        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        String path = req.getRequestURI();

        if (path.startsWith("/swagger") || path.startsWith("/v3/api-docs")) {
            chain.doFilter(request, response);
            return;
        }


        if (path.startsWith("/auth") || path.startsWith("/upload") || path.startsWith("/files")) {
            chain.doFilter(request, response);
            return;
        }

        String header = req.getHeader("Authorization");

        if (header == null || !header.startsWith("Bearer ")) {
            res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }

        String token = header.substring(7);

        if (!jwtUtil.validateToken(token)) {
            res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }

        Long userId = jwtUtil.extractUserId(token);

        UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(
                        userId,
                        null,
                        Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"))
                );

        SecurityContextHolder.getContext().setAuthentication(auth);

        chain.doFilter(request, response);
    }

}