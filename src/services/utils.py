import hashlib
import logging
from os import environ

logger = logging.getLogger(__name__)

def generate_hash(txnid, amount, productinfo, firstname, email):

    # Force 2 decimal format
    amount = f"{float(amount):.2f}"
    PAYU_KEY = environ.get("PAYU_KEY")
    PAYU_SALT = environ.get("PAYU_SALT")


    hash_string = (
        f"{PAYU_KEY}|{txnid}|{amount}|{productinfo}|"
        f"{firstname}|{email}|||||||||||{PAYU_SALT}"
    )

    return hashlib.sha512(
        hash_string.encode("utf-8")
    ).hexdigest().lower()

# def generate_hash(txnid, amount, productinfo, firstname, email):
#     PAYU_KEY = environ.get("PAYU_KEY")
#     PAYU_SALT = environ.get("PAYU_SALT")

#     hash_string = (
#         f"{PAYU_KEY}|{txnid}|{amount}|{productinfo}|"
#         f"{firstname}|{email}|||||||||||{PAYU_SALT}"
#     )

#     return hashlib.sha512(
#         hash_string.encode("utf-8")
#     ).hexdigest().lower()