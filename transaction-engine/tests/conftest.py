from datetime import datetime

import pytest

from pymongo import MongoClient

from app import blueprint
from app.api import create_app

from app.api.models.bank import Bank
from app.api.models.wallet import Wallet
from app.api.models.loan_request import LoanRequest
from app.api.models.investor import Investor, InvestorRdl
from app.api.models.investment import Investment, LoanRequestEmbed
from app.api.models.user import User
from app.api.models.transaction import PaymentEmbed, Transaction


@pytest.fixture(scope="session", autouse=True)
def setup_flask_app():
    flask_app = create_app("test")
    flask_app.register_blueprint(blueprint, url_prefix="/api/v1")

    ctx = flask_app.app_context()
    ctx.push()
    yield flask_app
    # drop collection on tear down
    client = MongoClient(flask_app.config["MONGO_URI"])
    client.drop_database(flask_app.config["MONGO_DBNAME"])
    ctx.pop()


@pytest.fixture(scope="session")
def setup_client(setup_flask_app):
    return setup_flask_app.test_client()


@pytest.fixture(scope="module")
def setup_user():
    data = {
        "email": "kelvin@modana.id",
        "password": "password",
        "account_type": "INVESTOR",
        "msidn": "081219644314",
        "otp_status": "VERIFIED",
        "is_email_verified": "VERIFIED",
    }
    user = User(**data)
    user.commit()
    return user


@pytest.fixture(scope="module")
def setup_analyst():
    data = {
        "email": "analyst@modana.id",
        "password": "password",
        "account_type": "ANALYST",
        "msidn": "081219644310",
        "role": "SUPERADMIN",
    }
    user = User(**data)
    user.commit()
    return user


@pytest.fixture(scope="module")
def setup_bni_bank():
    data = {
        "bank_name": "PT BNI Indonesia",
        "interbank_code": "009",
        "clearing_code": "90010",
        "rtgs_code": "BNINIDJA",
    }
    bank = Bank(**data)
    bank.commit()
    return bank


@pytest.fixture(scope="module")
def setup_bca_bank():
    data = {
        "bank_name": "PT BCA Indonesia",
        "interbank_code": "014",
        "clearing_code": "140397",
        "rtgs_code": "CENAIDJA",
    }
    bank = Bank(**data)
    bank.commit()
    return bank


@pytest.fixture(scope="module")
def setup_investor(setup_user, setup_analyst, setup_bni_bank, setup_bca_bank):
    data = {
        "user_id": setup_user.id,
        "email": "kelvin@modana.id",
        "title": "some title",
        "first_name": "kelvin",
        "last_name": "desman",
        "npwp": {"npwp_option": "1", "npwp_no": "137812783172"},
        "nationality": "ID",
        "domicile_country": "ID",
        "religion": "3",
        "birth_date": datetime.utcnow(),
        "birth_place": "Jakarta",
        "gender": "M",
        "is_married": "j",
        "mother_maiden_name": "fairy maiden",
        "job_code": "12345",
        "education": "007",
        "ktp": {
            "images": {
                "content_type": "ktp-content",
                "name": "ktp-name",
                "image": "ktp-image",
            },
            "no": "123441243123121421",
            "issuing_city": "JAKARTA",
            "expire_date": datetime.utcnow(),
        },
        "address": {
            "street": "must be street",
            "rt_rw_perum": "rt rw perum",
            "province": "must be province",
            "city": "must be address cirty",
            "kelurahan": "kelurahan",
            "kecamatan": "kecamatan",
            "zip_code": "122345",
        },
        "home_phone": "02112312312312",
        "office_phone": "02112312312312",
        "mobile_phone": "0812312312312",
        "fax": "01212312312321",
        "monthly_income": 800000000,
        "branch_opening": "0259",
        "source_of_funds": "HEIST",
        "source": "NEWS",
        "otp_status": "VERIFIED",
        "email_code": "some cool email code",
        "passport": "12312312312312321213",
        "is_email_verified": "VERIFIED",
        "approver_info": {"message": "some message", "approver_id": setup_analyst.id},
        "bank_accounts": [
            {
                "bank_id": setup_bni_bank.id,
                "bank_name": setup_bni_bank.bank_name,
                "account_no": "01231231312",
                "account_name": "Kelvin Desman",
                "account_type": "RDL_ACCOUNT",
            },
            {
                "bank_id": setup_bni_bank.id,
                "bank_name": setup_bni_bank.bank_name,
                "account_no": "001122330011",
                "account_name": "Kelvin Desman BNI",
                "account_type": "BANK_ACCOUNT",
            },
            {
                "bank_id": setup_bca_bank.id,
                "bank_name": setup_bca_bank.bank_name,
                "account_no": "009922113300",
                "account_name": "Kelvin Desman BCA",
                "account_type": "BANK_ACCOUNT",
            }
        ],
    }
    investor = Investor(**data)
    investor.commit()
    return investor


@pytest.fixture(scope="module")
def setup_investor_rdl(setup_investor):
    data = {
        "investor_id": setup_investor.id,
        "title": "01",
        "first_name": "Juan",
        "middle_name": "",
        "last_name": "Daniel",
        "npwp_option": "1",
        "npwp_no": "999999999999999",
        "nationality": "ID",
        "country": "ID",
        "religion": "2",
        "birth_place": "Semarang",
        "birth_date": "26111980",
        "gender": "M",
        "is_married": "L",
        "mother_maiden_name": "Dina Maryati",
        "job_code": "01",
        "education": "07",
        "id_number": "331234766887878518",
        "id_issuing_city": "Jakarta Barat",
        "id_expire_date": "26102099",
        "address_street": "Jalan Mawar Melati",
        "address_rt_rw_perum": "003009Sentosa",
        "address_kelurahan": "Cengkareng Barat",
        "address_kecamatan": "Cengkareng/Jakarta Barat",
        "zip_code": "11730",
        "home_phone_ext": "021",
        "home_phone": "745454545",
        "office_phone_ext": "",
        "office_phone": "",
        "mobile_phone_ext": "0812",
        "mobile_phone": "323232",
        "fax_ext": "",
        "fax": "",
        "email": "juan.daniel@gmail.com",
        "monthly_income": "8000000",
        "branch_opening": "0259",
    }
    investor_rdl = InvestorRdl(**data)
    investor_rdl.commit()
    return investor_rdl


@pytest.fixture(scope="module")
def setup_investment(setup_investor, setup_loan_request, setup_bni_bank):
    data = {
        "investor_id": setup_investor.id,
        "total_amount": 1000000,
        "bank_accounts": [
            {
                "bank_id": setup_bni_bank.id,
                "bank_name": setup_bni_bank.bank_name,
                "account_no": "01231231312123123",
                "account_name": "Investment Kelvin Desman",
                "account_type": "VIRTUAL_ACCOUNT",
            }
        ],
        "loan_requests": [{"loan_request_id": setup_loan_request.id}],
    }
    investment = Investment(**data)
    investment.commit()
    return investment


@pytest.fixture(scope="module")
def setup_loan_request(setup_bni_bank):
    data = {
        "bank_accounts": [
            {
                "bank_id": setup_bni_bank.id,
                "bank_name": setup_bni_bank.bank_name,
                "account_no": "9888888128381123",
                "account_name": "Kelvin Desman",
                "account_type": "VIRTUAL_ACCOUNT",
                "label": "MODANAKU"
            },
            {
                "bank_id": setup_bni_bank.id,
                "bank_name": setup_bni_bank.bank_name,
                "account_no": "9888888128000000",
                "account_name": "Repayment Kelvin Desman",
                "account_type": "VIRTUAL_ACCOUNT",
                "label": "REPAYMENT"
            }
        ]
    }
    loan_request = LoanRequest(**data)
    loan_request.commit()
    return loan_request


@pytest.fixture(scope="module")
def setup_investor_wallet(setup_user):
    wallet = Wallet(user_id=setup_user.id, balance=1000)
    wallet.commit()
    return wallet


@pytest.fixture(scope="module")
def setup_escrow_wallet(setup_bni_bank):
    bank_accounts = [
        {
            "bank_id": setup_bni_bank.id,
            "bank_name": setup_bni_bank.bank_name,
            "account_no": "111222334",
            "account_type": "BANK_ACCOUNT",
            "account_name": "PT AMANAH ESCROW",
        }
    ]
    wallet = Wallet(bank_accounts=bank_accounts)
    wallet.commit()
    return wallet


@pytest.fixture(scope="module")
def setup_profit_wallet(setup_bni_bank):
    bank_accounts = [
        {
            "bank_id": setup_bni_bank.id,
            "bank_name": setup_bni_bank.bank_name,
            "account_no": "000022334555",
            "account_type": "BANK_ACCOUNT",
            "account_name": "PT AMANAH PROFIT",
        }
    ]
    wallet = Wallet(bank_accounts=bank_accounts)
    wallet.commit()
    return wallet


@pytest.fixture(scope="module")
def setup_debit_transaction(setup_investor_wallet, setup_investor, setup_investment):
    # debit trransaction to deduct investor wallet
    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR",
        destination_id=setup_investment.id,
        destination_type="INVESTMENT",
        amount=-100,
        transaction_type="INVEST",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()
    return transaction


@pytest.fixture(scope="module")
def setup_credit_transaction(setup_investor_wallet, setup_investor):
    # debit trransaction to deduct investor wallet
    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR_RDL_ACC",
        destination_id=setup_investor.id,
        destination_type="INVESTOR",
        amount=1000000,
        transaction_type="TOP_UP_RDL",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()
    return transaction
