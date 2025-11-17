from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings
from src.db.models import Sender
from src.dto.auth import RegisterRequest, LoginRequest
from src.protocols.repo_protocols import SenderRepo


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, sender_repo: SenderRepo):
        self.sender_repo = sender_repo
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = 60 * 24  # сутки

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, *, subject: str) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": subject,
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def register(self, data: RegisterRequest) -> str:
        existing = await self.sender_repo.get_by_email(str(data.email))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed = self.hash_password(data.password)
        sender = Sender(
            email=str(data.email),
            password_hash=hashed,
            name=data.name,
            surname=data.surname,
            fathername=data.fathername,
            phone=data.phone,
        )
        sender = await self.sender_repo.add(sender)

        return self.create_access_token(subject=str(sender.id))

    async def login(self, data: LoginRequest) -> str:
        user = await self.sender_repo.get_by_email(str(data.email))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not self.verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return self.create_access_token(subject=str(user.id))
