from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.task import Task, TaskStatus

class TaskRepository:
    async def create(self, db: AsyncSession, task: Task) -> Task:
        db.add(task)
        await db.flush()
        await db.refresh(task)
        return task

    async def get_by_id(self, db: AsyncSession, task_id: int) -> Task | None:
        res = await db.execute(select(Task).where(Task.id == task_id))
        return res.scalar_one_or_none()

    async def list_filtered(
        self,
        db: AsyncSession,
        *,
        status: TaskStatus | None,
        assignee_user_id: int | None,
        q: str | None,
        offset: int,
        limit: int,
    ) -> list[Task]:
        stmt = select(Task)

        if status:
            stmt = stmt.where(Task.status == status)
        if assignee_user_id is not None:
            stmt = stmt.where(Task.assignee_user_id == assignee_user_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(Task.title.ilike(like) | Task.description.ilike(like))

        stmt = stmt.order_by(Task.id.desc()).offset(offset).limit(limit)
        res = await db.execute(stmt)
        return list(res.scalars().all())

    async def delete(self, db: AsyncSession, task: Task) -> None:
        await db.delete(task)
        await db.flush()
