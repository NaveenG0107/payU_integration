from os import environ
from fastapi import FastAPI, Request, Form, APIRouter
from dotenv import load_dotenv
from services.utils import generate_hash
from fastapi.responses import HTMLResponse
import uuid
import logging
import hashlib

load_dotenv()
logger = logging.getLogger(__name__)

class webHook:
    def __init__(self):
        self.PAYU_KEY = environ.get("PAYU_KEY")
        self.PAYU_SALT = environ.get("PAYU_SALT")
        self.PAYU_BASE_URL = environ.get("PAYU_BASE_URL")
        self.SUCCESS_URL = environ.get("SUCCESS_URL")
        self.FAILURE_URL = environ.get("FAILURE_URL")
        self.WEBHOOK_URL = environ.get("WEBHOOK_URL")

    def webhook_function(request):
        return {"status":"success", "details": "webhook callback function executed successfully"}