"""
    Services Class
    _______________
    Handle logic to models or external party API
"""

from rpc.models import VirtualAccount, generate_past_expired_at, update_document
from rpc.factories.provider.builder import generate_provider
from rpc.lib.core.provider import ProviderError

# base error
from rpc.lib.core.exceptions import BaseError


class ServicesError(BaseError):
    """ error raised when something wrong at services """


class BNIVaServices:
    """ BNI Va Services Class for gRPC"""

    def __init__(self, va_type, account_no=None):
        # look up account no first!
        if account_no is not None:
            virtual_account = VirtualAccount.objects(account_no=account_no).first()
            if virtual_account is None:
                raise ServicesError("VA_NOT_FOUND", "Virtual Account not found")
            self.virtual_account = virtual_account

        provider = generate_provider("BNI_VA")
        provider.set(va_type)
        self.provider = provider

    async def create_va(self, serialized_payload):
        """ execute create BNI Va through provider """
        try:
            result = await self.provider.create_va(**serialized_payload)
        except ProviderError as error:
            raise ServicesError(error.message, error.original_exception)
        return result

    async def inquiry_va(self):
        """ execute nquiry BNI Va through provider """
        try:
            result = await self.provider.get_inquiry(self.virtual_account.trx_id)
        except ProviderError as error:
            raise ServicesError(error.message, error.original_exception)
        return result

    async def update_va(self, serialized_payload):
        """ execute update BNI Va through provider """
        try:
            result = await self.provider.update_va(**serialized_payload)
        except ProviderError as error:
            raise ServicesError(error.message, error.original_exception)
        else:
            update_document(self.virtual_account, serialized_payload)
            self.virtual_account.save()
        return result

    async def disable_va(self):
        """ execute disable BNI Va through provider """
        payload = {
            "trx_id": self.virtual_account.trx_id,
            "amount": self.virtual_account.amount,
            "name": self.virtual_account.name,
            "expired_at": generate_past_expired_at(),
        }

        try:
            await self.provider.update_va(**payload)
        except ProviderError as error:
            raise ServicesError(error.message, error.original_exception)
        else:
            # remove record
            self.virtual_account.delete()
        return {"status": "OK"}
