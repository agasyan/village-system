from typing import List
from models import UserRole as ModelUserRole
from schema import UserRole as SchemaUserRole
from schema import UserRoleOut as SchemaUserRoles
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router =  APIRouter()

@router.post("", status_code=201)
async def create_user_role(user_role: SchemaUserRole):
    check_rp = await ModelUserRole.get_by_user_role_id(user_role.role_id, user_role.page_id)
    if check_rp != None:
        return JSONResponse(content={"error": "User Role Combination already exist"}, status_code=400)
    user_role_id = await ModelUserRole.create(**user_role.dict())
    return {"user_role_id": user_role_id}

@router.get("/all",response_model=List[SchemaUserRoles])
async def get_all_user_roles():
    urs = await ModelUserRole.get_all()
    return urs

@router.get("/{id}", response_model=SchemaUserRoles)
async def get_user_role_by_id(id: int):
    user_role = await ModelUserRole.get(id)
    if user_role == None:
        return JSONResponse(content={"error": "User Role id not found"}, status_code=400)
    return user_role

@router.delete("/{id}")
async def delete_user_role_by_id(id: int):
    user_role = await ModelUserRole.get(id)
    if user_role == None:
        return JSONResponse(content={"error": "User Role id not found"}, status_code=400)
    await ModelUserRole.delete(id)
    return JSONResponse(content={"message": "Success Delete User Role"}, status_code=200)

@router.get("/{user_id}/roles",response_model=List[SchemaUserRoles])
async def get_user_role_by_user_id(user_id: int):
    user_roles = await ModelUserRole.get_by_user_id(user_id)
    if user_roles == None:
        return JSONResponse(content={"error": "No User role relation found"}, status_code=200)
    return user_roles
