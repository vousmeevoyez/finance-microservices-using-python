"""
    Transaction Products
    _________________
"""
# pylint: disable=no-self-use
# pylint: disable=import-error
# pylint: disable=bad-whitespace
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from celery import chain
from abc import ABC
from datetime import datetime, timedelta

# models
from app.api.models.transaction import Transaction

# task
from task.transaction.tasks import TransactionTask
from task.external.tasks import ExternalTask
from task.utility.tasks import UtilityTask


class AbstractTransaction(ABC):
    """ abstract transaction class """

    def __init__(self):
        self.transaction = None

    def load(self, transaction):
        self.transaction = transaction

    def create(self):
        # should send queue here
        TransactionTask().apply.apply_async(
            args=[str(self.transaction.id)],
            queue="transaction"
        )

        return self.transaction.id


class DebitTransaction(AbstractTransaction):
    """ Base class that represent transaction that deduct balance """


class CreditTransaction(AbstractTransaction):
    """ Base class that represent transaction that add balance """
    def create(self):
        chain(
            TransactionTask().apply.s(
                str(self.transaction.id)
            ).set(queue="transaction"),

            # send callback
            UtilityTask().notify.si(
                str(self.transaction.id)
            ).set(queue="utility")
        ).apply_async()
        return self.transaction.id


""" DEBIT TRANSACTION """


class TransferTransaction(DebitTransaction):
    """ transfer between user """


class BankTransferTransaction(DebitTransaction):
    """ transaction for starting investment """

    def create(self):
        chain(
            TransactionTask().apply.s(
                str(self.transaction.id)
            ).set(queue="transaction"),

            ExternalTask().transfer.si(
                str(self.transaction.id)
            ).set(queue="external"),

            ExternalTask().apply_external.s(
            ).set(queue="external"),

            # send callback
            UtilityTask().notify.si(
                str(self.transaction.id)
            ).set(queue="utility")
        ).apply_async()
        return self.transaction.id


class DebitRefundTransaction(DebitTransaction):
    """ transaction for refunding credit """


class DisburseTransaction(BankTransferTransaction):
    """ transaction for starting investment """


class InvestTransaction(BankTransferTransaction):
    """ transaction for starting investment """


class UpfrontFeeTransaction(BankTransferTransaction):
    """ transaction for sending upfront fee """


class InvestFeeTransaction(BankTransferTransaction):
    """ transaction for sending invest fee that we cut upfront
    back to investor """


class InvestRepaymentTransaction(BankTransferTransaction):
    """ transaction for sending invest fee + repayment back to investor """


class WithdrawTransaction(BankTransferTransaction):
    """ transaction for withdraw money from rdl to any bank account """

""" CREDIT TRANSACTION """


class TopUpRdlTransaction(AbstractTransaction):
    """ top up transaction """


class CreditRefundTransaction(CreditTransaction):
    """ credit refund transaction """


class ReceiveTransferTransaction(CreditTransaction):
    """ receive transfer """


class ReceiveInvestTransaction(CreditTransaction):
    """ receive invest """


class ReceiveUpfrontFee(CreditTransaction):
    """ receive upfront fee """


class ReceiveInvestFee(CreditTransaction):
    """ receive investor fee """


class ReceiveRepayment(AbstractTransaction):
    """ receive repayment from modanaku """
