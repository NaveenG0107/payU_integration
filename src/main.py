from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
def health_check():
    return {
    "status": "ok",
    "service": "fastapi-app",
    "timestamp": datetime.utcnow()
    }