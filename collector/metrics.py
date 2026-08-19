from datetime import datetime, timezone


def normalize_system_metrics(system_info):
    memory = system_info["memory"]
    disk = system_info["disk"]
    load = system_info["load"]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": system_info["hostname"],
        "cpu_percent": system_info["cpu_usage_percent"],
        "memory_total_mb": memory["total_mb"],
        "memory_used_mb": memory["used_mb"],
        "memory_available_mb": memory["available_mb"],
        "memory_percent": memory["used_percent"],
        "disk_total_gb": disk["total_gb"],
        "disk_used_gb": disk["used_gb"],
        "disk_available_gb": disk["available_gb"],
        "disk_percent": disk["used_percent"],
        "load_1m": load["1m"],
        "load_5m": load["5m"],
        "load_15m": load["15m"],
    }


if __name__ == "__main__":
    from linux import collect_system_info

    system_info = collect_system_info()
    metrics = normalize_system_metrics(system_info)

    for key, value in metrics.items():
        print(f"{key}: {value}")
