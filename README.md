# API de Consulta de Dados de Vitivinicultura da Embrapa

## Introdução
Este projeto foi desenvolvido como parte do Tech Challenge fase 1 para analisar os dados de vitivinicultura da Embrapa, disponíveis no site VitiBrasil Embrapa.

A ideia principal deste projeto é a criação de uma API pública que permita a consulta dos dados nas seguintes categorias:

- Produção
- Processamento
- Comercialização
- Importação
- Exportação

Esses dados serão utilizados para alimentar uma base de dados, que futuramente servirá como base para a construção de um modelo de Machine Learning.

## Objetivos

- Criar uma REST API em Python que realiza a consulta no site da Embrapa.
- Documentar a API detalhadamente.
- Implementar um método de autenticação (recomendado, mas opcional).
- Desenvolver um plano de deploy para a API, incluindo a arquitetura do projeto, desde a ingestão de dados até a alimentação do modelo de Machine Learning.
- Entregar um MVP da API, com deploy realizado e um link compartilhável.
- Publicar o projeto em um repositório GitHub com toda a documentação necessária.

### Estrutura do Projeto
```
pos-tech-fiap-tech-challenge-1/
│
├── src/
│   ├── controller/
│   │   ├── auth_controller.py
│   │   └── file_controller.py 
│   ├── model/
|   |   └── user.py 
│   ├── services/
│   │   ├── auth_service.py
|   |   ├── dash_service.py
│   │   └── scraping_service.py 
│   ├── utils/
│   |     └── helpers.py
|   │── config.py
|   │── file_handler.py
|   └── main.py
├── Dockerfile
├── README.md
└── requirements.txt
```
## Como Executar

1. Clone o repositório e faça a instalação das dependencias num ambiente virtual.

```bash
git clone https://github.com/douglasVitoriano/pos-tech-fiap-tech-challenge-1.git
cd pos-tech-fiap-tech-challenge-1
```

2. Faça a instalação das dependecias usando ambiente virtual.
```bash
python3 -m venv .venv-tech-challenge-1

# Linux/MacOS
source .venv-tech-challenge-1/bin/activate

# Windows
.\.venv-tech-challenge-1\Scripts\activate

pip install -r requirements.txt
```

3. Inicie a API localmente
```bash
uvicorn src.main:app --prot 8000
```

4. Acesse o Swagger
http://localhost:8000/docs

## Contribuidores

- Ayres Alves Guimarães Neto | ayresguimaraes@gmail.com | RM357032

- Elzevir De Sousa Sá Filho | safilhoelzevirsafilho@gmail.com | RM356837

- Danilo Matrangolo Marano | danilo.m.marano@gmail.com | RM357884

- Douglas Augusto Vitoriano | douglas_vitoriano@yahoo.com.br | RM357899

- Wagner Calçada dos Santos | gyo1232010@hotmail.com | RM357846


