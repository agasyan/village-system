import datetime
import calendar

from typing import  Union, List
from models import  User as ModelUser, Pengumuman as ModelPengumuman, KomentarPengumuman as ModelKP
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class user(BaseModel):
    username: str
    full_name: Union[str, None] = None

class schemaUser(user):
    id: int

class PengumumanIn(BaseModel):
    title: str
    isi: str
    gambar: str
    user_id: int

class schemaDBPengumuman(BaseModel):
    title: str
    isi: str
    gambar: str
    created_by: int
    created_at_epoch_utc: int
    updated_by: int
    updated_at_epoch_utc: int

class PengumumanOut(BaseModel):
    id: int
    title: str
    isi: str
    gambar: str
    created_user: schemaUser
    updated_user: schemaUser
    created_at_utc: int
    updated_at_utc: int

class PengumumanUpdate(BaseModel):
    title: Union[str, None] = None
    isi: Union[str, None] = None
    gambar: Union[str, None] = None
    update_user_id: int

router =  APIRouter()

@router.post("", status_code=201)
async def create_pengumuman(new_pengumuman: PengumumanIn):
    check_user = await ModelUser.get(new_pengumuman.user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    if not new_pengumuman.gambar.endswith(".png") and not new_pengumuman.gambar.endswith(".jpg") and not new_pengumuman.gambar.endswith(".jpeg") and not new_pengumuman.gambar.endswith(".webp"):
        return JSONResponse(content={"error": "Gambar URL is not valid"}, status_code=400)
    dbObj = schemaDBPengumuman(
        title=new_pengumuman.title,
        isi=new_pengumuman.isi,
        gambar=new_pengumuman.gambar,
        created_by=new_pengumuman.user_id,
        updated_by=new_pengumuman.user_id,
        created_at_epoch_utc=calendar.timegm(datetime.datetime.utcnow().timetuple()),
        updated_at_epoch_utc=calendar.timegm(datetime.datetime.utcnow().timetuple()),
    )

    pengumuman_id = await ModelPengumuman.create(**dbObj.dict())
    return {"pengumuman_id": pengumuman_id}

@router.get("/all",response_model=List[PengumumanOut])
async def get_all_pengumuman():
    pengumumans = await ModelPengumuman.get_all()
    out_list = []
    for p in pengumumans:
        user_pengumuman_created = await ModelUser.get_by_user_id(p.created_by)
        user_pengumuman_updated = await ModelUser.get_by_user_id(p.updated_by)
        out = PengumumanOut(id=p.id,title=p.title,isi=p.isi,
            created_at_utc=p.created_at_epoch_utc,updated_at_utc=p.updated_at_epoch_utc,gambar=p.gambar,
            created_user=schemaUser(id=user_pengumuman_created.id,username=user_pengumuman_created.username,full_name=user_pengumuman_created.full_name),
            updated_user=schemaUser(id=user_pengumuman_updated.id,username=user_pengumuman_updated.username,full_name=user_pengumuman_updated.full_name))
        out_list.append(out)
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/{id}", response_model=PengumumanOut)
async def get_pengumuman_by_id(id: int):
    p = await ModelPengumuman.get(id)
    if p == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    user_pengumuman_created = await ModelUser.get_by_user_id(p.created_by)
    user_pengumuman_updated = await ModelUser.get_by_user_id(p.updated_by)
    out = PengumumanOut(id=p.id,title=p.title,isi=p.isi,
            created_at_utc=p.created_at_epoch_utc,updated_at_utc=p.updated_at_epoch_utc,gambar=p.gambar,
            created_user=schemaUser(id=user_pengumuman_created.id,username=user_pengumuman_created.username,full_name=user_pengumuman_created.full_name),
            updated_user=schemaUser(id=user_pengumuman_updated.id,username=user_pengumuman_updated.username,full_name=user_pengumuman_updated.full_name))
    return out

@router.delete("/{id}")
async def delete_pengumuman_by_id(id: int):
    pengumuman = await ModelPengumuman.get(id)
    if pengumuman == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    kps = await ModelKP.get_by_pengumuman_id(id)
    if len(kps) != 0:
        komentar_pengumuman_ids = []
        for kp in kps:
            komentar_pengumuman_ids.append(kp.id)
        return JSONResponse(content={"error": "Laporan Status still used", "komentar_pengumuman_ids": komentar_pengumuman_ids}, status_code=400)
    await ModelPengumuman.delete(id)
    return JSONResponse(content={"id": id, "message": "Success Delete Pengumuman ID"}, status_code=200)

@router.put("/{id}")
async def update_pengumuman(id: int, updated_pengumuman: PengumumanUpdate):
    curr_pengumuman = await ModelPengumuman.get(id)
    if curr_pengumuman == None:
        return JSONResponse(content={"error": "Pengumuman with specified id not found"}, status_code=400)
    cp = schemaDBPengumuman(
        title=curr_pengumuman.title,
        isi=curr_pengumuman.isi,
        gambar=curr_pengumuman.gambar,
        created_by=curr_pengumuman.created_by,
        updated_by=curr_pengumuman.updated_by,
        created_at_epoch_utc=curr_pengumuman.created_at_epoch_utc,
        updated_at_epoch_utc=curr_pengumuman.updated_at_epoch_utc,
    )
    if updated_pengumuman.gambar != None:
        if not updated_pengumuman.gambar.endswith(".png") and not updated_pengumuman.gambar.endswith(".jpg") and not updated_pengumuman.gambar.endswith(".jpeg") and not updated_pengumuman.gambar.endswith(".webp"):
            return JSONResponse(content={"error": "Gambar URL is not valid"}, status_code=400)
        cp.gambar = updated_pengumuman.gambar
    check_user = await ModelUser.get(updated_pengumuman.update_user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    cp.updated_by = updated_pengumuman.update_user_id
    cp.updated_at_epoch_utc = calendar.timegm(datetime.datetime.utcnow().timetuple())
    if updated_pengumuman.title != None:
        cp.title = updated_pengumuman.title
    if updated_pengumuman.isi != None:
        cp.isi = updated_pengumuman.isi
    await ModelPengumuman.update(id, **cp.dict())
    return JSONResponse(content={"id": id, "message": "Success Update Pengumuman"}, status_code=200)