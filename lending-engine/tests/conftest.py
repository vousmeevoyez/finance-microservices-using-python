from datetime import datetime, date
import random

import pytest

from pymongo import MongoClient

from app import blueprint
from app.api import create_app

from app.api.models.base import StatusEmbed
from app.api.models.bank import Bank
from app.api.models.product import Product
from app.api.models.wallet import Wallet
from app.api.models.loan_request import LoanRequest
from app.api.models.investor import Investor, InvestorRdl
from app.api.models.investment import Investment, LoanRequestEmbed
from app.api.models.user import User
from app.api.models.transaction import PaymentEmbed, Transaction
from app.api.models.borrower import Borrower
from app.api.models.file import File, Article


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
def setup_borrower_user():
    data = {
        "email": "jennie@blackpink.id",
        "password": "password",
        "account_type": "BORROWER",
        "msidn": "81219644123",
        "user_virtual_account": {
            "account_no": "some-account-no",
            "trx_id": "some-trx-id",
            "wallet_id": "some-wallet-id"
        }
    }
    user = User(**data)
    user.commit()
    return user


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
def setup_user2():
    data = {
        "email": "jennie@bp.com",
        "password": "password",
        "account_type": "INVESTOR",
        "msidn": "081219644319",
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
        "bank_name": "PT BANK NEGARA INDONESIA 1946 (Persero) Tbk",
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
def setup_mocepat_product():
    data = {
        "grades": [
            {
                "grade": "A",
                "min_score": 300,
                "max_score": 1000,
            },
            {
                "grade": "B",
                "min_score": 265,
                "max_score": 299,
            },
            {
                "grade": "C",
                "min_score": 238,
                "max_score": 264,
            }
        ],
        "product_type": "one-time-payment",
        "product_name": "Mocepat",
        "is_active": True,
        "interests": {
            "investor_fee": 30,
            "investor_fee_type": "PERCENT",
            "profit_fee": 70,
            "profit_fee_type": "PERCENT",
            "minimum_fee": 25000,
            "service_fee": 0,
            "service_fee_type": "PERCENT",
            "admin_fee": 0,
            "admin_fee_type": "PERCENT",
            "min_tenor": 6,
            "max_tenor": 30,
            "late_fee": 1,
            "late_fee_type": "PERCENT",
            "loan_amounts": [
                {
                    "amount": 500000
                },
                {
                    "amount": 1000000
                }
            ],
            "penalty_fee": 0,
            "penalty_fee_type": "PERCENT",
            "grade_period": 2,
            "max_late_fee": 30,
            "fees": [{
                "start_tenor": 7,
                "end_tenor": 14,
                "fee": 0.5,
                "fee_type": "PERCENT"
            }, {
                "start_tenor": 15,
                "end_tenor": 30,
                "fee": 0.4,
                "fee_type": "PERCENT"
            }]
        },
        "freeze_period": 7,
        "min_score": 181,
        "max_salary": 30,
        "max_salary_type": "PERCENT"
    }
    product = Product(**data)
    product.commit()
    return product


@pytest.fixture(scope="module")
def setup_investor(setup_user, setup_analyst, setup_bni_bank):
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
        "approver_info": {
            "message": "some message",
            "approver_id": setup_analyst.id
        },
        "fees": [
            {
                "late_fee": 30,
                "late_fee_type": "PERCENT",
                "upfront_fee": 10,
                "upfront_fee_type": "PERCENT",
                "penalty_fee": 30,
                "penalty_fee_type": "PERCENT",
                "service_fee": 30,
                "service_fee_type": "PERCENT",
                "admin_fee": 30,
                "admin_fee_type": "PERCENT",
            }
        ],
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
                "account_no": "112233445566",
                "account_name": "BNI Kelvin Desman",
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
def setup_investment(setup_investor, setup_bni_bank):
    data = {
        "investor_id": setup_investor.id,
        "total_amount": 500000,
        "bank_accounts": [
            {
                "bank_id": setup_bni_bank.id,
                "bank_name": setup_bni_bank.bank_name,
                "account_no": "9889909612123123",
                "account_name": "Investment Kelvin Desman",
                "account_type": "VIRTUAL_ACCOUNT",
            }
        ],
    }
    investment = Investment(**data)
    investment.commit()
    return investment


@pytest.fixture(scope="module")
def setup_tnc_file():
    data = {
        "file_type": "terms",
        "content": "$PEMBERI_PINJAMAN",
        "language": "id"
    }
    article = Article(**data)
    article.commit()
    return article


@pytest.fixture(scope="module")
def make_loan_request(setup_borrower,
                      setup_borrower_user,
                      setup_bni_bank,
                      setup_mocepat_product,
                      setup_investment,
                      setup_tnc_file):
    def _make_loan_request(overdue=0, tenor=15,
                           requested_loan_request=500000,
                           disburse_amount=477500, service_fee=22500,
                           status="APPROVED"):

        random_no = random.randint(111111, 999999)
        random_va = "9889909611" + str(random_no)

        data = {
            "investment_id": setup_investment.id,
            "overdue": overdue,
            "payment_state_status": "LANCAR",
            "product_id": setup_mocepat_product.id,
            "user_id": setup_borrower_user.id,
            "borrower_id": setup_borrower.id,
            "loan_request_code": "2891017100028",
            "tenor": tenor,
            "status": status,
            "requested_loan_request": requested_loan_request,
            "payment_date": date.today(),
            "due_date": "2019-11-25T00:00:00.000Z",
            "upfront_fee": 0.3,
            "upfront_fee_type": "PERCENT",
            "disburse_amount": disburse_amount,
            "loan_purpose": "Liburan",
            "service_fee": service_fee,
            "note": "",
            "loan_counter": 3,
            "requested_date": "2019-11-08T05:00:00.000Z",
            "payment_states": [],
            "payment_schedules": [],
            "loan_repayments": [],
            "approvals": [],
            "late_fee_logs": [],
            "credit_score": 194,
            "grade": "D",
            "tnc": {
                "file_id": setup_tnc_file.id,
                "is_agreed": True,
            },
            "modanaku": {
                "wallet_id": "modanaku-wallet-id"
            },
            "bank_accounts": [
                {
                    "bank_id": setup_bni_bank.id,
                    "bank_name": setup_bni_bank.bank_name,
                    "account_no": random_va,
                    "account_name": "Repayment Kelvin Desman",
                    "account_type": "VIRTUAL_ACCOUNT",
                    "label": "REPAYMENT"
                },
                {
                    "bank_id": setup_bni_bank.id,
                    "bank_name": setup_bni_bank.bank_name,
                    "account_no": "9889909600023123",
                    "account_name": "Modanaku Kelvin Desman",
                    "account_type": "VIRTUAL_ACCOUNT",
                    "label": "MODANAKU"
                }
            ],
        }
        loan_request = LoanRequest(**data)
        loan_request.commit()
        return loan_request
    return _make_loan_request


@pytest.fixture(scope="module")
def setup_investor_wallet(setup_user):
    wallet = Wallet(user_id=setup_user.id, balance=1000)
    wallet.commit()
    return wallet


@pytest.fixture(scope="module")
def setup_investor_wallet2(setup_user2):
    wallet = Wallet(user_id=setup_user2.id, balance=1000)
    wallet.commit()
    return wallet


@pytest.fixture(scope="module", autouse=True)
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
    wallet = Wallet(bank_accounts=bank_accounts, label="ESCROW")
    wallet.commit()
    return wallet


@pytest.fixture(scope="module", autouse=True)
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
    wallet = Wallet(bank_accounts=bank_accounts, label="PROFIT")
    wallet.commit()
    return wallet


@pytest.fixture(scope="module")
def make_transaction():
    def _make_transaction(wallet_id, source_id, source_type,
                          destination_id, destination_type, amount,
                          transaction_type):
        # debit trransaction to deduct investor wallet
        transaction = Transaction(
            wallet_id=wallet_id,
            source_id=source_id,
            source_type=source_type,
            destination_id=destination_id,
            destination_type=destination_type,
            amount=amount,
            transaction_type=transaction_type,
        )

        payment = PaymentEmbed()
        payment.generate_payment_info(transaction)

        transaction.payment = payment
        transaction.commit()
        return transaction
    return _make_transaction


@pytest.fixture(scope="module")
def setup_borrower(setup_borrower_user):
    data = {
        "domicile_country": "Indonesia",
        "email": "rose@blackpink.id",
        "first_name": "Rose",
        "birth_date": date.today(),
        "gender": "M",
        "marital_status": "L",
        "mobile_phone_ext": "62",
        "mobile_phone": "87880196680",
        "address": {
            "city": "Tangerang Selatan",
            "kecamatan": "Pondok Pucung",
            "kelurahan": "Pondok Aren",
            "province": "Banten",
            "zip_code": "15229",
            "correspondence_address": "Jalan Istora Madya",
            "city_validation": True,
            "kecamatan_validation": False,
            "kelurahan_validation": False,
            "province_validation": True,
            "rt_rw_perum": "",
            "street": "Jalan Istora Madya",
            "street_validation": False,
            "length_of_stay": 60,
            "length_of_stay_validation": False,
            "residency_status": "Pribadi",
            "residency_status_validation": False,
            "zip_code_validation": True
        },
        "ktp": {
            "no": "1471120607930002",
            "validation": True
        },
        "npwp": {
            "no": "88775566",
            "validation": True
        },
        "work_info": [
            {
                "basic_salary": 10000000,
                "employee_no": "1112223334445",
                "payslip": {
                },
                "address": {
                    "street": "Benhil No 101",
                    "kelurahan": "Tebet Timur",
                    "kecamatan": "Tebet",
                    "city": "Jakarta Selatan",
                    "province": "DKI Jakarta",
                    "zip_code": "32312",
                    "city_validation": True,
                    "kecamatan_validation": True,
                    "kelurahan_validation": True,
                    "province_validation": True,
                    "street_validation": True,
                    "zip_code_validation": True
                },
                "company_id": "88JeQUSRUaEPwR9i9fJEBF",
                "company_name": "pt baru banget",
                "company_phone_no": "1222333444",
                "industry_type": "Animasi",
                "position": "Assistant Manager",
                "employment_status": "Permanent",
                "work_date_start": date.today(),
                "payment_date": date.today(),
                "employee_id": "KQzTLbiH23vKuSKtykuFde",
                "basic_salary_validation": True,
                "contract_end_date": None,
                "contract_end_date_validation": False,
                "company_name_validation": True,
                "employee_no_validation": True,
                "employment_status_validation": False,
                "position_validation": True,
                "work_date_start_validation": False
            }
        ],
        "user_id": setup_borrower_user.id,
        "emergency_contacts": [
            {
                "first_name_validation": False,
                "first_name": "Jennie",
                "phone_no_validation": False,
                "phone_no": "087880196655",
                "relationship_validation": False,
                "relationship": "Saudara Perempuan",
                "index": "emergencyContact_1",
            },
            {
                "first_name_validation": False,
                "first_name": "Lisa",
                "phone_no_validation": False,
                "phone_no": "087880196633",
                "relationship_validation": False,
                "relationship": "Teman",
                "index": "emergencyContact_2",
            },
            {
                "first_name_validation": False,
                "first_name": "Hanekawa",
                "phone_no_validation": False,
                "phone_no": "087880195544",
                "relationship_validation": False,
                "relationship": "Sepupu",
                "index": "emergencyContact_3",
            }
        ],
        "borrower_code": "91017100027",
        "age": 26,
        "age_validation": True,
        "birth_date_validation": True,
        "birth_place": "Sleman",
        "birth_place_validation": True,
        "education": "S1",
        "education_validation": True,
        "email_validation": True,
        "first_name_validation": True,
        "gender_validation": True,
        "home_phone": "",
        "home_phone_validation": True,
        "last_name": "Kim",
        "last_name_validation": True,
        "mother_maiden_name": "Tifa",
        "mother_maiden_name_validation": False,
        "middle_name": "",
        "middle_name_validation": True,
        "mobile_phone_validation": True,
        "marital_status_validation": False,
        "no_of_child": 0,
        "no_of_child_validation": True,
        "partner_name_validation": False,
        "religion": "Islam",
        "religion_validation": True,
        "nationality": "Indonesia"
    }
    borrower = Borrower(**data)
    borrower.commit()
    return borrower


@pytest.fixture(scope="module")
def setup_investment_with_loan(setup_investment, make_loan_request):
    loan_request = make_loan_request()
    investment_loan_request = {
        "loan_request_id": loan_request.id,
        "disburse_amount": 477500,
        "total_fee": 22500,
        "fees": [
            {
                "name": "upfrontFee",
                "investor_fee": 225,
                "profit_fee": 2275
            }
        ]
    }
    setup_investment.loan_requests.append(investment_loan_request)
    setup_investment.commit()
    return setup_investment, loan_request


@pytest.fixture(scope="module")
def setup_investment_with_transaction(
    setup_escrow_wallet,
    setup_profit_wallet,
    setup_investment_with_loan,
    make_transaction,
    setup_investor_wallet,
    setup_investor
):
    # get investment object to be add
    investment, loan_request = setup_investment_with_loan
    # create invest transaction
    invest_trx = make_transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR",
        destination_id=investment.id,
        destination_type="INVESTMENT",
        amount=-500000,
        transaction_type="INVEST"
    )

    # create receive upfront fee transaction
    receive_upfront_trx = make_transaction(
        wallet_id=setup_profit_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=1000000,
        transaction_type="RECEIVE_UPFRONT_FEE"
    )

    # create send upfront fee transaction
    send_upfront_trx = make_transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=-1000000,
        transaction_type="UPFRONT_FEE"
    )

    # create send modanaku transaction
    send_modanaku_trx = make_transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=loan_request.id,
        destination_type="MODANAKU",
        amount=-1000000,
        transaction_type="DISBURSE"
    )

    # create send invest fee transaction
    send_invest_fee_trx = make_transaction(
        wallet_id=setup_profit_wallet.id,
        source_id=setup_profit_wallet.id,
        source_type="PROFIT",
        destination_id=setup_escrow_wallet.id,
        destination_type="ESCROW",
        amount=-1000000,
        transaction_type="INVEST_FEE"
    )

    # create receive invest fee transaction
    receive_invest_fee_trx = make_transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_profit_wallet.id,
        source_type="PROFIT",
        destination_id=setup_escrow_wallet.id,
        destination_type="ESCROW",
        amount=1000000,
        transaction_type="RECEIVE_INVEST_FEE"
    )

    transactions = []
    invest_trx_payload = {
        "transaction_id": invest_trx.id,
        "status": "SEND_TO_INVESTMENT_REQUESTED"
    }
    send_upfront_trx_payload = {
        "transaction_id": send_upfront_trx.id,
        "status": "SEND_TO_PROFIT_REQUESTED"
    }
    receive_upfront_trx_payload = {
        "transaction_id": receive_upfront_trx.id,
        "status": "RECEIVE_UPFRONT_FEE_REQUESTED"
    }
    send_modanaku_trx_payload = {
        "transaction_id": send_modanaku_trx.id,
        "status": "SEND_TO_MODANAKU_REQUESTED"
    }
    send_invest_fee_trx_payload = {
        "transaction_id": send_invest_fee_trx.id,
        "status": "SEND_FEE_TO_ESCROW_REQUESTED"
    }
    receive_invest_fee_trx_payload = {
        "transaction_id": receive_invest_fee_trx.id,
        "status": "RECEIVE_FEE_FROM_PROFIT_REQUESTED"
    }
    transactions.append(invest_trx)
    transactions.append(send_upfront_trx)
    transactions.append(receive_upfront_trx)
    transactions.append(send_modanaku_trx)
    transactions.append(send_invest_fee_trx)
    transactions.append(receive_invest_fee_trx)

    investment.list_of_status.append(invest_trx_payload)
    investment.list_of_status.append(send_upfront_trx_payload)
    investment.list_of_status.append(receive_upfront_trx_payload)
    investment.list_of_status.append(send_modanaku_trx_payload)
    investment.commit()

    # add modanaku transaction to loan request
    loan_request.list_of_status.append(send_modanaku_trx_payload)
    loan_request.list_of_status.append(send_invest_fee_trx_payload)
    loan_request.list_of_status.append(receive_invest_fee_trx_payload)
    loan_request.commit()

    return investment, loan_request, transactions
