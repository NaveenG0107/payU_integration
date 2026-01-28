from os import environ
from fastapi import FastAPI, Request, Form, APIRouter
from dotenv import load_dotenv
from services.utils import generate_hash
from fastapi.responses import HTMLResponse
import uuid
import logging
from services.payment_gatways.payU.service import payUPaymentGateway



load_dotenv()
logger = logging.getLogger(__name__)
payUPayment = payUPaymentGateway()
router = APIRouter(
	prefix="/api",
	tags=["Payment-Process"],
	responses={
		400: {"description": "Bad Request"},
		404: {"description": "Not Found"},
		500: {"description": "Internal Server Error"},
	},
)

PAYU_KEY = environ.get("PAYU_KEY")
PAYU_SALT = environ.get("PAYU_SALT")
PAYU_BASE_URL = environ.get("PAYU_BASE_URL")
SUCCESS_URL = environ.get("SUCCESS_URL")
FAILURE_URL = environ.get("FAILURE_URL")
WEBHOOK_URL = environ.get("WEBHOOK_URL")

# def generate_hash(txnid, amount, productinfo, firstname, email):
#     # Hash sequence: key|txnid|amount|productinfo|firstname|email|||||||||||salt
#     hash_string = f"{PAYU_KEY}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{PAYU_SALT}"
#     return hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()

# @router.post("/pay")
# async def pay(amount: float = 1, firstname: str = "test", email: str = "test@email.com" ):
#     print("Nav---> this block executed--->")
#     txnid = "txn12345"  # generate unique txnid per request
#     productinfo = "Test Product"
#     hashh = generate_hash(txnid, amount, productinfo, firstname, email)

#     payload = {
#         "key": PAYU_KEY,
#         "txnid": txnid,
#         "amount": amount,
#         "productinfo": productinfo,
#         "firstname": firstname,
#         "email": email,
#         "phone": "9999999999",
#         "surl": SUCCESS_URL,
#         "furl": FAILURE_URL,
#         "hash": hashh,
#         "service_provider": "payu_paisa"
#     }

#     # Redirect user to PayU payment page
#     print(f"utl {PAYU_BASE_URL}/_payment")
#     return RedirectResponse(url=f"{PAYU_BASE_URL}/_payment", status_code=303)



@router.post("/pay")
async def pay(amount: float = 1, firstname: str = "test", email: str = "test@email.com"):
    logger.info("NAV----> the payment function called")
    txnid = str(uuid.uuid4())
    productinfo = "Test Product"
    hash = payUPayment.generate_hash(txnid, amount, productinfo, firstname, email)
    response = payUPayment.initiate_payment(hash, txnid, amount, productinfo, firstname, email)
    return response


@router.post("/webhook/success")
async def webhook_success(request: Request):
    print("Nav----> the message is success")
    return payUPayment.webhook_success(request)
    

@router.post("/webhook/failure")
async def webhook_failure(request: Request):
    print("Nav---->the payment failed")
    return payUPayment.webhook_failure(request)
