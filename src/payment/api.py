from os import environ
from fastapi import FastAPI, Request, Form, APIRouter
from dotenv import load_dotenv
from services.utils import generate_hash
from fastapi.responses import HTMLResponse
import uuid
import logging

load_dotenv()
logger = logging.getLogger(__name__)

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
    logger.info("NAV-----> the payment function called")
    # txnid = "txn123456789012"
    txnid = str(uuid.uuid4())
    productinfo = "Test Product"
    hashh = generate_hash(txnid, amount, productinfo, firstname, email)

    html_form = f"""
    <html>
    <body onload="document.forms[0].submit()">
        <form action="{PAYU_BASE_URL}/_payment" method="post">
            <input type="hidden" name="key" value="{PAYU_KEY}" />
            <input type="hidden" name="txnid" value="{txnid}" />
            <input type="hidden" name="amount" value="{amount:.2f}" />
            <input type="hidden" name="productinfo" value="{productinfo}" />
            <input type="hidden" name="firstname" value="{firstname}" />
            <input type="hidden" name="email" value="{email}" />
            <input type="hidden" name="phone" value="9999999999" />
            <input type="hidden" name="surl" value="{SUCCESS_URL}" />
            <input type="hidden" name="furl" value="{FAILURE_URL}" />
            <input type="hidden" name="curl" value="{WEBHOOK_URL}" />
            <input type="hidden" name="hash" value="{hashh}" />
            <input type="hidden" name="service_provider" value="payu_paisa" />
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_form)


@router.post("/webhook/success")
async def webhook_success(request: Request):
    print("the message is success")
    form = await request.form()
    return {"status": "success", "details": dict(form)}

@router.post("/webhook/failure")
async def webhook_failure(request: Request):
    print("the payment failed")
    form = await request.form()
    return {"status": "failure", "details": dict(form)}
