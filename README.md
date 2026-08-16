                   GitHub Codespace
                          │
                          ▼
                    Ansible
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
      PostgreSQL         MySQL           SQLite
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▲
                          │
                    Python Agent
                          │
                ┌─────────┼─────────┐
                │         │         │
               CPU       RAM       Disk
                │         │         │
                ├─────────┼─────────┤
                │      Linux        │
                │     commands      │
                └─────────┬─────────┘
                          │
                          ▼
                    Prometheus
                          │
                          ▼
                       Grafana
                          │
                          ▼
                    Alerts / SLOs
