from fastapi import FastAPI, APIRouter
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from app.models import TORTOISE_ORM

from app.routers.syntess import router as syntess_router
from app.routers.checklist import router as checklist_router
from app.routers.files import router as files_router
from app.client.async_http_client import (
    initialize_http_client,
    close_http_client,
)


def create_app() -> FastAPI:
    app = FastAPI()
    api_router = APIRouter(prefix="/api")
    api_router.include_router(syntess_router, prefix="/syntess", tags=["Syntess"])
    api_router.include_router(checklist_router, prefix="/checklist", tags=["Checklist"])
    api_router.include_router(files_router, prefix="/files", tags=["Files"])
    app.include_router(api_router)

    # Register Tortoise ORM with FastAPI
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,  # Prototype mode: auto-create schemas on startup
        add_exception_handlers=True,
    )

    @app.on_event("startup")
    async def startup_tasks() -> None:
        """
        Initialize shared async HTTP client and ensure DB indexes.
        """
        # Initialize shared httpx.AsyncClient
        await initialize_http_client()

        # Ensure GIN index for JSONB columns exists. This is safe and idempotent.
        # The database maintains index contents automatically on INSERT/UPDATE/DELETE.
        # Ensure we have a connection (register_tortoise added its own startup handler already)
        conn = Tortoise.get_connection("default")
        # Create GIN index on checklistresponse.answers if it doesn't exist
        await conn.execute_script(
            """
            CREATE INDEX IF NOT EXISTS idx_checklistresponse_answers_gin
            ON checklistresponse USING GIN (answers);
            """
        )

    @app.on_event("shutdown")
    async def shutdown_tasks() -> None:
        # Close shared httpx.AsyncClient
        await close_http_client()

    return app


app = create_app()
