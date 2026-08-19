import os
import sqlite3
from datetime import datetime, timezone

import mysql.connector
import psycopg2


def save_sqlite(system_info, metrics):
    db_path = os.environ.get(
        "TELEMETRY_DB_PATH",
        "data/telemetry.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO hosts
        (hostname, os, kernel, architecture, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            system_info["hostname"],
            system_info["os"],
            system_info["kernel"],
            system_info["architecture"],
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    cursor.execute(
        "SELECT id FROM hosts WHERE hostname = ?",
        (system_info["hostname"],),
    )

    host_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO system_metrics (
            host_id,
            timestamp,
            cpu_percent,
            memory_total_mb,
            memory_used_mb,
            memory_available_mb,
            memory_percent,
            disk_total_gb,
            disk_used_gb,
            disk_available_gb,
            disk_percent,
            load_1m,
            load_5m,
            load_15m
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            host_id,
            metrics["timestamp"],
            metrics["cpu_percent"],
            metrics["memory_total_mb"],
            metrics["memory_used_mb"],
            metrics["memory_available_mb"],
            metrics["memory_percent"],
            metrics["disk_total_gb"],
            metrics["disk_used_gb"],
            metrics["disk_available_gb"],
            metrics["disk_percent"],
            metrics["load_1m"],
            metrics["load_5m"],
            metrics["load_15m"],
        ),
    )

    conn.commit()
    conn.close()


def save_postgres(system_info, metrics):
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="telemetry",
        user="telemetry",
        password="telemetry",
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO hosts
        (hostname, os, kernel, architecture, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (hostname) DO NOTHING
        """,
        (
            system_info["hostname"],
            system_info["os"],
            system_info["kernel"],
            system_info["architecture"],
            datetime.now(timezone.utc),
        ),
    )

    cursor.execute(
        "SELECT id FROM hosts WHERE hostname = %s",
        (system_info["hostname"],),
    )

    host_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO system_metrics (
            host_id,
            timestamp,
            cpu_percent,
            memory_total_mb,
            memory_used_mb,
            memory_available_mb,
            memory_percent,
            disk_total_gb,
            disk_used_gb,
            disk_available_gb,
            disk_percent,
            load_1m,
            load_5m,
            load_15m
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
        """,
        (
            host_id,
            metrics["timestamp"],
            metrics["cpu_percent"],
            metrics["memory_total_mb"],
            metrics["memory_used_mb"],
            metrics["memory_available_mb"],
            metrics["memory_percent"],
            metrics["disk_total_gb"],
            metrics["disk_used_gb"],
            metrics["disk_percent"],
            metrics["disk_available_gb"],
            metrics["load_1m"],
            metrics["load_5m"],
            metrics["load_15m"],
        ),
    )

    conn.commit()
    conn.close()


def save_mysql(system_info, metrics):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        database="telemetry",
        user="telemetry",
        password="telemetry",
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO hosts
        (hostname, os, kernel, architecture, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE hostname = hostname
        """,
        (
            system_info["hostname"],
            system_info["os"],
            system_info["kernel"],
            system_info["architecture"],
            datetime.now(timezone.utc).replace(tzinfo=None),
        ),
    )

    cursor.execute(
        "SELECT id FROM hosts WHERE hostname = %s",
        (system_info["hostname"],),
    )

    host_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO system_metrics (
            host_id,
            timestamp,
            cpu_percent,
            memory_total_mb,
            memory_used_mb,
            memory_available_mb,
            memory_percent,
            disk_total_gb,
            disk_used_gb,
            disk_available_gb,
            disk_percent,
            load_1m,
            load_5m,
            load_15m
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
        """,
        (
            host_id,
            metrics["timestamp"],
            metrics["cpu_percent"],
            metrics["memory_total_mb"],
            metrics["memory_used_mb"],
            metrics["memory_available_mb"],
            metrics["memory_percent"],
            metrics["disk_total_gb"],
            metrics["disk_used_gb"],
            metrics["disk_available_gb"],
            metrics["disk_percent"],
            metrics["load_1m"],
            metrics["load_5m"],
            metrics["load_15m"],
        ),
    )

    conn.commit()
    conn.close()


def save_metrics(system_info, metrics):
    save_sqlite(system_info, metrics)

    try:
        save_postgres(system_info, metrics)
        print("PostgreSQL saved")
    except Exception as e:
        print(f"PostgreSQL error: {e}")

    try:
        save_mysql(system_info, metrics)
        print("MySQL saved")
    except Exception as e:
        print(f"MySQL error: {e}")
