from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.task_schema import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TaskTransitionDTO,
    TaskResponseDTO,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])
service = TaskService()

@router.post("", response_model=TaskResponseDTO, status_code=201)
async def create_task(payload: TaskCreateDTO, db: AsyncSession = Depends(get_db)):
    task = await service.create_task(db, payload)
    return TaskResponseDTO.model_validate(task)

@router.get("", response_model=list[TaskResponseDTO])
async def list_tasks(
    status: str | None = Query(default=None),
    assignee_user_id: int | None = Query(default=None),
    q: str | None = Query(default=None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    tasks = await service.list_tasks(
        db,
        status=status,
        assignee_user_id=assignee_user_id,
        q=q,
        page=page,
        size=size,
    )
    return [TaskResponseDTO.model_validate(t) for t in tasks]

@router.get("/{task_id}", response_model=TaskResponseDTO)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await service.get_task(db, task_id)
    return TaskResponseDTO.model_validate(task)

@router.patch("/{task_id}", response_model=TaskResponseDTO)
async def update_task(task_id: int, payload: TaskUpdateDTO, db: AsyncSession = Depends(get_db)):
    task = await service.update_task(db, task_id, payload)
    return TaskResponseDTO.model_validate(task)

@router.post("/{task_id}/transition", response_model=TaskResponseDTO)
async def transition_task(task_id: int, payload: TaskTransitionDTO, db: AsyncSession = Depends(get_db)):
    task = await service.transition_task(db, task_id, payload)
    return TaskResponseDTO.model_validate(task)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    await service.delete_task(db, task_id)
    return None
