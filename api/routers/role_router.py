from typing import List
from models import Role as ModelRole
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
    if roles == None:
        return JSONResponse(content={"error": "No Roles found"}, status_code=200)
    return roles

@router.get("/{id}", response_model=SchemaRoles)
async def get_role_by_id(id: int):
    role = await ModelRole.get(id)
    if role == None:
        return JSONResponse(content={"error": "Roles id not found"}, status_code=400)
    return role

@router.delete("/{id}")
async def delete_role_by_id(id: int):
    role = await ModelRole.get(id)
    if role == None:
        return JSONResponse(content={"error": "Roles id not found"}, status_code=400)
    role_id = await ModelRole.delete(id)
    return role_id
