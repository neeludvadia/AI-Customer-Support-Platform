from fastapi import FastAPI
from modules.auth.router import router as auth_router
from modules.knowledge_base.router import router as kb_router
from modules.chat.router import router as chat_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(kb_router)
app.include_router(chat_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI Customer Support Platform is running"}
