from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Any, Dict

# === config ===
SECRET_KEY = "LUCAS_IS_AWESOME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Use classic bcrypt (what you're already doing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# If you ever need safer long-password handling:
# pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    """Hash a password for storage."""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create a signed JWT with an exp claim."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# explaination:# This code provides authentication utilities for a FastAPI application.
# It includes functions to hash and verify passwords using the bcrypt algorithm,
# as well as to create JSON Web Tokens (JWT) for user authentication.
# The SECRET_KEY and ALGORITHM constants are used to sign and verify the tokens.
# The create_access_token function generates a JWT with an expiration time.
# The verify_password function checks if a plain password matches a hashed password.
# The get_password_hash function hashes a plain password for secure storage.
