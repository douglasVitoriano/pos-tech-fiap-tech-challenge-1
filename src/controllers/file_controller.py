from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from src.file_handler import FileHandler

router = APIRouter()
file_handler = FileHandler(Path("C:/pasta-do-projeto/api-fiap-2mlet/files"))

@router.get("/files")
async def get_files():
    return {"message": "Files endpoint"}

@router.get("/download/")
async def download_file(link: str = Query(..., description="URL do link para o arquivo XLSX")):
    return file_handler.download_file(link)

@router.get("/latest-file-content")
async def read_latest_file_content():
    return file_handler.read_latest_file_content()
