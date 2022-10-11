from db import db
from fastapi import FastAPI
from routers import document_types_router

app = FastAPI(title="Async FastAPI",root_path="/api")
app.include_router(document_types_router.router, tags=["Document Types"], prefix="/doc-type")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()