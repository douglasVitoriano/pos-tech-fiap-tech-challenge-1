from typing import List
import bcrypt

class User:
    def __init__(self, username: str, full_name: str, email: str, hashed_password: str):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password

#função para criar senha com gash
def hash_password(password):
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