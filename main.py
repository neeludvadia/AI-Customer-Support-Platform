from fastapi import FastAPI
from modules.auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI Customer Support Platform is running"}
