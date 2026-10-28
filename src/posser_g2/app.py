from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_all_tables
from .settings import get_settings
from .service_registry import register_services


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        create_all_tables()
        yield

    app = FastAPI(lifespan=lifespan)
    controllers = register_services()
    controllers.room_controller.register_endpoints(app)
    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app)
