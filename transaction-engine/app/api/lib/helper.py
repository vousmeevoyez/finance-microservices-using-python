import functools
import sys
import random
import uuid
from datetime import datetime

from app.api.models.investment import Investment
from app.api.models.investor import Investor
from app.api.models.wallet import Wallet
from app.api.models.base import BankAccEmbed
from app.api.models.loan_request import LoanRequest


def generate_opg_ref(destination, amount=None):
    """ generate reference number matched to BNI OPG format"""
    now = datetime.utcnow()
    # first 8 digit is date
    value_date = now.strftime("%Y%m%d%H%M")
    randomize = random.randint(1, 99)

    end_fix = str(destination)[:8]
    if amount is not None:
        end_fix = str(destination)[:4] + str(amount)[:4]

    return str(value_date) + str(end_fix) + str(randomize)


def generate_rdl_ref():
    """ generate reference number matched to BNI RDL format"""
    return str(uuid.uuid4()).replace("-", "").upper()[:16]


@functools.lru_cache(maxsize=128)
def generate_ref_number(provider, destination, amount=None):
    """ generate reference number based on each accepted provider!"""
    reference = generate_opg_ref(destination, amount)
    if provider == "BNI_RDL":
        reference = generate_rdl_ref()
    return reference


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
