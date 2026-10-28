import asyncio
import json
from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

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
            services.animation_service.close()

    app = FastAPI(lifespan=lifespan)
    
    app.state.services = services

    @app.websocket("/ws/rfid")
    async def rfid_websocket(websocket: WebSocket) -> None:
        await websocket.accept()
        incoming_messages: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
        disconnected = asyncio.Event()

        async def receive_messages() -> None:
            while True:
                message = await websocket.receive()
                if message["type"] == "websocket.disconnect":
                    disconnected.set()
                    await incoming_messages.put(None)
                    return
                await incoming_messages.put(message)

        receiver = asyncio.create_task(receive_messages())
        try:
            while True:
                message = await incoming_messages.get()
                if message is None:
                    return

                text = message.get("text")
                protocol: str | None = None
                if text is not None:
                    try:
                        decoded = json.loads(text)
                    except json.JSONDecodeError:
                        protocol = text
                    else:
                        if isinstance(decoded, dict):
                            candidate = decoded.get("protocol")
                            if isinstance(candidate, str):
                                protocol = candidate
                        elif isinstance(decoded, str):
                            protocol = decoded

                if protocol != "get_rfid":
                    await websocket.send_json({"error": "unsupported_protocol"})
                    continue

                read_future = asyncio.wrap_future(
                    services.rfid_room_service.request_rfid_read()
                )
                disconnect_task = asyncio.create_task(disconnected.wait())
                done, _ = await asyncio.wait(
                    (read_future, disconnect_task),
                    return_when=asyncio.FIRST_COMPLETED,
                )
                if disconnect_task in done:
                    read_future.cancel()
                    await asyncio.gather(read_future, return_exceptions=True)
                    return

                disconnect_task.cancel()
                await asyncio.gather(disconnect_task, return_exceptions=True)
                response = read_future.result()
                await websocket.send_json(
                    {"protocol": "get_rfid", "tag": response.tag}
                )
        except WebSocketDisconnect:
            return
        finally:
            receiver.cancel()
            try:
                await receiver
            except asyncio.CancelledError:
                pass
    
    services.room_controller.register_endpoints(app)
    services.role_controller.register_endpoints(app)
    services.collaborator_controller.register_endpoints(app)
    services.room_control_controller.register_endpoints(app)
    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app)
