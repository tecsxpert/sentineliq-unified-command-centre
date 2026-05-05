package com.internship.tool.entity;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;


@Entity
@Table(name = "users")
@EntityListeners(AuditingEntityListener.class)
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "name", nullable = false)
    @NotBlank(message = "Name is required")
    private String name;

    @Column(name = "email", nullable = false, unique = true)
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @Column(name = "password", nullable = false)
    @NotBlank(message = "Password is required")
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    private String password;

    /**
     * AI-generated analysis of user profile
     * Populated asynchronously after user creation
     * Can be null if AI service is unavailable
     */
    @Column(name = "ai_analysis", columnDefinition = "TEXT")
    private String aiAnalysis;

    /**
     * Status of AI analysis processing
     * Values: PENDING, COMPLETED, FAILED, SKIPPED
     */
    @Column(name = "ai_analysis_status")
    @Enumerated(EnumType.STRING)
    private AiAnalysisStatus aiAnalysisStatus;

    /**
     * Timestamp when AI analysis was completed
     */
    @Column(name = "ai_analysis_completed_at")
    private LocalDateTime aiAnalysisCompletedAt;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    /**
     * AI Analysis Status Enum
     */
    public enum AiAnalysisStatus {
        PENDING("Waiting for AI analysis"),
        COMPLETED("AI analysis completed"),
        FAILED("AI analysis failed"),
        SKIPPED("AI analysis skipped");

        private final String description;

        AiAnalysisStatus(String description) {
            this.description = description;
        }

        public String getDescription() {
            return description;
        }
    }
}
