# ⚡ FastAPI Async Starter Kit — _“Blazingly fast, mildly caffeinated.”_ ☕🚀

A production-ready, fully async backend built with **FastAPI**, **PostgreSQL**, **Redis**, and **JWT Authentication**,  
supercharged with **Prometheus + Grafana** monitoring — because watching metrics is half the fun.

---

## 🧠 What’s Inside

This isn’t just another boilerplate — it’s a **real-world async playground** featuring:

- 🌀 **Full async stack** (FastAPI + SQLAlchemy + Redis)  
- 🔐 **JWT Authentication** (secure and stateless)  
- 💾 **Redis caching & rate limiting**  
- 📊 **Prometheus metrics + Grafana dashboards**  
- 🚦 **Custom rate-limiter middleware**  
- 🧩 **Profiling middleware** for request performance  
- 🐳 **Dockerized micro-stack** (Postgres, Redis, Grafana, Prometheus, Worker)

---

## 🏗️ Tech Stack

| Tech | Why |
|------|-----|
| **FastAPI** | Modern async web framework |
| **SQLAlchemy + asyncpg** | Async ORM for PostgreSQL |
| **Redis + RQ** | Queue, cache, and rate limiter |
| **Prometheus + Grafana** | Metrics, alerts, dashboards |
| **JWT + Passlib** | Authentication & password hashing |
| **Docker Compose** | Seamless local orchestration |

---

## 🗺️ Architecture

```
app/
├── main.py                  # FastAPI entrypoint
├── core/
│   ├── config.py            # Settings management
│   ├── database.py          # Async DB engine
│   ├── lifecycle.py         # Startup/shutdown events
│   └── router_registry.py   # Router registration
│
├── auth/
│   ├── routes.py            # Register & login endpoints
│   ├── service.py           # AuthService logic
│   ├── password_utils.py    # Hashing + validation
│   └── jwt_utils.py         # Token encode/decode helpers
│
├── users/
│   ├── routes.py            # CRUD routes
│   ├── service.py           # Business logic + caching
│   └── schemas.py           # Pydantic models
│
├── repositories/
│   └── user_repository.py   # DB access layer
│
├── utils/
│   ├── logging_utils.py     # @log_time decorator
│   ├── profile_middleware.py
│   ├── rate_limiter.py
│   └── redis_manager.py
│
├── queue/
│   ├── routes.py            # Job endpoints
│   └── worker.py            # Background processor
│
└── tasks.py                 # Job logic
```

---

## ⚙️ Quickstart

### 🧩 Option 1: Local (Windows/macOS/Linux)

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# or
source .venv/bin/activate # macOS/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🐳 Option 2: Docker (Recommended)

```bash
docker compose up --build
```

This spins up:
- FastAPI (`:8000`)
- PostgreSQL (`:5432`)
- Redis (`:6379`)
- Grafana (`:3000`)
- Prometheus (`:9090`)
- pgAdmin (`:5050`)

| Service | URL |
|----------|-----|
| 🧠 **API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 📊 **Prometheus** | [http://localhost:9090](http://localhost:9090) |
| 📈 **Grafana** | [http://localhost:3000](http://localhost:3000) |
| 🗄️ **pgAdmin** | [http://localhost:5050](http://localhost:5050) |

---

## 🔐 Auth Flow

| Step | Endpoint | Description |
|------|-----------|-------------|
| 🪪 1 | `POST /auth/register` | Create a user |
| 🔑 2 | `POST /auth/token` | Get JWT token |
| 🛡️ 3 | Use `Bearer <token>` | Access protected endpoints |

---

### 🔧 Example

#### Register
```bash
POST /auth/register?name=Alice&password=secret123
```

**Response:**
```json
{ "id": 1, "name": "Alice" }
```

#### Login
```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded
username=Alice&password=secret123
```

**Response:**
```json
{ "access_token": "<JWT_TOKEN>", "token_type": "bearer" }
```

---

## 📊 Monitoring

| Metric | Meaning | PromQL |
|---------|----------|--------|
| `http_requests_total` | Total requests | `sum(rate(http_requests_total[1m])) by (handler)` |
| `cache_hits_total` | Redis cache hits | `rate(cache_hits_total[1m])` |
| `jobs_finished_total` | Completed background jobs | `increase(jobs_finished_total[5m])` |

---

## 🧩 Environment Variables

| Variable | Default | Description |
|-----------|----------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://myuser:mypassword@db:5432/mydb` | Postgres DSN |
| `REDIS_URL` | `redis://redis:6379` | Redis connection |
| `SECRET_KEY` | `"dev_secret_key"` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration |
| `PROFILE` | `0` | Enable request profiling |
| `PASSLIB_BUILTIN_BCRYPT` | `1` | Use stable bcrypt backend |

---

## 🧠 Troubleshooting

| Problem | Cause | Fix |
|----------|--------|-----|
| ❌ `password cannot be longer than 72 bytes` | bcrypt C extension bug | `ENV PASSLIB_BUILTIN_BCRYPT=1` (already in Dockerfile) |
| ❌ `Registration failed` | Database missing `users` table | Rebuild containers: `docker compose down && docker compose up --build` |
| ❌ Redis not connected | Startup race condition | Wait a few seconds, Redis retries automatically |
| ❌ `/users` cache not updating | Redis TTL expired | Restart app or flush Redis (`redis-cli FLUSHALL`) |

---

## 🧰 Developer Tools

| Command | Description |
|----------|-------------|
| `make up` | Start Docker stack |
| `make down` | Stop all containers |
| `make logs` | Tail FastAPI logs |

> 💡 Windows users: Install `make` via `choco install make` or use the PowerShell equivalents.

---

## 🧙‍♂️ Tips

- Always `await` async DB + Redis calls.
- Enable profiling with `PROFILE=1` for per-request `.prof` dumps.
- Use Grafana dashboards under `grafana/dashboards/` — preconfigured for metrics.

---

## 📜 License

MIT © 2025 — Use, modify, and deploy freely.  
If it crashes in production… congratulations, you’re a backend engineer now. 😎

---

### 🪄 TL;DR

```bash
git clone https://github.com/<your-username>/fastapi-async-starter
cd fastapi-async-starter
docker compose up --build
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs)  
and say hello to your fully async, observability-ready API 🚀
