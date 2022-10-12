from typing import List
from models import RolePage as ModelRolePage
from schema import RolePage as SchemaRolePage
from schema import RolePageOut as SchemaRolePages
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_role_page(role_page: SchemaRolePage):
    check_rp = await ModelRolePage.get_by_role_page_id(role_page.role_id, role_page.page_id)
    if check_rp != None:
        return JSONResponse(content={"error": "Role Page Combination already exist"}, status_code=400)
    role_page_id = await ModelRolePage.create(**role_page.dict())
    return {"role_page_id": role_page_id}

@router.get("/all",response_model=List[SchemaRolePages])
async def get_all_role_pages():
    role_pages = await ModelRolePage.get_all()
    if role_pages == None:
        return JSONResponse(content={"error": "No Role Pages found"}, status_code=200)
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
    role_page_id = await ModelRolePage.delete(id)
    return role_page_id

@router.get("/{role_id}/pages",response_model=List[SchemaRolePages])
async def get_role_page_by_role_id(role_id: int):
    dts = await ModelRolePage.get_by_role_id(role_id)
    if dts == None:
        return JSONResponse(content={"error": "No Role Pages found"}, status_code=200)
    return dts
