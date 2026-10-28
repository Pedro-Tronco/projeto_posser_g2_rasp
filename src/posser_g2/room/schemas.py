from pydantic import BaseModel
from dataclasses import dataclass
from typing import Sequence

from ..tables import Room


class CreateRoomRequest(BaseModel):
    name: str
    
    
@dataclass(frozen=True, slots=True)
class GetRoomResponse:
    room: Room
    
    
@dataclass(frozen=True, slots=True)
class GetAllRoomsResponse:
    rooms: Sequence[Room]