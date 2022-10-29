from typing import List, Optional
from models import LaporanStatus as ModelLaporanStatus, Laporan as ModelLaporan
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class LaporanStatus(BaseModel):
    name: str
    desc: Optional[str]

    class Config:
        orm_mode = True

class LaporanStatuses(LaporanStatus):
    id: int

router =  APIRouter()

@router.post("", status_code=201)
async def create_laporan_status(laporan_status: LaporanStatus):
    check_dt = await ModelLaporanStatus.get_by_name(laporan_status.name)
    if check_dt != None:
        return JSONResponse(content={"error": "Laporan Status already exist"}, status_code=400)
    laporan_status_id = await ModelLaporanStatus.create(**laporan_status.dict())
    return {"laporan_status_id": laporan_status_id}

@router.get("/all",response_model=List[LaporanStatuses])
async def get_all_laporan_status():
    laporan_statuses = await ModelLaporanStatus.get_all()
    return laporan_statuses

@router.get("/{id}", response_model=LaporanStatuses)
async def get_laporan_status_by_id(id: int):
    laporan_status = await ModelLaporanStatus.get(id)
    if laporan_status == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    return laporan_status

@router.delete("/{id}")
async def delete_laporan_status_by_id(id: int):
    laporan_status = await ModelLaporanStatus.get(id)
    if laporan_status == None:
        return JSONResponse(content={"error": "id not found"}, status_code=400)
    laporans = await ModelLaporan.get_by_laporan_status_id(id)
    if laporans != None:
        laporan_ids = []
        for laporan in laporans:
            laporan_ids.append(laporan.id)
        return JSONResponse(content={"error": "Laporan Status still used", "laporan_ids": laporan_ids}, status_code=400)
    await ModelLaporanStatus.delete(id)
    return JSONResponse(content={"message": "Success Delete Laporan Status"}, status_code=200)


