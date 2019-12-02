# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: autogen/virtual_account.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='autogen/virtual_account.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1d\x61utogen/virtual_account.proto\"j\n\x0f\x43reateVaRequest\x12\x0f\n\x07va_type\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x05\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x14\n\x0cphone_number\x18\x05 \x01(\t\x12\x12\n\nexpired_at\x18\x07 \x01(\t\"6\n\x10\x43reateVaResponse\x12\x0e\n\x06trx_id\x18\x01 \x01(\t\x12\x12\n\naccount_no\x18\x02 \x01(\t\"7\n\x10InquiryVaRequest\x12\x0f\n\x07va_type\x18\x01 \x01(\t\x12\x12\n\naccount_no\x18\x02 \x01(\t\"\xaf\x02\n\x11InquiryVaResponse\x12\x0e\n\x06trx_id\x18\x01 \x01(\t\x12\x12\n\naccount_no\x18\x02 \x01(\t\x12\x12\n\ntrx_amount\x18\x03 \x01(\x05\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x14\n\x0cphone_number\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t\x12\x12\n\ncreated_at\x18\x07 \x01(\t\x12\x12\n\nexpired_at\x18\x08 \x01(\t\x12\x0f\n\x07paid_at\x18\t \x01(\t\x12\x12\n\nupdated_at\x18\n \x01(\t\x12\x12\n\nref_number\x18\x0b \x01(\t\x12\x13\n\x0bpaid_amount\x18\x0c \x01(\x05\x12\x0e\n\x06status\x18\r \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x0e \x01(\t\x12\x14\n\x0c\x62illing_type\x18\x0f \x01(\t\"d\n\x0fUpdateVaRequest\x12\x0f\n\x07va_type\x18\x01 \x01(\t\x12\x0e\n\x06trx_id\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x05\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x12\n\nexpired_at\x18\x05 \x01(\t\"3\n\x10UpdateVaResponse\x12\x0f\n\x07va_type\x18\x01 \x01(\t\x12\x0e\n\x06trx_id\x18\x02 \x01(\t\"7\n\x10\x44isableVaRequest\x12\x0f\n\x07va_type\x18\x01 \x01(\t\x12\x12\n\naccount_no\x18\x02 \x01(\t\"#\n\x11\x44isableVaResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2\xe2\x01\n\x0eVirtualAccount\x12\x31\n\x08\x43reateVa\x12\x10.CreateVaRequest\x1a\x11.CreateVaResponse\"\x00\x12\x34\n\tInquiryVa\x12\x11.InquiryVaRequest\x1a\x12.InquiryVaResponse\"\x00\x12\x31\n\x08UpdateVa\x12\x10.UpdateVaRequest\x1a\x11.UpdateVaResponse\"\x00\x12\x34\n\tDisableVa\x12\x11.DisableVaRequest\x1a\x12.DisableVaResponse\"\x00\x62\x06proto3')
)




_CREATEVAREQUEST = _descriptor.Descriptor(
  name='CreateVaRequest',
  full_name='CreateVaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='va_type', full_name='CreateVaRequest.va_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='CreateVaRequest.amount', index=1,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='CreateVaRequest.name', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phone_number', full_name='CreateVaRequest.phone_number', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expired_at', full_name='CreateVaRequest.expired_at', index=4,
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
  serialized_start=33,
  serialized_end=139,
)


_CREATEVARESPONSE = _descriptor.Descriptor(
  name='CreateVaResponse',
  full_name='CreateVaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trx_id', full_name='CreateVaResponse.trx_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_no', full_name='CreateVaResponse.account_no', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=141,
  serialized_end=195,
)


_INQUIRYVAREQUEST = _descriptor.Descriptor(
  name='InquiryVaRequest',
  full_name='InquiryVaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='va_type', full_name='InquiryVaRequest.va_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_no', full_name='InquiryVaRequest.account_no', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=197,
  serialized_end=252,
)


_INQUIRYVARESPONSE = _descriptor.Descriptor(
  name='InquiryVaResponse',
  full_name='InquiryVaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trx_id', full_name='InquiryVaResponse.trx_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_no', full_name='InquiryVaResponse.account_no', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trx_amount', full_name='InquiryVaResponse.trx_amount', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='InquiryVaResponse.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phone_number', full_name='InquiryVaResponse.phone_number', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='email', full_name='InquiryVaResponse.email', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='InquiryVaResponse.created_at', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expired_at', full_name='InquiryVaResponse.expired_at', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='paid_at', full_name='InquiryVaResponse.paid_at', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='InquiryVaResponse.updated_at', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ref_number', full_name='InquiryVaResponse.ref_number', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='paid_amount', full_name='InquiryVaResponse.paid_amount', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='InquiryVaResponse.status', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='InquiryVaResponse.description', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='billing_type', full_name='InquiryVaResponse.billing_type', index=14,
      number=15, type=9, cpp_type=9, label=1,
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
  serialized_start=255,
  serialized_end=558,
)


_UPDATEVAREQUEST = _descriptor.Descriptor(
  name='UpdateVaRequest',
  full_name='UpdateVaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='va_type', full_name='UpdateVaRequest.va_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trx_id', full_name='UpdateVaRequest.trx_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='UpdateVaRequest.amount', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='UpdateVaRequest.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expired_at', full_name='UpdateVaRequest.expired_at', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=560,
  serialized_end=660,
)


_UPDATEVARESPONSE = _descriptor.Descriptor(
  name='UpdateVaResponse',
  full_name='UpdateVaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='va_type', full_name='UpdateVaResponse.va_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trx_id', full_name='UpdateVaResponse.trx_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=662,
  serialized_end=713,
)


_DISABLEVAREQUEST = _descriptor.Descriptor(
  name='DisableVaRequest',
  full_name='DisableVaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='va_type', full_name='DisableVaRequest.va_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_no', full_name='DisableVaRequest.account_no', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=715,
  serialized_end=770,
)


_DISABLEVARESPONSE = _descriptor.Descriptor(
  name='DisableVaResponse',
  full_name='DisableVaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='DisableVaResponse.status', index=0,
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
  serialized_start=772,
  serialized_end=807,
)

DESCRIPTOR.message_types_by_name['CreateVaRequest'] = _CREATEVAREQUEST
DESCRIPTOR.message_types_by_name['CreateVaResponse'] = _CREATEVARESPONSE
DESCRIPTOR.message_types_by_name['InquiryVaRequest'] = _INQUIRYVAREQUEST
DESCRIPTOR.message_types_by_name['InquiryVaResponse'] = _INQUIRYVARESPONSE
DESCRIPTOR.message_types_by_name['UpdateVaRequest'] = _UPDATEVAREQUEST
DESCRIPTOR.message_types_by_name['UpdateVaResponse'] = _UPDATEVARESPONSE
DESCRIPTOR.message_types_by_name['DisableVaRequest'] = _DISABLEVAREQUEST
DESCRIPTOR.message_types_by_name['DisableVaResponse'] = _DISABLEVARESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateVaRequest = _reflection.GeneratedProtocolMessageType('CreateVaRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEVAREQUEST,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:CreateVaRequest)
  })
_sym_db.RegisterMessage(CreateVaRequest)

CreateVaResponse = _reflection.GeneratedProtocolMessageType('CreateVaResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEVARESPONSE,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:CreateVaResponse)
  })
_sym_db.RegisterMessage(CreateVaResponse)

InquiryVaRequest = _reflection.GeneratedProtocolMessageType('InquiryVaRequest', (_message.Message,), {
  'DESCRIPTOR' : _INQUIRYVAREQUEST,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:InquiryVaRequest)
  })
_sym_db.RegisterMessage(InquiryVaRequest)

InquiryVaResponse = _reflection.GeneratedProtocolMessageType('InquiryVaResponse', (_message.Message,), {
  'DESCRIPTOR' : _INQUIRYVARESPONSE,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:InquiryVaResponse)
  })
_sym_db.RegisterMessage(InquiryVaResponse)

UpdateVaRequest = _reflection.GeneratedProtocolMessageType('UpdateVaRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEVAREQUEST,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:UpdateVaRequest)
  })
_sym_db.RegisterMessage(UpdateVaRequest)

UpdateVaResponse = _reflection.GeneratedProtocolMessageType('UpdateVaResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEVARESPONSE,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:UpdateVaResponse)
  })
_sym_db.RegisterMessage(UpdateVaResponse)

DisableVaRequest = _reflection.GeneratedProtocolMessageType('DisableVaRequest', (_message.Message,), {
  'DESCRIPTOR' : _DISABLEVAREQUEST,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:DisableVaRequest)
  })
_sym_db.RegisterMessage(DisableVaRequest)

DisableVaResponse = _reflection.GeneratedProtocolMessageType('DisableVaResponse', (_message.Message,), {
  'DESCRIPTOR' : _DISABLEVARESPONSE,
  '__module__' : 'autogen.virtual_account_pb2'
  # @@protoc_insertion_point(class_scope:DisableVaResponse)
  })
_sym_db.RegisterMessage(DisableVaResponse)



_VIRTUALACCOUNT = _descriptor.ServiceDescriptor(
  name='VirtualAccount',
  full_name='VirtualAccount',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=810,
  serialized_end=1036,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateVa',
    full_name='VirtualAccount.CreateVa',
    index=0,
    containing_service=None,
    input_type=_CREATEVAREQUEST,
    output_type=_CREATEVARESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='InquiryVa',
    full_name='VirtualAccount.InquiryVa',
    index=1,
    containing_service=None,
    input_type=_INQUIRYVAREQUEST,
    output_type=_INQUIRYVARESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateVa',
    full_name='VirtualAccount.UpdateVa',
    index=2,
    containing_service=None,
    input_type=_UPDATEVAREQUEST,
    output_type=_UPDATEVARESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DisableVa',
    full_name='VirtualAccount.DisableVa',
    index=3,
    containing_service=None,
    input_type=_DISABLEVAREQUEST,
    output_type=_DISABLEVARESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_VIRTUALACCOUNT)

DESCRIPTOR.services_by_name['VirtualAccount'] = _VIRTUALACCOUNT

# @@protoc_insertion_point(module_scope)
