# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: autogen/transfer.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="autogen/transfer.proto",
    package="",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x16\x61utogen/transfer.proto".\n\x16TransferInquiryRequest\x12\x14\n\x0crequest_uuid\x18\x01 \x01(\t"\xa9\x01\n\x17TransferInquiryResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x12\n\ncreated_at\x18\x02 \x01(\t\x12\x18\n\x10transaction_type\x18\x03 \x01(\t\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65stination\x18\x05 \x01(\t\x12\x14\n\x0crequest_uuid\x18\x06 \x01(\t\x12\x15\n\rresponse_uuid\x18\x07 \x01(\t"\x96\x01\n\x0fTransferRequest\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65stination\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x03\x12\x0e\n\x06remark\x18\x04 \x01(\t\x12\x11\n\tbank_code\x18\x05 \x01(\t\x12\x14\n\x0cinquiry_uuid\x18\x06 \x01(\t\x12\x15\n\rtransfer_uuid\x18\x07 \x01(\t")\n\x10TransferResponse\x12\x15\n\rresponse_uuid\x18\x01 \x01(\t2\x88\x01\n\x0bOpgTransfer\x12\x46\n\x0fTransferInquiry\x12\x17.TransferInquiryRequest\x1a\x18.TransferInquiryResponse"\x00\x12\x31\n\x08Transfer\x12\x10.TransferRequest\x1a\x11.TransferResponse"\x00\x62\x06proto3'
    ),
)


_TRANSFERINQUIRYREQUEST = _descriptor.Descriptor(
    name="TransferInquiryRequest",
    full_name="TransferInquiryRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="request_uuid",
            full_name="TransferInquiryRequest.request_uuid",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=26,
    serialized_end=72,
)


_TRANSFERINQUIRYRESPONSE = _descriptor.Descriptor(
    name="TransferInquiryResponse",
    full_name="TransferInquiryResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="status",
            full_name="TransferInquiryResponse.status",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="created_at",
            full_name="TransferInquiryResponse.created_at",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="transaction_type",
            full_name="TransferInquiryResponse.transaction_type",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="source",
            full_name="TransferInquiryResponse.source",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="destination",
            full_name="TransferInquiryResponse.destination",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="request_uuid",
            full_name="TransferInquiryResponse.request_uuid",
            index=5,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="response_uuid",
            full_name="TransferInquiryResponse.response_uuid",
            index=6,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=75,
    serialized_end=244,
)


_TRANSFERREQUEST = _descriptor.Descriptor(
    name="TransferRequest",
    full_name="TransferRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="source",
            full_name="TransferRequest.source",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="destination",
            full_name="TransferRequest.destination",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="amount",
            full_name="TransferRequest.amount",
            index=2,
            number=3,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="remark",
            full_name="TransferRequest.remark",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="bank_code",
            full_name="TransferRequest.bank_code",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="inquiry_uuid",
            full_name="TransferRequest.inquiry_uuid",
            index=5,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="transfer_uuid",
            full_name="TransferRequest.transfer_uuid",
            index=6,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=247,
    serialized_end=397,
)


_TRANSFERRESPONSE = _descriptor.Descriptor(
    name="TransferResponse",
    full_name="TransferResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="response_uuid",
            full_name="TransferResponse.response_uuid",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=399,
    serialized_end=440,
)

DESCRIPTOR.message_types_by_name["TransferInquiryRequest"] = _TRANSFERINQUIRYREQUEST
DESCRIPTOR.message_types_by_name["TransferInquiryResponse"] = _TRANSFERINQUIRYRESPONSE
DESCRIPTOR.message_types_by_name["TransferRequest"] = _TRANSFERREQUEST
DESCRIPTOR.message_types_by_name["TransferResponse"] = _TRANSFERRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TransferInquiryRequest = _reflection.GeneratedProtocolMessageType(
    "TransferInquiryRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSFERINQUIRYREQUEST,
        "__module__": "autogen.transfer_pb2"
        # @@protoc_insertion_point(class_scope:TransferInquiryRequest)
    },
)
_sym_db.RegisterMessage(TransferInquiryRequest)

TransferInquiryResponse = _reflection.GeneratedProtocolMessageType(
    "TransferInquiryResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSFERINQUIRYRESPONSE,
        "__module__": "autogen.transfer_pb2"
        # @@protoc_insertion_point(class_scope:TransferInquiryResponse)
    },
)
_sym_db.RegisterMessage(TransferInquiryResponse)

TransferRequest = _reflection.GeneratedProtocolMessageType(
    "TransferRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSFERREQUEST,
        "__module__": "autogen.transfer_pb2"
        # @@protoc_insertion_point(class_scope:TransferRequest)
    },
)
_sym_db.RegisterMessage(TransferRequest)

TransferResponse = _reflection.GeneratedProtocolMessageType(
    "TransferResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSFERRESPONSE,
        "__module__": "autogen.transfer_pb2"
        # @@protoc_insertion_point(class_scope:TransferResponse)
    },
)
_sym_db.RegisterMessage(TransferResponse)


_OPGTRANSFER = _descriptor.ServiceDescriptor(
    name="OpgTransfer",
    full_name="OpgTransfer",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    serialized_start=443,
    serialized_end=579,
    methods=[
        _descriptor.MethodDescriptor(
            name="TransferInquiry",
            full_name="OpgTransfer.TransferInquiry",
            index=0,
            containing_service=None,
            input_type=_TRANSFERINQUIRYREQUEST,
            output_type=_TRANSFERINQUIRYRESPONSE,
            serialized_options=None,
        ),
        _descriptor.MethodDescriptor(
            name="Transfer",
            full_name="OpgTransfer.Transfer",
            index=1,
            containing_service=None,
            input_type=_TRANSFERREQUEST,
            output_type=_TRANSFERRESPONSE,
            serialized_options=None,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_OPGTRANSFER)

DESCRIPTOR.services_by_name["OpgTransfer"] = _OPGTRANSFER

# @@protoc_insertion_point(module_scope)