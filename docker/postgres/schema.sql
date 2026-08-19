CREATE TABLE IF NOT EXISTS hosts (
    id SERIAL PRIMARY KEY,
    hostname TEXT NOT NULL UNIQUE,
    os TEXT,
    kernel TEXT,
    architecture TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    host_id INTEGER NOT NULL REFERENCES hosts(id),
    timestamp TIMESTAMPTZ NOT NULL,

    cpu_percent DOUBLE PRECISION,

    memory_total_mb DOUBLE PRECISION,
    memory_used_mb DOUBLE PRECISION,
    memory_available_mb DOUBLE PRECISION,
    memory_percent DOUBLE PRECISION,

    disk_total_gb DOUBLE PRECISION,
    disk_used_gb DOUBLE PRECISION,
    disk_available_gb DOUBLE PRECISION,
    disk_percent DOUBLE PRECISION,

    load_1m DOUBLE PRECISION,
    load_5m DOUBLE PRECISION,
    load_15m DOUBLE PRECISION
);