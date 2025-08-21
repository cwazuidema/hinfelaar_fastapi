from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from app.models import TORTOISE_ORM

from app.routers.syntess import router as syntess_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(syntess_router, prefix="/syntess", tags=["syntess"])
    # Register Tortoise ORM with FastAPI
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,  # Prototype mode: auto-create schemas on startup
        add_exception_handlers=True,
    )

    @app.on_event("startup")
    async def ensure_jsonb_gin_indexes() -> None:
        """
        Ensure GIN index for JSONB columns exists. This is safe and idempotent.
        The database maintains index contents automatically on INSERT/UPDATE/DELETE.
        """
        # Ensure we have a connection (register_tortoise added its own startup handler already)
        conn = Tortoise.get_connection("default")
        # Create GIN index on checklistresponse.answers if it doesn't exist
        await conn.execute_script(
            """
            CREATE INDEX IF NOT EXISTS idx_checklistresponse_answers_gin
            ON checklistresponse USING GIN (answers);
            """
        )

    return app


app = create_app()