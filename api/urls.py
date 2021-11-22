from fastapi.routing import APIRouter

from api.views.file_crud import router as routes

router = APIRouter()

router.include_router(routes)
