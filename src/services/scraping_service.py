import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

class SiteScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None

    def fetch_page(self):
        response = requests.get(self.url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def fetch_page_from_link(self, link: str):
        response = requests.get(link)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def get_buttons(self):
        if not self.soup:
            self.fetch_page()
        buttons = self.soup.find_all('button', {'class': 'btn_opt'})
        return {button.text.strip(): button['value'] for button in buttons}
    
    def get_sub_buttons(self, soup):
        sub_buttons = soup.find_all('button', {'class': 'btn_sopt'})
        return {button.text.strip(): button['value'] for button in sub_buttons}
    
    def get_tab_link(self, tab_name: str):
        buttons = self.get_buttons()
        option_value = buttons.get(tab_name)
        if option_value:
            # Construir a URL completa
            full_url = urljoin(self.url, f'index.php?opcao={option_value}')
            return full_url
        return f"Link da aba '{tab_name}' não encontrado."
    
    def get_tab_with_sub_links(self, tab_name: str):
        option_link = self.get_tab_link(tab_name)
        if option_link:
            new_soup = self.fetch_page_from_link(option_link)
            sub_buttons = self.get_sub_buttons(new_soup)
            if sub_buttons:
                links = {}
                for sub_tab_name, sub_option_value in sub_buttons.items():
                    full_url = urljoin(self.url, f'index.php?subopcao={sub_option_value}&opcao={option_link.split("=")[-1]}')
                    links[sub_tab_name] = full_url
                return links
            else:
                return {"link": option_link}
        return f"Link da aba '{tab_name}' não encontrado."

    def find_download_links(self, link: str):
        soup = self.fetch_page_from_link(link)
        download_links = {}
        download_elements = soup.select("table.tb_base.tb_link.no_print a.footer_content[href^='download/']")
        for elem in download_elements:
            download_url = urljoin(self.url, elem['href'])
            download_links[elem.text.strip()] = download_url
        return download_links

    def get_tab_with_sub_and_download_links(self, tab_name: str):
        sub_links = self.get_tab_with_sub_links(tab_name)
        download_links = {}
        if isinstance(sub_links, dict):
            for sub_tab, link in sub_links.items():
                download_links[sub_tab] = self.find_download_links(link)
        elif isinstance(sub_links, str):
            return {"message": sub_links}
        return download_links