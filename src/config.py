import bcrypt

SECRET_KEY = "usertest123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "usertest": {
        "username": "usertest",
        "full_name": "User Test",
        "email": "usertest@example.com",
        "hashed_password": bcrypt.hashpw("secret".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Senha: secret
    }
}