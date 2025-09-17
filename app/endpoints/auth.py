from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db
from app.services.token_service import TokenService
from app.services.user_service import UserService

from app.schemas.auth.request import LoginRequest, RefreshRequest, RegisterRequest
from app.schemas.auth.response import TokenResponse

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.create_user(data)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")

    token_service = TokenService(db, request.app.state.redis)
    tokens = await token_service.login_user(user.user_id)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    service = TokenService(db, request.app.state.redis)
    tokens = await service.login_user(data.user_id)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshRequest, request: Request, db: AsyncSession = Depends(get_db)):
    service = TokenService(db, request.app.state.redis)
    new_token = await service.refresh_token(data.session_id, data.refresh_token)
    if not new_token:
        raise HTTPException(401, "Invalid refresh token")
    return {
            "access_token": new_token,
        "refresh_token": data.refresh_token,
        "session_id": data.session_id,
        "token_type": "bearer"
    }