from pydantic import BaseModel
from dataclasses import dataclass
from typing import Sequence

from .tables import Room


class CreateRoomRequest(BaseModel):
    name: str
    
    
@dataclass
class GetRoomResponse:
    room: Room
    
    
@dataclass
class GetAllRoomsResponse:
    rooms: Sequence[Room]