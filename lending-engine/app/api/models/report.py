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
from app.api.models.base import (
    BaseDocument,
    BaseEmbeddedDocument,
    BankAccEmbed,
    StatusEmbed,
)
from app.api.lib.core.exceptions import BaseError


@instance.register
class RegulationReport(BaseDocument):
    report_type = StrField(attribute="rt")
    file_type = StrField(attribute="ft")
    file_url = StrField(attribute="fu")
    file_name = StrField(attribute="fn")
    file_path = StrField(attribute="fp")
    version = IntField(attribute="v", default=1)
    list_of_status = ListField(
        EmbeddedField(StatusEmbed), attribute="lst", default=list
    )

    class Meta:
        collection_name = "lender_regulation_reports"


@instance.register
class AfpiReport(BaseDocument):
    regulation_report_id = ObjectIdField()
    p2p_id = StrField()
    borrower_id = StrField()
    borrower_type = StrField()
    borrower_name = StrField()
    identity_no = StrField()
    npwp_no = StrField()
    loan_id = StrField()
    agreement_date = StrField()
    disburse_date = StrField()
    loan_amount = StrField()
    reported_date = StrField()
    remaining_loan_amount = StrField()
    due_date = StrField()
    quality = StrField()
    current_dpd = StrField()
    max_dpd = StrField()
    status = StrField()

    class Meta:
        collection_name = "lender_afpi_reports"
