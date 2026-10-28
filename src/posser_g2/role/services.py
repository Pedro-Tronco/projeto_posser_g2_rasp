from fastapi import HTTPException

from .repositories import RoleRepository

from .schemas import (
    CreateRoleBody,
    RoleResponse,
    AllRolesResponse,
)


class RoleService:
    def __init__(self, role_repo: RoleRepository) -> None:
        self._role_repo = role_repo
        
        
    def get_role_by_id(self, role_id: int) -> RoleResponse:
        role = self._role_repo.get_role_by_id(role_id)
        
        if role is None:
            raise HTTPException(status_code=204, detail=f'Role "{role_id}" not found')
        
        return RoleResponse(
            role=role
        )
        
        
    def get_all_roles(self) -> AllRolesResponse:
        return AllRolesResponse(
            roles=self._role_repo.get_all_roles()
        )
        
        
    def create_role(self, role: CreateRoleBody) -> RoleResponse:
        return RoleResponse(
            role=self._role_repo.create_role(role)
        )
        
        
    def update_role(
        self,
        role_id: int,
        updated_role: CreateRoleBody,
    ) -> RoleResponse:
        if self._role_repo.get_role_by_id(role_id) is None:
            raise HTTPException(status_code=204, detail=f'Role "{role_id}" not found')
        
        return RoleResponse(
            role=self._role_repo.update_role(
                role_id=role_id,
                updated_role=updated_role,
            )
        )
        
    
    def delete_role(self, role_id: int) -> RoleResponse:
        if self._role_repo.get_role_by_id(role_id) is None:
            raise HTTPException(status_code=204, detail=f'Role "{role_id}" not found')
        
        return RoleResponse(
            role=self._role_repo.delete_role(role_id)
        )
