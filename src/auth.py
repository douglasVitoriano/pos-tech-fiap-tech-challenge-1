from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# Secret key for JWT
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Simulação de um banco de dados de usuários fictício
fake_users_db = {
    "usertest": {
        "username": "usertest",
        "full_name": "User Test",
        "email": "usertest@example.com",
        "hashed_password": "Senha@teste2024",  # Senha: secret
    }
}

# Funções auxiliares
def verify_password(plain_password, hashed_password):
    # Verificação de senha simples
    return plain_password == hashed_password

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return user_dict

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Tempo padrão de expiração
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
