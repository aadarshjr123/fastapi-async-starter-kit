# ==============================================
# FastAPI Async Starter – Developer Shortcuts
# ==============================================

# 🐍 Run app locally
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 🐳 Docker operations
build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f web

# 🧹 Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	docker system prune -f

# 📊 Profiling (optional)
profile:
	PROFILE=1 uvicorn app.main:app --host 0.0.0.0 --port 8000

# 🚀 Quick check
status:
	docker ps
