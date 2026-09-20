# Production box

Provider VPS, one host, billed monthly.

- Ubuntu 24.04 LTS, x86_64
- 4 vCPU, 8 GB RAM (free -h shows 7.8 GB), 80 GB SSD
- Node v20.11.1 (from the distribution packages)
- PostgreSQL 16.2, running
- Docker 27.1.1, Docker Compose v2
- Nginx 1.24, TLS via certbot
- Open ports: 22, 80, 443
- Postgres listens on 0.0.0.0:5432
- Two other services already run on this box: a status page and a small
  internal wiki.
