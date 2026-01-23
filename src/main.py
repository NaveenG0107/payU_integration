from fastapi import FastAPI
from datetime import datetime
from os import environ
from dotenv import load_dotenv
import logging
import os
from payment.api import router as payment_router
from payment.webhook import router as webhoomk_router

load_dotenv()

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(payment_router)
app.include_router(webhoomk_router)

@app.get("/health")
def health_check():
    logger.info("NAV-----> the health function called")
    return {
    "status": "success",
    "service": "fastapi-app",
    "timestamp": datetime.utcnow()
    }