# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: autogen/email.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='autogen/email.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x13\x61utogen/email.proto\"`\n\x10SendEmailRequest\x12\x11\n\trecipient\x18\x01 \x01(\t\x12\x14\n\x0cproduct_type\x18\x02 \x01(\t\x12\x12\n\nemail_type\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\"#\n\x11SendEmailResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2I\n\x11\x45mailNotification\x12\x34\n\tSendEmail\x12\x11.SendEmailRequest\x1a\x12.SendEmailResponse\"\x00\x62\x06proto3')
)




_SENDEMAILREQUEST = _descriptor.Descriptor(
  name='SendEmailRequest',
  full_name='SendEmailRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='recipient', full_name='SendEmailRequest.recipient', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_type', full_name='SendEmailRequest.product_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='email_type', full_name='SendEmailRequest.email_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='SendEmailRequest.content', index=3,
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
  serialized_start=23,
  serialized_end=119,
)


_SENDEMAILRESPONSE = _descriptor.Descriptor(
  name='SendEmailResponse',
  full_name='SendEmailResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='SendEmailResponse.status', index=0,
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
  serialized_start=121,
  serialized_end=156,
)

DESCRIPTOR.message_types_by_name['SendEmailRequest'] = _SENDEMAILREQUEST
DESCRIPTOR.message_types_by_name['SendEmailResponse'] = _SENDEMAILRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SendEmailRequest = _reflection.GeneratedProtocolMessageType('SendEmailRequest', (_message.Message,), {
  'DESCRIPTOR' : _SENDEMAILREQUEST,
  '__module__' : 'autogen.email_pb2'
  # @@protoc_insertion_point(class_scope:SendEmailRequest)
  })
_sym_db.RegisterMessage(SendEmailRequest)

SendEmailResponse = _reflection.GeneratedProtocolMessageType('SendEmailResponse', (_message.Message,), {
  'DESCRIPTOR' : _SENDEMAILRESPONSE,
  '__module__' : 'autogen.email_pb2'
  # @@protoc_insertion_point(class_scope:SendEmailResponse)
  })
_sym_db.RegisterMessage(SendEmailResponse)



_EMAILNOTIFICATION = _descriptor.ServiceDescriptor(
  name='EmailNotification',
  full_name='EmailNotification',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=158,
  serialized_end=231,
  methods=[
  _descriptor.MethodDescriptor(
    name='SendEmail',
    full_name='EmailNotification.SendEmail',
    index=0,
    containing_service=None,
    input_type=_SENDEMAILREQUEST,
    output_type=_SENDEMAILRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_EMAILNOTIFICATION)

DESCRIPTOR.services_by_name['EmailNotification'] = _EMAILNOTIFICATION

# @@protoc_insertion_point(module_scope)
