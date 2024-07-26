from fastapi import FastAPI
from src.controllers import auth_controller, file_controller

app = FastAPI()

app.include_router(auth_controller.router, prefix="/auth")
app.include_router(file_controller.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
