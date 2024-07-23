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


# Simulação de um banco de dados de usuários fictício
fake_users_db = {
    "usertest": User(
        username="usertest",
        full_name="User Test",
        email="usertest@example.com",
        hashed_password="Senha@teste2024"  # Senha: secret
    )
}