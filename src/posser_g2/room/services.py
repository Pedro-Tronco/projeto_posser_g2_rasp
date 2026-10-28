from fastapi import HTTPException

from .repositories import RoomRepository

from .schemas import (
    GetRoomResponse,
    GetAllRoomsResponse,
    CreateRoomRequest,
)

class RoomService:
    def __init__(self, room_repo: RoomRepository) -> None:
        self._room_repo = room_repo
        
        
    def get_room(self, room_id: int) -> GetRoomResponse:
        room = self._room_repo.get_room_by_id(room_id)
        
        if room == None:
            raise HTTPException(status_code=204, detail=f'Room {room_id} not found')
        
        return GetRoomResponse(
            room=room
        )


    def get_all_rooms(self) -> GetAllRoomsResponse:
        return GetAllRoomsResponse(
            rooms=self._room_repo.get_all_rooms()
        )
        
        
    def create_room(
        self, 
        new_room: CreateRoomRequest,
    ) -> GetRoomResponse:
        return GetRoomResponse( 
            room=self._room_repo.create_room(new_room)
        )
        
        
    def update_room(
        self, 
        room_id: int, 
        new_room: CreateRoomRequest,
    ) -> GetRoomResponse:
        if self._room_repo.get_room_by_id(room_id) is None:
            raise HTTPException(status_code = 204, detail=f'Room {room_id} not found')
        
        return GetRoomResponse(
            room=self._room_repo.update_room(room_id=room_id, new_room=new_room)
        )
        

    def delete_room(self, room_id: int) -> GetRoomResponse:
        if self._room_repo.get_room_by_id(room_id) is None:
            raise HTTPException(status_code = 204, detail=f'Room {room_id} not found')
        
        return GetRoomResponse(
            room=self._room_repo.delete_room(room_id)
        )
        
        