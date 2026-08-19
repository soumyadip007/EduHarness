# Cloud VM Deployment Playbook (Prepared)

## Baseline VM
- Ubuntu 22.04
- 4 vCPU, 16 GB RAM
- Docker + Docker Compose

## Deployment Steps
1. Clone repo.
2. Copy `.env.example` to `.env`.
3. Run `docker compose up -d`.
4. Verify `/health` endpoint.
5. Configure Nginx + TLS.
6. Enable daily DB backup.

## Rollback
- Keep previous image tags.
- Restore DB from last snapshot if migration fails.
