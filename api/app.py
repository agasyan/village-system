from db import db
from fastapi import FastAPI

app = FastAPI(title="Async FastAPI",root_path="/api")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()