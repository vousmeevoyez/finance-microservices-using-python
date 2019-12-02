from datetime import datetime
from bson import ObjectId

from umongo import post_dump
from umongo.fields import (
    ObjectIdField,
    StrField,
    DateTimeField,
    DecimalField,
    ListField,
    EmbeddedField,
    IntField
)

from app.api import instance

# shared models
from app.api.models.base import (
    BaseEmbeddedDocument,
    BaseBankDocument,
    StatusEmbed
)
from app.api.models.loan_request import LoanRequest
from app.api.lib.core.exceptions import BaseError


class InvestmentNotFound(BaseError):
    """ raised when investment not found """


@instance.register
class LoanFeeEmbed(BaseEmbeddedDocument):
    name = StrField(attribute="na")
    investor_fee = DecimalField(attribute="if")
    profit_fee = DecimalField(attribute="af")


@instance.register
class LoanRequestEmbed(BaseEmbeddedDocument):
    loan_request_id = ObjectIdField(required=True, attribute="loanRequest_id")
    disburse_amount = DecimalField(attribute="da")
    total_fee = DecimalField(attribute="tafees")
    investor_fee = StrField(attribute="if")
    fees = ListField(EmbeddedField(LoanFeeEmbed), default=[])

    def get_loan_request_details(self):
        loan_request = LoanRequest.find_one({"id": self.loan_request_id})
        return loan_request


@instance.register
class Investment(BaseBankDocument):
    investment_code = StrField(attribute="ic")
    investor_id = ObjectIdField(required=True)
    total_amount = DecimalField(attribute="ta")
    loan_requests = ListField(
        EmbeddedField(LoanRequestEmbed), attribute="lr", default=[]
    )

    class Meta:
        collection_name = "lender_investments"

    @staticmethod
    def get_by_va(account_no):
        investment = Investment.find({
            "bank_accounts": {
                "$elemMatch": {
                    "account_no": account_no,
                    "account_type": "VIRTUAL_ACCOUNT"
                }
            }
        })
        try:
            return list(investment)[0].dump()
        except IndexError:
            raise InvestmentNotFound

    @staticmethod
    def get_by_loan_request(loan_request_id):
        investment = Investment.find({
            "lr": {
                "$elemMatch": {
                    "loanRequest_id": ObjectId(loan_request_id),
                }
            }
        })
        try:
            return list(investment)[0].dump()
        except IndexError:
            raise InvestmentNotFound

    @post_dump
    def custom_dump(self, data):
        total_amount = data["total_amount"]
        data["total_amount"] = str(total_amount)

        for item in data["loan_requests"]:
            disburse_amount = item["disburse_amount"]
            item["disburse_amount"] = int(disburse_amount)

            total_fee = item["total_fee"]
            item["total_fee"] = int(total_fee)
