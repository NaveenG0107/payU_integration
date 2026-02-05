from os import environ
from typing import Dict, Optional
from fastapi import FastAPI, Request, Form, APIRouter
from dotenv import load_dotenv
from services.utils import generate_hash, generate_hash_check_payment_status, generate_unique_refund_token, generate_refund_hash
from fastapi.responses import HTMLResponse
import uuid
import logging
import hashlib
import httpx

load_dotenv()
logger = logging.getLogger(__name__)

class payUPaymentGateway:
    def __init__(self):
        self.PAYU_KEY = environ.get("PAYU_KEY")
        self.PAYU_SALT = environ.get("PAYU_SALT")
        self.PAYU_BASE_URL = environ.get("PAYU_BASE_URL")
        self.SUCCESS_URL = environ.get("SUCCESS_URL")
        self.FAILURE_URL = environ.get("FAILURE_URL")
        self.WEBHOOK_URL = environ.get("WEBHOOK_URL")
        self.PAYMENT_STATUS_URL = environ.get('PAYMENT_STATUS_URL')

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

    # def initiate_payment(self, payment_data: dict):
    #     return HTMLResponse(content=f"""
    #         <!DOCTYPE html>
    #         <html lang="en">
    #         <head>
    #             <meta charset="UTF-8">
    #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #             <title>Redirecting to PayU...</title>
    #             <style>
    #                 body {{
    #                     font-family: Arial, sans-serif;
    #                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    #                     min-height: 100vh;
    #                     display: flex;
    #                     align-items: center;
    #                     justify-content: center;
    #                     margin: 0;
    #                 }}
    #                 .loader {{
    #                     text-align: center;
    #                     color: white;
    #                 }}
    #                 .spinner {{
    #                     width: 60px;
    #                     height: 60px;
    #                     border: 5px solid rgba(255,255,255,0.3);
    #                     border-top: 5px solid white;
    #                     border-radius: 50%;
    #                     animation: spin 1s linear infinite;
    #                     margin: 0 auto 30px;
    #                 }}
    #                 @keyframes spin {{
    #                     0% {{ transform: rotate(0deg); }}
    #                     100% {{ transform: rotate(360deg); }}
    #                 }}
    #                 h2 {{
    #                     font-size: 28px;
    #                     margin-bottom: 15px;
    #                 }}
    #             </style>
    #         </head>
    #         <body>
    #             <div class="loader">
    #                 <div class="spinner"></div>
    #                 <h2>Redirecting to PayU...</h2>
    #                 <p>Transaction ID: {payment_data['txnid']}</p>
    #                 <p>Amount: ₹{payment_data['amount']}</p>
    #             </div>
                
    #             <form id="payuForm" action="{self.PAYU_BASE_URL}/_payment" method="post">
    #                 <input type="hidden" name="key" value="{payment_data['key']}">
    #                 <input type="hidden" name="txnid" value="{payment_data['txnid']}">
    #                 <input type="hidden" name="amount" value="{payment_data['amount']}">
    #                 <input type="hidden" name="productinfo" value="{payment_data['productinfo']}">
    #                 <input type="hidden" name="firstname" value="{payment_data['firstname']}">
    #                 <input type="hidden" name="lastname" value="{payment_data['lastname']}">
    #                 <input type="hidden" name="email" value="{payment_data['email']}">
    #                 <input type="hidden" name="phone" value="{payment_data['phone']}">
    #                 <input type="hidden" name="surl" value="{payment_data['surl']}">
    #                 <input type="hidden" name="furl" value="{payment_data['furl']}">
    #                 <input type="hidden" name="curl" value="{payment_data['curl']}">
    #                 <input type="hidden" name="address1" value="{payment_data['address1']}">
    #                 <input type="hidden" name="city" value="{payment_data['city']}">
    #                 <input type="hidden" name="state" value="{payment_data['state']}">
    #                 <input type="hidden" name="country" value="{payment_data['country']}">
    #                 <input type="hidden" name="zipcode" value="{payment_data['zipcode']}">
    #                 <input type="hidden" name="hash" value="{payment_data['hash']}">
    #             </form>
                
    #             <script>
    #                 setTimeout(function() {{
    #                     document.getElementById('payuForm').submit();
    #                 }}, 2000);
    #             </script>
    #         </body>
    #         </html>
    #         """)

    def initiate_payment(self, payment_data: dict):
        return HTMLResponse(content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Redirecting to PayU...</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0;
                    }}
                    .loader {{
                        text-align: center;
                        color: white;
                    }}
                    .spinner {{
                        width: 60px;
                        height: 60px;
                        border: 5px solid rgba(255,255,255,0.3);
                        border-top: 5px solid white;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin: 0 auto 30px;
                    }}
                    @keyframes spin {{
                        0% {{ transform: rotate(0deg); }}
                        100% {{ transform: rotate(360deg); }}
                    }}
                    h2 {{
                        font-size: 28px;
                        margin-bottom: 15px;
                    }}
                </style>
            </head>
            <body>
                <div class="loader">
                    <div class="spinner"></div>
                    <h2>Redirecting to PayU...</h2>
                    <p>Transaction ID: {payment_data['txnid']}</p>
                    <p>Amount: ₹{payment_data['amount']}</p>
                </div>
                
                <form id="payuForm" action="{self.PAYU_BASE_URL}/_payment" method="post">
                    <input type="hidden" name="key" value="{payment_data['key']}">
                    <input type="hidden" name="txnid" value="{payment_data['txnid']}">
                    <input type="hidden" name="amount" value="{payment_data['amount']}">
                    <input type="hidden" name="productinfo" value="{payment_data['productinfo']}">
                    <input type="hidden" name="firstname" value="{payment_data['firstname']}">
                    <input type="hidden" name="lastname" value="{payment_data['lastname']}">
                    <input type="hidden" name="email" value="{payment_data['email']}">
                    <input type="hidden" name="phone" value="{payment_data['phone']}">
                    <input type="hidden" name="surl" value="{payment_data['surl']}">
                    <input type="hidden" name="furl" value="{payment_data['furl']}">
                    <input type="hidden" name="curl" value="{payment_data['curl']}">
                    <input type="hidden" name="address1" value="{payment_data['address1']}">
                    <input type="hidden" name="city" value="{payment_data['city']}">
                    <input type="hidden" name="state" value="{payment_data['state']}">
                    <input type="hidden" name="country" value="{payment_data['country']}">
                    <input type="hidden" name="zipcode" value="{payment_data['zipcode']}">
                    <input type="hidden" name="udf1" value="{payment_data['udf1']}">
                    <input type="hidden" name="udf2" value="{payment_data['udf2']}">
                    <input type="hidden" name="udf3" value="{payment_data['udf3']}">
                    <input type="hidden" name="udf4" value="{payment_data['udf4']}">
                    <input type="hidden" name="udf5" value="{payment_data['udf5']}">
                    <input type="hidden" name="hash" value="{payment_data['hash']}">
                </form>
                <script>
                    setTimeout(function() {{
                        document.getElementById('payuForm').submit();
                    }}, 2000);
                </script>
            </body>
            </html>
            """)
    

    async def redirect_success_response(self, payment_details: Dict):
        html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Payment Successful</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 20px;
                    }}
                    
                    .container {{
                        background: white;
                        border-radius: 20px;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                        max-width: 600px;
                        width: 100%;
                        padding: 40px;
                        text-align: center;
                        animation: slideIn 0.5s ease-out;
                    }}
                    
                    @keyframes slideIn {{
                        from {{
                            opacity: 0;
                            transform: translateY(-30px);
                        }}
                        to {{
                            opacity: 1;
                            transform: translateY(0);
                        }}
                    }}
                    
                    .success-icon {{
                        width: 100px;
                        height: 100px;
                        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 30px;
                        animation: scaleIn 0.5s ease-out 0.3s both;
                    }}
                    
                    @keyframes scaleIn {{
                        from {{
                            transform: scale(0);
                        }}
                        to {{
                            transform: scale(1);
                        }}
                    }}
                    
                    .success-icon::before {{
                        content: "✓";
                        color: white;
                        font-size: 60px;
                        font-weight: bold;
                    }}
                    
                    h1 {{
                        color: #11998e;
                        font-size: 32px;
                        margin-bottom: 15px;
                    }}
                    
                    .subtitle {{
                        color: #666;
                        font-size: 18px;
                        margin-bottom: 40px;
                    }}
                    
                    .details {{
                        background: #f8f9fa;
                        border-radius: 15px;
                        padding: 30px;
                        margin: 30px 0;
                        text-align: left;
                    }}
                    
                    .detail-row {{
                        display: flex;
                        justify-content: space-between;
                        padding: 12px 0;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    
                    .detail-row:last-child {{
                        border-bottom: none;
                    }}
                    
                    .label {{
                        color: #666;
                        font-weight: 600;
                    }}
                    
                    .value {{
                        color: #333;
                        font-weight: bold;
                        word-break: break-all;
                        text-align: right;
                        max-width: 60%;
                    }}
                    
                    .amount {{
                        font-size: 24px;
                        color: #11998e;
                    }}
                    
                    .btn {{
                        padding: 15px 40px;
                        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                        color: white;
                        border: none;
                        border-radius: 10px;
                        font-size: 16px;
                        font-weight: bold;
                        cursor: pointer;
                        text-decoration: none;
                        display: inline-block;
                        margin-top: 20px;
                    }}
                    
                    @media (max-width: 600px) {{
                        .value {{
                            max-width: 50%;
                            font-size: 14px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-icon"></div>
                    
                    <h1>Payment Successful! 🎉</h1>
                    <p class="subtitle">Your transaction has been completed successfully</p>
                    
                    <div class="details">
                        <div class="detail-row">
                            <span class="label">Amount Paid</span>
                            <span class="value amount">₹{payment_details['amount']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Transaction ID</span>
                            <span class="value">{payment_details['txnid']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Payment ID</span>
                            <span class="value">{payment_details['mihpayid']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Payment Mode</span>
                            <span class="value">{payment_details['payment_mode']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Bank Reference</span>
                            <span class="value">{payment_details['bank_ref_num']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Status</span>
                            <span class="value" style="color: #11998e;">{payment_details['status']}</span>
                        </div>
                    </div>
                    
                    <a href="/" class="btn">Make Another Payment</a>
                </div>
            </body>
            </html>
            """
            
        return HTMLResponse(content=html_content)
    

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
    

    async def check_payment_status(self, transaction_id: str) -> Optional[Dict]:

        command = "verify_payment"
        hash_value = generate_hash_check_payment_status(command, transaction_id)

        payload = {
            "key": self.PAYU_KEY,
            "command": command,
            "var1": transaction_id,
            "hash": hash_value
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:

                response = await client.post(
                    self.PAYMENT_STATUS_URL,
                    data=payload
                )

                response.raise_for_status()
                data = response.json()

                if data.get("status") == 1:
                    return {
                        "success": True,
                        "transaction_details": data.get("transaction_details", {}),
                        "message": "Payment details retrieved successfully"
                    }

                return {
                    "success": False,
                    "message": data.get("msg", "Unknown error"),
                    "data": data
                }

        except httpx.HTTPError as e:
            return {
                "success": False,
                "message": str(e)
            }

    async def check_payment_by_payu_id(self, mihpayid:str ):

        command = "check_payment"
        merchant_key = self.PAYU_KEY
        salt = self.PAYU_SALT

        hash_string = f"{merchant_key}|{command}|{mihpayid}|{salt}"
        hash_value = hashlib.sha512(hash_string.encode()).hexdigest()

        payload = {
            "key": merchant_key,
            "command": command,
            "var1": mihpayid,
            "hash": hash_value
        }

        url = "https://test.payu.in/merchant/postservice?form=2"

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, data=payload)

        print("Status Code:", response.status_code)
        print("Raw Response:", response.text)

        try:
            return response.json()
        except Exception:
            return {
                "error": "Invalid JSON response",
                "raw_response": response.text
            }
        
    async def initiate_refund(self, transaction_id, refund_amount, refund_token=None):

        if not refund_token:
            logger.info(f'NAV----> the refund_toke is {refund_token}')
            refund_token = generate_unique_refund_token()
            logger.info(f'NAV----> the refund_token after {refund_token}')

        command = "cancel_refund_transaction"

        hash_value = generate_refund_hash(
            self.PAYU_KEY,
            command,
            transaction_id,
            self.PAYU_SALT
        )

        payload = {
            "key": self.PAYU_KEY,
            "command": command,
            "var1": transaction_id,
            "var2": refund_token,
            "var3": str(refund_amount),
            "hash": hash_value
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                self.PAYMENT_STATUS_URL,
                data=payload,
                headers=headers
            )

        try:
            return response.json()

        except Exception:
            return {
                "status": 0,
                "msg": "Invalid JSON response",
                "raw_response": response.text
            }

    async def check_refund_status_reqid(self, request_id: str):

        command = "check_action_status"

        hash_value = generate_refund_hash(
            self.PAYU_KEY,
            command,
            request_id,
            self.PAYU_SALT
        )

        payload = {
            "key": self.PAYU_KEY,
            "command": command,
            "var1": request_id,
            "hash": hash_value
        }

        logger.info(f'NAV---->the payload data {payload}')
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                self.PAYMENT_STATUS_URL,
                data=payload,
                headers=headers
            )

        try:
            return response.json()

        except Exception:
            return {
                "status": 0,
                "msg": "Invalid JSON response",
                "raw_response": response.text
            }
        
    async def check_all_refunds_by_payu_id(self, payuid: str) -> Dict:

        command = "check_action_status"

        hash_value = generate_refund_hash(
            self.PAYU_KEY,
            command,
            payuid,
            self.PAYU_SALT
        )

        payload = {
            "key": self.PAYU_KEY,
            "command": command,
            "var1": payuid,   # PayU ID
            "var2": "payuid",              # Search by PayU ID
            "hash": hash_value
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                self.PAYMENT_STATUS_URL,
                data=payload,
                headers=headers
            )

        try:
            return response.json()

        except Exception:
            return {
                "status": 0,
                "msg": "Invalid JSON response",
                "raw_response": response.text
            }