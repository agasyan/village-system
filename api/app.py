from db import db
from fastapi import FastAPI
from routers import document_types_router, document_status_router, role_router, user_router, role_page_router, page_router, user_role_router, token_router, document_router

app = FastAPI(title="Village System API",root_path="/api")
app.include_router(document_types_router.router, tags=["Document Types"], prefix="/doc-type")
app.include_router(document_status_router.router, tags=["Document Status"], prefix="/doc-status")
app.include_router(document_router.router, tags=["Document"], prefix="/doc")
app.include_router(user_router.router, tags=["User"], prefix="/user")
app.include_router(token_router.router, tags=["User"], prefix="/token")
app.include_router(role_router.router, tags=["Role"], prefix="/role")
app.include_router(page_router.router, tags=["Page"], prefix="/page")
app.include_router(role_page_router.router, tags=["Role-Page"], prefix="/role-page")
app.include_router(user_role_router.router, tags=["User-Role"], prefix="/user-role")

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()