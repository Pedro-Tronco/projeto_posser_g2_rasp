from collections.abc import Callable
from contextlib import AbstractContextManager
from sqlmodel import Session, select
from typing import Sequence

from .tables import (
    Room, 
)

from .schemas import (
    CreateRoomRequest
)


class RoomRepository:
    def __init__(self, session: Callable[[], AbstractContextManager[Session]]):
        self._session = session
        
        
    def get_room_by_id(self, room_id: int) -> Room | None:
        with self._session() as session:
            return session.get(Room, room_id)
    
    
    def get_all_rooms(self) -> Sequence[Room]:
        with self._session() as session:
            return session.exec(select(Room)).all()
    
    
    def create_room(self, room: CreateRoomRequest) -> Room:
        with self._session() as session:
            db_room = Room(**room.model_dump())
            session.add(db_room)
            session.commit()
            session.refresh(db_room)
            return db_room
        
        
    def update_room(self, room_id: int, new_room: CreateRoomRequest) -> Room:
        with self._session() as session:
            room = session.get(Room, room_id)
            if room is None:
                raise RuntimeError(f'Room {room_id} not found in DB')

            room.name = new_room.name
            session.add(room)
            session.commit()
            session.refresh(room)
            
            return room
        
    
    def delete_room(self, room_id: int) -> Room:
        with self._session() as session:
            room = session.get(Room, room_id)
            if room is None:
                raise RuntimeError(f'Room {room_id} not found in DB')
            
            session.delete(room)
            session.commit()
            
            return room
        