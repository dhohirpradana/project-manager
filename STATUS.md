# Project Manager MVP - Status

## ✅ Working
- Backend API healthy: `/health` + `/docs` OK
- Frontend: port 3001 (Grafana conflict solved)
- Postgres: healthy
- Docker stack: up
- Alembic migrations: run (11 tables created)

## ❌ Blockers
- **Seed blocked**: SQLAlchemy ORM metadata cache stale despite:
  - Fresh DB drop/create
  - Migration run
  - Model rebuild
  - Container recreate
  - Postgres restart
  - Columns exist in DB (`is_active`, `is_superuser`)
  - Model has columns
  - Still: `UndefinedColumn` error
- **DB empty**: no demo data
- **Frontend**: port 3001 up but health check failing (wget/curl missing in container)
- **Missing UI**: dashboard/kanban/timeline incomplete (8 subagent LLM timeout)

## Next
Manual workaround seed script bypass ORM direct SQL, or accept partial MVP empty DB.

**Repo:** `github.com/dhohirpradana/project-manager`  
**Access:** Backend http://localhost:8000, Frontend http://localhost:3001
