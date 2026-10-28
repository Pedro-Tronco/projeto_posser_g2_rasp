from fastapi import FastAPI
from dataclasses import asdict

from .services import RoomService

from .schemas import (
    CreateRoomRequest,
)

class RoomController:
    def __init__(self, room_service: RoomService) -> None:
        self._room_service = room_service

    def register_endpoints(self, app: FastAPI) -> None:
        @app.get("/room")
        def get_all_rooms():
            return asdict(
                self._room_service.get_all_rooms()
            )
        
        @app.get("/room/{room_id}")
        def get_room_by_id(room_id: int):
            return asdict(
                self._room_service.get_room(room_id)
            )
        
        @app.post("/room")
        def create_room(room: CreateRoomRequest):
            return asdict(
                self._room_service.create_room(room)
            )
            
            
        @app.put("/room/{room_id}")
        def update_room(room_id: int, room: CreateRoomRequest):
            return asdict(
                self._room_service.update_room(
                    room_id=room_id,
                    new_room=room,
                )
            )
            
            
        @app.delete("/room/{room_id}")
        def delete_room(room_id: int):
            return asdict(
                self._room_service.delete_room(
                    room_id=room_id,
                )
            )