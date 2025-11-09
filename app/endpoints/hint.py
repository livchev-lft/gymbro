from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db
from app.schemas.hint.response import HintResponse
from app.services.hint_service import
router = APIRouter()

@router.get("/check", response_model=HintResponse)
async def hint_check(data: HintResponse, request: Request, db: AsyncSession = Depends(get_db)):
    hint_service =