import datetime
import calendar

from typing import  Union, List
from models import  User as ModelUser, KomentarPengumuman as ModelKomentarPengumuman, Pengumuman as ModelPengumuman
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class user(BaseModel):
    username: str
    full_name: Union[str, None] = None

class schemaUser(user):
    id: int

class KomentarPengumumanIn(BaseModel):
    title: str
    isi: str
    pengumuman_id: int
    user_id: int

class schemaDBKomentarPengumuman(BaseModel):
    title: str
    isi: str
    pengumuman_id: int
    created_by: int
    created_at_epoch_utc: int
    updated_at_epoch_utc: int

class KomentarPengumumanOut(BaseModel):
    id: int
    title: str
    isi: str
    created_user: schemaUser
    created_at_utc: int
    updated_at_utc: int

class KomentarPengumumanUpdate(BaseModel):
    title: Union[str, None] = None
    isi: Union[str, None] = None

router =  APIRouter()

@router.post("", status_code=201)
async def create_komentar_pengumuman(new_komentar_pengumuman: KomentarPengumumanIn):
    check_user = await ModelUser.get(new_komentar_pengumuman.user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    check_pengumuman = await ModelPengumuman.get(new_komentar_pengumuman.pengumuman_id)
    if check_pengumuman == None:
        return JSONResponse(content={"error": "Pengumuman not exist"}, status_code=400)
    dbObj = schemaDBKomentarPengumuman(
        title=new_komentar_pengumuman.title,
        isi=new_komentar_pengumuman.isi,
        pengumuman_id=new_komentar_pengumuman.pengumuman_id,
        created_by=new_komentar_pengumuman.user_id,
        created_at_epoch_utc=calendar.timegm(datetime.datetime.utcnow().timetuple()),
        updated_at_epoch_utc=calendar.timegm(datetime.datetime.utcnow().timetuple()),
    )

    komentar_pengumuman_id = await ModelKomentarPengumuman.create(**dbObj.dict())
    return {"komentar_pengumuman_id": komentar_pengumuman_id}

@router.get("/all",response_model=List[KomentarPengumumanOut])
async def get_all_komentar_pengumuman():
    komentar_pengumumans = await ModelKomentarPengumuman.get_all()
    out_list = []
    for p in komentar_pengumumans:
        user_komentar_pengumuman_created = await ModelUser.get_by_user_id(p.created_by)
        out = KomentarPengumumanOut(id=p.id,title=p.title,isi=p.isi,
            created_at_utc=p.created_at_epoch_utc,updated_at_utc=p.updated_at_epoch_utc,
            created_user=schemaUser(id=user_komentar_pengumuman_created.id,username=user_komentar_pengumuman_created.username,full_name=user_komentar_pengumuman_created.full_name))
        out_list.append(out)
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/{id}", response_model=KomentarPengumumanOut)
async def get_komentar_pengumuman_by_id(id: int):
    p = await ModelKomentarPengumuman.get(id)
    if p == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    user_komentar_pengumuman_created = await ModelUser.get_by_user_id(p.created_by)
    out = KomentarPengumumanOut(id=p.id,title=p.title,isi=p.isi,
            created_at_utc=p.created_at_epoch_utc,updated_at_utc=p.updated_at_epoch_utc,
            created_user=schemaUser(id=user_komentar_pengumuman_created.id,username=user_komentar_pengumuman_created.username,full_name=user_komentar_pengumuman_created.full_name))
    return out

@router.get("/all/{pengumuan_id}",response_model=List[KomentarPengumumanOut])
async def get_all_komentar_pengumuman(pengumuan_id:int):
    komentar_pengumumans = await ModelKomentarPengumuman.get_by_pengumuman_id(pengumuan_id)
    out_list = []
    for p in komentar_pengumumans:
        user_komentar_pengumuman_created = await ModelUser.get_by_user_id(p.created_by)
        out = KomentarPengumumanOut(id=p.id,title=p.title,isi=p.isi,
            created_at_utc=p.created_at_epoch_utc,updated_at_utc=p.updated_at_epoch_utc,
            created_user=schemaUser(id=user_komentar_pengumuman_created.id,username=user_komentar_pengumuman_created.username,full_name=user_komentar_pengumuman_created.full_name))
        out_list.append(out)
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.delete("/{id}")
async def delete_komentar_pengumuman_by_id(id: int):
    komentar_pengumuman = await ModelKomentarPengumuman.get(id)
    if komentar_pengumuman == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    await ModelKomentarPengumuman.delete(id)
    return JSONResponse(content={"id": id, "message": "Success Delete KomentarPengumuman ID"}, status_code=200)

@router.put("/{id}")
async def update_komentar_pengumuman(id: int, updated_komentar_pengumuman: KomentarPengumumanUpdate):
    curr_komentar_pengumuman = await ModelKomentarPengumuman.get(id)
    if curr_komentar_pengumuman == None:
        return JSONResponse(content={"error": "KomentarPengumuman with specified id not found"}, status_code=400)
    cp = schemaDBKomentarPengumuman(
        title=curr_komentar_pengumuman.title,
        isi=curr_komentar_pengumuman.isi,
        pengumuman_id=curr_komentar_pengumuman.pengumuman_id,
        created_by=curr_komentar_pengumuman.created_by,
        created_at_epoch_utc=curr_komentar_pengumuman.created_at_epoch_utc,
        updated_at_epoch_utc=curr_komentar_pengumuman.updated_at_epoch_utc,
    )
    cp.updated_at_epoch_utc = calendar.timegm(datetime.datetime.utcnow().timetuple())
    if updated_komentar_pengumuman.title != None:
        cp.title = updated_komentar_pengumuman.title
    if updated_komentar_pengumuman.isi != None:
        cp.isi = updated_komentar_pengumuman.isi
    await ModelKomentarPengumuman.update(id, **cp.dict())
    return JSONResponse(content={"id": id, "message": "Success Update KomentarPengumuman"}, status_code=200)