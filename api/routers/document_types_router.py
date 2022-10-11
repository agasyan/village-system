from typing import List
from models import DocumentType as ModelDocumentType
from schema import DocumentType as SchemaDocumentType
from schema import DocumentTypes as SchemaDocumentTypes
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_document_type(document_type: SchemaDocumentType):
    check_dt = await ModelDocumentType.get_by_name(document_type.name)
    if check_dt != None:
        return JSONResponse(content={"error": "Mail Types already exist"}, status_code=400)
    document_type_id = await ModelDocumentType.create(**document_type.dict())
    return {"document_type_id": document_type_id}

@router.get("/all",response_model=List[SchemaDocumentTypes])
async def get_all_doc_types():
    dts = await ModelDocumentType.get_all()
    if dts == None:
        return JSONResponse(content={"error": "No Documents found"}, status_code=200)
    return dts

@router.get("/{id}", response_model=SchemaDocumentTypes)
async def get_mail_type_by_id(id: int):
    document_type = await ModelDocumentType.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    return document_type

@router.delete("/{id}")
async def delete_mail_type_by_id(id: int):
    document_type = await ModelDocumentType.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    document_type_id = await ModelDocumentType.delete(id)
    return document_type_id


