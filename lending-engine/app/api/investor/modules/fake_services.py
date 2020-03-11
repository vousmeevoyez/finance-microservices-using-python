"""
    Services Class
    _______________
    Handle logic to models or external party API
"""
import bcrypt

from datetime import datetime, timedelta
from faker import Faker
from bson import ObjectId
from flask import current_app

from app.api.lib.core.exceptions import BaseError
from app.api.models.user import User
from app.api.models.investor import Investor, InvestorRdl


class ServicesError(BaseError):
    """ error raised when something wrong at services """


faker = Faker("en_US")


def create_random_user():
    password = "password"
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt)
    data = {
        "email": faker.email(),
        "password": hashed_pw,
        "account_type": "INVESTOR",
        "msidn": "08" + faker.msisdn()[0:10],
        "otp_status": "VERIFIED",
        "is_email_verified": "VERIFIED",
        "permissions": [
            "list_loans",
            "approve_loans",
            "fetch_loan",
            "list_approved_loans",
            "invest",
            "view_account_information",
            "view_rdl_balance",
            "manage_account",
            "rdl_withdraw",
            "list_loan_history",
            "manage_users",
            "superadmin",
        ],
    }
    user = User(**data)
    user.commit()
    return user


def create_random_investor():
    user = create_random_user()

    products = list(current_app.db.lender_products.find({}))
    fees = []
    for product in products:
        interest = product["interests"]
        fees.append(
            {
                "product_id": product["_id"],
                "late_fee": interest["lf"],
                "upfront_fee": interest["uf"],
                "upfront_fee_type": interest["ut"],
                "penalty_fee": interest["pf"],
                "penalty_fee_type": interest["pft"],
                "service_fee": interest["sf"],
                "service_fee_type": interest["sft"],
                "admin_fee": interest["adf"],
                "admin_fee_type": interest["adft"],
            }
        )

    data = {
        "user_id": user.id,
        "email": user.email,
        "title": "01",
        "first_name": faker.first_name(),
        "middle_name": "",
        "last_name": faker.last_name(),
        "npwp": {"npwp_option": "1", "npwp_no": "999999999999999"},
        "nationality": "ID",
        "domicile_country": "ID",
        "religion": "3",
        "birth_date": faker.date_time_between(start_date="-40y", end_date="-1y"),
        "birth_place": "Jakarta",
        "gender": "M",
        "is_married": "J",
        "mother_maiden_name": faker.name(),
        "job_code": "01",
        "education": "07",
        "ktp": {
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
            "zip_code": "15142",
        },
        "home_phone": "021745454545",
        "office_phone": "02112312312312",
        "mobile_phone": "08" + faker.msisdn()[0:10],
        "fax": "01212312312321",
        "monthly_income": 8000000,
        "branch_opening": "0259",
        "source_of_funds": "1",
        "source": "INTERNET",
        "approver_info": {
            "reason_id": ObjectId("7c6519967d3aa0cae0985325"),
            "message": "",
            "approver_id": ObjectId("5d12da2baba97641c806baac"),
        },
        "approvals": [{"status": "PENDING"}],
        "fees": fees,
    }
    investor = Investor(**data)
    investor.commit()

    # add investor id
    user.investor_id = investor.id
    user.commit()

    rdl_data = {
        "investor_id": investor.id,
        "address_kecamatan": investor["address"]["kecamatan"],
        "address_kelurahan": investor["address"]["kelurahan"],
        "address_rt_rw_perum": "113/123",
        "address_street": "1312313",
        "birth_date": "15061971",
        "birth_place": "Jakarta",
        "branch_opening": "0259",
        "country": "ID",
        "education": "04",
        "email": investor["email"],
        "fax": "",
        "fax_ext": "",
        "first_name": investor["first_name"],
        "gender": "M",
        "home_phone": "11317659",
        "home_phone_ext": "0853",
        "id_expire_date": "01012098",
        "id_issuing_city": "jakarta barat",
        "id_number": investor["ktp"]["no"],
        "is_married": "L",
        "job_code": "01",
        "last_name": investor["last_name"],
        "middle_name": investor["middle_name"],
        "mobile_phone": investor["mobile_phone"][:8],
        "mobile_phone_ext": "0853",
        "monthly_income": "8000000",
        "mother_maiden_name": "asadsdasd",
        "nationality": "ID",
        "npwp_no": investor["npwp"]["npwp_no"],
        "npwp_option": "1",
        "office_phone": "11317659",
        "office_phone_ext": "0853",
        "religion": "5",
        "title": "01",
        "zip_code": "33512",
    }

    investor_rdl = InvestorRdl(**rdl_data)
    investor_rdl.commit()
    return investor, user
