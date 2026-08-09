# Blockers (WIP MVP)

## Backend
- ✅ Healthy: `/health` OK, `/docs` OK, API routes loaded
- ❌ Seed blocked: passlib 1.7.2 bcrypt `detect_wrap_bug` crashes on short password `"admin"` (5 char). All versions tested fail. Workaround: pure bcrypt direct (code written, rebuild needed).
- ❌ DB empty: no demo data. Alembic migrations exist but not run (no tables created yet).

## Frontend
- ✅ Built: Next.js 14, TypeScript, Tailwind, shadcn/ui
- ❌ Unhealthy: port 3000 no HTTP response (container up 20min, health check failing)
- ⚠️ Partial: 7 components (auth, nav, sidebar, task-status, theme), routes exist (dashboard, projects, tasks, board, timeline, reports), no full dashboard/kanban/timeline implementation

## Subagent Failures
- 8/8 subagent timeout: LLM network error (provider overload apikum/combo1)
- backend_core, api_routes, frontend_shell, frontend_components, docker_infra, seed_data, integration_tests, docs_readme all failed before completion
- Partial work salvaged: API 9 routes, frontend shell 7 components, docker-compose, alembic, seed script, README

## Next Steps
1. Fix frontend container (port 3000 not serving)
2. Rebuild backend with pure bcrypt (no passlib), run alembic migration, seed DB
3. Complete dashboard/kanban/timeline components
4. Integration tests
5. Push final healthy stack
