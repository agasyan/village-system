from typing import List, Union

from pydantic import BaseModel
from models import RolePage as ModelRolePage, Page as ModelPage
from schema import RolePage as SchemaRolePage, RolePageOut as SchemaRolePages, PageOut as SchemaPageOut
from fastapi import APIRouter
from fastapi.responses import JSONResponse

class RolePageByRoleID(BaseModel):
    id: int
    role_id: int
    page_detail: Union[SchemaPageOut,None]

router =  APIRouter()

@router.post("", status_code=201)
async def create_role_page(role_page: SchemaRolePage):
    check_rp = await ModelRolePage.get_by_role_id_page_id(role_page.role_id, role_page.page_id)
    if check_rp != None:
        return JSONResponse(content={"error": "Role Page Combination already exist"}, status_code=400)
    role_page_id = await ModelRolePage.create(**role_page.dict())
    return {"role_page_id": role_page_id}

@router.get("/all",response_model=List[SchemaRolePages])
async def get_all_role_pages():
    role_pages = await ModelRolePage.get_all()
    return role_pages

@router.get("/{id}", response_model=SchemaRolePages)
async def get_role_page_by_id(id: int):
    role_page = await ModelRolePage.get(id)
    if role_page == None:
        return JSONResponse(content={"error": "Role Page id not found"}, status_code=400)
    return role_page

@router.delete("/{id}")
async def delete_role_page_by_id(id: int):
    role_page = await ModelRolePage.get(id)
    if role_page == None:
        return JSONResponse(content={"error": "Role Page id not found"}, status_code=400)
    await ModelRolePage.delete(id)
    return JSONResponse(content={"message": "Success Delete Role Page"}, status_code=200)

@router.get("/{role_id}/pages",response_model=List[RolePageByRoleID])
async def get_role_page_by_role_id(role_id: int):
    role_pages = await ModelRolePage.get_by_role_id(role_id)
    if role_pages == None:
        return JSONResponse(content={"error": "No Role Pages found"}, status_code=200)
    out_list = []
    for rp in role_pages:
        page = await ModelPage.get(rp.page_id)
        page_out = SchemaPageOut(id=page.id,name=page.name)
        role_page_by_role_id_out = RolePageByRoleID(id=rp.id, role_id=rp.role_id,page_detail=page_out)
        out_list.append(role_page_by_role_id_out)
    return out_list
