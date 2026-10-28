from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI

from .database import create_all_tables
from .rasp.rfid_reader import MFRC522Reader
from .rasp.services import RFIDReaderProtocol
from .service_registry import register_services


def create_app(rfid_reader: RFIDReaderProtocol | None = None) -> FastAPI:
    if rfid_reader is None:
        rfid_reader = MFRC522Reader()
        
    services = register_services(rfid_reader)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        create_all_tables()
        listener = Thread(
            target=services.rfid_room_service.listen_for_tags,
            name="rfid-listener",
            daemon=True,
        )
        listener.start()
        try:
            yield
        finally:
            services.raspberry_pi_service.stop()
            listener.join()
            services.raspberry_pi_service.close()

    app = FastAPI(lifespan=lifespan)
    
    app.state.services = services
    
    services.room_controller.register_endpoints(app)
    services.role_controller.register_endpoints(app)
    services.collaborator_controller.register_endpoints(app)
    services.room_control_controller.register_endpoints(app)
    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app)
