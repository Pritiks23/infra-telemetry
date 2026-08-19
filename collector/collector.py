import time

from linux import collect_system_info
from metrics import normalize_system_metrics
from database import save_metrics


COLLECTION_INTERVAL = 10


def collect_once():
    system_info = collect_system_info()
    metrics = normalize_system_metrics(system_info)

    save_metrics(system_info, metrics)

    print(
        f"Telemetry saved | "
        f"host={system_info['hostname']} | "
        f"cpu={metrics['cpu_percent']}% | "
        f"memory={metrics['memory_percent']}% | "
        f"disk={metrics['disk_percent']}%"
    )


def main():
    print("Starting infrastructure telemetry collector...")
    print(f"Collection interval: {COLLECTION_INTERVAL} seconds")

    while True:
        try:
            collect_once()
            time.sleep(COLLECTION_INTERVAL)

        except KeyboardInterrupt:
            print("\nCollector stopped.")
            break

        except Exception as error:
            print(f"Collector error: {error}")
            time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
