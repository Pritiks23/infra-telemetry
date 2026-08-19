import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "telemetry.db"


def connect():
    return sqlite3.connect(DATABASE_PATH)


def get_or_create_host(connection, system_info):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO hosts (
            hostname,
            os,
            kernel,
            architecture,
            created_at
        )
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (
            system_info["hostname"],
            system_info["os"],
            system_info["kernel"],
            system_info["architecture"],
        ),
    )

    cursor.execute(
        """
        SELECT id
        FROM hosts
        WHERE hostname = ?
        """,
        (system_info["hostname"],),
    )

    row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Could not find host after inserting it")

    return row[0]


def insert_metrics(connection, host_id, metrics):
    connection.execute(
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
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?
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


def save_metrics(system_info, metrics):
    connection = connect()

    try:
        host_id = get_or_create_host(connection, system_info)

        insert_metrics(
            connection,
            host_id,
            metrics,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
