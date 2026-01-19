from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user import User
from app.repositories.user_repo import UserRepository


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    async def create_user(self, db: AsyncSession, dto) -> User:
        existing = await self.repo.get_by_email(db, dto.email)
        if existing:
            raise ValueError("Email already exists")

        user = User(full_name=dto.full_name, email=dto.email)

        await self.repo.create(db, user)
        await db.commit()          # ✅ commit here
        await db.refresh(user)     # ✅ refresh to ensure id is available
        return user

    async def list_users(self, db: AsyncSession, page: int, size: int):
        offset = (page - 1) * size
        return await self.repo.list(db, offset=offset, limit=size)
