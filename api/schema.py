from pydantic import BaseModel
from typing import Optional


class DocumentType(BaseModel):
    name: str
    desc: Optional[str]

    class Config:
        orm_mode = True

class DocumentTypes(DocumentType):
    id: int
