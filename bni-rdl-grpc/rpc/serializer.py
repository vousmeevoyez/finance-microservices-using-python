"""
    Handle Serialization from BNI Ecollection
"""
from datetime import datetime
from marshmallow import Schema, fields, EXCLUDE


class RdlAccountHistoryDetailsSchema(Schema):
    """ schema to represent rdl history details """

    sequenceNum = fields.Str(data_key="id")
    date = fields.Method("string_to_created_at", data_key="created_at")
    amount = fields.Float()
    balance = fields.Float()
    description = fields.Method("aggregate_description")
    tofrAccount = fields.Str(data_key="account_no")
    transaction_type = fields.Method("debit_credit_to_string", data_key="debit_credit")

    def debit_credit_to_string(self, obj):
        transaction_type = {"K": "CREDIT", "D": "DEBIT"}
        return transaction_type[obj["debit_credit"]]

    def string_to_created_at(self, obj):
        date_time = obj["date"]
        trx_time = obj["transactionTime"]
        created_at = "{} {}".format(date_time, trx_time)
        return created_at

    def aggregate_description(self, obj):
        description = "{} {} {} {} {} {} {}".format(
            obj["description"],
            obj["narative"],
            obj["narative36"],
            obj["narative02"],
            obj["narative03"],
            obj["narative38"],
            obj["narative39"],
        )
        return description

    class Meta:
        unknown = EXCLUDE


class RdlAccountHistorySchema(Schema):
    """ schema used for rdl history"""

    fromDate = fields.Str(data_key="start_date")
    toDate = fields.Str(data_key="end_date")
    beginingBalance = fields.Float(data_key="start_balance")
    endingBalance = fields.Float(data_key="end_balance")
    debitsTotal = fields.Float(data_key="total_debit")
    creditsTotal = fields.Float(data_key="total_credit")
    longHistoricals = fields.Nested(
        RdlAccountHistoryDetailsSchema, many=True, data_key="details"
    )

    class Meta:
        unknown = EXCLUDE


class RdlAccountSchema(Schema):
    """ schema used for rdl history"""

    title = fields.Str()
    first_name = fields.Str()
    middle_name = fields.Str(missing="")
    last_name = fields.Str()
    npwp_option = fields.Str()
    npwp_no = fields.Str()
    nationality = fields.Str()
    country = fields.Str()
    religion = fields.Str()
    birth_place = fields.Str()
    birth_date = fields.Str()
    gender = fields.Str()
    is_married = fields.Str()
    mother_maiden_name = fields.Str()
    job_code = fields.Str()
    education = fields.Str()
    id_number = fields.Str()
    id_issuing_city = fields.Str()
    id_expire_date = fields.Str()
    address_street = fields.Str()
    address_rt_rw_perum = fields.Str()
    address_kelurahan = fields.Str()
    address_kecamatan = fields.Str()
    zip_code = fields.Str()
    home_phone_ext = fields.Str(missing="")
    home_phone = fields.Str(missing="")
    office_phone_ext = fields.Str(missing="")
    office_phone = fields.Str(missing="")
    mobile_phone_ext = fields.Str()
    mobile_phone = fields.Str()
    fax_ext = fields.Str(missing="")
    fax = fields.Str(missing="")
    email = fields.Str()
    monthly_income = fields.Str()
    branch_opening = fields.Str(missing="0259")
    reason = fields.Str(missing="2")
    source_of_fund = fields.Str(missing="4")

    class Meta:
        unknown = EXCLUDE


class TransferInquirySchema(Schema):
    """ schema used for get rdl payment status """

    requestedUuid = fields.Str(data_key="request_uuid")
    responseUuid = fields.Str(data_key="response_uuid")
    transactionStatus = fields.Str(data_key="status")
    transactionDateTime = fields.Str(data_key="created_at")
    accountNumber = fields.Str(data_key="source")
    beneficiaryAccountNumber = fields.Str(data_key="destination")
    transactionType = fields.Method(
        "transaction_type_to_string", data_key="transaction_type"
    )
    amount = fields.Float()

    def transaction_type_to_string(self, obj):
        transaction_types = {
            "paymentUsingTransfer": "INHOUSE",
            "paymentUsingInterbank": "INTERBANK",
            "paymentUsingClearing": "CLEARING",
            "paymentUsingRtgs": "RTGS",
        }
        return transaction_types[obj["transactionType"]]

    class Meta:
        unknown = EXCLUDE
