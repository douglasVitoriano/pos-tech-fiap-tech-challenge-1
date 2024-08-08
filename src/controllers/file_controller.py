from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from src.file_handler import FileHandler
from src.services.scraping_service import SiteScraper
import logging
import subprocess
import shutil
import os

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
    
    # Verificar e deletar a pasta 'files' se existir
    files_dir = file_handler.files_directory
    if files_dir.exists() and files_dir.is_dir():
        shutil.rmtree(files_dir)
    
    downloaded_files = file_handler.download_files(links_to_download)
    return downloaded_files

# Lista de nomes de abas fixos
FIXED_TABS = ["Produção", "Processamento", "Comercialização", "Importação", "Exportação"]

@router.get("/download-all")
async def download_all_tabs():
    scraper = SiteScraper("http://vitibrasil.cnpuv.embrapa.br/")
    all_download_links = []

    for tab_name in FIXED_TABS:
        try:
            download_links = scraper.get_tab_with_sub_and_download_links(tab_name)
            if isinstance(download_links, dict):
                for sub_tab, links in download_links.items():
                    if isinstance(links, dict):
                        all_download_links.extend(links.values())
                    else:
                        all_download_links.append(links)
            elif isinstance(download_links, list):
                all_download_links.extend(download_links)
        except Exception as e:
            logging.error(f"Erro ao processar a aba '{tab_name}': {e}")

    if not all_download_links:
        raise HTTPException(status_code=404, detail="Nenhum link de download encontrado em nenhuma aba.")
    
    # Verificar e deletar a pasta 'files' se existir
    files_dir = file_handler.files_directory
    if files_dir.exists() and files_dir.is_dir():
        shutil.rmtree(files_dir)

    downloaded_files = file_handler.download_files(all_download_links)
    return downloaded_files

@router.get("/start-dashboard")
async def start_streamlit():
    try:
        # Inicia o Streamlit em um subprocesso
        current_dir = Path.cwd()
        dash_path = current_dir.parent / 'pos-tech-fiap-tech-challenge-1' / 'src' / 'services' / 'dash_service.py'
        dash_path
        
        if not dash_path.exists():
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {dash_path}")
        
        # Inicia o Streamlit
        subprocess.Popen(["streamlit", "run", str(dash_path)])
        return {"message": "Streamlit iniciado com sucesso."}
    except Exception as e:
        logging.error(f"Erro ao iniciar o Streamlit: {e}")
        return {"error": str(e)}