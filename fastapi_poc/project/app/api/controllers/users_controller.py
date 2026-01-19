from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user_schema import UserCreateDTO, UserResponseDTO
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
service = UserService()

@router.post("", response_model=UserResponseDTO, status_code=201)
async def create_user(payload: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    user = await service.create_user(db, payload)
    return UserResponseDTO.model_validate(user)

@router.get("", response_model=list[UserResponseDTO])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    users = await service.list_users(db, page=page, size=size)
    return [UserResponseDTO.model_validate(u) for u in users]
