-- Performance indexes for slow queries

-- Full text search index on title
CREATE INDEX idx_items_title
    ON items(title);

-- Index on score for range queries
CREATE INDEX idx_items_score
    ON items(score);

-- Composite index for status + created_at queries
CREATE INDEX idx_items_status_created
    ON items(status, created_at);

-- Index on updated_at for sorting
CREATE INDEX idx_items_updated_at
    ON items(updated_at);