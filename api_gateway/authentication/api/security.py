import hashlib
import secrets
import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...settings import settings
from ..database.models import RefreshToken


hashing_context = CryptContext(
    schemes=["bcrypt"],
    deprecated='auto',
    bcrypt__ident="2b"
)


async def create_hash(data: str):
    return hashing_context.hash(data)


async def verify_hash(password: str, hashed: str):
    return hashing_context.verify(password, hashed)


async def hash_refersh_token(data: str):
    return hashlib.sha256(data.encode()).hexdigest()


async def create_access_token(
        subject: str,
        expire_delta: timedelta | None = None
) -> str:

    expire = datetime.now(timezone.utc) + (
        expire_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE)
    )

    payload = {
        "sub": subject,
        "expire": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRETE,
        algorithm=settings.JWT_ALGORITHM
    )


async def create_refersh_token(db: Session, user_id):

    refresh_token = secrets.token_urlsafe(32)

    hashed_refersh_token = await hash_refersh_token(data=refresh_token)

    refresh_db = RefreshToken(
        user_id=user_id,
        hashed_refersh_token=hashed_refersh_token,
        expire_at=datetime.now(timezone.utc) + timedelta(days=7)
    )

    db.add(refresh_db)
    db.commit()

    return refresh_token
