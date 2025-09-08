from fastapi import APIRouter, Depends, HTTPException, Request
from app.core.jwt_utils import create_access_token
from app.services.token_service import store_refresh_token, is_refresh_token_valid
from app.models.user import SessionToken
from app.deps import get_db
from sqlalchemy.orm import Session
import uuid, datetime

router = APIRouter()

@router.post("/login")
async def login(user_id: int, request: Request, db: Session = Depends(get_db)):
    redis = request.app.state.redis
    access_token = create_access_token(user_id)
    refresh_token = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    session = SessionToken(
        user_id=user_id,
        session_id=session_id,
        expires_at=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    )
    db.add(session)
    db.commit()
    await db.refresh(session)

    await store_refresh_token(redis, refresh_token, session_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session_id": session_id,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token(session_id: str, refresh_token: str, db: Session = Depends(get_db)):
    # Проверяем Redis
    valid = await is_refresh_token_valid(refresh_token, session_id)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Получаем user_id через session
    session = db.query(SessionToken).filter_by(session_id=session_id, is_active=True).first()
    if not session:
        raise HTTPException(status_code=401, detail="Session not found or expired")

    # Создаём новый access token
    new_access_token = create_access_token(session.user_id)
    return {"access_token": new_access_token, "token_type": "bearer"}
