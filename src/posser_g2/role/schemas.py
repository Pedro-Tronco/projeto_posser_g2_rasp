from pydantic import BaseModel
from dataclasses import dataclass
from typing import Sequence

from ..tables import Role


class CreateRoleBody(BaseModel):
    name: str
    
    
@dataclass(frozen=True, slots=True)
class RoleResponse:
    role: Role
    
    
@dataclass(frozen=True, slots=True)
class AllRolesResponse:
    roles: Sequence[Role]