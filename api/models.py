import sqlalchemy
from db import db, metadata, sqlalchemy

document_types = sqlalchemy.Table(
    "document_type",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("desc", sqlalchemy.String),
)

class DocumentType:
    @classmethod
    async def get(cls, id):
        query = document_types.select().where(document_types.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_all(cls):
        query = document_types.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = document_types.insert().values(**doc_type)
        doc_type_id = await db.execute(query)
        return doc_type_id