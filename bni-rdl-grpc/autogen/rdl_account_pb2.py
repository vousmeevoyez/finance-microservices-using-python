# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: autogen/rdl_account.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='autogen/rdl_account.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x19\x61utogen/rdl_account.proto\"\x9b\x06\n\x10\x43reateRdlRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x13\n\x0bmiddle_name\x18\x03 \x01(\t\x12\x11\n\tlast_name\x18\x04 \x01(\t\x12\x13\n\x0bnpwp_option\x18\x05 \x01(\t\x12\x0f\n\x07npwp_no\x18\x06 \x01(\t\x12\x13\n\x0bnationality\x18\x07 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x08 \x01(\t\x12\x10\n\x08religion\x18\t \x01(\t\x12\x13\n\x0b\x62irth_place\x18\n \x01(\t\x12\x12\n\nbirth_date\x18\x0b \x01(\t\x12\x0e\n\x06gender\x18\x0c \x01(\t\x12\x12\n\nis_married\x18\r \x01(\t\x12\x1a\n\x12mother_maiden_name\x18\x0e \x01(\t\x12\x10\n\x08job_code\x18\x0f \x01(\t\x12\x11\n\teducation\x18\x10 \x01(\t\x12\x11\n\tid_number\x18\x11 \x01(\t\x12\x17\n\x0fid_issuing_city\x18\x12 \x01(\t\x12\x16\n\x0eid_expire_date\x18\x13 \x01(\t\x12\x16\n\x0e\x61\x64\x64ress_street\x18\x14 \x01(\t\x12\x1b\n\x13\x61\x64\x64ress_rt_rw_perum\x18\x15 \x01(\t\x12\x19\n\x11\x61\x64\x64ress_kelurahan\x18\x16 \x01(\t\x12\x19\n\x11\x61\x64\x64ress_kecamatan\x18\x17 \x01(\t\x12\x10\n\x08zip_code\x18\x18 \x01(\t\x12\x16\n\x0ehome_phone_ext\x18\x19 \x01(\t\x12\x12\n\nhome_phone\x18\x1a \x01(\t\x12\x18\n\x10office_phone_ext\x18\x1b \x01(\t\x12\x14\n\x0coffice_phone\x18\x1c \x01(\t\x12\x18\n\x10mobile_phone_ext\x18\x1d \x01(\t\x12\x14\n\x0cmobile_phone\x18\x1e \x01(\t\x12\x0f\n\x07\x66\x61x_ext\x18\x1f \x01(\t\x12\x0b\n\x03\x66\x61x\x18  \x01(\t\x12\r\n\x05\x65mail\x18! \x01(\t\x12\x16\n\x0emonthly_income\x18\" \x01(\t\x12\x16\n\x0e\x62ranch_opening\x18# \x01(\t\x12\x0e\n\x06reason\x18$ \x01(\t\x12\x16\n\x0esource_of_fund\x18% \x01(\t\"I\n\x11\x43reateRdlResponse\x12\x12\n\njournal_no\x18\x01 \x01(\t\x12\x12\n\naccount_no\x18\x02 \x01(\t\x12\x0c\n\x04uuid\x18\x03 \x01(\t\"\x91\x01\n\x0bHistoryItem\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\ncreated_at\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x03\x12\x0f\n\x07\x62\x61lance\x18\x04 \x01(\x03\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x12\n\naccount_no\x18\x06 \x01(\t\x12\x18\n\x10transaction_type\x18\x07 \x01(\t\"\'\n\x11GetHistoryRequest\x12\x12\n\naccount_no\x18\x01 \x01(\t\"\xb0\x01\n\x12GetHistoryResponse\x12\x12\n\nstart_date\x18\x01 \x01(\t\x12\x10\n\x08\x65nd_date\x18\x02 \x01(\t\x12\x15\n\rstart_balance\x18\x03 \x01(\x03\x12\x13\n\x0btotal_debit\x18\x04 \x01(\x03\x12\x14\n\x0ctotal_credit\x18\x05 \x01(\x03\x12\x13\n\x0b\x65nd_balance\x18\x06 \x01(\x03\x12\x1d\n\x07\x64\x65tails\x18\x07 \x03(\x0b\x32\x0c.HistoryItem\"\'\n\x11GetBalanceRequest\x12\x12\n\naccount_no\x18\x01 \x01(\t\"^\n\x12GetBalanceResponse\x12\x12\n\naccount_no\x18\x01 \x01(\t\x12\x15\n\rcustomer_name\x18\x02 \x01(\t\x12\x0f\n\x07\x62\x61lance\x18\x03 \x01(\x02\x12\x0c\n\x04uuid\x18\x04 \x01(\t2\xb4\x01\n\nRdlAccount\x12\x34\n\tCreateRdl\x12\x11.CreateRdlRequest\x1a\x12.CreateRdlResponse\"\x00\x12\x37\n\nGetHistory\x12\x12.GetHistoryRequest\x1a\x13.GetHistoryResponse\"\x00\x12\x37\n\nGetBalance\x12\x12.GetBalanceRequest\x1a\x13.GetBalanceResponse\"\x00\x62\x06proto3')
)




_CREATERDLREQUEST = _descriptor.Descriptor(
  name='CreateRdlRequest',
  full_name='CreateRdlRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='CreateRdlRequest.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='first_name', full_name='CreateRdlRequest.first_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='middle_name', full_name='CreateRdlRequest.middle_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='last_name', full_name='CreateRdlRequest.last_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='npwp_option', full_name='CreateRdlRequest.npwp_option', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='npwp_no', full_name='CreateRdlRequest.npwp_no', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nationality', full_name='CreateRdlRequest.nationality', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='country', full_name='CreateRdlRequest.country', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='religion', full_name='CreateRdlRequest.religion', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='birth_place', full_name='CreateRdlRequest.birth_place', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='birth_date', full_name='CreateRdlRequest.birth_date', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gender', full_name='CreateRdlRequest.gender', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_married', full_name='CreateRdlRequest.is_married', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mother_maiden_name', full_name='CreateRdlRequest.mother_maiden_name', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job_code', full_name='CreateRdlRequest.job_code', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='education', full_name='CreateRdlRequest.education', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id_number', full_name='CreateRdlRequest.id_number', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id_issuing_city', full_name='CreateRdlRequest.id_issuing_city', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id_expire_date', full_name='CreateRdlRequest.id_expire_date', index=18,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address_street', full_name='CreateRdlRequest.address_street', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address_rt_rw_perum', full_name='CreateRdlRequest.address_rt_rw_perum', index=20,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address_kelurahan', full_name='CreateRdlRequest.address_kelurahan', index=21,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address_kecamatan', full_name='CreateRdlRequest.address_kecamatan', index=22,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zip_code', full_name='CreateRdlRequest.zip_code', index=23,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='home_phone_ext', full_name='CreateRdlRequest.home_phone_ext', index=24,
      number=25, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='home_phone', full_name='CreateRdlRequest.home_phone', index=25,
      number=26, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='office_phone_ext', full_name='CreateRdlRequest.office_phone_ext', index=26,
      number=27, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='office_phone', full_name='CreateRdlRequest.office_phone', index=27,
      number=28, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mobile_phone_ext', full_name='CreateRdlRequest.mobile_phone_ext', index=28,
      number=29, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mobile_phone', full_name='CreateRdlRequest.mobile_phone', index=29,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fax_ext', full_name='CreateRdlRequest.fax_ext', index=30,
      number=31, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fax', full_name='CreateRdlRequest.fax', index=31,
      number=32, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='email', full_name='CreateRdlRequest.email', index=32,
      number=33, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='monthly_income', full_name='CreateRdlRequest.monthly_income', index=33,
      number=34, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='branch_opening', full_name='CreateRdlRequest.branch_opening', index=34,
      number=35, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reason', full_name='CreateRdlRequest.reason', index=35,
      number=36, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source_of_fund', full_name='CreateRdlRequest.source_of_fund', index=36,
      number=37, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=825,
)


_CREATERDLRESPONSE = _descriptor.Descriptor(
  name='CreateRdlResponse',
  full_name='CreateRdlResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='journal_no', full_name='CreateRdlResponse.journal_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_no', full_name='CreateRdlResponse.account_no', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='CreateRdlResponse.uuid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=827,
  serialized_end=900,
)


_HISTORYITEM = _descriptor.Descriptor(
  name='HistoryItem',
  full_name='HistoryItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='HistoryItem.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='HistoryItem.created_at', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='HistoryItem.amount', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='balance', full_name='HistoryItem.balance', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='HistoryItem.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_no', full_name='HistoryItem.account_no', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transaction_type', full_name='HistoryItem.transaction_type', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=903,
  serialized_end=1048,
)


_GETHISTORYREQUEST = _descriptor.Descriptor(
  name='GetHistoryRequest',
  full_name='GetHistoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_no', full_name='GetHistoryRequest.account_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1050,
  serialized_end=1089,
)


_GETHISTORYRESPONSE = _descriptor.Descriptor(
  name='GetHistoryResponse',
  full_name='GetHistoryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_date', full_name='GetHistoryResponse.start_date', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_date', full_name='GetHistoryResponse.end_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_balance', full_name='GetHistoryResponse.start_balance', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_debit', full_name='GetHistoryResponse.total_debit', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_credit', full_name='GetHistoryResponse.total_credit', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_balance', full_name='GetHistoryResponse.end_balance', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='details', full_name='GetHistoryResponse.details', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1092,
  serialized_end=1268,
)


_GETBALANCEREQUEST = _descriptor.Descriptor(
  name='GetBalanceRequest',
  full_name='GetBalanceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_no', full_name='GetBalanceRequest.account_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1270,
  serialized_end=1309,
)


_GETBALANCERESPONSE = _descriptor.Descriptor(
  name='GetBalanceResponse',
  full_name='GetBalanceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_no', full_name='GetBalanceResponse.account_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='customer_name', full_name='GetBalanceResponse.customer_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='balance', full_name='GetBalanceResponse.balance', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='GetBalanceResponse.uuid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1311,
  serialized_end=1405,
)

_GETHISTORYRESPONSE.fields_by_name['details'].message_type = _HISTORYITEM
DESCRIPTOR.message_types_by_name['CreateRdlRequest'] = _CREATERDLREQUEST
DESCRIPTOR.message_types_by_name['CreateRdlResponse'] = _CREATERDLRESPONSE
DESCRIPTOR.message_types_by_name['HistoryItem'] = _HISTORYITEM
DESCRIPTOR.message_types_by_name['GetHistoryRequest'] = _GETHISTORYREQUEST
DESCRIPTOR.message_types_by_name['GetHistoryResponse'] = _GETHISTORYRESPONSE
DESCRIPTOR.message_types_by_name['GetBalanceRequest'] = _GETBALANCEREQUEST
DESCRIPTOR.message_types_by_name['GetBalanceResponse'] = _GETBALANCERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateRdlRequest = _reflection.GeneratedProtocolMessageType('CreateRdlRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATERDLREQUEST,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:CreateRdlRequest)
  })
_sym_db.RegisterMessage(CreateRdlRequest)

CreateRdlResponse = _reflection.GeneratedProtocolMessageType('CreateRdlResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATERDLRESPONSE,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:CreateRdlResponse)
  })
_sym_db.RegisterMessage(CreateRdlResponse)

HistoryItem = _reflection.GeneratedProtocolMessageType('HistoryItem', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYITEM,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:HistoryItem)
  })
_sym_db.RegisterMessage(HistoryItem)

GetHistoryRequest = _reflection.GeneratedProtocolMessageType('GetHistoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETHISTORYREQUEST,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:GetHistoryRequest)
  })
_sym_db.RegisterMessage(GetHistoryRequest)

GetHistoryResponse = _reflection.GeneratedProtocolMessageType('GetHistoryResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETHISTORYRESPONSE,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:GetHistoryResponse)
  })
_sym_db.RegisterMessage(GetHistoryResponse)

GetBalanceRequest = _reflection.GeneratedProtocolMessageType('GetBalanceRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBALANCEREQUEST,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:GetBalanceRequest)
  })
_sym_db.RegisterMessage(GetBalanceRequest)

GetBalanceResponse = _reflection.GeneratedProtocolMessageType('GetBalanceResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETBALANCERESPONSE,
  '__module__' : 'autogen.rdl_account_pb2'
  # @@protoc_insertion_point(class_scope:GetBalanceResponse)
  })
_sym_db.RegisterMessage(GetBalanceResponse)



_RDLACCOUNT = _descriptor.ServiceDescriptor(
  name='RdlAccount',
  full_name='RdlAccount',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1408,
  serialized_end=1588,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateRdl',
    full_name='RdlAccount.CreateRdl',
    index=0,
    containing_service=None,
    input_type=_CREATERDLREQUEST,
    output_type=_CREATERDLRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetHistory',
    full_name='RdlAccount.GetHistory',
    index=1,
    containing_service=None,
    input_type=_GETHISTORYREQUEST,
    output_type=_GETHISTORYRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetBalance',
    full_name='RdlAccount.GetBalance',
    index=2,
    containing_service=None,
    input_type=_GETBALANCEREQUEST,
    output_type=_GETBALANCERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_RDLACCOUNT)

DESCRIPTOR.services_by_name['RdlAccount'] = _RDLACCOUNT

# @@protoc_insertion_point(module_scope)
