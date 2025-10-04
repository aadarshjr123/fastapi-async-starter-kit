# 🚀 FastAPI + SQLite + JWT Auth

A simple backend project built with **FastAPI**, **SQLite**, and **JWT authentication**.

---

## 📌 Overview
This project demonstrates:
- User storage in **SQLite** (`users.db`)
- **JWT Authentication** (issue tokens via `/token`)
- **Protected routes** (accessible only with a valid JWT)
- Basic **CRUD** endpoints for managing users
- Auto-generated **Swagger UI** docs

---

## ✨ Features
- **JWT Auth**
  - `POST /token` → login & get access token
  - `GET /protected` → requires valid JWT
- **CRUD**
  - `POST /users` → add a user
  - `GET /users` → list all users
- **Other**
  - `GET /` → health check (“Hello, World!”)
- **Interactive Docs** → [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Project Structure
```
.
├─ auth.py          # Password hashing & JWT creation
├─ main.py          # Routes (CRUD + auth endpoints)
├─ models.py        # SQLAlchemy models + DB setup
├─ users.db         # SQLite database file
├─ requirements.txt # Python dependencies
├─ Dockerfile       # Docker build config
├─ docker-compose.yml
└─ venv/            # (local virtual environment, ignored in Docker)
```

---

## 🛠 How to Run

### ▶ Local
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Open:
   - API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🐳 Docker
1. Build & run:
   ```bash
   docker compose up --build
   ```

2. Open:
   - API: [http://localhost:8000](http://localhost:8000)
   - Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📬 Example Requests

### 1) Login & Get JWT
```bash
curl -X POST "http://localhost:8000/token"   -H "Content-Type: application/x-www-form-urlencoded"   -d "username=test&password=secret"
```

**Response**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

### 2) Access Protected Route
```bash
curl -H "Authorization: Bearer <JWT_TOKEN>"   http://localhost:8000/protected
```

**Response**
```json
{
  "message": "This is a protected route"
}
```

---

### 3) Add User
```bash
curl -X POST "http://localhost:8000/users?name=Alice&email=alice@example.com"
```

**Response**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

---

### 4) List Users
```bash
curl http://localhost:8000/users
```

**Response**
```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
]
```

---

## ✅ Test the Full Flow in Swagger
1. Go to: [http://localhost:8000/docs](http://localhost:8000/docs)  
2. Use **`/token`** to log in with:
   - `username=test`
   - `password=secret`
3. Copy the `access_token` from the response.  
4. Click **Authorize** (top right), paste:  
   ```
   Bearer <JWT_TOKEN>
   ```
5. Try `/protected` and `/users` routes.

---

## ⚡ Notes
- Default demo user is:
  - `username = test`
  - `password = secret`
- Database file: `users.db` (auto-created in root).
- If you see an error like:
  ```
  Form data requires "python-multipart"
  ```
  → install it: `pip install python-multipart`.
- On Windows, bcrypt might require extra build tools. Already included via `passlib[bcrypt]`.

---

## 📜 License
This project is free to use for learning, demos, or as a boilerplate.
