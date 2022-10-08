from typing import List, Type
from models import DocumentType as ModelDocumentType
from schema import DocumentType as SchemaDocumentType
from schema import DocumentTypes as SchemaDocumentTypes
from app import app
from fastapi import Request
from fastapi.responses import JSONResponse


@app.post("/mail-type", status_code=201)
async def create_mail_type(document_type: SchemaDocumentType):
    document_type_id = await ModelDocumentType.create(**document_type.dict())
    return {"document_type_id": document_type_id}

@app.get("/mail-types",response_model=List[SchemaDocumentTypes])
async def get_all_mail_type():
    dts = await ModelDocumentType.get_all()
    if dts == None:
        return JSONResponse(content={"error": "No Documents found"}, status_code=200)
    return dts


@app.get("/mail-type/{id}", response_model=SchemaDocumentTypes)
async def get_mail_type_by_id(id: int):
    document_type = await ModelDocumentType.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=200)
    return document_type

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


