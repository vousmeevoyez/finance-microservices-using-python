"""
    Document Models
"""
from datetime import datetime
from bson.objectid import ObjectId

from umongo import post_dump
from umongo.fields import (
    EmbeddedField,
    ObjectIdField,
    StrField,
    DecimalField,
    DateTimeField,
    IntField,
    ListField,
)

from app.api import instance
from app.api.models.base import BaseDocument, BaseEmbeddedDocument, BaseBankDocument
from app.api.models.approval import ApprovalEmbed
from app.api.lib.core.exceptions import BaseError


class InvestorNotFound(BaseError):
    """ raised when investor not ofund"""


@instance.register
class NpwpEmbed(BaseEmbeddedDocument):
    npwp_option = StrField(required=True, attribute="onp", default="1")
    npwp_no = StrField(required=True, attribute="nn")


@instance.register
class KtpImageEmbed(BaseEmbeddedDocument):
    content_type = StrField(required=True, attribute="ct")
    name = StrField(required=True, attribute="na")
    image = StrField(required=True, attribute="img")


@instance.register
class KtpEmbedDocument(BaseEmbeddedDocument):
    images = EmbeddedField(KtpImageEmbed, attribute="ki")
    no = StrField(required=True, attribute="kn")
    issuing_city = StrField(required=True, attribute="kic")
    expire_date = DateTimeField(required=True, attribute="ked")


@instance.register
class AddressEmbed(BaseEmbeddedDocument):
    street = StrField(required=True, attribute="as")
    rt_rw_perum = StrField(required=True, attribute="arr")
    province = StrField(required=True, attribute="ap")
    city = StrField(required=True, attribute="ac")
    kelurahan = StrField(required=True, attribute="akl")
    kecamatan = StrField(required=True, attribute="akc")
    zip_code = StrField(required=True, attribute="zc")


@instance.register
class ApproverInfoEmbed(BaseEmbeddedDocument):
    reason_id = ObjectIdField(allow_none=True)
    message = StrField(attribute="msg")
    approver_id = ObjectIdField()


@instance.register
class InvestorFeesEmbed(BaseEmbeddedDocument):
    product_id = ObjectIdField()
    agreement = ObjectIdField(attribute="ag")
    late_fee = DecimalField(attribute="lf", default=0)
    late_fee_type = StrField(attribute="lft")
    upfront_fee = DecimalField(attribute="uf", default=0)
    upfront_fee_type = StrField(attribute="ut")
    penalty_fee = DecimalField(attribute="pf", default=0)
    penalty_fee_type = StrField(attribute="pft")
    service_fee = DecimalField(attribute="sf", default=0)
    service_fee_type = StrField(attribute="sft")
    admin_fee = DecimalField(attribute="adf", default=0)
    admin_fee_type = StrField(attribute="adft")


@instance.register
class Investor(BaseBankDocument):
    user_id = ObjectIdField()
    email = StrField(required=True, unique=True, attribute="em")
    title = StrField(required=True, attribute="ti")
    first_name = StrField(attribute="fn", default="")
    middle_name = StrField(attribute="mn", default="")
    last_name = StrField(required=True, attribute="ln", default="")
    npwp = EmbeddedField(NpwpEmbed)
    nationality = StrField(required=True, attribute="na")
    domicile_country = StrField(required=True, attribute="dc")
    religion = StrField(required=True, attribute="re")
    birth_place = StrField(required=True, attribute="bp")
    birth_date = DateTimeField(required=True, attribute="bd")
    gender = StrField(required=True, attribute="ge")
    is_married = StrField(required=True, attribute="im")
    mother_maiden_name = StrField(required=True, attribute="mmn")
    job_code = StrField(required=True, attribute="jc")
    education = StrField(required=True, attribute="ed")
    ktp = EmbeddedField(KtpEmbedDocument)
    address = EmbeddedField(AddressEmbed)
    home_phone = StrField(attribute="hp")
    office_phone = StrField(attribute="op")
    mobile_phone = StrField(required=True, attribute="mp")
    fax = StrField()
    monthly_income = DecimalField(attribute="mi")
    branch_opening = StrField(required=True, attribute="bo")
    source_of_funds = StrField(required=True, attribute="sof")
    source = StrField(required=True, attribute="so")
    otp_status = StrField(attribute="os")
    email_code = StrField(attribute="emc")
    passport = StrField(attribute="pas")
    is_email_verified = StrField(attribute="iev")
    ca = DateTimeField(default=datetime.utcnow)
    ua = DateTimeField(default=datetime.utcnow)
    approvals = ListField(EmbeddedField(ApprovalEmbed), attribute="app", default=[])
    approver_info = EmbeddedField(ApproverInfoEmbed, attribute="approverInformation")
    fees = ListField(EmbeddedField(InvestorFeesEmbed), default=[])

    class Meta:
        collection_name = "lender_investors"

    @staticmethod
    def get_investor_by_rdl(rdl_account):
        investor = Investor.find(
            {
                "bank_accounts": {
                    "$elemMatch": {
                        "account_no": rdl_account,
                        "account_type": "RDL_ACCOUNT",
                    }
                }
            }
        )
        result = list(investor)
        if len(result) == 0:
            raise InvestorNotFound()
        return result[0]

    def get_wallet(self):
        pipeline = [
            {
                "$lookup": {
                    "from": "lender_wallets",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "investor_wallet",
                }
            },
            {"$match": {"user_id": self.user_id}},
            {"$project": {"investor_wallet": 1}},
            {"$unwind": "$investor_wallet"},
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]

    @post_dump
    def custom_dump(self, data):
        monthly_income = data["monthly_income"]
        data["monthly_income"] = str(monthly_income)

        for fee in data["fees"]:
            late_fee = fee["late_fee"]
            fee["late_fee"] = str(late_fee)

            upfront_fee = fee["upfront_fee"]
            fee["upfront_fee"] = str(upfront_fee)

            penalty_fee = fee["penalty_fee"]
            fee["penalty_fee"] = str(penalty_fee)

            service_fee = fee["service_fee"]
            fee["service_fee"] = str(service_fee)

            admin_fee = fee["admin_fee"]
            fee["admin_fee"] = str(admin_fee)

        return data


@instance.register
class InvestorRdl(BaseDocument):
    investor_id = ObjectIdField()
    title = StrField(required=True)
    first_name = StrField(required=True)
    middle_name = StrField(required=True)
    last_name = StrField(required=True)
    npwp_option = StrField(required=True)
    npwp_no = StrField(required=True)
    nationality = StrField(required=True)
    country = StrField(required=True)
    religion = StrField(required=True)
    birth_place = StrField(required=True)
    birth_date = StrField(required=True)
    gender = StrField(required=True)
    is_married = StrField(required=True)
    mother_maiden_name = StrField(required=True)
    job_code = StrField(required=True)
    education = StrField(required=True)
    id_number = StrField(required=True)
    id_issuing_city = StrField(required=True)
    id_expire_date = StrField(required=True)
    address_street = StrField(required=True)
    address_rt_rw_perum = StrField(required=True)
    address_kelurahan = StrField(required=True)
    address_kecamatan = StrField(required=True)
    zip_code = StrField(required=True)
    home_phone_ext = StrField(required=True)
    home_phone = StrField(required=True)
    office_phone_ext = StrField(required=True)
    office_phone = StrField(required=True)
    mobile_phone_ext = StrField(required=True)
    mobile_phone = StrField(required=True)
    fax_ext = StrField(required=True)
    fax = StrField(required=True)
    email = StrField(required=True)
    monthly_income = StrField(required=True)
    branch_opening = StrField(required=True)

    class Meta:
        collection_name = "lender_investorsRdlData"
