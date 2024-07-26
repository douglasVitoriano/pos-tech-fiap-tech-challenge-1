from typing import List
from pydantic import BaseModel
import bcrypt

# Definição do modelo Pydantic
class User(BaseModel):
    username: str
    full_name: str
    email: str
    hashed_password: str

# Função para criar senha com hash
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')