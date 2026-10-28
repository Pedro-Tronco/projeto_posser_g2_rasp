from dataclasses import dataclass

from .database import get_session

from .room.repositories import RoomRepository
from .room.services import RoomService
from .room.controllers import RoomController
    
@dataclass
class ControllersContainer:
    room_controller: RoomController
    

def register_services() -> ControllersContainer:
    room_repository = RoomRepository(get_session)
    room_service = RoomService(room_repo=room_repository)
    room_controller = RoomController(room_service=room_service)
    
    return ControllersContainer(
        room_controller = room_controller
    )