# app/services/task_service.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.task import Task, TaskStatus
from app.repositories.task_repo import TaskRepository


# Business rule: allowed status transitions
ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS, TaskStatus.DONE},
    TaskStatus.IN_PROGRESS: {TaskStatus.DONE},
    TaskStatus.DONE: set(),
}


class TaskService:
    def __init__(self) -> None:
        self.repo = TaskRepository()

    async def create_task(self, db: AsyncSession, dto) -> Task:
        task = Task(
            title=dto.title,
            description=dto.description,
            due_date=dto.due_date,
            assignee_user_id=dto.assignee_user_id,
            status=TaskStatus.TODO,
        )

        await self.repo.create(db, task)
        await db.commit()          # ✅ commit transaction
        await db.refresh(task)     # ✅ reload (id + db defaults)
        return task

    async def get_task(self, db: AsyncSession, task_id: int) -> Task:
        task = await self.repo.get_by_id(db, task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    async def list_tasks(
        self,
        db: AsyncSession,
        *,
        status: str | None,
        assignee_user_id: int | None,
        q: str | None,
        page: int,
        size: int,
    ) -> list[Task]:
        offset = (page - 1) * size

        status_enum = None
        if status:
            # Will raise ValueError if invalid; fine for now (POC)
            status_enum = TaskStatus(status)

        return await self.repo.list_filtered(
            db,
            status=status_enum,
            assignee_user_id=assignee_user_id,
            q=q,
            offset=offset,
            limit=size,
        )

    async def update_task(self, db: AsyncSession, task_id: int, dto) -> Task:
        task = await self.get_task(db, task_id)

        if dto.title is not None:
            task.title = dto.title
        if dto.description is not None:
            task.description = dto.description
        if dto.due_date is not None:
            task.due_date = dto.due_date
        if dto.assignee_user_id is not None:
            task.assignee_user_id = dto.assignee_user_id

        await db.commit()          # ✅ commit changes
        await db.refresh(task)
        return task

    async def transition_task(self, db: AsyncSession, task_id: int, dto) -> Task:
        task = await self.get_task(db, task_id)

        allowed = ALLOWED_TRANSITIONS.get(task.status, set())
        if dto.status not in allowed:
            raise ValueError(f"Invalid transition {task.status} -> {dto.status}")

        task.status = dto.status

        await db.commit()
        await db.refresh(task)
        return task

    async def delete_task(self, db: AsyncSession, task_id: int) -> None:
        task = await self.get_task(db, task_id)

        await self.repo.delete(db, task)
        await db.commit()          # ✅ commit delete
