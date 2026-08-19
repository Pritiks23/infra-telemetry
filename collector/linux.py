import os
import platform
import time


def get_hostname():
    return platform.node()


def get_os():
    with open("/etc/os-release") as f:
        data = {}

        for line in f:
            key, value = line.rstrip().split("=", 1)
            data[key] = value.strip('"')

    return data.get("PRETTY_NAME", data.get("NAME", "Unknown"))


def get_kernel():
    return platform.release()


def get_architecture():
    return platform.machine()


def get_cpu_count():
    return os.cpu_count()


def read_cpu_stats():
    with open("/proc/stat") as f:
        line = f.readline()

    values = line.split()[1:]

    return [int(value) for value in values]


def get_cpu_usage(interval=1):
    first = read_cpu_stats()

    time.sleep(interval)

    second = read_cpu_stats()

    idle_first = first[3] + first[4]
    idle_second = second[3] + second[4]

    total_first = sum(first)
    total_second = sum(second)

    total_delta = total_second - total_first
    idle_delta = idle_second - idle_first

    if total_delta == 0:
        return 0.0

    usage = (1 - idle_delta / total_delta) * 100

    return round(usage, 2)


def get_memory():
    memory = {}

    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)

            value = value.strip().split()[0]

            memory[key] = int(value)

    total = memory["MemTotal"]
    available = memory["MemAvailable"]

    used = total - available

    percent = (used / total) * 100

    return {
        "total_mb": round(total / 1024, 2),
        "available_mb": round(available / 1024, 2),
        "used_mb": round(used / 1024, 2),
        "used_percent": round(percent, 2),
    }


def get_load_average():
    with open("/proc/loadavg") as f:
        values = f.read().split()

    return {
        "1m": float(values[0]),
        "5m": float(values[1]),
        "15m": float(values[2]),
    }


def get_disk_usage(path="/"):
    stat = os.statvfs(path)

    total = stat.f_blocks * stat.f_frsize
    available = stat.f_bavail * stat.f_frsize
    used = total - available

    return {
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "available_gb": round(available / (1024 ** 3), 2),
        "used_percent": round((used / total) * 100, 2),
    }


def collect_system_info():
    return {
        "hostname": get_hostname(),
        "os": get_os(),
        "kernel": get_kernel(),
        "architecture": get_architecture(),
        "cpu_count": get_cpu_count(),
        "cpu_usage_percent": get_cpu_usage(),
        "memory": get_memory(),
        "load": get_load_average(),
        "disk": get_disk_usage(),
    }


if __name__ == "__main__":
    import pprint

    pprint.pprint(collect_system_info())
