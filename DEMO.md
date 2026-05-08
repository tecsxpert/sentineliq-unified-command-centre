# Demo Day — Java Developer 2 — 8 Minute Presentation

## My Demo Segment (2 minutes)

### Step 1 — Show Audit Log
- Open Swagger UI: http://localhost:8080/swagger-ui.html
- Call GET /api/items/all
- Show audit_log table has recorded the action
- Say: "Every create and update is automatically recorded in the audit log"

### Step 2 — Update Status
- Call PUT /api/items/{id} with new status
- Show the updated record
- Say: "When I update this item status, it is instantly reflected"

### Step 3 — Show Search and Filter
- Call GET /api/items/all?page=0&size=5&sortBy=createdAt&sortDir=desc
- Say: "The API supports pagination — page, size, sort by any field"

### Step 4 — CSV Export
- Call GET /api/items/export
- Show the downloaded CSV file
- Say: "One click to export all data as CSV"

## Q&A Answers

### What does your role do?
"I built the database layer using Flyway migrations,
the REST API endpoints, authentication with JWT,
role-based access control, scheduled jobs,
and the Docker Compose setup."

### What database do you use?
"PostgreSQL 15, managed with Flyway migrations.
Every schema change is in a numbered SQL file."

### What is your API port?
"Backend runs on port 8080.
Swagger UI is at http://localhost:8080/swagger-ui.html"

### What roles exist?
"Three roles — ADMIN, MANAGER, and VIEWER.
Each has different permissions enforced
with @PreAuthorize annotations."

## Demo Checklist
- [ ] Docker is running
- [ ] docker-compose up --build passes
- [ ] Swagger UI accessible at port 8080
- [ ] GET /api/items/all returns data
- [ ] PUT /api/items/{id} works
- [ ] GET /api/items/export downloads CSV
- [ ] Audit log shows entries