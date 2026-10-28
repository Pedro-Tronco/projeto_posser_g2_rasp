from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel


class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    collaborators: list["Colaborator"] = Relationship(back_populates="room")
    allowed_rooms: list["AllowedRooms"] = Relationship(back_populates="room")


class Function(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    collaborators: list["Colaborator"] = Relationship(back_populates="function")
    allowed_rooms: list["AllowedRooms"] = Relationship(back_populates="function")


class Colaborator(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    rfid_tag: str = Field(unique=True, index=True)
    active: bool = Field(default=True)

    room_id: Optional[int] = Field(default=None, foreign_key="room.id")
    function_id: Optional[int] = Field(default=None, foreign_key="function.id")

    room: Optional[Room] = Relationship(back_populates="collaborators")
    function: Optional[Function] = Relationship(back_populates="collaborators")


class AllowedRooms(SQLModel, table=True):
    room_id: Optional[int] = Field(default=None, foreign_key="room.id", primary_key=True)
    function_id: Optional[int] = Field(default=None, foreign_key="function.id", primary_key=True)

    room: Optional[Room] = Relationship(back_populates="allowed_rooms")
    function: Optional[Function] = Relationship(back_populates="allowed_rooms")
