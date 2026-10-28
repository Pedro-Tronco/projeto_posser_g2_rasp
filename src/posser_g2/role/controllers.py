from fastapi import FastAPI
from dataclasses import asdict

from .services import RoleService

from .schemas import (
    CreateRoleBody
)


class RoleController:
    def __init__(self, role_service: RoleService) -> None:
        self._role_service = role_service
        
        
    def register_endpoints(self, app: FastAPI) -> None:
        @app.get("/role")
        def get_all_roles():
            return asdict(
                self._role_service.get_all_roles()
            )
            
            
        @app.get("/role/{role_id}")
        def get_role_by_id(role_id: int):
            return asdict(
                self._role_service.get_role_by_id(role_id)
            )
            
            
        @app.post("/role")
        def post_role(role: CreateRoleBody):
            return asdict(
                self._role_service.create_role(role)
            )
            
            
        @app.patch("/role/{role_id}")
        def patch_role(role_id: int, role: CreateRoleBody):
            return asdict(
                self._role_service.update_role(role_id, role)
            )
            
            
        @app.delete("/role/{role_id}")
        def delete_role(role_id: int):
            return asdict(
                self._role_service.delete_role(role_id)
            )