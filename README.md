# Project Manager — Homelab Task Management System

Self-hosted project & task management for infrastructure, DevOps, Kubernetes, and homelab work.

## Features

- **Unlimited nested projects** — sub-projects within sub-projects
- **Unlimited nested tasks** — sub-tasks within sub-tasks
- **Time tracking** — start/stop timers, manual entries, variance tracking
- **Task dependencies** — block tasks until others complete
- **Activity history** — full audit log of changes
- **Comments** — markdown-supported task discussions
- **Attachments** — file uploads per task
- **Tags** — flexible categorization
- **Environments** — DEV, UAT, STAGING, PROD (extensible)
- **Progress tracking** — auto-calculated or weighted
- **Dashboard** — overview of active projects and tasks
- **Search & filters** — find anything fast

## Architecture

```mermaid
graph TB
    subgraph "Frontend"
        A[Next.js 16 / React 19]
        B[Tailwind CSS + shadcn/ui]
        C[TypeScript]
    end
    
    subgraph "Backend"
        D[FastAPI]
        E[SQLAlchemy]
        F[Pydantic]
    end
    
    subgraph "Database"
        G[PostgreSQL 16]
    end
    
    A -->|REST API| D
    D --> E
    E --> G
    
    style A fill:#61dafb
    style D fill:#009688
    style G fill:#336791
```

## Tech Stack

**Frontend:**
- Next.js 16.3
- React 19.2
- TypeScript 5
- Tailwind CSS 4
- shadcn/ui

**Backend:**
- FastAPI 0.104
- Python 3.11+
- SQLAlchemy 2.0
- Pydantic 2.5

**Database:**
- PostgreSQL 16

**Deployment:**
- Docker + Docker Compose

## Requirements

- Docker 24+
- Docker Compose 2.20+
- 2GB RAM minimum
- 10GB disk space

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/project-manager.git
cd project-manager
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Database
POSTGRES_USER=projectmgr
POSTGRES_PASSWORD=change_this_password
POSTGRES_DB=projectmgr
DATABASE_URL=postgresql://projectmgr:change_this_password@db:5432/projectmgr

# Backend
SECRET_KEY=generate_random_secret_here
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Generate secret key:

```bash
openssl rand -hex 32
```

### 3. Start Services

```bash
docker compose up -d
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 4. Run Migrations

```bash
docker compose exec backend alembic upgrade head
```

### 5. Seed Data (Optional)

```bash
docker compose exec backend python -m app.seeds.init
```

Creates:
- Default admin user: `admin@example.com` / `admin123`
- Sample projects and tasks

### 6. Access Application

Open http://localhost:3000

Default login:
- Email: `admin@example.com`
- Password: `admin123`

**Change password immediately after first login.**

## Development Setup

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Backend must be running at http://localhost:8000

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Requires PostgreSQL connection.

### Database Migrations

Create new migration:

```bash
docker compose exec backend alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
docker compose exec backend alembic upgrade head
```

Rollback:

```bash
docker compose exec backend alembic downgrade -1
```

## Environment Variables

### Backend (.env)

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
UPLOAD_DIR=/app/uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

### Backend Tests

```bash
docker compose exec backend pytest
```

With coverage:

```bash
docker compose exec backend pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Backup & Restore

### Database Backup

```bash
docker compose exec db pg_dump -U projectmgr projectmgr > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database

```bash
docker compose exec -T db psql -U projectmgr projectmgr < backup_20260809_150000.sql
```

### Backup Uploads

```bash
tar -czf uploads_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

### Restore Uploads

```bash
tar -xzf uploads_20260809_150000.tar.gz
```

See [docs/BACKUP.md](docs/BACKUP.md) for automated backup setup.

## API Documentation

Interactive docs: http://localhost:8000/docs

Key endpoints:

- `GET /api/v1/projects` — list projects
- `POST /api/v1/projects` — create project
- `GET /api/v1/projects/{id}` — project details
- `GET /api/v1/tasks` — list tasks
- `POST /api/v1/tasks` — create task
- `POST /api/v1/tasks/{id}/time-entries` — log time
- `POST /api/v1/tasks/{id}/comments` — add comment

Full API reference: [docs/API.md](docs/API.md)

## Production Deployment

### Reverse Proxy

Compatible with:
- Nginx Proxy Manager
- Nginx
- Traefik
- Caddy

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for setup guides.

### SSL/TLS

Application works behind any reverse proxy with SSL termination. No internal HTTPS required.

Example Nginx config:

```nginx
server {
    listen 443 ssl http2;
    server_name pm.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/pm.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pm.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Environment Variables for Production

Update `.env`:

```bash
# Production database with strong password
POSTGRES_PASSWORD=strong_random_password_here

# Production secret key
SECRET_KEY=production_secret_key_here

# Production origins
BACKEND_CORS_ORIGINS=["https://pm.yourdomain.com"]

# Production API URL
NEXT_PUBLIC_API_URL=https://pm.yourdomain.com/api
```

Restart services:

```bash
docker compose down
docker compose up -d
```

## Troubleshooting

### Frontend can't connect to backend

Check CORS origins in backend `.env`:

```bash
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

Restart backend:

```bash
docker compose restart backend
```

### Database connection error

Verify PostgreSQL is running:

```bash
docker compose ps
docker compose logs db
```

Check `DATABASE_URL` in `.env` matches PostgreSQL credentials.

### Migrations fail

Reset database (⚠️ deletes all data):

```bash
docker compose down -v
docker compose up -d
docker compose exec backend alembic upgrade head
```

### Upload permission errors

Fix upload directory permissions:

```bash
docker compose exec backend chmod -R 755 /app/uploads
docker compose exec backend chown -R 1000:1000 /app/uploads
```

### Ports already in use

Change ports in `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Change 3001 to available port
  backend:
    ports:
      - "8001:8000"  # Change 8001 to available port
```

Update `NEXT_PUBLIC_API_URL` in frontend `.env.local`.

### Container logs

```bash
docker compose logs backend
docker compose logs frontend
docker compose logs db
```

Follow logs:

```bash
docker compose logs -f backend
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — tech stack, database schema, API design
- [Deployment](docs/DEPLOYMENT.md) — reverse proxy setup, SSL, firewall
- [Backup](docs/BACKUP.md) — automated backup/restore procedures
- [API Reference](docs/API.md) — full endpoint documentation

## Project Structure

```
project-manager/
├── frontend/           # Next.js frontend
│   ├── app/           # Next.js 13+ app directory
│   ├── components/    # React components
│   ├── lib/          # Utilities
│   └── types/        # TypeScript types
│
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   ├── repositories/ # Data access
│   │   └── core/     # Config, database
│   ├── alembic/      # Database migrations
│   └── tests/        # Backend tests
│
├── docs/             # Documentation
├── docker-compose.yml
├── .env.example
└── README.md
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature/name`
5. Submit pull request

## License

MIT License. See [LICENSE](LICENSE) for details.

## Support

- Issues: https://github.com/yourusername/project-manager/issues
- Discussions: https://github.com/yourusername/project-manager/discussions

## Acknowledgments

Built for homelab and DevOps teams who need self-hosted task management without vendor lock-in.
