from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Content Moderation System")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "running"}
