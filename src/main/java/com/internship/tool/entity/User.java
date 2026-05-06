package com.internship.tool.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@EntityListeners(AuditingEntityListener.class)

@Data
@NoArgsConstructor
@AllArgsConstructor

@Schema(description = "User entity")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Schema(example = "1", description = "User ID")
    private Long id;

    @Column(nullable = false)
    @NotBlank(message = "Name is required")
    @Schema(example = "Akhila")
    private String name;

    @Column(nullable = false, unique = true)
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    @Schema(example = "test@gmail.com")
    private String email;

    @Column(nullable = false)
    @NotBlank(message = "Password is required")
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    @Schema(example = "1234")
    private String password;

    @CreatedDate
    @Column(updatable = false)
    @Schema(example = "2026-05-05T10:15:30")
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Schema(example = "2026-05-05T12:30:00")
    private LocalDateTime updatedAt;
}