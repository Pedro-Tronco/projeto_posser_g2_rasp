from fastapi import FastAPI, Query
from typing import Annotated
from dataclasses import asdict
from uuid import UUID

from .services import CollaboratorService

from .schemas import (
    CreateCollaboratorBody,
    GetCollaboratorsParams,
)


class CollaboratorController:
    def __init__(self, collaborator_service: CollaboratorService) -> None:
        self._collaborator_service = collaborator_service
        
        
    def register_endpoints(self, app: FastAPI) -> None:
        @app.get("/collaborator")
        def get_collaborators(params: Annotated[GetCollaboratorsParams, Query()]):
            return asdict(
                self._collaborator_service.get_colaborators(params)
            )
            
            
        @app.get("/collaborator/{collaborator_id}")
        def get_collaborator_by_id(collaborator_id: UUID):
            return asdict(
                self._collaborator_service.get_collaborator_by_id(collaborator_id)
            )
            
        
        @app.post("/collaborator")
        def post_collaborator(collaborator: CreateCollaboratorBody):
            return asdict(
                self._collaborator_service.create_collaborator(collaborator)
            )
            
            
        @app.patch("/collaborator/{collaborator_id}")
        def patch_collaborator(collaborator_id: UUID, updated_collaborator: CreateCollaboratorBody):
            return asdict(
                self._collaborator_service.update_collaborator(
                    collaborator_id=collaborator_id,
                    updated_collaborator=updated_collaborator,
                )
            )
            
            
        @app.delete("/collaborator/{collaborator_id}")
        def delete_collaborator(collaborator_id: UUID):
            return asdict(
                self._collaborator_service.delete_collaborator(collaborator_id)
            )