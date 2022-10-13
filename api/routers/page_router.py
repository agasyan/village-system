from typing import List
from models import Page as ModelPage, RolePage as ModelRolePage
from schema import Page as SchemaPage
from schema import PageOut as SchemaPages
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_page(page: SchemaPage):
    check_dt = await ModelPage.get_by_name(page.name)
    if check_dt != None:
        return JSONResponse(content={"error": "Pages already exist"}, status_code=400)
    page_id = await ModelPage.create(**page.dict())
    return {"page_id": page_id}

@router.get("/all",response_model=List[SchemaPages])
async def get_all_pages():
    pages = await ModelPage.get_all()
    if pages == None:
        return JSONResponse(content={"error": "No pages found"}, status_code=200)
    return pages

@router.get("/{id}", response_model=SchemaPages)
async def get_page_by_id(id: int):
    page = await ModelPage.get(id)
    if page == None:
        return JSONResponse(content={"error": "pages id not found"}, status_code=400)
    return page

@router.delete("/{page_id}")
async def delete_page_by_id(page_id: int):
    page = await ModelPage.get(page_id)
    if page == None:
        return JSONResponse(content={"error": "pages id not found"}, status_code=400)
    role_pages = await ModelRolePage.get_by_page_id(page_id)
    if role_pages != None:
        page_ids = []
        for rp in role_pages:
            page_ids.append(rp.page_id)
        return JSONResponse(content={"error": "Pages still used", "role_ids": page_ids}, status_code=400)
    page_id = await ModelPage.delete(page_id)
    return page_id
