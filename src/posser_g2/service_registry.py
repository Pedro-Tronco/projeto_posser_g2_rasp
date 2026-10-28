from dataclasses import dataclass

from .database import get_session
from .rasp.services import (
    RaspberryPiService,
    RFIDReaderProtocol,
    RFIDRoomService,
)

from .room.repositories import RoomRepository
from .room.services import RoomService
from .room.controllers import RoomController
    
@dataclass
class ServicesContainer:
    room_controller: RoomController
    raspberry_pi_service: RaspberryPiService
    rfid_room_service: RFIDRoomService


def register_services(
    rfid_reader: RFIDReaderProtocol,
) -> ServicesContainer:
    room_repository = RoomRepository(get_session)
    room_service = RoomService(room_repo=room_repository)
    room_controller = RoomController(room_service=room_service)
    raspberry_pi_service = RaspberryPiService(rfid_reader)
    rfid_room_service = RFIDRoomService(
        raspberry_pi_service=raspberry_pi_service,
        room_service=room_service,
    )

    return ServicesContainer(
        room_controller=room_controller,
        raspberry_pi_service=raspberry_pi_service,
        rfid_room_service=rfid_room_service,
    )
