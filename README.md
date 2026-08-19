


## Infrastructure Telemetry Project — How It Works

This project is an infrastructure monitoring pipeline that collects CPU, memory, disk, and system information from a Linux machine, stores that telemetry in multiple databases, exposes metrics for Prometheus, and visualizes the data in Grafana. Ansible is responsible for deploying and configuring the collector on the host, while Docker Compose runs the supporting observability infrastructure such as PostgreSQL, MySQL, Prometheus, and Grafana. The collector runs Python code that reads Linux system information, normalizes it into consistent metrics, and writes the results to SQLite, PostgreSQL, and MySQL. Prometheus can then scrape metrics exposed by the collector, and Grafana connects to Prometheus or PostgreSQL to turn the collected data into dashboards and time-series visualizations. The overall flow is: Linux host → Python telemetry collector → databases / Prometheus → Grafana dashboard, with Ansible automating deployment and Docker Compose managing the monitoring services.


<img width="2856" height="1788" alt="image" src="https://github.com/user-attachments/assets/d445c11e-8ee7-427d-8e4b-f43ced937dc8" />
[View Grafana Infrastructure Telemetry Dashboard](https://snapshots.raintank.io/dashboard/snapshot/lSk86nk3LInIGmcUHTVoa1W9vSl1LwHa)



              APPLICATION
                  │
             collector.py
                  │
                  ▼
             DATA LAYER
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    SQLite    PostgreSQL    MySQL
                  │
                  ▼
          OBSERVABILITY
                  │
             Prometheus
                  │
                  ▼
              Grafana
                  │
                  ▼
             VISUALIZATION


          DEPLOYMENT LAYER
                  │
               Ansible
                  │
                  ▼
              Linux Host
                  │
               systemd
                  │
                  ▼
             collector.py



## 1) Python Collector
collector.py

The main program:

Start
  ↓
Load configuration
  ↓
Collect system information
  ↓
Normalize metrics
  ↓
Save metrics
  ↓
Wait 10 seconds
  ↓
Repeat

The collector produced output such as:

Telemetry saved | host=codespaces-b34412 | cpu=17.68% | memory=50.29% | disk=49.24%
Important lesson

The collector is the application, while Ansible is the deployment mechanism.

Ansible does not collect the metrics itself.

It installs and configures the collector so that the collector can run reliably.




## 2 System Information Collection
linux.py

Responsible for gathering Linux-level information.

Examples:

hostname
operating system
kernel
architecture
CPU utilization
memory
disk usage
load averages

Conceptually:

Linux OS
   │
   ├── CPU
   ├── Memory
   ├── Disk
   ├── Load
   └── Host information
          │
          ▼
      linux.py


  ## 3) Metric Normalization
metrics.py

Converts raw system information into a consistent structure.

For example:

{
    "timestamp": "...",
    "hostname": "codespaces-b34412",
    "cpu_percent": 17.68,
    "memory_percent": 50.29,
    "disk_percent": 49.24,
    "load_1m": ...,
    "load_5m": ...,
    "load_15m": ...
}
Why normalize?

Different collection sources can represent information differently.

Normalization gives the rest of the system a predictable schema:

raw Linux information
        ↓
   normalization
        ↓
standard telemetry model

This makes database storage and visualization easier.


## 4)Database.py

The database layer abstracts storage away from the collector.

The collector essentially does:

save_metrics(system_info, metrics)

The database layer decides where the information goes.

                 save_metrics()
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     save_sqlite   save_postgres  save_mysql

This is a useful software engineering pattern:

The collector doesn't need to know the implementation details of each database.

## 5) SQLite

SQLite stores the data locally:

/opt/infra-telemetry/data/telemetry.db

Tables:

hosts
system_metrics

Example:

SELECT timestamp,
       cpu_percent,
       memory_percent,
       disk_percent
FROM system_metrics;

We verified that the database actually contained telemetry:

samples
-------
14

## 6) PostgreSQL

PostgreSQL runs inside Docker:

infra-postgres

Database:

telemetry

Tables:

hosts
system_metrics

We verified the collector was successfully writing:

samples
-------
6

## 7) MySQL

MySQL also runs inside Docker:

infra-mysql

Database:

telemetry

Tables:

hosts
system_metrics

We verified:

samples
-------
6
## 8) Why Multiple Databases?

This was useful as an infrastructure engineering exercise.

The telemetry application has a database abstraction layer that can support:

SQLite
PostgreSQL
MySQL

The actual collector logic remains the same.

This demonstrates the distinction between:

Application logic
        vs.
Storage implementation


## 9) Ansible

Ansible became the deployment automation layer.

Instead of manually doing:

mkdir /opt/infra-telemetry
cp collector.py ...
python -m venv ...
pip install ...
cp config.yaml ...
create database ...
create systemd service ...

we can run:

ansible-playbook ansible/playbooks/collector.yml

Ansible performs those operations automatically.

## 10) Ansible Inventory

The inventory defines which machines Ansible manages.

Our inventory contains:

localhost

So currently we're practicing deployment against the Codespace itself.

The important production concept is:

Ansible Controller
        │
        ├── Host A
        ├── Host B
        ├── Host C
        └── Host D

The same role could eventually be deployed to many Linux servers.

## 11)Ansible Role

Our role:

ansible/roles/collector/ 

Role responsibilities
Create directories
       ↓
Install dependencies
       ↓
Create Python venv
       ↓
Install Python packages
       ↓
Deploy application files
       ↓
Deploy configuration
       ↓
Deploy database schema
       ↓
Initialize database
       ↓
Install systemd service

## 12) Idempotency

One of the biggest Ansible concepts learned.

Running:

ansible-playbook ansible/playbooks/collector.yml

multiple times should not continually recreate everything.

For example:

TASK [Create collector directory]
ok

instead of:

changed

means Ansible determined that the desired state already existed.

Desired model
Current state
     +
Desired state
     ↓
Ansible
     ↓
Only make necessary changes

This is idempotent infrastructure automation.

## 13) We eventually deployed a dedicated virtual environment:

/opt/infra-telemetry/venv/

with dependencies such as:

PyYAML
psycopg2
mysql-connector-python

The collector should therefore run with:

/opt/infra-telemetry/venv/bin/python

rather than relying on whatever Python packages happen to exist in the Codespace.

## 14) systemd

We created a systemd service:

infra-telemetry.service

This changes the collector from something manually launched with:

python collector.py

into a Linux service.

Conceptually:

systemd
   │
   ▼
infra-telemetry.service
   │
   ▼
collector.py
   │
   ▼
continuous telemetry

The service definition specifies things such as:

executable
working directory
environment variables
restart behavior
service user
startup behavior

This is much closer to how a production Linux service would be deployed.

## 15) Docker Compose

Docker Compose manages the supporting infrastructure:

docker-compose.yml

Services:

PostgreSQL
MySQL
Prometheus
Grafana

We verified:

docker compose ps

and saw all four containers running.

## 16) 20. Prometheus

Prometheus is the metrics monitoring system.

Its job is different from PostgreSQL/MySQL.

Database:

Long-term application/data storage

Prometheus:

Time-series metrics collection
## 17) Grafana

Grafana is the visualization layer.

Architecture:

PostgreSQL ───────┐
                  │
MySQL ────────────┤
                  │
Prometheus ───────┤
                  ▼
               Grafana
                  │
                  ▼
             Dashboards

We configured Grafana's Prometheus datasource with:

http://prometheus:9090

Important Docker networking concept:

Inside the Compose network:

prometheus

is a hostname.

Therefore Grafana can reach Prometheus using:

http://prometheus:9090

rather than:

localhost:9090

because localhost inside the Grafana container means the Grafana container itself


