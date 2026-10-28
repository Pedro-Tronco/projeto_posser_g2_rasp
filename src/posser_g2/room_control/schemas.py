from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Optional, Sequence

from ..tables import RoomControl


class CreateRoomControlBody(BaseModel):
    room_id: int = Field(gt=0)
    role_id: int = Field(gt=0)


class GetRoomControlParams(BaseModel):
    room_id: Optional[int] = Field(None, gt=0)
    role_id: Optional[int] = Field(None, gt=0)


@dataclass(frozen=True, slots=True)
class AllRoomControlsResponse:
    room_controls: Sequence[RoomControl]


@dataclass(frozen=True, slots=True)
class RoomControlResponse:
    room_control: RoomControl
    