import time
from pathlib import Path

import yaml

from linux import collect_system_info
from metrics import normalize_system_metrics
from database import save_metrics


CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config():
    with open(CONFIG_PATH) as file:
        return yaml.safe_load(file)


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
    config = load_config()

    collection_interval = config["collection_interval"]

    print("Starting infrastructure telemetry collector...")
    print(f"Collection interval: {collection_interval} seconds")

    while True:
        try:
            collect_once()
            time.sleep(collection_interval)

        except KeyboardInterrupt:
            print("\nCollector stopped.")
            break

        except Exception as error:
            print(f"Collector error: {error}")
            time.sleep(collection_interval)


if __name__ == "__main__":
    main()
