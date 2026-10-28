from collections import deque
from collections.abc import Callable
from concurrent.futures import Future
from enum import Enum
from threading import Lock
from typing import Protocol

from ..room.schemas import CreateRoomRequest
from ..room.services import RoomService
from .animations import AnimationService
from .schemas import RFIDReadResponse


class RFIDReadState(Enum):
    LISTENING_FOR_TAGS = "listening_for_tags"
    READING_FOR_WEBSOCKET = "reading_for_websocket"


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
        animation_service: AnimationService,
    ) -> None:
        self._raspberry_pi_service = raspberry_pi_service
        self._room_service = room_service
        self._animation_service = animation_service
        self._state = RFIDReadState.LISTENING_FOR_TAGS
        self._state_lock = Lock()
        self._pending_reads: deque[Future[RFIDReadResponse]] = deque()

    @property
    def state(self) -> RFIDReadState:
        with self._state_lock:
            return self._state

    def request_rfid_read(self) -> Future[RFIDReadResponse]:
        future: Future[RFIDReadResponse] = Future()
        with self._state_lock:
            self._pending_reads.append(future)
            self._state = RFIDReadState.READING_FOR_WEBSOCKET
        future.add_done_callback(self._remove_cancelled_read)
        return future

    def listen_for_tags(self) -> None:
        self._animation_service.show_waiting()
        try:
            self._raspberry_pi_service.listen(self._handle_tag)
        finally:
            self._animation_service.stop()

    def _handle_tag(self, rfid_response: RFIDReadResponse) -> None:
        future: Future[RFIDReadResponse] | None = None
        with self._state_lock:
            while self._pending_reads:
                candidate = self._pending_reads.popleft()
                if not candidate.cancelled():
                    future = candidate
                    break
            self._state = (
                RFIDReadState.READING_FOR_WEBSOCKET
                if self._pending_reads
                else RFIDReadState.LISTENING_FOR_TAGS
            )

        if future is not None and future.set_running_or_notify_cancel():
            future.set_result(rfid_response)
            return

        self._create_room_for_tag(rfid_response)

    def _remove_cancelled_read(self, future: Future[RFIDReadResponse]) -> None:
        if not future.cancelled():
            return

        with self._state_lock:
            try:
                self._pending_reads.remove(future)
            except ValueError:
                pass
            self._state = (
                RFIDReadState.READING_FOR_WEBSOCKET
                if self._pending_reads
                else RFIDReadState.LISTENING_FOR_TAGS
            )

    def _create_room_for_tag(
        self,
        rfid_response: RFIDReadResponse,
    ) -> None:
        self._animation_service.beep_rfid_read()
        self._room_service.create_room(
            CreateRoomRequest(name=str(rfid_response.tag))
        )
