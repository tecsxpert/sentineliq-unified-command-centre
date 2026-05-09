CREATE TABLE items (
                       id          BIGSERIAL PRIMARY KEY,
                       title       VARCHAR(255) NOT NULL,
                       description TEXT,
                       status      VARCHAR(50)  DEFAULT 'ACTIVE',
                       score       INTEGER,
                       created_at  TIMESTAMP    DEFAULT NOW(),
                       updated_at  TIMESTAMP    DEFAULT NOW()
);

CREATE INDEX idx_items_status     ON items(status);
CREATE INDEX idx_items_created_at ON items(created_at);