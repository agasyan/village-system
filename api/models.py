import sqlalchemy
from db import db, metadata, sqlalchemy

document_types = sqlalchemy.Table(
    "document_type",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("desc", sqlalchemy.String),
    __table_args__ = {'extend_existing': True} 
)

document_status = sqlalchemy.Table(
    "document_status",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("desc", sqlalchemy.String),
    __table_args__ = {'extend_existing': True} 
)

document = sqlalchemy.Table(
    "document",
    metadata,
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    judul = sqlalchemy.Column("judul", sqlalchemy.String, unique=True),
    desc = sqlalchemy.Column("deskripsi", sqlalchemy.String),
    document_status_id = sqlalchemy.Column("doc_status", sqlalchemy.ForeignKey("document_status.id"), nullable=False),
    document_type_id = sqlalchemy.Column("doc_type", sqlalchemy.ForeignKey("document_type.id"), nullable=False),
    __table_args__ = {'extend_existing': True} 
)

class DocumentType:
    @classmethod
    async def get(cls, id):
        query = document_types.select().where(document_types.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_by_name(cls, name):
        query = document_types.select().where(document_types.c.name == name)
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
    
    @classmethod
    async def delete(cls, id):
        query = document_types.delete().where(document_types.c.id == id)
        doc_type_id = await db.execute(query)
        return doc_type_id

class DocumentStatus:
    @classmethod
    async def get(cls, id):
        query = document_types.select().where(document_types.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_by_name(cls, name):
        query = document_types.select().where(document_types.c.name == name)
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
    
    @classmethod
    async def delete(cls, id):
        query = document_types.delete().where(document_types.c.id == id)
        doc_type_id = await db.execute(query)
        return doc_type_id