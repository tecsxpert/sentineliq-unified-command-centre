# SentinelIQ Unified Command Centre

## Overview
SentinelIQ Unified Command Centre is a Spring Boot backend application developed for secure user management, authentication, file handling, Swagger API documentation, Docker deployment, and automated demo data seeding.

---

## Features
- JWT Authentication
- User Management APIs
- File Upload & Download
- Swagger/OpenAPI Documentation
- Docker Support
- DataLoader for Demo Records
- Spring Security Integration

---

## ASCII Architecture Diagram

+-------------+
|   Swagger   |
+-------------+
|
v
+-------------------+
| Spring Boot APIs  |
+-------------------+
|           |
v           v
Users API    File API
|
v
+-------------+
| H2 Database |
+-------------+

---

## Prerequisites
- Java 17
- Maven
- Docker Desktop
- IntelliJ IDEA

---

## Setup Steps

### Clone Repository
```bash
git clone <repository-url>
```