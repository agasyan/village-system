import sqlalchemy as sa
from db import db, metadata

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
    sa.Column("full_name", sa.String),
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
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.ForeignKey("user.id"), nullable=False),
    sa.Column("role_id", sa.ForeignKey("role.id"), nullable=False),
    extend_existing = True
)

role_page = sa.Table(
    "role_page",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
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

class Role:
    @classmethod
    async def get(cls, id):
        query = role.select().where(role.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_by_name(cls, name):
        query = role.select().where(role.c.name == name)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_all(cls):
        query = role.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = role.insert().values(**doc_type)
        role_id = await db.execute(query)
        return role_id
    
    @classmethod
    async def delete(cls, id):
        query = role.delete().where(role.c.id == id)
        role_id = await db.execute(query)
        return role_id

class Page:
    @classmethod
    async def get(cls, id):
        query = page.select().where(page.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_by_name(cls, name):
        query = page.select().where(page.c.name == name)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_all(cls):
        query = page.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = page.insert().values(**doc_type)
        page_id = await db.execute(query)
        return page_id
    
    @classmethod
    async def delete(cls, id):
        query = page.delete().where(page.c.id == id)
        page_id = await db.execute(query)
        return page_id

class RolePage:
    @classmethod
    async def get(cls, id):
        query = role_page.select().where(role_page.c.id == id)
        return await db.fetch_one(query)

    @classmethod
    async def get_by_role_id(cls, id):
        query = role_page.select().where(role_page.c.role_id == id)
        return await db.fetch_all(query)
    
    @classmethod
    async def get_by_page_id(cls, id):
        query = role_page.select().where(role_page.c.page_id == id)
        return await db.fetch_all(query)

    @classmethod
    async def get_by_role_id_page_id(cls, role_id, page_id):
        query = role_page.select().where(sa.and_(role_page.c.role_id == role_id, role_page.c.page_id == page_id ))
        return await db.fetch_one(query)
    
    @classmethod
    async def get_all(cls):
        query = role_page.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = role_page.insert().values(**doc_type)
        role_page_id = await db.execute(query)
        return role_page_id
    
    @classmethod
    async def delete(cls, id):
        query = role.delete().where(role_page.c.id == id)
        role_page_id = await db.execute(query)
        return role_page_id

class UserRole:
    @classmethod
    async def get(cls, id):
        query = user_role.select().where(user_role.c.id == id)
        return await db.fetch_one(query)

    @classmethod
    async def get_by_user_id(cls, id):
        query = user_role.select().where(user_role.c.user_id == id)
        return await db.fetch_all(query)
    
    @classmethod
    async def get_by_role_id(cls, id):
        query = user_role.select().where(user_role.c.role_id == id)
        return await db.fetch_all(query)
    
    @classmethod
    async def get_by_user_role_id(cls, role_id, user_id):
        query = user_role.select().where(sa.and_(user_role.c.role_id == role_id, user_role.c.user_id == user_id ))
        return await db.fetch_all(query)
    
    @classmethod
    async def get_all(cls):
        query = user_role.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = user_role.insert().values(**doc_type)
        user_role_id = await db.execute(query)
        return user_role_id
    
    @classmethod
    async def delete_by_user_id(cls, id):
        query = user_role.delete().where(user_role.c.user_id == id)
        return await db.fetch_all(query)

    @classmethod
    async def delete(cls, id):
        query = role.delete().where(user_role.c.id == id)
        user_role_id = await db.execute(query)
        return user_role_id

class User:
    @classmethod
    async def get(cls, id):
        query = user.select().where(user.c.id == id)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_by_username(cls, username):
        query = user.select().where(user.c.username == username)
        return await db.fetch_one(query)
    
    @classmethod
    async def get_all(cls):
        query = user.select()
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, **doc_type):
        query = user.insert().values(**doc_type)
        user_id = await db.execute(query)
        return user_id
    
    @classmethod
    async def delete(cls, id):
        query = user.delete().where(user.c.id == id)
        user_id = await db.execute(query)
        return user_id
    