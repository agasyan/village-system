from typing import Union, List
import os

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from models import User as ModelUser, Role as ModelRole, UserRole as ModelUserRole, RolePage as ModelRP, Page as ModelPage, Document as ModelDoc, Laporan as ModelLap, Pengumuman as ModelPengumuman, KomentarPengumuman as ModelKP
from schema import RoleOut as SchemaRoleOutput, PageOut as SchemaPageOut
from routers.token_router import TokenData as SchemaTokenData


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

class UserAll(User):
    id: int

class UserCreate(User):
    password: str
    role_ids: List[int] = []

class UserOut(UserAll):
    roles: List[SchemaRoleOutput] = []
    pages: List[SchemaPageOut] = []


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router =  APIRouter()


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get("/me", response_model=UserOut)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = SchemaTokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await ModelUser.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    user_roles = await ModelUserRole.get_by_user_id(user.id)
    urs_out = []
    pages_out = []
    for ur in user_roles:
        role_info = await ModelRole.get(ur.role_id)
        role_info_out = SchemaRoleOutput(id=role_info.id, name=role_info.name)
        urs_out.append(role_info_out)

        role_pages = await ModelRP.get_by_role_id(role_info.id)
        for rp in role_pages:
            page_info = await ModelPage.get(rp.page_id)
            page_out = {"id":page_info.id, "name":page_info.name}
            if page_out not in pages_out:
                pages_out.append(page_out)
    out = UserOut(id=user.id, username=user.username, full_name=user.full_name, roles=urs_out, pages=pages_out)
    return out


@router.post("/registration", status_code=201)
async def registration(req_reg: UserCreate):
    if len(req_reg.role_ids) == 0:
        return JSONResponse(content={"error": "Please add role"}, status_code=400)
    role_ids = []
    for i in req_reg.role_ids:
        check_role = await ModelRole.get(i)
        if check_role == None:
            return JSONResponse(content={"error": "Roles not exist"}, status_code=400)
        if i not in role_ids:
            role_ids.append(i)
    fname = ""
    if req_reg.full_name != None:
        fname = req_reg.full_name
    user_id = await ModelUser.create(username=req_reg.username,full_name=fname,hashed_password=get_password_hash(req_reg.password))
    for r_id in role_ids:
        await ModelUserRole.create(user_id=user_id,role_id=r_id)
    return {"user_id": user_id}

@router.get("/all",response_model=List[UserAll])
async def get_all_users():
    users = await ModelUser.get_all()
    if users == None:
        return JSONResponse(content={"error": "No users found"}, status_code=200)
    return users

@router.delete("/{id}")
async def delete_user_by_id(id: int):
    user = await ModelUser.get(id)
    if user == None:
        return JSONResponse(content={"error": "user id not found"}, status_code=400)
    docs = await ModelDoc.get_by_user_id(id)
    if len(docs) != 0:
        doc_ids = []
        for doc in docs:
            doc_ids.append(doc.id)
        return JSONResponse(content={"error": "User have document and still used", "doc_ids": doc_ids}, status_code=400)
    laporans = await ModelLap.get_by_user_id(id)
    if len(laporans) != 0:
        laporan_ids = []
        for doc in laporans:
            laporan_ids.append(doc.id)
        return JSONResponse(content={"error": "User have Laporan and still used", "laporan_ids": laporan_ids}, status_code=400)
    pengumumans = await ModelPengumuman.get_by_user_id(id)
    if len(pengumumans) != 0:
        penguman_ids = []
        for doc in pengumumans:
            penguman_ids.append(doc.id)
        return JSONResponse(content={"error": "User have pengumuman and still used", "penguman_ids": penguman_ids}, status_code=400)
    komentar_pengumans = await ModelKP.get_by_user_id(id)
    if len(komentar_pengumans) != 0:
        kp_ids = []
        for kp in komentar_pengumans:
            kp_ids.append(kp.id)
        return JSONResponse(content={"error": "User have komentar pengumuman and still used", "komentar_pengumuman_ids": kp_ids}, status_code=400)
    await ModelUserRole.delete_by_user_id(id)
    await ModelUser.delete(id)
    return JSONResponse(content={"message": "Success Delete User"}, status_code=200)
