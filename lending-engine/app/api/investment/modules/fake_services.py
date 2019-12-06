"""
    Services Class
    _______________
    Handle logic to models or external party API
"""
import random
from datetime import datetime, timedelta
from faker import Faker
import bcrypt
from bson import ObjectId

from flask import current_app
from app.api.lib.core.exceptions import BaseError
from app.api.models.investment import Investment
from app.api.models.user import User
from app.api.models.loan_request import LoanRequest
from app.api.models.borrower import Borrower


class ServicesError(BaseError):
    """ error raised when something wrong at services """


faker = Faker("en_US")


def create_random_borrower_user():
    password = "password"
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt)
    data = {
        "email": faker.email(),
        "password": hashed_pw,
        "account_type": "BORROWER",
        "msidn": "08" + faker.msisdn()[0:10],
        "otp_status": "VERIFIED",
        "is_email_verified": "VERIFIED",
    }
    user = User(**data)
    user.commit()
    return user


def create_random_borrower():
    user = create_random_borrower_user()
    borrower_code = random.randint(11111111, 9999999999)
    data = {
        "domicile_country": "Indonesia",
        "email": user.email,
        "first_name": faker.first_name(),
        "birth_date": faker.date_time_between(start_date="-40y", end_date="-1y"),
        "gender": "M",
        "marital_status": "L",
        "mobile_phone_ext": "62",
        "mobile_phone": "8" + faker.msisdn()[0:10],
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
                "work_date_start": faker.date_this_decade(
                    before_today=True,
                    after_today=False
                ),
                "payment_date": faker.future_date(
                    end_date="+14d", tzinfo=None
                ),
                "employee_id": "KQzTLbiH23vKuSKtykuFde",
                "basic_salary_validation": True,
                "contract_end_date_validation": False,
                "company_name_validation": True,
                "employee_no_validation": True,
                "employment_status_validation": False,
                "position_validation": True,
                "work_date_start_validation": False
            }
        ],
        "user_id": user.id,
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
        "borrower_code": str(borrower_code),
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
        "last_name": faker.last_name(),
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
        "nationality": "Indonesia",
    }
    borrower = Borrower(**data)
    borrower.commit()
    return borrower


def generate_random_score():
    credit_score = random.randint(181, 500)
    grade = ""
    if credit_score >= 300:
        grade = "A"
    elif credit_score >= 265 and credit_score <= 299:
        grade = "B"
    elif credit_score >= 238 and credit_score <= 264:
        grade = "C"
    elif credit_score >= 181 and credit_score <= 237:
        grade = "D"
    return credit_score, grade


def create_random_loan_request():
    borrower = create_random_borrower()
    tenor = 14
    credit_score, grade = generate_random_score()
    loan_request_code = random.randint(11111111, 9999999999)
    # find products!
    product = current_app.db.lender_products.find_one({"pn": "Mocepat"})
    tnc = current_app.db.lender_files.find_one({
        "ft": "terms",
    })
    bank = current_app.db.lender_banks.find_one({
        "bna": "PT BANK NEGARA INDONESIA 1946 (Persero) Tbk",
    })

    data = {
        "overdue": 0,
        "payment_state_status": "LANCAR",
        "product_id": product["_id"],
        "user_id": borrower.user_id,
        "borrower_id": borrower.id,
        "loan_request_code": str(loan_request_code),
        "tenor": tenor,
        "status": "PENDING",
        "requested_loan_request": 500000,
        "payroll_date": borrower.work_info[0].payment_date,
        "due_date": borrower.work_info[0].payment_date,
        "upfront_fee": 0.3,
        "upfront_fee_type": "PERCENT",
        "disburse_amount": 477500,
        "loan_purpose": "Liburan",
        "service_fee": 22500,
        "note": "",
        "loan_counter": 0,
        "requested_date": datetime.utcnow(),
        "payment_states": [],
        "payment_schedules": [],
        "loan_repayments": [],
        "late_fee_logs": [],
        "credit_score": credit_score,
        "grade": grade,
        "tnc": {
            "is_agreed": True,
            "file_id": tnc["_id"]
        },
        "modanaku": {
            "wallet_id": "31ec22c4-dcf4-4679-a358-faa3ab832fda"
        },
        "bank_accounts": [
            {
                "account_no": "9889909694513183",
                "account_type": "VIRTUAL_ACCOUNT",
                "bank_name": "BNI",
                "account_name": "EMPLOYEE VA",
                "label": "MODANAKU",
                "bank_id": bank["_id"]
            }
        ],
        "approvals": [{
            "status": "PENDING"
        }]
    }
    loan_request = LoanRequest(**data)
    loan_request.commit()
    return {"loan_request": loan_request.dump(), "borrower": borrower.dump()}


def create_random_investment(investor_id, loan_ids):
    loan_requests = []
    for loan_id in loan_ids:
        loan_requests.append({
            "loan_request_id": loan_id,
            "disburse_amount": 477500,
            "total_fee": 22500
        })

    data = {
        "investor_id": investor_id,
        "total_amount": 1000000,
        "loan_requests": loan_requests
    }
    investment = Investment(**data)
    investment.commit()
    return {"investment": investment.dump()}
