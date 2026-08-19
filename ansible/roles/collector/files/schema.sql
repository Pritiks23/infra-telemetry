CREATE TABLE IF NOT EXISTS hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT NOT NULL UNIQUE,
    os TEXT,
    kernel TEXT,
    architecture TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,

    cpu_percent REAL,

    memory_total_mb REAL,
    memory_used_mb REAL,
    memory_available_mb REAL,
    memory_percent REAL,

    disk_total_gb REAL,
    disk_used_gb REAL,
    disk_available_gb REAL,
    disk_percent REAL,

    load_1m REAL,
    load_5m REAL,
    load_15m REAL,

    FOREIGN KEY (host_id) REFERENCES hosts(id)
);
