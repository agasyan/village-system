from typing import List
from models import DocumentStatus as ModelDocumentStatus
from schema import DocumentStatus as SchemaDocumentStatus
from schema import DocumentStatuses as SchemaDocumentStatuses
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_document_status(document_status: SchemaDocumentStatus):
    check_dt = await ModelDocumentStatus.get_by_name(document_status.name)
    if check_dt != None:
        return JSONResponse(content={"error": "Document Status already exist"}, status_code=400)
    document_status_id = await ModelDocumentStatus.create(**document_status.dict())
    return {"document_status_id": document_status_id}

@router.get("/all",response_model=List[SchemaDocumentStatuses])
async def get_all_doc_status():
    doc_statuses = await ModelDocumentStatus.get_all()
    if doc_statuses == None:
        return JSONResponse(content={"error": "No Document statuses found"}, status_code=200)
    return doc_statuses

@router.get("/{id}", response_model=SchemaDocumentStatuses)
async def get_doc_status_by_id(id: int):
    document_status = await ModelDocumentStatus.get(id)
    if document_status == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    return document_status

@router.delete("/{id}")
async def delete_doc_status_by_id(id: int):
    document_status = await ModelDocumentStatus.get(id)
    if document_status == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    document_status_id = await ModelDocumentStatus.delete(id)
    return document_status_id


