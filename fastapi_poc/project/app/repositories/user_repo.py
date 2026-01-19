from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user import User

class UserRepository:
    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def list(self, db: AsyncSession, offset: int, limit: int) -> list[User]:
        res = await db.execute(select(User).order_by(User.id.desc()).offset(offset).limit(limit))
        return list(res.scalars().all())

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        res = await db.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        res = await db.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
