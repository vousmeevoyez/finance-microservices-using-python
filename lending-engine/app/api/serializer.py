"""
    Serializer & Deserialize
"""
import pytz
from datetime import datetime
from marshmallow import (
    fields,
    ValidationError,
    validates,
    validates_schema,
    post_load
)
from app.api import ma
from app.api.const import P2P_ID
from app.config.external.bank import BNI_ECOLLECTION


def cannot_be_blank(string):
    """
        function to make user not enter empty string
        args :
            string -- user inputted data
    """
    if not string:
        raise ValidationError("Data cannot be blank")


def generate_local_date():
    timezone = pytz.timezone("Asia/Jakarta")
    now = datetime.utcnow()
    local_now = timezone.localize(now)
    local_date_string = local_now.strftime("%Y%m%d")
    return local_date_string

def is_repayment_or_investment(account_no):
    # fixed pattern
    fixed_pattern = BNI_ECOLLECTION["VA_PREFIX"] + \
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"]
    fixed_index = len(fixed_pattern)
    # prefix pattern
    investment_prefix = BNI_ECOLLECTION["INVESTMENT_PREFIX"]
    repayment_prefix = BNI_ECOLLECTION["REPAYMENT_PREFIX"]
    prefix_length = len(investment_prefix)

    va_type = "INVALID"
    if account_no[fixed_index:fixed_index+prefix_length] ==\
            investment_prefix:
        va_type = "INVESTMENT"
    elif account_no[fixed_index:fixed_index+prefix_length] ==\
            repayment_prefix:
        va_type = "REPAYMENT"
    return va_type


class BniVaCallbackSchema(ma.Schema):
    """ this is schema for callback object """
    virtual_account = fields.Str(required=True, validate=cannot_be_blank)
    customer_name = fields.Str(required=True, validate=cannot_be_blank)
    trx_id = fields.Int(required=True, validate=cannot_be_blank)
    trx_amount = fields.Float(required=True)
    payment_amount = fields.Int(required=True, validate=cannot_be_blank)
    cumulative_payment_amount = fields.Int(required=True,
                                           validate=cannot_be_blank)
    payment_ntb = fields.Str(required=True, validate=cannot_be_blank)
    datetime_payment = fields.Str(required=True, validate=cannot_be_blank)

    @validates("virtual_account")
    def validate_va_number(self, va_number):
        """
            function to validate virtual_account number
            args:
                va_number -- virtual account number
        """
        va_number = str(va_number)
        valid = True

        va_prefix = BNI_ECOLLECTION["VA_PREFIX"]
        va_client_id = BNI_ECOLLECTION["CREDIT_CLIENT_ID"]

        # first make sure va_number is 16 digit can't be less or more
        if len(va_number) != 16:
            valid = False
        # second make sure 3 first va_number is valid
        if va_number[:len(va_prefix)] != va_prefix:
            valid = False
        # third make sure 3 first va_number is valid
        if va_number[len(va_prefix):len(va_prefix+va_client_id)] != va_client_id:
            valid = False
        # fourth make sure the va is either repayment or investment
        if is_repayment_or_investment(va_number) == "INVALID":
                valid = False

        if valid is not True:
            raise ValidationError("Invalid Virtual Account Number")

    @post_load
    def custom_load(self, data, **kwargs):
        """ based on incoming loaded data we decided it is repayment or
        investment """
        account_no = data["virtual_account"]
        va_type = is_repayment_or_investment(account_no)
        data["va_type"] = va_type
        return data


class BniRdlCallbackSchema(ma.Schema):
    """ this is schema for callback object """
    p2p_id = fields.Str(required=True, validate=cannot_be_blank)
    account_number = fields.Str(required=True, validate=cannot_be_blank)
    payment_amount = fields.Decimal(required=True, validate=cannot_be_blank)
    accounting_flag = fields.Str(required=True, validate=cannot_be_blank)
    journal_number = fields.Int(required=True, validate=cannot_be_blank)
    datetime_payment = fields.Str(required=True, validate=cannot_be_blank)

    @validates("accounting_flag")
    def validate_accounting_flag(self, flag):
        """
            function to validate accounting flag
            args:
                flag -- C / D
        """
        if flag != "C":
            raise ValidationError("Only accept Credit Flag")

class TransactionCallbackSchema(ma.Schema):
    """ this is schema for transaction callback """
    transaction_id = fields.Str(required=True, validate=cannot_be_blank)
    transaction_type = fields.Str(required=True, validate=cannot_be_blank)
    status = fields.Str(required=True, validate=cannot_be_blank)


class WithdrawSchema(ma.Schema):
    """ this is schema for withdraw callback """
    destination_id = fields.Str(required=True, validate=cannot_be_blank)
    amount = fields.Int(required=True, validate=cannot_be_blank)


class LoanBorrowerReportSchema(ma.Schema):
    """ this is schema for withdraw callback """
    p2p_id = fields.Str(default=P2P_ID)
    borrower_id = fields.Method("extract_borrower_code")
    borrower_type = fields.Str(default="1")
    borrower_name = fields.Method("concat_to_full_name")
    identity_no = fields.Method("extract_ktp_no")
    npwp_no = fields.Method("extract_npwp_no")
    loan_id = fields.Str(attribute="lrc")
    agreement_date = fields.Method("extract_agreement_date")
    disburse_date = fields.Method("extract_disburse_date")
    loan_amount = fields.Str(attribute="lar")
    reported_date = fields.Str(default=generate_local_date)
    remaining_loan_amount = fields.Method("calculate_remaining_loan_amount")
    due_date = fields.Method("extract_due_date")
    quality = fields.Method("convert_to_quality")
    current_dpd = fields.Str(attribute="ov")
    max_dpd = fields.Str(attribute="ov")
    status = fields.Method("convert_to_status")

    def concat_to_full_name(self, obj):
        first_name = obj["borrower"]["fn"]
        middle_name = obj["borrower"]["mn"]
        last_name = obj["borrower"]["ln"]

        full_name = first_name + " " + middle_name + " " + last_name
        if middle_name == "":
            full_name = first_name + " " + last_name
        return full_name


    def extract_borrower_code(self, obj):
        return obj["borrower"]["bc"]


    def extract_ktp_no(self, obj):
        return obj["borrower"]["ktp"]["kn"]


    def extract_npwp_no(self, obj):
        return obj["borrower"]["npwp"]["nn"]


    def extract_agreement_date(self, obj):
        agreement_date = obj["tnc"]["aa"]
        agreement_date_string = agreement_date.strftime("%Y%m%d")
        return agreement_date_string


    def extract_disburse_date(self, obj):
        list_of_status = obj["lst"]
        result = list(filter(
            lambda item: item["st"] == \
            'SEND_TO_MODANAKU_COMPLETED', list_of_status
        ))
        try:
            disburse_date = result[0]["ca"]
        except IndexError:
            print("no disburse date")
        else:
            disburse_date_string = disburse_date.strftime("%Y%m%d")
            return disburse_date_string


    def calculate_remaining_loan_amount(self, obj):
        remaining = obj["lar"]
        if obj["st"] == "PAID":
            remaining = 0
        return str(remaining)


    def extract_due_date(self, obj):
        due_date = obj["dd"]
        due_date_string = due_date.strftime("%Y%m%d")
        return due_date_string

    def convert_to_quality(self, obj):
        quality = "1"
        if obj["psts"] == "TIDAK_LANCAR":
            quality = "2"
        elif obj["psts"] == "MACET":
            quality = "3"
        return quality

    def convert_to_status(self, obj):
        status = "O"
        if obj["st"] == "PAID":
            status = "L"
        elif obj["st"] == "WRITEOFF":
            status = "W"
        return status
