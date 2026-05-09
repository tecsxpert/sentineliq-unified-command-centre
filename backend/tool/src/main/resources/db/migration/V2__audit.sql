CREATE TABLE IF NOT EXISTS audit_log (
                                         id BIGSERIAL PRIMARY KEY,
                                         entity_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    entity_id BIGINT,
    old_value TEXT,
    new_value TEXT,
    performed_by VARCHAR(100),
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );