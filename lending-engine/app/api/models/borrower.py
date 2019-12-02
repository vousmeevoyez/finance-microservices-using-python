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
    ListField
)

from app.api import instance
from app.api.models.base import (
    BaseDocument,
    BaseEmbeddedDocument,
    BankAccEmbed
)
from app.api.lib.core.exceptions import BaseError


@instance.register
class BorrowerNpwpEmbed(BaseEmbeddedDocument):
    opt = StrField(attribute="onp")
    no = StrField(attribute="nn")
    validation = BoolField(attribute="nn_v")
    image = StrField(attribute="ni")


@instance.register
class BorrowerKtpEmbed(BaseEmbeddedDocument):
    no = StrField(attribute="kn")
    issuing_city = StrField(attribute="kic")
    expire_date = DateField(attribute="ked")
    image = StrField(attribute="ktpi")
    validation = BoolField(attribute="kn_v")


@instance.register
class FamilyCardEmbed(BaseEmbeddedDocument):
    no = StrField(attribute="fcn")
    image = StrField(attribute="fci")


@instance.register
class BorrowerAddressEmbed(BaseEmbeddedDocument):
    street = StrField(attribute="as")
    street_validation = BoolField(attribute="as_v")
    rt_rw_perum = StrField(attribute="arr")
    province = StrField(attribute="ap")
    province_validation = BoolField(attribute="ap_v")
    city = StrField(attribute="ac")
    city_validation = BoolField(attribute="ac_v")
    kelurahan = StrField(attribute="akl")
    kelurahan_validation = BoolField(attribute="akl_v")
    kecamatan = StrField(attribute="akc")
    kecamatan_validation = BoolField(attribute="akc_v")
    zip_code = StrField(attribute="zc")
    zip_code_validation = BoolField(attribute="zc_v")
    correspondence_address = StrField(attribute="cadd")
    residency_status = StrField(attribute="rs")
    residency_status_validation = BoolField(attribute="rs_v")
    length_of_stay = IntField(attribute="ls")
    length_of_stay_validation = BoolField(attribute="ls_v")


@instance.register
class VirtualAccountEmbed(BaseEmbeddedDocument):
    user_id = ObjectIdField()
    account_no = StrField(attribute="vaa")
    balance = DecimalField(attribute="ba")


@instance.register
class EmergencyContactEmbed(BaseEmbeddedDocument):
    index = StrField(attribute="in")
    full_name = StrField(attribute="fna")
    first_name = StrField(attribute="fn")
    first_name_validation = BoolField(attribute="fn_v")
    middle_name = StrField(attribute="mn")
    last_name = StrField(attribute="ln")
    phone_no = StrField(attribute="pn")
    phone_no_validation = BoolField(attribute="pn_v")
    phone_ext = StrField(attribute="pne")
    email = StrField(attribute="em")
    contact_address = StrField(attribute="cad")
    relationship = StrField(attribute="re")
    relationship_validation = BoolField(attribute="re_v")


@instance.register
class WorkLogEmbed(BaseEmbeddedDocument):
    regular_shit = StrField(attribute="rs")
    overtime = StrField(attribute="ot")
    unpaid = StrField(attribute="ul")
    working_period = StrField(attribute="wp")


@instance.register
class PayrollScoreEmbed(BaseEmbeddedDocument):
    user_id = ObjectIdField()
    regular_shift = StrField(attribute="pd")
    overtime = StrField(attribute="ov")
    unpaid = StrField(attribute="ul")
    date_start = StrField(attribute="pds")
    date_end = StrField(attribute="pde")
    working_period = StrField(attribute="wp")


@instance.register
class PayslipEmbed(BaseEmbeddedDocument):
    no = StrField(attribute="psn")
    image = StrField(attribute="psi")
    validation = BoolField(attribute="psi_v")


@instance.register
class WorkInfoEmbed(BaseEmbeddedDocument):
    user_id = ObjectIdField()
    payment_date = DateField(attribute="pd")
    company_id = StrField(attribute="coid")
    industry_type = StrField(attribute="it")
    company_name = StrField(attribute="cn")
    company_name_validation = BoolField(attribute="cn_v")
    position = StrField(attribute="po")
    position_validation = BoolField(attribute="po_v")
    employment_status = StrField(attribute="es")
    employment_status_validation = BoolField(attribute="es_v")
    contract_end_date = DateField(attribute="cd", allow_none=True)
    contract_end_date_validation = BoolField(attribute="cd_v")
    employee_id = StrField(attribute="ei")
    work_date_start = DateField(attribute="wds")
    work_date_start_validation = BoolField(attribute="wds_v")
    job_code = StrField(attribute="jc")
    office_phone = StrField(attribute="op")
    basic_salary = IntField(attribute="bs")
    basic_salary_validation = BoolField(attribute="bs_v")
    company_email = StrField(attribute="emc")
    company_email_validation = BoolField(attribute="emc_v")
    company_phone_no = StrField(attribute="nc")
    company_phone_no_validation = BoolField(attribute="nc_v")
    company_address = StrField(attribute="ac")
    worklog = EmbeddedField(WorkLogEmbed, attribute="wl")
    employee_no = StrField(attribute="en")
    employee_no_validation = BoolField(attribute="en_v")
    address = EmbeddedField(BorrowerAddressEmbed, attribute="add")
    payroll_score = EmbeddedField(PayrollScoreEmbed, attribute="psd")
    payslip = EmbeddedField(PayslipEmbed, attribute="ps")


@instance.register
class Borrower(BaseDocument):
    credit_score = StrField(attribute="cs")
    user_id = ObjectIdField(attribute="user_id")
    borrower_code = StrField(attribute="bc")
    email = StrField(unique=True, attribute="em")
    email_validation = BoolField(attribute="em_v")
    title = StrField(attribute="t")
    first_name = StrField(attribute="fn")
    first_name_validation = BoolField(attribute="fn_v")
    middle_name = StrField(attribute="mn")
    middle_name_validation = BoolField(attribute="mn_v")
    last_name = StrField(attribute="ln")
    last_name_validation = BoolField(attribute="ln_v")
    middle_name_validation = BoolField(attribute="mn_v")
    last_name = StrField(attribute="ln")
    npwp = EmbeddedField(BorrowerNpwpEmbed)
    nationality = StrField(attribute="na")
    domicile_country = StrField(attribute="dc")
    religion = StrField(attribute="re")
    religion_validation = BoolField(attribute="re_v")
    birth_place = StrField(attribute="bp")
    birth_place_validation = BoolField(attribute="bp_v")
    birth_date = DateField(attribute="bd")
    birth_date_validation = BoolField(attribute="bd_v")
    age = IntField()
    age_validation = BoolField(attribute="age_v")
    gender = StrField(attribute="ge")
    gender_validation = BoolField(attribute="ge_v")
    marital_status = StrField(attribute="ms")
    marital_status_validation = BoolField(attribute="ms_v")
    mother_maiden_name = StrField(attribute="mmn")
    mother_maiden_name_validation = BoolField(attribute="mmn_v")
    education = StrField(attribute="ed")
    education_validation = BoolField(attribute="ed_v")
    ktp = EmbeddedField(BorrowerKtpEmbed)
    family_card = EmbeddedField(FamilyCardEmbed, attribute="fc")
    address = EmbeddedField(BorrowerAddressEmbed, attribute="add")
    home_phone = StrField(attribute="hp")
    home_phone_validation = BoolField(attribute="hp_v")
    mobile_phone_ext = StrField(attribute="mpe")
    mobile_phone_ext_validation = BoolField(attribute="mpe_v")
    mobile_phone = StrField(attribute="mp")
    mobile_phone_validation = BoolField(attribute="mp_v")
    fax_number = StrField(attribute="fan")
    branch_opening = StrField(attribute="bo")
    virtual_account = EmbeddedField(VirtualAccountEmbed, attribute="vab")
    no_of_child = IntField(attribute="nc")
    no_of_child_validation = BoolField(attribute="nc_v")
    employee_virtual_account = StrField(attribute="vae")
    loan_to = IntField(attribute="lt")
    emergency_contacts = ListField(
        EmbeddedField(EmergencyContactEmbed),
        attribute="ec"
    )
    partner_name = StrField(attribute="pn")
    partner_name_validation = BoolField(attribute="pn_v")
    wallet_bank_account_id = StrField(attribute="wba")
    wallet_payment_schedule_id = StrField(attribute="wps")
    work_info = ListField(EmbeddedField(WorkInfoEmbed), attribute="wi")

    class Meta:
        collection_name = "lender_borrowers"
