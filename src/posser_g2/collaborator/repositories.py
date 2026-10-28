from collections.abc import Callable
from contextlib import AbstractContextManager
from sqlmodel import Session, select, and_
from typing import Sequence
from uuid import UUID

from ..tables import Collaborator, Role, Room

from .schemas import (
    CreateCollaboratorBody,
    GetCollaboratorsParams,
)


class CollaboratorRepository:
    def __init__(self, session: Callable[[], AbstractContextManager[Session]]):
        self._session = session
        
        
    def _get_collaborator(self, collaborator_id: UUID) -> Collaborator | None:
        with self._session() as session:
            return session.get(Collaborator, collaborator_id)
        
        
    def get_collaborator_by_id(self, collaborator_id: UUID) -> Collaborator | None:
        return self._get_collaborator(collaborator_id)
    
    
    def get_collaborators(self, params: GetCollaboratorsParams) -> Sequence[Collaborator]:
        with self._session() as session:
            query = select(Collaborator)
            
            filters = []
            
            if params.role_id is not None:
                filters.append(Collaborator.role_id == params.role_id)
                
            if params.rfid_tag is not None:
                filters.append(Collaborator.rfid_tag == params.rfid_tag)
                
            if params.name is not None:
                filters.append(Collaborator.name.ilike(f"%{params.name}%"))
            
            if params.room_id is not None:
                filters.append(Role.allowed_rooms.any(Room.id == params.room_id))
                
            if params.active is not None:
                filters.append(Collaborator.active == params.active)
                
            if filters:
                query = query.where(and_(*filters))
            
            return session.exec(query).all()
        
        
    def create_collaborator(self, new_collaborator: CreateCollaboratorBody):
        with self._session() as session:
            collaborator = Collaborator(**new_collaborator.model_dump())
            
            session.add(collaborator)
            session.commit()
            session.refresh(collaborator)
            
            return collaborator
        
        
    def update_collaborator(
        self, 
        collaborator_id: UUID,
        updated_collaborator: CreateCollaboratorBody,
    ) -> Collaborator:
        with self._session() as session:
            collaborator = self._get_collaborator(collaborator_id)
            
            if collaborator is None:
                raise RuntimeError(f'Collaborator {collaborator_id} not found')
            
            collaborator.sqlmodel_update(updated_collaborator.model_dump(exclude_unset=True))
            
            session.add(collaborator)
            session.commit()
            session.refresh(collaborator)
            
            return collaborator
        
        
    def delete_collaborator(self, collaborator_id: UUID) -> Collaborator:
        with self._session() as session:
            collaborator = self._get_collaborator(collaborator_id)
            
            if collaborator is None:
                raise RuntimeError(f'Collaborator {collaborator_id} not found')
            
            session.delete(collaborator)
            session.commit()
            
            return collaborator
