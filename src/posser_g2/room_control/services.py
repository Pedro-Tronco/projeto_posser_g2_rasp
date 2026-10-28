from fastapi import HTTPException

from .repositories import RoomControlRepository
from .schemas import (
    AllRoomControlsResponse,
    CreateRoomControlBody,
    GetRoomControlParams,
    RoomControlResponse,
)


class RoomControlService:
    def __init__(self, room_control_repo: RoomControlRepository) -> None:
        self._room_control_repo = room_control_repo

    def get_room_controls(
        self,
        params: GetRoomControlParams,
    ) -> AllRoomControlsResponse:
        return AllRoomControlsResponse(
            room_controls=self._room_control_repo.get_room_controls(params)
        )

    def get_room_control_by_ids(
        self,
        room_id: int,
        role_id: int,
    ) -> RoomControlResponse:
        room_control = self._room_control_repo.get_room_control_by_ids(
            room_id,
            role_id,
        )
        if room_control is None:
            raise HTTPException(status_code=204)

        return RoomControlResponse(room_control=room_control)

    def create_room_control(
        self,
        room_control: CreateRoomControlBody,
    ) -> RoomControlResponse:
        return RoomControlResponse(
            room_control=self._room_control_repo.create_room_control(room_control)
        )

    def update_room_control(
        self,
        room_id: int,
        role_id: int,
        updated_room_control: CreateRoomControlBody,
    ) -> RoomControlResponse:
        if self._room_control_repo.get_room_control_by_ids(room_id, role_id) is None:
            raise HTTPException(status_code=204)

        return RoomControlResponse(
            room_control=self._room_control_repo.update_room_control(
                room_id=room_id,
                role_id=role_id,
                updated_room_control=updated_room_control,
            )
        )

    def delete_room_control(self, room_id: int, role_id: int) -> RoomControlResponse:
        if self._room_control_repo.get_room_control_by_ids(room_id, role_id) is None:
            raise HTTPException(status_code=204)

        return RoomControlResponse(
            room_control=self._room_control_repo.delete_room_control(room_id, role_id)
        )