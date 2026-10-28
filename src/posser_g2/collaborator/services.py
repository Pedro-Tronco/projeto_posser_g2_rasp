from fastapi import HTTPException
from uuid import UUID

from .repositories import CollaboratorRepository

from .schemas import (
    CreateCollaboratorBody,
    GetCollaboratorsParams,
    AllCollaboratorsResponse,
    CollaboratorResponse,
)


class CollaboratorService:
    def __init__(self, collaborator_repo: CollaboratorRepository) -> None:
        self._collaborator_repo = collaborator_repo
        
        
    def get_colaborators(self, params: GetCollaboratorsParams) -> AllCollaboratorsResponse:
        return AllCollaboratorsResponse(
            collaborators=self._collaborator_repo.get_collaborators(params)
        )
        
        
    def get_collaborator_by_id(self, collaborator_id: UUID) -> CollaboratorResponse:
        collaborator = self._collaborator_repo.get_collaborator_by_id(collaborator_id)
        
        if collaborator is None:
            raise HTTPException(status_code=204)
        
        return CollaboratorResponse(
            collaborator=collaborator
        )
        
        
    def create_collaborator(self, collaborator: CreateCollaboratorBody) -> CollaboratorResponse:
        if any(
            self._collaborator_repo.get_collaborators(GetCollaboratorsParams(
                rfid_tag=collaborator.rfid_tag,
                active=None,
                room_id=None,
                name=None,
                role_id=None,
            ))
        ):
            raise HTTPException(status_code=400, detail=f'RFID {collaborator.rfid_tag} já cadastrado para outro Colaborador')
                                                     
        return CollaboratorResponse(
            collaborator=self._collaborator_repo.create_collaborator(collaborator)
        )
        
        
    def update_collaborator(
        self,
        collaborator_id: UUID,
        updated_collaborator: CreateCollaboratorBody,
    ) -> CollaboratorResponse:
        collaborator = self._collaborator_repo.get_collaborator_by_id(collaborator_id)
        
        if collaborator is None:
            raise HTTPException(status_code=204)
        
        return CollaboratorResponse(
            collaborator=self._collaborator_repo.update_collaborator(
                collaborator_id=collaborator_id,
                updated_collaborator=updated_collaborator,
            )
        )
        
        
    def delete_collaborator(self, collaborator_id: UUID) -> CollaboratorResponse:
        collaborator = self._collaborator_repo.get_collaborator_by_id(collaborator_id)
        
        if collaborator is None:
            raise HTTPException(status_code=204)
        
        return CollaboratorResponse(
            collaborator=self._collaborator_repo.delete_collaborator(collaborator_id)
        )
        