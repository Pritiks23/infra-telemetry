Infrastructure Telemetry Project — Key Learnings

This project gave me a practical understanding of how a Linux infrastructure monitoring system is built from the ground up. The main lesson was that infrastructure engineering is not just about writing an application; it is about deploying, configuring, running, monitoring, and maintaining that application reliably. I built a Python telemetry collector that runs on a Linux host, gathers CPU, memory, disk, and system-load information, normalizes the data, and stores it in multiple databases. I then used Ansible to automate deployment, Docker Compose to run supporting infrastructure, Prometheus/Grafana for observability, and systemd to make the collector behave like a production Linux service.

Linux and System Fundamentals

I learned how a Linux system exposes information about its own resources and how monitoring software can collect that information programmatically. CPU utilization, memory usage, disk capacity, and load averages represent different aspects of system health: CPU percentage measures how busy the processors are, memory utilization measures how much RAM is being consumed, disk usage measures storage capacity, and load averages describe the amount of work competing for CPU resources. I also learned that infrastructure monitoring is fundamentally about turning these low-level operating-system signals into structured data that can be stored, queried, and visualized.

Python Telemetry Collector

The Python collector taught me how to separate an infrastructure application into components instead of putting everything into one script. The collector gathers raw information, the metrics module normalizes it into a consistent structure, and the database module handles persistence. The collector runs continuously in a loop, waits for a defined collection interval, gathers another sample, and saves it. This created the basic telemetry pipeline: collect → normalize → store → repeat. I also learned why environment variables such as TELEMETRY_DB_PATH are useful: configuration such as database locations can be changed without modifying the application code itself.

Databases and Persistence

I learned how the same telemetry data can be stored in different database systems for different purposes. SQLite provides simple local storage directly on the host, while PostgreSQL and MySQL provide server-based relational databases that can support more centralized or production-oriented workloads. I created schemas for the telemetry tables and verified that data was actually being inserted by querying system_metrics. This was particularly useful because it demonstrated the difference between having a database configured and proving that an application is successfully writing data to it. Checking row counts and querying recent records became an important validation technique.

Ansible and Configuration Management

One of the biggest lessons was understanding what Ansible actually provides. Instead of manually creating directories, copying Python files, installing dependencies, creating a virtual environment, deploying configuration, initializing the database, and installing a service, I encoded those operations into an Ansible role. The role makes the deployment repeatable: running the playbook brings the machine toward the desired state. I also learned about Ansible inventories, playbooks, roles, tasks, handlers, templates, and configuration files. The project demonstrated an important infrastructure principle: configuration should be represented as code rather than existing only as a sequence of commands someone remembers to execute.

Python Environments and Dependencies

The dependency problems were particularly valuable because they demonstrated a real infrastructure failure mode. Initially, yaml was installed for the Codespaces Python environment, but the collector was executed with a different Python environment, so import yaml failed. Creating /opt/infra-telemetry/venv and explicitly installing dependencies there solved the problem. Later, adding PostgreSQL and MySQL support required psycopg2 and mysql.connector to exist inside that same virtual environment. The important lesson is that "the package is installed" does not necessarily mean "the application can import the package." The package must exist in the specific Python interpreter/environment that actually runs the application.

systemd and Linux Services

I learned how systemd turns the Python collector from a manually executed program into a managed Linux service. The infra-telemetry.service.j2 template specifies the executable, working directory, environment variables, startup ordering, restart behavior, and boot target. Instead of manually running the collector every time, systemd can start it, monitor it, and restart it if it crashes. The Restart=always and RestartSec=5 settings provide basic resilience. This introduced the distinction between an application process and a production-managed service: the Python code performs the work, while systemd manages its lifecycle.

Docker and Docker Compose

Docker Compose taught me how multiple infrastructure components can be brought up as a single environment. PostgreSQL, MySQL, Prometheus, and Grafana were each represented as containers with their own images, configuration, ports, and persistent volumes. Compose created the shared network that allowed the services to communicate using service names. I learned that containers provide isolation and reproducibility, while volumes allow important data to survive container recreation. The docker compose ps command became a simple way to verify whether the infrastructure components were actually running.
