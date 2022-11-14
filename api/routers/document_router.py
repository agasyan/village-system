from typing import Union,List

from models import DocumentType as ModelDT, DocumentStatus as ModelDS, User as ModelUser, Document as ModelDocument
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schema import DocumentStatuses as SchemaDS, DocumentTypes as SchemaDT
from pydantic import BaseModel

class user(BaseModel):
    username: str
    full_name: Union[str, None] = None

class schemaUser(user):
    id: int

class DocumentOutput(BaseModel):
    id: int
    judul: str
    deskripsi: str
    doc_status: SchemaDS
    doc_type: SchemaDT
    created_by_user: schemaUser

class DocumentInput(BaseModel):
    judul: str
    deskripsi: str
    doc_status_id: int
    doc_type_id: int
    doc_user_id: int

class DocumentUpdate(BaseModel):
    judul: Union[str, None] = None
    deskripsi: Union[str, None] = None
    doc_status_id: Union[int, None] = None
    doc_type_id: Union[int, None] = None
    doc_user_id: Union[int, None] = None

router =  APIRouter()

@router.post("", status_code=201)
async def create_document(new_doc: DocumentInput):
    check_dt = await ModelDT.get(new_doc.doc_type_id)
    if check_dt == None:
        return JSONResponse(content={"error": "Document Types not exist"}, status_code=400)
    check_ds = await ModelDS.get(new_doc.doc_status_id)
    if check_ds == None:
        return JSONResponse(content={"error": "Document Statuses not exist"}, status_code=400)
    check_user = await ModelUser.get(new_doc.doc_user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    document_id = await ModelDocument.create(**new_doc.dict())
    return {"document_id": document_id}

@router.get("/all",response_model=List[DocumentOutput])
async def get_all_doc():
    docs = await ModelDocument.get_all()
    out_list = []
    for d in docs:
        out = await helper_add(d)
        out_list.append(out) 
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/all/{user_id}",response_model=List[DocumentOutput])
async def get_all_doc_by_user_id(user_id: int):
    docs = await ModelDocument.get_by_user_id(user_id)
    out_list = []
    for d in docs:
        out = await helper_add(d)
        out_list.append(out) 
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/all/{status_id}",response_model=List[DocumentOutput])
async def get_all_doc_by_status_id(status_id: int):
    docs = await ModelDocument.get_by_document_status_id(status_id)
    out_list = []
    for d in docs:
        out = await helper_add(d)
        out_list.append(out) 
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/all/{type_id}",response_model=List[DocumentOutput])
async def get_all_doc_by_status_id(type_id: int):
    docs = await ModelDocument.get_by_document_type_id(type_id)
    out_list = []
    for d in docs:
        out = await helper_add(d)
        out_list.append(out) 
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/{id}", response_model=DocumentOutput)
async def get_doc_by_id(id: int):
    document = await ModelDocument.get(id)
    if document == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    out = await helper_add(document)
    return out

@router.delete("/{id}")
async def delete_doc_by_id(id: int):
    document_type = await ModelDocument.get(id)
    if document_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    document_type_id = await ModelDocument.delete(id)
    return document_type_id

@router.put("/{id}")
async def update_document(id: int, updated_doc: DocumentUpdate):
    curr_doc = await ModelDocument.get(id)
    if curr_doc == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    if updated_doc.judul != None:
        curr_doc.judul = updated_doc.judul
    if updated_doc.deskripsi != None:
        curr_doc.deskripsi = updated_doc.deskripsi
    if updated_doc.doc_type_id != None:
        check_dt = await ModelDT.get(updated_doc.doc_type_id)
        if check_dt == None:
            return JSONResponse(content={"error": "Document Types not exist"}, status_code=400)
        curr_doc.doc_type_id = updated_doc.doc_type_id
    if updated_doc.doc_status_id != None:
        check_ds = await ModelDS.get(updated_doc.doc_status_id)
        if check_ds == None:
            return JSONResponse(content={"error": "Document Statuses not exist"}, status_code=400)
        curr_doc.doc_status_id = updated_doc.doc_status_id
    if updated_doc.doc_user_id != None:
        check_user = await ModelUser.get(updated_doc.doc_user_id)
        if check_user == None:
            return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
        curr_doc.doc_user_id = updated_doc.doc_user_id
    newDoc = DocumentInput(
        judul=curr_doc.judul,
        deskripsi=curr_doc.deskripsi,
        doc_status_id=curr_doc.doc_status_id,
        doc_type_id=curr_doc.doc_type_id,
        doc_user_id=curr_doc.doc_user_id
    )
    await ModelDocument.update(id, **newDoc.dict())
    return JSONResponse(content={"id": id, "message": "Success Update Document"}, status_code=200)

async def helper_add(doc):
    user_doc = await ModelUser.get_by_user_id(doc.doc_user_id)
    doc_status = await ModelDS.get(doc.doc_status_id)
    doc_type = await ModelDT.get(doc.doc_type_id)
    output = DocumentOutput(
        id=doc.id,
        judul=doc.judul,
        deskripsi=doc.deskripsi,
        doc_status=SchemaDS(id=doc_status.id,name=doc_status.name,desc=doc_status.desc),
        doc_type=SchemaDT(id=doc_type.id,name=doc_type.name,desc=doc_type.desc),
        created_by_user=schemaUser(id=user_doc.id,username=user_doc.username,full_name=user_doc.full_name),
    )
    return output