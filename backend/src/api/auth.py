from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.dto.auth import RegisterRequest, LoginRequest, TokenResponse
from src.services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
@inject
async def register(
    data: RegisterRequest,
    service: FromDishka[AuthService],
) -> TokenResponse:
    token = await service.register(data)
    return TokenResponse(access_token=token)


@router.post("/login")
@inject
async def login(
    data: LoginRequest,
    service: FromDishka[AuthService],
) -> TokenResponse:
    token = await service.login(data)
    return TokenResponse(access_token=token)
