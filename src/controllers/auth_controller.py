from fastapi import APIRouter, HTTPException, Depends
from src.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

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