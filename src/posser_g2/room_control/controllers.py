from dataclasses import asdict
from typing import Annotated

from fastapi import FastAPI, Query

from .schemas import CreateRoomControlBody, GetRoomControlParams
from .services import RoomControlService


class RoomControlController:
    def __init__(self, room_control_service: RoomControlService) -> None:
        self._room_control_service = room_control_service

    def register_endpoints(self, app: FastAPI) -> None:
        @app.get("/room-control")
        def get_room_controls(
            params: Annotated[GetRoomControlParams, Query()],
        ):
            return asdict(self._room_control_service.get_room_controls(params))

        @app.get("/room-control/{room_id}/{role_id}")
        def get_room_control_by_ids(room_id: int, role_id: int):
            return asdict(
                self._room_control_service.get_room_control_by_ids(room_id, role_id)
            )

        @app.post("/room-control")
        def post_room_control(room_control: CreateRoomControlBody):
            return asdict(
                self._room_control_service.create_room_control(room_control)
            )

        @app.patch("/room-control/{room_id}/{role_id}")
        def patch_room_control(
            room_id: int,
            role_id: int,
            updated_room_control: CreateRoomControlBody,
        ):
            return asdict(
                self._room_control_service.update_room_control(
                    room_id=room_id,
                    role_id=role_id,
                    updated_room_control=updated_room_control,
                )
            )

        @app.delete("/room-control/{room_id}/{role_id}")
        def delete_room_control(room_id: int, role_id: int):
            return asdict(
                self._room_control_service.delete_room_control(room_id, role_id)
            )