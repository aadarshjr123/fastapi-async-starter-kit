from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# local imports (match your files at repo root)
from models import User, SessionLocal
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    jwt,
    SECRET_KEY,
    ALGORITHM,
)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# demo in-memory user
fake_user = {"username": "test", "hashed_password": get_password_hash("secret")}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or not verify_password(
        form_data.password, fake_user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": fake_user["username"]})
    return {"access_token": token, "token_type": "bearer"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- minimal JWT validation helper (no new features, just actual verify) ---
def require_valid_token(token: str = Depends(oauth2_scheme)) -> str:
    from jose import JWTError
    from fastapi import HTTPException

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/protected")
def protected_route(_: str = Depends(require_valid_token)):
    return {"message": "This is a protected route"}


# --- users CRUD (unchanged behavior) ---
@app.post("/users")
def add_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# VERSION = os.getenv("BUILD_ID", "dev")
# DATA_FILE = "/app/data"
# DATA_DIR = os.getenv("DATA_DIR", "/app/data")
# os.makedirs(DATA_DIR, exist_ok=True)
# USERS_FILE = os.path.join(DATA_DIR, "users.json")

# # functions
# def load_users():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r") as f:
#             return json.load(f)
#     return []


# def save_users(users):
#     with open(DATA_FILE, "w") as f:
#         json.dump(users, f, indent=2)


# # routes
# @app.get("/")
# def home():
#     return {"message": f"Hello v={VERSION}"}


# @app.get("/users")
# def get_users():
#     return load_users()


# @app.post("/users")
# def add_users(user: dict):
#     users = load_users()
#     users.append(user)
#     save_users(users)
#     return {"message": "User added successfully", "user": user}


# @app.put("/users/{user_id}")
# def update_user(user_id: int, update_data: dict):
#     users = load_users()

#     for i, user in enumerate(users):
#         if user["id"] == user_id:
#             users[i].update(update_data)
#             save_users(users)
#             return {"message": "User updated successfully", "user": users[i]}

#     return {"error": "User not found"}


# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     users = load_users()
#     for i, user in enumerate(users):
#         if user["id"] == user_id:
#             delete_user = users.pop(i)
#             save_users(users)
#             return {"message": "User deleted successfully", "user": delete_user}
