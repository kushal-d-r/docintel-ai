from fastapi import FastAPI
from backend.routes import router

app = FastAPI(title="DocIntel AI")

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocIntel AI"
    }