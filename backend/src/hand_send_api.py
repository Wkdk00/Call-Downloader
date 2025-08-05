import datetime
from typing import Optional, List
from fastapi import APIRouter, Form
from fastapi.requests import Request
from src.models import Files
from src.database import db_dependency

router = APIRouter()

@router.get("/get_files_list")
async def get_files_list(
    db: db_dependency,
    agent_id: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    query = db.query(Files)
    if agent_id:
        query = query.filter(Files.agentId == agent_id)
    if date_from:
        try:
            date_from_dt = datetime.fromisoformat(date_from)
            query = query.filter(Files.date >= date_from_dt)
        except Exception:
            pass
    if date_to:
        try:
            date_to_dt = datetime.fromisoformat(date_to)
            query = query.filter(Files.date <= date_to_dt)
        except Exception:
            pass
    files = query.all()
    return [
        {
            "fileId": str(f.fileId),
            "date": f.date,
            "file_size": len(f.filedata) if f.filedata else 0
        }
        for f in files
    ]

@router.post('/download_files')
async def download_files(
        request: Request,
        db: db_dependency,
        agent_id: str = Form(...),
        selected_files: List[str] = Form(...),
        send_to_sense_trigger: bool = Form(False),
        send_to_cxm_online: bool = Form(False)
):
    pass