from os import environ
from fastapi import FastAPI, Request, Form, APIRouter, HTTPException
from dotenv import load_dotenv
from services.utils import generate_hash, verify_payu_hash, extract_payment_details
from fastapi.responses import HTMLResponse
import uuid
import logging
import httpx
from datetime import datetime, timezone
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

# @router.post("/pay", response_class=HTMLResponse)
# async def initiate_payment(
#     firstname: str = Form(...),
#     email: str = Form(...),
#     phone: str = Form(...),
#     amount: float = Form(...),
#     productinfo: str = Form(...),
#     lastname: str = Form(""),
#     address1: str = Form(""),
#     city: str = Form(""),
#     state: str = Form(""),
#     country: str = Form("India"),
#     zipcode: str = Form(""),
# ):
#     """Initiate payment (WITHOUT UDF)"""

#     txnid = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
#     payment_data = {
#         "key": PAYU_KEY,
#         "txnid": txnid,
#         "amount": f"{amount:.2f}",
#         "productinfo": productinfo,
#         "firstname": firstname,
#         "lastname": lastname,
#         "email": email,
#         "phone": phone,
#         "surl": SUCCESS_URL,
#         "furl": FAILURE_URL,
#         "curl": FAILURE_URL,
#         "address1": address1,
#         "city": city,
#         "state": state,
#         "country": country,
#         "zipcode": zipcode,
#     }
    
#     payment_data["hash"] = generate_hash(payment_data)

#     response = payUPayment.initiate_payment(payment_data)
#     return response

@router.post("/pay", response_class=HTMLResponse)
async def initiate_payment(

    firstname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    amount: float = Form(...),
    productinfo: str = Form(...),

    lastname: str = Form(""),
    address1: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    country: str = Form("India"),
    zipcode: str = Form(""),

    udf1: str = Form(""),
    udf2: str = Form(""),
    udf3: str = Form(""),
    udf4: str = Form(""),
    udf5: str = Form(""),
):

    """Initiate payment (WITH UDF)"""

    txnid = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    payment_data = {

        "key": PAYU_KEY,
        "txnid": txnid,
        "amount": f"{amount:.2f}",

        "productinfo": productinfo,

        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phone": phone,

        "surl": SUCCESS_URL,
        "furl": FAILURE_URL,
        "curl": FAILURE_URL,

        "address1": address1,
        "city": city,
        "state": state,
        "country": country,
        "zipcode": zipcode,

        "udf1": udf1,
        "udf2": udf2,
        "udf3": udf3,
        "udf4": udf4,
        "udf5": udf5,
    }

    payment_data["hash"] = generate_hash(payment_data)

    response = payUPayment.initiate_payment(payment_data)

    return response


@router.post("/webhook/success")
async def payment_success_webhook(request: Request):

    form_data = await request.form()
    response_data = dict(form_data)
    logger.info(f"Nav----> the success url response {response_data}")

    is_valid = verify_payu_hash(response_data)
    
    if not is_valid:
        logger.info("Hash verification failed!")
    else:
        logger.info("Hash verified successfully")
    
    payment_details = extract_payment_details(response_data)

    response = await payUPayment.redirect_success_response(payment_details)

    return response


@router.post("/webhook/failure")
async def webhook_failure(request: Request):
    logger.info("Nav---->the payment failed")
    return payUPayment.webhook_failure(request)

@router.post("/payment/status/reqid")
async def verify_payment(request: Request):
    data = await request.json()

    result = await payUPayment.check_payment_status(
        data['transaction_id']
    )

    if not result:
        raise HTTPException(
            status_code=500,
            detail="PayU API Error"
        )

    if result["success"] is False:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return {
        "status": "success",
        "data": result
    }


@router.post("/payment/status/payuid")
async def verify_payment(request: Request):
    data = await request.json()

    try:
        result = await payUPayment.check_payment_by_payu_id(data['payuid'])
        return {
            "success": True,
            "data": result
        }

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"PayU connection error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/initiate_refund")
async def refund_api(request: Request):

    try:
        data = data = await request.json()

        result = await payUPayment.initiate_refund(
            data.get('transaction_id',''),
            data.get('refund_amount',''),
            data.get('refund_token',None)
        )

        return {
            "success": True,
            "data": result
        }

    except httpx.RequestError as e:

        raise HTTPException(
            status_code=502,
            detail=f"PayU connection error: {str(e)}"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )   

@router.post("/check-refund-status/reqid")
async def refund_status_reqid(request: Request):

    try:
        data = await request.json()

        result = await payUPayment.check_refund_status_reqid(data.get('transaction_id',''))

        return {
            "success": True,
            "data": result
        }

    except httpx.RequestError as e:

        raise HTTPException(
            status_code=502,
            detail=f"PayU connection error: {str(e)}"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post("/check-refund-status/payuid")
async def check_all_refunds_api(request: Request):

    try:
        data = await request.json()

        result = await payUPayment.check_all_refunds_by_payu_id(
            data.get('payuid','')
        )

        return {
            "success": True,
            "data": result
        }

    except httpx.RequestError as e:

        raise HTTPException(
            status_code=502,
            detail=f"PayU sandbox connection error: {str(e)}"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

@router.get("/sms")
async def webhook_failure(request: Request):
    html_content = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting to PayU...</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }

        .loader {
            text-align: center;
            color: white;
        }

        .spinner {
            width: 60px;
            height: 60px;
            border: 5px solid rgba(255, 255, 255, 0.3);
            border-top: 5px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 30px;
        }

        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }

            100% {
                transform: rotate(360deg);
            }
        }

        h2 {
            font-size: 28px;
            margin-bottom: 15px;
        }
    </style>
</head>

<body>
    <div class="loader">
        <div class="spinner"></div>
        <h2>Redirecting to PayU...</h2>
        <p>Transaction ID: TXN20260204131521995404</p>
        <p>Amount: ₹10.00</p>
    </div>

    <form id="payuForm" action="https://test.payu.in/_payment" method="post">
        <input type="hidden" name="key" value="IatdlB">
        <input type="hidden" name="txnid" value="TXN20260204131521995404">
        <input type="hidden" name="amount" value="10.00">
        <input type="hidden" name="productinfo" value="Test Product">
        <input type="hidden" name="firstname" value="Test User">
        <input type="hidden" name="lastname" value="Kumar">
        <input type="hidden" name="email" value="test@example.com">
        <input type="hidden" name="phone" value="9876543210">
        <input type="hidden" name="surl" value="https://lankly-multipointed-kirstie.ngrok-free.dev/api/webhook/success">
        <input type="hidden" name="furl" value="https://lankly-multipointed-kirstie.ngrok-free.dev/api/webhook/failure">
        <input type="hidden" name="curl" value="https://lankly-multipointed-kirstie.ngrok-free.dev/api/webhook/failure">
        <input type="hidden" name="address1" value="">
        <input type="hidden" name="city" value="">
        <input type="hidden" name="state" value="">
        <input type="hidden" name="country" value="India">
        <input type="hidden" name="zipcode" value="">
        <input type="hidden" name="hash" value="927d773052575e17602fb0eff9322c9e6e61aa8f547c7604985de2ee8909c1004d1e3d531118c05dc55d9c59c7a0f4620a6da921769984c86216433e8fe46bce">
    </form>

    <script>
        setTimeout(function() {
                        document.getElementById('payuForm').submit();
                    }, 2000);
    </script>
</body>

</html>"""


    logger.info(f'html contetrn {html_content}')
    return HTMLResponse(html_content)