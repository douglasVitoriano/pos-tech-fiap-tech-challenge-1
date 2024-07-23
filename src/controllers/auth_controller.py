from fastapi import APIRouter, HTTPException, Depends
from src.services.auth_service import AuthService
from src.models.user import User
from src.services.db_connection import fetch_users_from_database, save_user_to_database
from typing import List

router = APIRouter()
auth_service = AuthService()

@router.get("/login")
async def login():
    return {"message": "Login endpoint"}

@router.post("/login")
def login(username: str, password: str):
    user = auth_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/decode_token")
def decode_token(token: str):
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/users")
def create_user(user: User):

    users = fetch_users_from_database('database.db')

    # Verificar se o username ou email já existem
    if AuthService.authenticate_user(users, user.email, user.username):
        raise HTTPException(status_code=400, detail="Usuário ou email já cadastrados.")

    # Hash da senha
    hashed_password = hashed_password(user.hashed_password)

    # Criar um objeto User para salvar no banco de dados
    user_to_save = User(username=user.username, full_name=user.full_name, email=user.email, hashed_password=hashed_password)

    # Salvar o usuário no banco de dados
    save_user_to_database('database.db', user_to_save)

    return {"username": user.username, "full_name": user.full_name, "email": user.email}
