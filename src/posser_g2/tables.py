from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel


class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    room_control: list["RoomControl"] = Relationship(back_populates="room")


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    collaborators: list["Collaborator"] = Relationship(back_populates="role")
    room_control: list["RoomControl"] = Relationship(back_populates="role")


class Collaborator(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    rfid_tag: str = Field(unique=True, index=True)
    active: bool = Field(default=True)

    role_id: Optional[int] = Field(default=None, foreign_key="role.id")

    role: Optional[Role] = Relationship(back_populates="collaborators")


class RoomControl(SQLModel, table=True):
    room_id: Optional[int] = Field(default=None, foreign_key="room.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)

    room: Optional[Room] = Relationship(back_populates="room_control")
    role: Optional[Role] = Relationship(back_populates="room_control")
