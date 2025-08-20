from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from app.models import TORTOISE_ORM

from app.routers.syntess import router as syntess_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure default startup/shutdown handlers (e.g., from register_tortoise) run
    async with app.router.lifespan_context(app):
        # After Tortoise is initialized and schemas potentially created, ensure JSONB GIN index exists
        conn = Tortoise.get_connection("default")
        await conn.execute_script(
            """
            CREATE INDEX IF NOT EXISTS idx_checklistresponse_answers_gin
            ON checklistresponse USING GIN (answers);
            """
        )
        yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(syntess_router, prefix="/syntess", tags=["syntess"])
    # Register Tortoise ORM with FastAPI
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,  # Prototype mode: auto-create schemas on startup
        add_exception_handlers=True,
    )
    return app


app = create_app()
