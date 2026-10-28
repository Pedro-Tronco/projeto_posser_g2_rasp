from dataclasses import dataclass

from .database import get_session
from .rasp.animations import AnimationService
from .rasp.services import (
    RaspberryPiService,
    RFIDReaderProtocol,
    RFIDRoomService,
)

from .room.repositories import RoomRepository
from .room.services import RoomService
from .room.controllers import RoomController

from .role.repositories import RoleRepository
from .role.services import RoleService
from .role.controllers import RoleController

from .collaborator.repositories import CollaboratorRepository
from .collaborator.services import CollaboratorService
from .collaborator.controllers import CollaboratorController

from .room_control.repositories import RoomControlRepository
from .room_control.services import RoomControlService
from .room_control.controllers import RoomControlController
    
@dataclass
class ServicesContainer:
    room_controller: RoomController
    role_controller: RoleController
    collaborator_controller: CollaboratorController
    room_control_controller: RoomControlController
    animation_service: AnimationService
    raspberry_pi_service: RaspberryPiService
    rfid_room_service: RFIDRoomService


def register_services(
    rfid_reader: RFIDReaderProtocol,
) -> ServicesContainer:
    room_repository = RoomRepository(get_session)
    room_service = RoomService(room_repo=room_repository)
    room_controller = RoomController(room_service=room_service)
    
    role_repository = RoleRepository(get_session)
    role_service = RoleService(role_repo=role_repository)
    role_controller = RoleController(role_service=role_service)
    
    collaborator_repository = CollaboratorRepository(get_session)
    collaborator_service = CollaboratorService(collaborator_repo=collaborator_repository)
    collaborator_controller = CollaboratorController(collaborator_service=collaborator_service)

    room_control_repository = RoomControlRepository(get_session)
    room_control_service = RoomControlService(room_control_repo=room_control_repository)
    room_control_controller = RoomControlController(
        room_control_service=room_control_service
    )
    
    animation_service = AnimationService()
    raspberry_pi_service = RaspberryPiService(rfid_reader)
    
    rfid_room_service = RFIDRoomService(
        raspberry_pi_service=raspberry_pi_service,
        room_service=room_service,
        animation_service=animation_service,
    )

    return ServicesContainer(
        room_controller=room_controller,
        role_controller=role_controller,
        collaborator_controller=collaborator_controller,
        room_control_controller=room_control_controller,
        animation_service=animation_service,
        raspberry_pi_service=raspberry_pi_service,
        rfid_room_service=rfid_room_service,
    )
