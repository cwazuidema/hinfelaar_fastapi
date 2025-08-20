from fastapi import FastAPI

from app.routers.syntess import router as syntess_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(syntess_router, prefix="/syntess", tags=["syntess"])
    return app


app = create_app()
