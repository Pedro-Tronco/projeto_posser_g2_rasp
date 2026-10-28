from collections.abc import Callable
from contextlib import AbstractContextManager
from sqlmodel import Session, select
from typing import Sequence

from ..tables import Role

from .schemas import (
    CreateRoleBody,
)

class RoleRepository:
    def __init__(self, session: Callable[[], AbstractContextManager[Session]]):
        self._session = session
        
        
    def _get_role(self, role_id) -> Role | None:
        with self._session() as session:
            return session.get(Role, role_id)
        
        
    def get_role_by_id(self, role_id: int) -> Role | None:
        return self._get_role(role_id)
    
    
    def get_all_roles(self) -> Sequence[Role]:
        with self._session() as session:
            return session.exec(select(Role)).all()
            
            
    def create_role(self, new_role: CreateRoleBody) -> Role:
        with self._session() as session:
            role = Role(**new_role.model_dump())
    
            session.add(role)
            session.commit()
            session.refresh(role)
            
            return role
        
        
    def update_role(
        self, 
        role_id: int, 
        updated_role: CreateRoleBody,
    ) -> Role:
        with self._session() as session:
            role = self._get_role(role_id)
            
            if role is None:
                raise RuntimeError(f'Role with id "{role_id}" not found.')
            
            role.name = updated_role.name
            
            session.add(role)
            session.commit()
            session.refresh(role)
            
            return role
        
        
    def delete_role(self, role_id: int) -> Role:
        with self._session() as session:
            role = self._get_role(role_id)
            
            if role is None:
                raise RuntimeError(f'Role with id "{role_id}" not found.')
            
            session.delete(role)
            session.commit()
            
            return role