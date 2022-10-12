import sqlalchemy as sa
from db import db, metadata
from sqlalchemy.orm import relationship

document_types = sa.Table(
    "document_type",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, unique=True),
    sa.Column("desc", sa.String),
    extend_existing = True
)

document_status = sa.Table(
    "document_status",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, unique=True),
    sa.Column("desc", sa.String),
    extend_existing = True
)

document = sa.Table(
    "document",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("judul", sa.String, unique=True),
    sa.Column("deskripsi", sa.Text),
    sa.Column("doc_status_id", sa.ForeignKey("document_status.id"), nullable=False),
    sa.Column("doc_type_id", sa.ForeignKey("document_type.id"), nullable=False),
    sa.Column("doc_user_id", sa.ForeignKey("user.id"), nullable=False),
    extend_existing = True
)

user = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String, unique=True),
    sa.Column("hashed_password", sa.Text, nullable=False),
    extend_existing = True
)

role = sa.Table(
    "role",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, unique=True),
    extend_existing = True
)

page = sa.Table(
    "page",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, unique=True),
    extend_existing = True
)

user_role = sa.Table(
    "user_role",
    metadata,
    sa.Column("user_id", sa.ForeignKey("user.id"), nullable=False),
    sa.Column("role_id", sa.ForeignKey("role.id"), nullable=False),
    extend_existing = True
)

role_page = sa.Table(
    "role_page",
    metadata,
    sa.Column("page_id", sa.ForeignKey("page.id"), nullable=False),
    sa.Column("role_id", sa.ForeignKey("role.id"), nullable=False),
    extend_existing = True
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
        query = document_status.select().where(document_status.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_by_name(cls, name):
        query = document_status.select().where(document_status.c.name == name)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_all(cls):
        query = document_status.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = document_status.insert().values(**doc_type)
        doc_type_id = await db.execute(query)
        return doc_type_id
    
    @classmethod
    async def delete(cls, id):
        query = document_status.delete().where(document_status.c.id == id)
        doc_type_id = await db.execute(query)
        return doc_type_id