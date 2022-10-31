import datetime
import calendar
import string

from typing import  Union, List
from models import LaporanStatus as ModelLS, User as ModelUser, Laporan as ModelLaporan
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class user(BaseModel):
    username: str
    full_name: Union[str, None] = None

class schemaUser(user):
    id: int

class LaporanIn(BaseModel):
    title: str
    deskripsi: str
    alamat: str
    laporan_status_id: int
    user_id: int

class schemaDBLaporan(BaseModel):
    title: str
    deskripsi: str
    alamat: str
    laporan_status_id: int
    created_by: int
    created_at_epoch_utc: int
    updated_by: int
    updated_at_epoch_utc: int

class schemaLapStatus(BaseModel):
    laporan_status_id: int
    laporan_status_name: str
    laporan_status_desc: str

class LaporanOut(BaseModel):
    id: int
    title: str
    deskripsi: str
    alamat: Union[str, None] = None
    laporan_status: schemaLapStatus
    created_user: schemaUser
    updated_user: schemaUser
    created_at_utc: int
    updated_at_utc: int

class LaporanUpdate(BaseModel):
    title: Union[str, None] = None
    deskripsi: Union[str, None] = None
    alamat: Union[str, None] = None
    laporan_status_id: Union[int, None] = None
    update_user_id: int

router =  APIRouter()

@router.post("", status_code=201)
async def create_laporan(new_laporan: LaporanIn):
    check_ls = await ModelLS.get(new_laporan.laporan_status_id)
    if check_ls == None:
        return JSONResponse(content={"error": "Laporan Statuses not exist"}, status_code=400)
    check_user = await ModelUser.get(new_laporan.user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    dbObj = schemaDBLaporan(
        title=new_laporan.title,
        deskripsi=new_laporan.deskripsi,
        laporan_status_id=new_laporan.laporan_status_id,
        created_by=new_laporan.user_id,
        updated_by=new_laporan.user_id,
        created_at_epoch_utc=calendar.timegm(datetime.datetime.utcnow().timetuple()),
        updated_at_epoch_utc=calendar.timegm(datetime.datetime.utcnow().timetuple()),
        alamat=new_laporan.alamat,
    )

    laporan_id = await ModelLaporan.create(**dbObj.dict())
    return {"laporan_id": laporan_id}

@router.get("/all",response_model=List[LaporanOut])
async def get_all_laporan():
    laporans = await ModelLaporan.get_all()
    out_list = []
    for l in laporans:
        user_laporan_created = await ModelUser.get_by_user_id(l.created_by)
        user_laporan_updated = await ModelUser.get_by_user_id(l.updated_by)
        lap_status = await ModelLS.get(l.laporan_status_id)
        out = LaporanOut(id=l.id,title=l.title,deskripsi=l.deskripsi,alamat=l.alamat,
            laporan_status=schemaLapStatus(laporan_status_id=l.laporan_status_id,laporan_status_name=lap_status.name,laporan_status_desc=lap_status.desc),
            created_at_utc=l.created_at_epoch_utc,updated_at_utc=l.updated_at_epoch_utc,
            created_user=schemaUser(id=user_laporan_created.id,username=user_laporan_created.username,full_name=user_laporan_created.full_name),
            updated_user=schemaUser(id=user_laporan_updated.id,username=user_laporan_updated.username,full_name=user_laporan_updated.full_name))
        out_list.append(out)
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/all/{user_id}",response_model=List[LaporanOut])
async def get_all_laporan_by_user_id(user_id: int):
    laporans = await ModelLaporan.get_by_user_id(user_id)
    out_list = []
    for l in laporans:
        user_laporan_created = await ModelUser.get_by_user_id(l.created_by)
        user_laporan_updated = await ModelUser.get_by_user_id(l.updated_by)
        lap_status = await ModelLS.get(l.laporan_status_id)
        out = LaporanOut(id=l.id,title=l.title,deskripsi=l.deskripsi,alamat=l.alamat,
            laporan_status=schemaLapStatus(laporan_status_id=l.laporan_status_id,laporan_status_name=lap_status.name,laporan_status_desc=lap_status.desc),
            created_at_utc=l.created_at_epoch_utc,updated_at_utc=l.updated_at_epoch_utc,
            created_user=schemaUser(id=user_laporan_created.id,username=user_laporan_created.username,full_name=user_laporan_created.full_name),
            updated_user=schemaUser(id=user_laporan_updated.id,username=user_laporan_updated.username,full_name=user_laporan_updated.full_name))
        out_list.append(out)
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/all/{status_id}",response_model=List[LaporanOut])
async def get_all_laporan_by_status_id(status_id: int):
    laporans = await ModelLaporan.get_by_laporan_status_id(status_id)
    out_list = []
    for l in laporans:
        user_laporan_created = await ModelUser.get_by_user_id(l.created_by)
        user_laporan_updated = await ModelUser.get_by_user_id(l.updated_by)
        lap_status = await ModelLS.get(l.laporan_status_id)
        out = LaporanOut(id=l.id,title=l.title,deskripsi=l.deskripsi,alamat=l.alamat,
            laporan_status=schemaLapStatus(laporan_status_id=l.laporan_status_id,laporan_status_name=lap_status.name,laporan_status_desc=lap_status.desc),
            created_at_utc=l.created_at_epoch_utc,updated_at_utc=l.updated_at_epoch_utc,
            created_user=schemaUser(id=user_laporan_created.id,username=user_laporan_created.username,full_name=user_laporan_created.full_name),
            updated_user=schemaUser(id=user_laporan_updated.id,username=user_laporan_updated.username,full_name=user_laporan_updated.full_name))
        out_list.append(out)
    new_list = sorted(out_list, key=lambda x: x.id, reverse=True)
    return new_list

@router.get("/{id}", response_model=LaporanOut)
async def get_laporan_by_id(id: int):
    l = await ModelLaporan.get(id)
    if l == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    user_laporan_created = await ModelUser.get_by_user_id(l.created_by)
    user_laporan_updated = await ModelUser.get_by_user_id(l.updated_by)
    lap_status = await ModelLS.get(l.laporan_status_id)
    out = LaporanOut(id=l.id,title=l.title,deskripsi=l.deskripsi,alamat=l.alamat,
            laporan_status=schemaLapStatus(laporan_status_id=l.laporan_status_id,laporan_status_name=lap_status.name,laporan_status_desc=lap_status.desc),
            created_at_utc=l.created_at_epoch_utc,updated_at_utc=l.updated_at_epoch_utc,
            created_user=schemaUser(id=user_laporan_created.id,username=user_laporan_created.username,full_name=user_laporan_created.full_name),
            updated_user=schemaUser(id=user_laporan_updated.id,username=user_laporan_updated.username,full_name=user_laporan_updated.full_name))
    return out

@router.delete("/{id}")
async def delete_laporan_by_id(id: int):
    laporan_type = await ModelLaporan.get(id)
    if laporan_type == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    await ModelLaporan.delete(id)
    return JSONResponse(content={"id": id, "message": "Success Delete Laporan ID"}, status_code=200)

@router.put("/{id}")
async def update_laporan(id: int, updated_laporan: LaporanUpdate):
    curr_laporan = await ModelLaporan.get(id)
    if curr_laporan == None:
        return JSONResponse(content={"error": "Laporan with specified id not found"}, status_code=400)
    cl = schemaDBLaporan(
        title=curr_laporan.title,
        deskripsi=curr_laporan.deskripsi,
        alamat=curr_laporan.alamat,
        laporan_status_id=curr_laporan.laporan_status_id,
        created_by=curr_laporan.created_by,
        updated_by=curr_laporan.updated_by,
        created_at_epoch_utc=curr_laporan.created_at_epoch_utc,
        updated_at_epoch_utc=curr_laporan.updated_at_epoch_utc,
    )
    check_user = await ModelUser.get(updated_laporan.update_user_id)
    if check_user == None:
        return JSONResponse(content={"error": "User ID not exist"}, status_code=400)
    cl.updated_by = updated_laporan.update_user_id
    cl.updated_at_epoch_utc = calendar.timegm(datetime.datetime.utcnow().timetuple())
    if updated_laporan.laporan_status_id != None:
        check_lap_status = await ModelLS.get(updated_laporan.laporan_status_id)
        if check_lap_status == None:
            return JSONResponse(content={"error": "Laporan Statuses not exist"}, status_code=400)
        cl.laporan_status_id = updated_laporan.laporan_status_id
    if updated_laporan.title != None:
        cl.title = updated_laporan.title
    if updated_laporan.deskripsi != None:
        cl.deskripsi = updated_laporan.deskripsi
    if updated_laporan.alamat != None:
        cl.alamat = updated_laporan.alamat
    await ModelLaporan.update(id, **cl.dict())
    return JSONResponse(content={"id": id, "message": "Success Update Laporan"}, status_code=200)