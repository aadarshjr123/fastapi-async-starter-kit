"""
Password hashing and verification utilities.
"""

from passlib.context import CryptContext
from fastapi import HTTPException, status

# ✅ use bcrypt_sha256 (safe against length and encoding issues)
_pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def validate_password_strength(password: str):
    """
    Ensure password length and safety limits.
    """
    if len(password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too short (min 4 characters required).",
        )
    if len(password.encode("utf-8")) > 256:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long (max 256 bytes allowed).",
        )


def hash_password(password: str) -> str:
    """
    Hash a plaintext password after validating its strength.
    """
    validate_password_strength(password)
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a plaintext password against a stored hash.
    """
    return _pwd_context.verify(plain, hashed)
