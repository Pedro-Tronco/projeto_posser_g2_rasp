from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Sequence

from ..tables import Collaborator


class CreateCollaboratorBody(BaseModel):
    name: str
    rfid_tag: str
    role_id: Optional[int]
    active: bool = True
    
    
@dataclass(frozen=True, slots=True)
class AllCollaboratorsResponse:
    collaborators: Sequence[Collaborator]
    
    
@dataclass(frozen=True, slots=True)
class CollaboratorResponse:
    collaborator: Collaborator