"""
    Document Models
"""
from datetime import datetime
from bson.objectid import ObjectId

from umongo.fields import (
    EmbeddedField,
    ObjectIdField,
    StrField,
    DecimalField,
    DateTimeField,
    DateField,
    IntField,
    BoolField,
    ListField,
)

from app.api import instance
from app.api.models.base import BaseDocument, BaseEmbeddedDocument, BankAccEmbed
from app.api.lib.core.exceptions import BaseError


@instance.register
class GradeEmbed(BaseEmbeddedDocument):
    grade = StrField()
    min_score = IntField(attribute="mincs")
    max_score = IntField(attribute="maxcs")


@instance.register
class LoanAmountEmbed(BaseEmbeddedDocument):
    amount = IntField(attribute="la")


@instance.register
class FeeEmbed(BaseEmbeddedDocument):
    start_tenor = IntField(attribute="slt")
    end_tenor = IntField(attribute="elt")
    fee = DecimalField()
    fee_type = StrField(attribute="type")


@instance.register
class InterestEmbed(BaseEmbeddedDocument):
    min_tenor = IntField(attribute="mit")
    max_tenor = IntField(attribute="mat")
    loan_amounts = ListField(EmbeddedField(LoanAmountEmbed), attribute="loanAmounts")
    investor_fee = DecimalField(attribute="if")
    investor_fee_type = StrField(attribute="ift")
    profit_fee = DecimalField(attribute="af")
    profit_fee_type = StrField(attribute="aft")
    minimum_fee = DecimalField(attribute="msf")
    service_fee = DecimalField(attribute="sf")
    service_fee_type = StrField(attribute="sft")
    admin_fee = DecimalField(attribute="adf")
    admin_fee_type = StrField(attribute="adft")
    late_fee = DecimalField(attribute="lf")
    late_fee_type = StrField(attribute="lft")
    max_late_fee = DecimalField(attribute="mlf")
    upfront_fee = DecimalField(attribute="uf")
    upfront_fee_type = StrField(attribute="ut")
    penalty_fee = DecimalField(attribute="pf")
    penalty_fee_type = StrField(attribute="pft")
    grade_period = IntField(attribute="gp")
    fees = ListField(EmbeddedField(FeeEmbed))


@instance.register
class Product(BaseDocument):
    file_id = ObjectIdField(attribute="files_id")
    grades = ListField(EmbeddedField(GradeEmbed), attribute="gr")
    min_score = IntField(attribute="mcs")
    start_date = DateField(attribute="sd")
    end_date = DateField(attribute="ed")
    product_name = StrField(attribute="pn")
    product_type = StrField(attribute="pt")
    is_active = BoolField(attribute="ia", default=True)
    created_by = ObjectIdField(attribute="cb")
    max_salary = IntField(attribute="mls", defaul=0)
    max_salary_type = StrField(attribute="mlst")
    interests = EmbeddedField(InterestEmbed)
    freeze_period = IntField(attribute="fp")
    product_code = StrField(attribute="pc")

    class Meta:
        collection_name = "lender_products"
