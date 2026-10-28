from collections.abc import Callable
from typing import Protocol

from ..room.schemas import CreateRoomRequest
from ..room.services import RoomService
from .schemas import RFIDReadResponse


class RFIDReaderProtocol(Protocol):
    def read(self) -> int | None:
        ...

    def stop(self) -> None:
        ...

    def close(self) -> None:
        ...


class RaspberryPiService:
    def __init__(self, rfid_reader: RFIDReaderProtocol) -> None:
        self._rfid_reader = rfid_reader

    def listen(self, on_tag: Callable[[RFIDReadResponse], None]) -> None:
        while True:
            tag = self._rfid_reader.read()
            if tag is None:
                return
            on_tag(RFIDReadResponse(tag=tag))

    def stop(self) -> None:
        self._rfid_reader.stop()

    def close(self) -> None:
        self._rfid_reader.close()


class RFIDRoomService:
    def __init__(
        self,
        raspberry_pi_service: RaspberryPiService,
        room_service: RoomService,
    ) -> None:
        self._raspberry_pi_service = raspberry_pi_service
        self._room_service = room_service

    def listen_for_tags(self) -> None:
        self._raspberry_pi_service.listen(self._create_room_for_tag)

    def _create_room_for_tag(
        self,
        rfid_response: RFIDReadResponse,
    ) -> None:
        self._room_service.create_room(
            CreateRoomRequest(name=str(rfid_response.tag))
        )
