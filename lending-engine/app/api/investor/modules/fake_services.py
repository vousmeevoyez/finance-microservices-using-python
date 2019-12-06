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
from app.api.models.investor import Investor


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
        fees.append({
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
        })

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
            "approver_id": ObjectId("5d12da2baba97641c806baac")
        },
        "approvals": [{
            "status": "PENDING"
        }],
        "fees": fees
    }
    investor = Investor(**data)
    investor.commit()
    return investor, user
