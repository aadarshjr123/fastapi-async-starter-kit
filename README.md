# 🚀 Async FastAPI + PostgreSQL + Redis + JWT Auth + Prometheus

A high-performance backend built with **FastAPI**, **SQLAlchemy 2.0 (async)**, **PostgreSQL**, **Redis**, and **JWT authentication**,  
instrumented with **Prometheus + Grafana** for observability.

---

## 📘 Overview
This project demonstrates a **production-grade FastAPI architecture**:
- Fully asynchronous (database, cache, endpoints)
- JWT-based user authentication
- Caching with Redis
- Prometheus metrics and Grafana dashboards
- Rate limiting and request profiling
- Dockerized environment for simple local setup

---

## ✨ Features
| Category | Description |
|-----------|-------------|
| 🧠 **Core** | FastAPI async CRUD endpoints for users |
| 🔐 **Auth** | JWT login + protected routes |
| 🗃️ **Database** | Async SQLAlchemy with PostgreSQL |
| ⚡ **Cache** | Redis caching for `/users` list |
| 📊 **Monitoring** | Prometheus metrics + Grafana dashboards |
| 🚦 **Rate Limiting** | Per-IP request limiter using Redis |
| 🧾 **Profiling** | Optional request profiling middleware |
| 🐳 **Docker** | One-command full-stack deployment |

---

## 📂 Project Structure
```
app/
├── main.py                 # FastAPI entrypoint (registers routers)
├── database.py             # Async DB setup
├── models.py               # SQLAlchemy ORM models
│
├── auth/
│   ├── routes.py           # Register & login endpoints
│   └── service.py          # Password hashing, JWT creation
│
├── users/
│   ├── routes.py           # CRUD endpoints for users
│   └── service.py          # Async DB + Redis logic
│
├── utils/
│   ├── logging_utils.py    # Async-safe timing decorator
│   ├── profile_middleware.py
│   └── rate_limiter.py
│
└── metrics/
    └── prometheus.py       # Prometheus counters + Instrumentator setup

docker-compose.yml
Dockerfile
requirements.txt
README.md
```

---

## ⚙️ Tech Stack

- **FastAPI** — modern, async Python web framework  
- **SQLAlchemy 2.0 + asyncpg** — async ORM + PostgreSQL driver  
- **Redis 5.x** — async cache + rate-limiting backend  
- **Prometheus + Grafana** — metrics collection & visualization  
- **JWT Auth** — secure stateless authentication  
- **Docker Compose** — orchestrates all services  

---

## 🛠 Setup & Run

### ▶ Run Locally
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Open:
   - API → [http://127.0.0.1:8000](http://127.0.0.1:8000)  
   - Swagger → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🐳 Run with Docker
```bash
docker compose up --build
```

Then access:
| Service | URL |
|----------|-----|
| FastAPI Swagger | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| pgAdmin | http://localhost:5050 |

---

## 🔐 Auth Flow (via Swagger)
1. **Register:** `POST /auth/register` → create new user  
2. **Login:** `POST /auth/token` → get `access_token`  
3. **Authorize:** Click 🔒 *Authorize* in Swagger → `Bearer <token>`  
4. Access protected routes (e.g. `/users/`)

---

## 📬 Example Requests

### 1️⃣ Register
```bash
POST /auth/register?name=Alice&password=secret
```

**Response**
```json
{ "id": 1, "name": "Alice" }
```

---

### 2️⃣ Login (Get Token)
```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded
username=Alice&password=secret
```

**Response**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

### 3️⃣ Get Users
```bash
GET /users/
Authorization: Bearer <JWT_TOKEN>
```

**Response**
```json
[
  { "id": 1, "name": "Alice", "email": "alice@example.com" }
]
```

---

## 📊 Grafana Queries

| Metric | Description | PromQL |
|---------|--------------|--------|
| Requests/sec | Request throughput | `sum(rate(http_requests_total[1m])) by (handler)` |
| Avg latency | Mean response time | `sum(rate(http_request_duration_seconds_sum[1m])) / sum(rate(http_request_duration_seconds_count[1m]))` |
| P95 latency | 95th percentile | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, handler))` |
| Error rate | 5xx ratio | `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` |
| Cache hit rate | Redis efficiency | `cache_hits_total / (cache_hits_total + cache_misses_total)` |

---

## ✅ Test the Full Flow in Swagger
1. Open → [http://localhost:8000/docs](http://localhost:8000/docs)  
2. Call `/auth/register` to add a user  
3. Login via `/auth/token`  
4. Click **Authorize** and paste:  
   ```
   Bearer <access_token>
   ```
5. Try `/users/` (now authenticated)

---

## 🧩 Environment Variables (optional)
If you want to externalize secrets:
```bash
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@db:5432/mydb
SECRET_KEY=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🧠 Developer Notes
- `@log_time` measures request latency in logs  
- Profiling can be enabled via `PROFILE=1` env var  
- Prometheus metrics exposed at `/metrics`  
- Redis caching TTL = 60 s  
- Postgres data persisted in `pgdata/` volume (ignored by git)

---

## 📜 License
MIT License © 2025 — Free for personal & educational use
