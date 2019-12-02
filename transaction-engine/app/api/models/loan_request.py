from datetime import datetime
from bson import ObjectId

from umongo import post_dump
from umongo.fields import (
    DecimalField,
    ObjectIdField,
    StrField,
    DateTimeField,
    DateField,
    EmbeddedField,
    ListField,
    IntField,
    BoolField
)

from app.api import instance

# shared models
from app.api.models.approval import ApprovalEmbed
from app.api.models.base import (
    BaseDocument,
    BaseBankDocument,
    BaseEmbeddedDocument,
    StatusEmbed,
    TransactionStatusNotFound
)
from app.api.models.borrower import Borrower
from app.api.lib.core.exceptions import BaseError


class LoanRequestNotFound(BaseError):
    """ raised when loan request not found """


@instance.register
class TermConditionEmbed(BaseEmbeddedDocument):
    file_id = ObjectIdField()
    is_agreed = BoolField(default=False, attribute="ia")
    agreed_at = DateTimeField(default=datetime.utcnow, attribute="aa")


@instance.register
class PaymentStateEmbed(BaseEmbeddedDocument):
    status = StrField(default="LANCAR", attribute="st")
    created_by = ObjectIdField(attribute="db")  # user who approve


@instance.register
class PaymentSchemaEmbed(BaseEmbeddedDocument):
    created_by = ObjectIdField(attribute="cb")  # user who approve
    type_ = StrField(default="MAIN", attribute="tp")
    amount = DecimalField(attribute="am")
    late_fees = DecimalField(attribute="lf")
    early_fees = DecimalField(attribute="ef")
    admin_fees = DecimalField(attribute="af")
    risk_fees = DecimalField(attribute="rf")
    services_fees = DecimalField(attribute="sf")


@instance.register
class PaymentScheduleEmbed(BaseEmbeddedDocument):
    due_date = DateTimeField(attribute="dd")
    amount = DecimalField(attribute="am")
    payment_state = EmbeddedField(PaymentStateEmbed, attribute="pst")
    payment_schema = EmbeddedField(PaymentStateEmbed, attribute="pa")


@instance.register
class LoanRepaymentEmbed(BaseEmbeddedDocument):
    id = ObjectIdField(default=ObjectId, attribute="_id")
    status = StrField(attribute="st")
    created_by = ObjectIdField(attribute="cb")


@instance.register
class LateFeeEmbed(BaseEmbeddedDocument):
    late_fee_day = IntField(attribute="lfd")
    late_fee_amount = DecimalField(attribute="lfa")
    total_payment_amount = DecimalField(attribute="tpa")


@instance.register
class ModanakuEmbedded(BaseEmbeddedDocument):
    bank_account_id = StrField(attribute="bid")
    wallet_id = StrField(attribute="wid")
    payment_plan_id = StrField(attribute="ppid")


@instance.register
class LoanRequest(BaseBankDocument):
    user_id = ObjectIdField()
    investor_id = ObjectIdField()
    product_id = ObjectIdField()
    investment_id = ObjectIdField()
    borrower_id = ObjectIdField()
    credit_score = IntField(attribute="cs")
    grade = StrField(attribute="gr")
    tnc = EmbeddedField(TermConditionEmbed)
    status = StrField(default="VERIFYING", attribute="st")  #|PENDING | APPROVED | REJECTED
    requested_loan_request = DecimalField(attribute="lar")
    total_amount = DecimalField(attribute="ta")
    payment_states = ListField(EmbeddedField(PaymentStateEmbed),
                               attribute="pst")
    payment_schedules = ListField(EmbeddedField(PaymentScheduleEmbed),
                                  attribute="psc")
    loan_repayments = ListField(
        EmbeddedField(LoanRepaymentEmbed),
        attribute="lrs"
    )
    approvals = ListField(EmbeddedField(ApprovalEmbed),
                          attribute="app")
    payroll_date = DateField(attribute="pd")
    due_date = DateField(attribute="dd")
    tenor = IntField(attribute="te")
    upfront_fee = DecimalField(attribute="uf")
    upfront_fee_type = StrField(attribute="ut")
    disburse_amount = DecimalField(attribute="da")
    payment_amount = DecimalField(attribute="pa")
    payment_date = DateField(attribute="pda")
    late_fee = DecimalField(attribute="lf")
    late_fee_type = StrField(attribute="lft")
    total_payment_amount = DecimalField(attribute="tpa")
    date_transfer = DateField(attribute="dt")
    transfer_by = ObjectIdField(attribute="tb")
    status_transfer = StrField(attribute="stt")
    late_fee_logs = ListField(EmbeddedField(LateFeeEmbed),
                              attribute="lateFeeLog")
    loan_request_code = StrField(attribute="lrc")
    overdue = IntField(attribute="ov")
    loan_purpose = StrField(attribute="lp")
    tenor_type = StrField(attribute="tt")
    service_fee = DecimalField(attribute="sf")
    note = StrField(attribute="no")
    loan_counter = IntField(attribute="lc")
    payment_state_status = StrField(default="LANCAR", attribute="psts")
    investment_date = DateField(attribute="ida")
    requested_date = DateField(attribute="rd")
    modanaku = EmbeddedField(ModanakuEmbedded)

    class Meta:
        collection_name = "lender_loan_requests"

    @post_dump
    def custom_dump(self, data):
        requested_loan_request = data["requested_loan_request"]
        data["requested_loan_request"] = str(requested_loan_request)

        disburse_amount = data["disburse_amount"]
        data["disburse_amount"] = str(disburse_amount)

        service_fee = data["service_fee"]
        data["service_fee"] = str(service_fee)

        upfront_fee = data["upfront_fee"]
        data["upfront_fee"] = str(upfront_fee)
        return data

    def get_borrower(self):
        borrower = Borrower.find_one({"id": self.borrower_id})
        return borrower

    @staticmethod
    def get_by_va(account_no):
        loan_request = LoanRequest.find({
            "bank_accounts": {
                "$elemMatch": {
                    "account_no": account_no,
                    "account_type": "VIRTUAL_ACCOUNT"
                }
            }
        })
        try:
            return list(loan_request)[0].dump()
        except IndexError:
            raise LoanRequestNotFound
