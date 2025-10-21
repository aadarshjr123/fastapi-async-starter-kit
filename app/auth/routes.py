from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", summary="Register a new user")
async def register_user(
    name: str,
    password: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user with a hashed password.
    """
    service = AuthService(db)
    try:
        user = await service.register_user(name, password)
        return {"id": user["id"], "name": user["name"]}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Registration failed: {type(e).__name__}: {str(e)}"
        )


@router.post("/token", summary="Login and get JWT token")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate a user and issue a JWT token.
    """
    service = AuthService(db)
    user = await service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = service.create_access_token({"sub": user.name})
    return {"access_token": token, "token_type": "bearer"}
