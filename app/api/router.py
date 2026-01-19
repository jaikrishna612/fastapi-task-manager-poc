from fastapi import APIRouter

from app.api.controllers.users_controller import router as users_router
from app.api.controllers.tasks_controller import router as tasks_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router)
api_router.include_router(tasks_router)
