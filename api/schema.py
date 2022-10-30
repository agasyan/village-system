from pydantic import BaseModel
from typing import Optional


class DocumentType(BaseModel):
    name: str
    desc: Optional[str]

    class Config:
        orm_mode = True

class DocumentTypes(DocumentType):
    id: int

class DocumentStatus(BaseModel):
    name: str
    desc: Optional[str]

    class Config:
        orm_mode = True

class DocumentStatuses(DocumentStatus):
    id: int

class Role(BaseModel):
    name:str

class RoleOut(Role):
    id: int

class Page(BaseModel):
    name:str

class PageOut(Page):
    id: int

class RolePage(BaseModel):
    role_id: int
    page_id: int

class RolePageOut(RolePage):
    id: int

class UserRole(BaseModel):
    role_id: int
    user_id: int

class UserRoleOut(UserRole):
    id: int