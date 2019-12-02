"""
    Serializer & Deserialize
"""
from marshmallow import (
    fields,
    ValidationError,
    validates,
    post_load
)
from app.api import ma
from app.config.external.bank import BNI_ECOLLECTION


def cannot_be_blank(string):
    """
        function to make user not enter empty string
        args :
            string -- user inputted data
    """
    if not string:
        raise ValidationError("Data cannot be blank")


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
    payment_amount = fields.Int(required=True, validate=cannot_be_blank)
    accounting_flag = fields.Str(required=True, validate=cannot_be_blank)
    journal_number = fields.Int(required=True, validate=cannot_be_blank)
    datetime_payment = fields.Str(required=True, validate=cannot_be_blank)


class TransactionCallbackSchema(ma.Schema):
    """ this is schema for transaction callback """
    transaction_id = fields.Str(required=True, validate=cannot_be_blank)
    transaction_type = fields.Str(required=True, validate=cannot_be_blank)
    status = fields.Str(required=True, validate=cannot_be_blank)


class WithdrawSchema(ma.Schema):
    """ this is schema for withdraw callback """
    destination_id = fields.Str(required=True, validate=cannot_be_blank)
    amount = fields.Int(required=True, validate=cannot_be_blank)
