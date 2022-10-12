from datetime import datetime, timedelta
from typing import Union, List
import os

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from models import User as ModelUser, Role as ModelRole, UserRole as ModelUserRole
from schema import RoleOut as SchemaRoleOutput
from fastapi.responses import JSONResponse


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

class UserCreate(User):
    password: str
    role_ids: List[int] = []

class UserOut(User):
    roles: List[SchemaRoleOutput] = []


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router =  APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = ModelUser.get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await ModelUser.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    user_roles = await ModelUserRole.get_by_user_id(user.id)
    urs_out = []
    for i in user_roles:
        role_info = await ModelRole.get(i)
        role_info_out = SchemaRoleOutput(name=role_info.name, id=role_info.id)
        urs_out.append(role_info_out)
    out = UserOut(username=user.username,full_name=user.full_name,roles=urs_out)
    return out


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/registration", status_code=201)
async def registration(req_reg: UserCreate):
    if len(req_reg.role_id) == 0:
        return JSONResponse(content={"error": "Please add role"}, status_code=400)
    role_ids = []
    for i in req_reg.role_id:
        check_role = await ModelRole.get(req_reg.role_id)
        if check_role == None:
            return JSONResponse(content={"error": "Roles not exist"}, status_code=400)
        if i not in role_ids:
            role_ids.append(i)
    user_id = await ModelUser.create(username=req_reg.username,full_name=req_reg.full_name,hashed_password=get_password_hash(req_reg.password))
    for r_id in role_ids:
        await ModelUserRole.create(user_id=user_id,role_id=r_id)
    return {"user_id": user_id}

