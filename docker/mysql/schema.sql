CREATE TABLE IF NOT EXISTS hosts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL UNIQUE,
    os TEXT,
    kernel TEXT,
    architecture VARCHAR(100),
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,

    timestamp DATETIME NOT NULL,

    cpu_percent DOUBLE,

    memory_total_mb DOUBLE,
    memory_used_mb DOUBLE,
    memory_available_mb DOUBLE,
    memory_percent DOUBLE,

    disk_total_gb DOUBLE,
    disk_used_gb DOUBLE,
    disk_available_gb DOUBLE,
    disk_percent DOUBLE,

    load_1m DOUBLE,
    load_5m DOUBLE,
    load_15m DOUBLE,

    FOREIGN KEY (host_id) REFERENCES hosts(id)
);