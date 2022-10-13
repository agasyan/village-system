from typing import List
from models import DocumentType as ModelDT, DocumentStatus as ModelDS, User as ModelUser, Document as ModelDocument
from schema import DocumentInput as DocIn, DocumentOutput as DocOut
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_document(new_doc: DocIn):
    check_dt = await ModelDT.get(new_doc.doc_type_id)
    if check_dt == None:
        return JSONResponse(content={"error": "Document Types not exist"}, status_code=400)
    check_ds = await ModelDS.get(new_doc.doc_status_id)
    if check_ds == None:
        return JSONResponse(content={"error": "Document Statuses not exist"}, status_code=400)
    check_user = await ModelUser.get(new_doc.user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    document_id = await ModelDocument.create(**new_doc.dict())
    return {"document_id": document_id}

@router.get("/all",response_model=List[DocOut])
async def get_all_doc():
    docs = await ModelDocument.get_all()
    return docs

@router.get("/all/{user_id}",response_model=List[DocOut])
async def get_all_doc_by_user_id(user_id: int):
    docs = await ModelDocument.get_by_user_id(user_id)
    return docs

@router.get("/all/{status_id}",response_model=List[DocOut])
async def get_all_doc_by_status_id(status_id: int):
    docs = await ModelDocument.get_by_document_status_id(status_id)
    return docs

@router.get("/all/{type_id}",response_model=List[DocOut])
async def get_all_doc_by_status_id(type_id: int):
    docs = await ModelDocument.get_by_document_type_id(type_id)
    return docs

@router.get("/{id}", response_model=DocOut)
async def get_doc_by_id(id: int):
    document_type = await ModelDocument.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    return document_type

@router.delete("/{id}")
async def delete_doc_by_id(id: int):
    document_type = await ModelDocument.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    document_type_id = await ModelDocument.delete(id)
    return document_type_id

@router.put("/{id}")
async def update_document(id: int, updated_doc: DocIn):
    curr_dt = await ModelDocument.get(id)
    if curr_dt == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    check_dt = await ModelDT.get(updated_doc.doc_type_id)
    if check_dt == None:
        return JSONResponse(content={"error": "Document Types not exist"}, status_code=400)
    check_ds = await ModelDS.get(updated_doc.doc_status_id)
    if check_ds == None:
        return JSONResponse(content={"error": "Document Statuses not exist"}, status_code=400)
    check_user = await ModelUser.get(updated_doc.user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    await ModelDocument.update(id, **updated_doc.dict())
    return JSONResponse(content={"id": id, "message": "Success Update Document Type"}, status_code=200)