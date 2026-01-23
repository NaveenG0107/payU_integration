from os import environ
from fastapi import FastAPI, Request, Form, APIRouter
from dotenv import load_dotenv
from services.utils import generate_hash
from fastapi.responses import HTMLResponse
import logging

load_dotenv()

router = APIRouter(
	prefix="/api",
	tags=["Payment-Process"],
	responses={
		400: {"description": "Bad Request"},
		404: {"description": "Not Found"},
		500: {"description": "Internal Server Error"},
	},
)


@router.post("/webhook")
async def webhook(request: Request):
   return {"status": "success", "details": "webhook called successfully"}