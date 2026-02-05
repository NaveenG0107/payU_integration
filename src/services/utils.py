import hashlib
import logging
from os import environ
from datetime import datetime
from typing import Any, Dict
import uuid

logger = logging.getLogger(__name__)

# def generate_hash(data: dict) -> str:
#     PAYU_KEY = environ.get("PAYU_KEY")
#     PAYU_SALT = environ.get("PAYU_SALT")
#     hash_string = (
#         f"{PAYU_KEY}|{data['txnid']}|{data['amount']}|"
#         f"{data['productinfo']}|{data['firstname']}|{data['email']}|"
#         f"||||||||||{PAYU_SALT}"
#     )
#     generated_hash = hashlib.sha512(hash_string.encode()).hexdigest()
#     return generated_hash

def generate_hash(data: dict):
    PAYU_KEY = environ.get("PAYU_KEY")
    PAYU_SALT = environ.get("PAYU_SALT")
    hash_string = (
        f"{PAYU_KEY}|{data['txnid']}|{data['amount']}|"
        f"{data['productinfo']}|{data['firstname']}|{data['email']}|"
        f"{data.get('udf1','')}|{data.get('udf2','')}|{data.get('udf3','')}|"
        f"{data.get('udf4','')}|{data.get('udf5','')}||||||{PAYU_SALT}"
    )

    return hashlib.sha512(hash_string.encode()).hexdigest()

def verify_payu_hash(data: dict) -> bool:
    PAYU_KEY = environ.get("PAYU_KEY")
    PAYU_SALT = environ.get("PAYU_SALT")
    try:
        status = data.get('status', '')
        udf5 = data.get('udf5', '')
        udf4 = data.get('udf4', '')
        udf3 = data.get('udf3', '')
        udf2 = data.get('udf2', '')
        udf1 = data.get('udf1', '')
        email = data.get('email', '')
        firstname = data.get('firstname', '')
        productinfo = data.get('productinfo', '')
        amount = data.get('amount', '')
        txnid = data.get('txnid', '')

        hash_string = (
            f"{PAYU_SALT}|{status}|"
            f"||||||{udf5}|{udf4}|{udf3}|{udf2}|{udf1}|{email}|"
            f"{firstname}|{productinfo}|{amount}|{txnid}|{PAYU_KEY}"
        )
        generated_hash = hashlib.sha512(hash_string.encode()).hexdigest().lower()
        received_hash = data.get('hash', '').lower()

        logger.info(f"\n[HASH VERIFICATION]")
        logger.info(f"String: {hash_string}")
        logger.info(f"Generated: {generated_hash}")
        logger.info(f"Received:  {received_hash}")
        logger.info(f"Match: {generated_hash == received_hash}\n")
        
        return generated_hash == received_hash   
    except Exception as e:
        logger.info(f"[HASH VERIFICATION ERROR] {str(e)}")
        return False

def extract_payment_details(data: dict) -> Dict[str, Any]:
    """Extract structured payment details from PayU response"""
    return {
        "txnid": data.get('txnid'),
        "mihpayid": data.get('mihpayid'),
        "status": data.get('status'),
        "amount": data.get('amount'),
        "discount": data.get('discount', '0.00'),
        "net_amount_debit": data.get('net_amount_debit'),
        "firstname": data.get('firstname'),
        "lastname": data.get('lastname'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "address1": data.get('address1'),
        "city": data.get('city'),
        "state": data.get('state'),
        "country": data.get('country'),
        "zipcode": data.get('zipcode'),
        "productinfo": data.get('productinfo'),
        "payment_mode": data.get('mode'),
        "bank_ref_num": data.get('bank_ref_num'),
        "bankcode": data.get('bankcode'),
        "cardnum": data.get('cardnum'),
        "name_on_card": data.get('name_on_card'),
        "issuing_bank": data.get('issuing_bank'),
        "card_type": data.get('card_type'),
        "addedon": data.get('addedon'),
        "webhook_received_at": datetime.now().isoformat(),
        "error_message": data.get('error_Message', data.get('field9')),
        "hash": data.get('hash'),
        "hash_verified": verify_payu_hash(data)
    }

def generate_hash_check_payment_status(command: str, var1: str) -> str:
        PAYU_KEY = environ.get("PAYU_KEY")
        PAYU_SALT = environ.get("PAYU_SALT")
        hash_string = f"{PAYU_KEY}|{command}|{var1}|{PAYU_SALT}"
        return hashlib.sha512(hash_string.encode("utf-8")).hexdigest()

def generate_refund_hash(key, command, var1, salt):
    hash_string = f"{key}|{command}|{var1}|{salt}"
    return hashlib.sha512(hash_string.encode("utf-8")).hexdigest()

def generate_unique_refund_token():
    """
    Generate a unique refund token (max 23 characters)
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:6]
    return f"{timestamp}{unique_id}" 