import os
import requests
import shutil
import logging
from datetime import datetime
from pathlib import Path
from fastapi import HTTPException

class FileHandler:
    def __init__(self, files_directory: Path):
        self.files_directory = files_directory

    def download_file(self, link: str):
        logging.info(f"Recebendo link de download: {link}")

        if not link:
            raise HTTPException(status_code=400, detail="Parâmetro 'link' é obrigatório")

        try:
            response = requests.get(link, stream=True)
            response.raise_for_status()

            if not link.lower().endswith('.csv'):
                raise HTTPException(status_code=400, detail="O link não aponta para um arquivo csv")

            filename = link.split('/')[-1]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename_with_timestamp = f"{timestamp}_{filename}"

            save_dir = self.files_directory
            os.makedirs(save_dir, exist_ok=True)
            file_path = save_dir / filename_with_timestamp

            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

            logging.info("Arquivo XLSX baixado e salvo com sucesso")
            return {"message": "Arquivo XLSX baixado e salvo com sucesso", "file_path": str(file_path)}

        except requests.RequestException as e:
            logging.error(f"Erro durante o download do arquivo: {e}")
            raise HTTPException(status_code=500, detail="Erro durante o download do arquivo")

        except Exception as e:
            logging.error(f"Erro durante o processamento do arquivo: {e}")
            raise HTTPException(status_code=500, detail="Erro durante o processamento do arquivo")

    def read_latest_file_content(self):
        try:
            files = list(self.files_directory.glob("*"))

            if not files:
                raise HTTPException(status_code=404, detail="Nenhum arquivo encontrado na pasta")

            latest_file = max(files, key=lambda f: f.stat().st_mtime)

            with open(latest_file, "r", encoding="latin1") as file:
                file_content = file.read()

            return {"file_name": latest_file.name, "content": file_content}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
