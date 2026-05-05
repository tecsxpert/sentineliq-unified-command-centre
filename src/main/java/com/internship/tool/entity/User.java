package com.internship.tool.entity;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import io.swagger.v3.oas.annotations.media.Schema;
import com.fasterxml.jackson.annotation.JsonProperty;

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