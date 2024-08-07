from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from src.file_handler import FileHandler
from src.services.scraping_service import SiteScraper

router = APIRouter()
file_handler = FileHandler(Path("/Users/suportescsa/Documents/cursos/api-fiap-2mlet/pos-tech-fiap-tech-challenge-1/files"))

""" @router.get("/files")
async def get_files():
    return {"message": "Files endpoint"}

@router.get("/download/")
async def download_file(link: str = Query(..., description="URL do link para o arquivo XLSX")):
    return file_handler.download_file(link) """

@router.get("/latest-file-content")
async def read_latest_file_content():
    return file_handler.read_latest_file_content()

""" @router.get("/site-links")
async def get_site_links():
    scraper = SiteScraper("http://vitibrasil.cnpuv.embrapa.br/")
    buttons = scraper.get_buttons()
    return buttons

@router.get("/tab-link")
async def get_tab_link(tab_name: str = Query(..., description="Nome da aba para procurar")):
    scraper = SiteScraper("http://vitibrasil.cnpuv.embrapa.br/")
    tab_link = scraper.get_tab_link(tab_name)
    return {"tab_link": tab_link}

@router.get("/tab-with-sub-links")
async def get_tab_with_sub_links(tab_name: str = Query(..., description="Nome da aba para procurar")):
    scraper = SiteScraper("http://vitibrasil.cnpuv.embrapa.br/")
    sub_links = scraper.get_tab_with_sub_links(tab_name)
    return sub_links

@router.get("/tab-with-sub-and-download-links")
async def get_tab_with_sub_and_download_links(tab_name: str = Query(..., description="Nome da aba para procurar")):
    scraper = SiteScraper("http://vitibrasil.cnpuv.embrapa.br/")
    download_links = scraper.get_tab_with_sub_and_download_links(tab_name)
    if download_links:
        return download_links
    raise HTTPException(status_code=404, detail=f"Link da aba '{tab_name}' não encontrado.") """

@router.get("/download-multiple")
async def download_multiple_files(tab_name: str = Query(..., description="Nome da aba para procurar")):
    scraper = SiteScraper("http://vitibrasil.cnpuv.embrapa.br/")
    download_links = scraper.get_tab_with_sub_and_download_links(tab_name)
    
    links_to_download = []
    if isinstance(download_links, dict):
        for sub_tab, links in download_links.items():
            if isinstance(links, dict):
                links_to_download.extend(links.values())
            else:
                links_to_download.append(links)

    if not links_to_download:
        raise HTTPException(status_code=404, detail="Nenhum link de download encontrado.")
    
    downloaded_files = file_handler.download_files(links_to_download)
    return downloaded_files