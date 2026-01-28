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

class payUPaymentGateway:
    def __init__(self):
        self.PAYU_KEY = environ.get("PAYU_KEY")
        self.PAYU_SALT = environ.get("PAYU_SALT")
        self.PAYU_BASE_URL = environ.get("PAYU_BASE_URL")
        # self.SUCCESS_URL = environ.get("SUCCESS_URL")
        # self.FAILURE_URL = environ.get("FAILURE_URL")
        self.SUCCESS_URL = "https://lankly-multipointed-kirstie.ngrok-free.dev/api/webhook/success"
        self.FAILURE_URL = "https://webhook.site/ac78172b-f7f6-4608-aaba-8dbf3ef36f3e"
        self.WEBHOOK_URL = environ.get("WEBHOOK_URL")

    def generate_hash(self, txnid, amount, productinfo, firstname, email):

        # Force 2 decimal format
        amount = f"{float(amount):.2f}"


        hash_string = (
            f"{self.PAYU_KEY}|{txnid}|{amount}|{productinfo}|"
            f"{firstname}|{email}|||||||||||{self.PAYU_SALT}"
        )

        logger.info(f"NAV----> the hash string value are {hash_string}")
        hashh = hashlib.sha512(
            hash_string.encode("utf-8")
        ).hexdigest().lower()

        logger.info(f"NAV----> the hashh value are {hashh}")
        return hashh

    def initiate_payment(self, hash, txnid, amount, productinfo, firstname, email):
        html_form = f"""
        <html>
        <body onload="document.forms[0].submit()">
            <form action="{self.PAYU_BASE_URL}/_payment" method="post">
                <input type="hidden" name="key" value="{self.PAYU_KEY}" />
                <input type="hidden" name="txnid" value="{txnid}" />
                <input type="hidden" name="amount" value="{amount:.2f}" />
                <input type="hidden" name="productinfo" value="{productinfo}" />
                <input type="hidden" name="firstname" value="{firstname}" />
                <input type="hidden" name="email" value="{email}" />
                <input type="hidden" name="phone" value="9999999999" />
                <input type="hidden" name="surl" value="{self.SUCCESS_URL}" />
                <input type="hidden" name="furl" value="{self.FAILURE_URL}" />
                <input type="hidden" name="hash" value="{hash}" />
                <input type="hidden" name="service_provider" value="payu_paisa" />
            </form>
        </body>
        </html>
        """
        return HTMLResponse(content=html_form)

    # async def webhook_success(self, request):
    #     form = await request.form()
    #     return {"status": "success", "details": dict(form)}
    
    async def webhook_success(request: Request):

        data = await request.form()

        print("PAYU SUCCESS:", dict(data))

        html = f"""
        <html>
            <head>
                <title>Payment Success</title>
            </head>
            <body>
                <h2>Payment Successful ✅</h2>

                <p>Transaction ID: {data.get('txnid')}</p>
                <p>Amount: {data.get('amount')}</p>
                <p>Status: {data.get('status')}</p>

                <p>Thank you for your payment.</p>
            </body>
        </html>
        """

        return HTMLResponse(content=html, status_code=200)
    
    # async def webhook_failure(self, request):
    #     form = await request.form()
    #     return {"status": "failure", "details": dict(form)}

    async def webhook_failure(request: Request):

        data = await request.form()

        print("PAYU FAILURE:", dict(data))

        html = """
        <html>
            <body>
                <h2>Payment Failed ❌</h2>
                <p>Please try again.</p>
            </body>
        </html>
        """

        return HTMLResponse(content=html, status_code=200)