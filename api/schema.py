from pydantic import BaseModel


class DocumentType(BaseModel):
    name: str
    desc: str

    class Config:
        orm_mode = True

class DocumentTypes(BaseModel):
    id: int
    name: str
    desc: str

    class Config:
        orm_mode = True