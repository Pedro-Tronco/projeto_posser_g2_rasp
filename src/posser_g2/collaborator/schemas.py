from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Optional, Sequence

from ..tables import Collaborator


class CreateCollaboratorBody(BaseModel):
    name: str
    rfid_tag: str
    role_id: int
    active: Optional[bool] = True
    
    
class GetCollaboratorsParams(BaseModel):
    room_id: Optional[int] = Field(None, gt=0)
    role_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, min_length=1)
    rfid_tag: Optional[str] = Field(None) 
    active: Optional[bool] = Field(None)
    
@dataclass(frozen=True, slots=True)
class AllCollaboratorsResponse:
    collaborators: Sequence[Collaborator]
    
    
@dataclass(frozen=True, slots=True)
class CollaboratorResponse:
    collaborator: Collaborator