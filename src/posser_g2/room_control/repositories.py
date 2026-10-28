from collections.abc import Callable
from contextlib import AbstractContextManager
from sqlmodel import Session, select
from typing import Sequence

from ..tables import RoomControl

from .schemas import (
    CreateRoomControlBody,
    GetRoomControlParams,
)


class RoomControlRepository:
    def __init__(self, session: Callable[[], AbstractContextManager[Session]]):
        self._session = session

    def get_room_control_by_ids(
        self,
        room_id: int,
        role_id: int,
    ) -> RoomControl | None:
        with self._session() as session:
            return session.get(RoomControl, (room_id, role_id))

    def get_room_controls(
        self,
        params: GetRoomControlParams,
    ) -> Sequence[RoomControl]:
        with self._session() as session:
            query = select(RoomControl)

            if params.room_id is not None:
                query = query.where(RoomControl.room_id == params.room_id)

            if params.role_id is not None:
                query = query.where(RoomControl.role_id == params.role_id)

            return session.exec(query).all()

    def create_room_control(
        self,
        new_room_control: CreateRoomControlBody,
    ) -> RoomControl:
        with self._session() as session:
            room_control = RoomControl(**new_room_control.model_dump())
            session.add(room_control)
            session.commit()
            session.refresh(room_control)
            return room_control

    def update_room_control(
        self,
        room_id: int,
        role_id: int,
        updated_room_control: CreateRoomControlBody,
    ) -> RoomControl:
        with self._session() as session:
            room_control = session.get(RoomControl, (room_id, role_id))
            if room_control is None:
                raise RuntimeError(
                    f'Room control for room "{room_id}" and role "{role_id}" not found.'
                )

            room_control.sqlmodel_update(updated_room_control.model_dump())
            session.add(room_control)
            session.commit()
            session.refresh(room_control)
            return room_control

    def delete_room_control(self, room_id: int, role_id: int) -> RoomControl:
        with self._session() as session:
            room_control = session.get(RoomControl, (room_id, role_id))
            if room_control is None:
                raise RuntimeError(
                    f'Room control for room "{room_id}" and role "{role_id}" not found.'
                )

            session.delete(room_control)
            session.commit()
            return room_control
