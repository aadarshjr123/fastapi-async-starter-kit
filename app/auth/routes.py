from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.service import authenticate_user, create_access_token, get_password_hash
from app.models import User

router = APIRouter()


@router.post("/register", summary="Register a new user")
async def register(name: str, password: str, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.name == name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = get_password_hash(password)
    user = User(name=name, hashed_password=hashed)
    db.add(user)
    await db.commit()
    return {"id": user.id, "name": user.name}


@router.post("/token", summary="Login and get JWT")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.name})
    return {"access_token": token, "token_type": "bearer"}
