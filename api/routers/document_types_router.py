from typing import List
from models import DocumentType as ModelDocumentType, Document as ModelDoc
from schema import DocumentType as SchemaDocumentType
from schema import DocumentTypes as SchemaDocumentTypes
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_document_type(document_type: SchemaDocumentType):
    check_dt = await ModelDocumentType.get_by_name(document_type.name)
    if check_dt != None:
        return JSONResponse(content={"error": "Document Types already exist"}, status_code=400)
    document_type_id = await ModelDocumentType.create(**document_type.dict())
    return {"document_type_id": document_type_id}

@router.get("/all",response_model=List[SchemaDocumentTypes])
async def get_all_doc_types():
    dts = await ModelDocumentType.get_all()
    return dts

@router.get("/{id}", response_model=SchemaDocumentTypes)
async def get_document_type_by_id(id: int):
    document_type = await ModelDocumentType.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    return document_type

@router.delete("/{id}")
async def delete_document_type_by_id(id: int):
    document_type = await ModelDocumentType.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    docs = await ModelDoc.get_by_document_type_id(id)
    if len(docs) != 0:
        doc_ids = []
        for doc in docs:
            doc_ids.append(doc.id)
        return JSONResponse(content={"error": "Doc Types still used", "doc_ids": doc_ids}, status_code=400)
    await ModelDocumentType.delete(id)
    return JSONResponse(content={"id": id, "message": "Success Delete Document Type"}, status_code=200)

@router.put("/{id}")
async def get_document_type_by_id(id: int, document_type: SchemaDocumentType):
    curr_dt = await ModelDocumentType.get(id)
    if curr_dt == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    await ModelDocumentType.update(id, **document_type.dict())
    return JSONResponse(content={"id": id, "message": "Success Update Document Type"}, status_code=200)