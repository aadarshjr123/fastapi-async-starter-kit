# ⚡ FastAPI Async Starter Kit

> “Blazingly fast, mildly caffeinated.” ☕🚀

A fully async backend built with **FastAPI**, **PostgreSQL**, **Redis**, and **JWT Authentication**,  
supercharged with **Prometheus + Grafana** to keep an eye on how awesome (or broken) it is.

---

## 🧠 What’s This?

This isn’t “just another FastAPI project.”  
It’s your **personal playground for async perfection** — featuring:

- 🌀 Async everything (DB, Redis, endpoints)  
- 🔐 JWT Auth that even your cat can’t brute-force  
- 💾 Redis cache because speed is life  
- 📊 Prometheus metrics because who doesn’t love pretty charts  
- 🚦 Rate limiter (be kind, API abusers)  
- 🐳 Docker because “it works on my machine” isn’t good enough anymore  

---

## 🏗️ Stack of Awesome

| Tech | Why |
|------|-----|
| **FastAPI** | Async, fast, Pythonic — like the name says |
| **SQLAlchemy + asyncpg** | PostgreSQL with async sugar |
| **Redis** | Caching + rate limiting (and instant regret if you forget await) |
| **Prometheus + Grafana** | See your API panic in real time |
| **JWT Auth** | Stateless and simple |
| **Docker Compose** | Because DevOps said so |

---

## 🗺️ Architecture (Because We’re Fancy)

```
app/
├── main.py              # Entry point (registers routers)
├── database.py          # Async SQLAlchemy setup
├── models.py            # ORM models
│
├── auth/
│   ├── routes.py        # Login + register endpoints
│   └── service.py       # JWT, hashing, verification
│
├── users/
│   ├── routes.py        # CRUD routes for users
│   └── service.py       # Async DB + Redis logic
│
├── utils/
│   ├── logging_utils.py # log_time decorator (fast & curious)
│   ├── profile_middleware.py
│   └── rate_limiter.py

```

---

## 🧩 Setup (Choose Your Adventure)

### 🐍 Local Mode

For those who enjoy typing commands manually:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🐳 Docker Mode

For those who prefer one-line world domination:

```bash
docker compose up --build
```

Everything just… works™.

| Service | URL |
|----------|-----|
| **FastAPI Swagger** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) |
| **Grafana** | [http://localhost:3000](http://localhost:3000) |
| **pgAdmin** | [http://localhost:5050](http://localhost:5050) |

---

## 🔐 Auth Flow (a.k.a. How to Feel Powerful)

1. Register → `POST /auth/register`  
2. Login → `POST /auth/token`  
3. Copy your **access_token** (a.k.a. VIP pass)  
4. Click **Authorize** in Swagger → `Bearer <token>`  
5. Flex on protected routes 💪

---

## 📬 Example Requests

### 👶 Register

```bash
POST /auth/register?name=Alice&password=secret
```

**Response:**
```json
{ "id": 1, "name": "Alice" }
```

---

### 🔑 Login

```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded
username=Alice&password=secret
```

**Response:**
```json
{ "access_token": "<JWT_TOKEN>", "token_type": "bearer" }
```

---

### 🧑‍💻 Get Users

```bash
GET /users/
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[ { "id": 1, "name": "Alice", "email": "alice@example.com" } ]
```

---

## 📊 Monitoring (aka “Graphs Make Me Feel Productive”)

| Metric | Description | PromQL |
|---------|--------------|--------|
| `http_requests_total` | How often users bug your API | `sum(rate(http_requests_total[1m])) by (handler)` |
| `http_request_duration_seconds` | How long you made them wait | `sum(rate(http_request_duration_seconds_sum[1m])) / sum(rate(http_request_duration_seconds_count[1m]))` |
| `cache_hits_total` | Redis high-fives | `rate(cache_hits_total[1m])` |
| `cache_misses_total` | Redis facepalms | `rate(cache_misses_total[1m])` |

---

## 🧠 Pro Tips

- Don’t forget to `await` everything — async is unforgiving.  
- Want to feel fancy? Add `PROFILE=1` to env vars to auto-profile requests.  
- If your cache hit rate is 0%… maybe you forgot to call the API twice 😅.  
- Logs say `"get_users took 13.37 ms"` → you’re basically Google now.  

---

## 🧩 Environment Variables

| Variable | Description |
|-----------|--------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime |
| `PROFILE` | Enable profiling middleware (0/1) |

---

## 🧙‍♂️ Final Words

> Code is async. Coffee is sync.  
> Push responsibly. ☕

---

## 🧾 License

MIT License © 2025 — free to use, improve, or break at your own risk.  

If you deploy it in production and it crashes — congratulations, you just learned DevOps.
