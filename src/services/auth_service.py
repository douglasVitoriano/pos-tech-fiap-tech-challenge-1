from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import List, Optional
from src.services.db_connection import fetch_users_from_database
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
  
    def verify_password(self, plain_password, hashed_password):
        # Verificação de senha simples
        return plain_password == hashed_password

    # def get_user(self, username: str):
    #     if username in fake_users_db:
    #         user = fake_users_db[username]
    #         return user
    #     return None

    def authenticate_user(users, email: str, username: str):
        for user in users:
            if user.email == email or user.username == username:
                return True  # Já existe usuário ou email
        return False  # Não existe usuário ou email

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Tempo padrão de expiração
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None