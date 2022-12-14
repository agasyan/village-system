from typing import List
from models import Role as ModelRole, RolePage as ModelRolePage, UserRole as ModelUserRole
from schema import Role as SchemaRole
from schema import RoleOut as SchemaRoles
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_role(role: SchemaRole):
    check_dt = await ModelRole.get_by_name(role.name)
    if check_dt != None:
        return JSONResponse(content={"error": "Role already exist"}, status_code=400)
    role_id = await ModelRole.create(**role.dict())
    return {"role_id": role_id}

@router.get("/all",response_model=List[SchemaRoles])
async def get_all_roles():
    roles = await ModelRole.get_all()
    return roles

@router.get("/{id}", response_model=SchemaRoles)
async def get_role_by_id(id: int):
    role = await ModelRole.get(id)
    if role == None:
        return JSONResponse(content={"error": "Roles id not found"}, status_code=400)
    return role

@router.delete("/{role_id}")
async def delete_role_by_id(role_id: int):
    role = await ModelRole.get(role_id)
    if role == None:
        return JSONResponse(content={"error": "Roles id not found"}, status_code=400)
    user_roles = await ModelUserRole.get_by_role_id(role_id)
    role_pages = await ModelRolePage.get_by_role_id(role_id)
    if len(role_pages) != 0:
        page_ids = []
        for rp in role_pages:
            page_ids.append(rp.page_id)
        return JSONResponse(content={"error": "Roles still used", "page_ids": page_ids}, status_code=400)
    if len(user_roles) != 0:
        user_ids = []
        for ur in user_roles:
            user_ids.append(ur.user_id)
        return JSONResponse(content={"error": "Roles still used", "user_ids": user_ids}, status_code=400)
    await ModelRole.delete(role_id)
    return JSONResponse(content={"message": "Success Delete Role"}, status_code=200)