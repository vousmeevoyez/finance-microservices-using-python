from app.api.lib.core.factory import Factory
from app.api.transactions.factories.transactions.products import *


def generate_transaction(transaction, type_):
    """ interface to generate debit and credit """
    factory = Factory()
    # regist known transaction here
    # DEBIT TYPE
    factory.register("TRANSFER", TransferTransaction)
    factory.register("INVEST", InvestTransaction)
    factory.register("BANK_TRANSFER", BankTransferTransaction)
    factory.register("UPFRONT_FEE", UpfrontFeeTransaction)
    factory.register("INVEST_FEE", InvestFeeTransaction)
    factory.register("INVEST_REPAYMENT", InvestRepaymentTransaction)
    factory.register("CREDIT_REFUND", DebitRefundTransaction)
    factory.register("DISBURSE", DisburseTransaction)
    factory.register("WITHDRAW", WithdrawTransaction)
    # CREDIT TYPE
    factory.register("TOP_UP_RDL", TopUpRdlTransaction)
    factory.register("RECEIVE_TRANSFER", ReceiveTransferTransaction)
    factory.register("RECEIVE_INVEST", ReceiveInvestTransaction)
    factory.register("RECEIVE_UPFRONT_FEE", ReceiveUpfrontFee)
    factory.register("RECEIVE_INVEST_FEE", ReceiveInvestFee)
    factory.register("RECEIVE_REPAYMENT", ReceiveRepayment)
    factory.register("DEBIT_REFUND", CreditRefundTransaction)

    generator = factory.get(type_)
    transaction.load(generator)
    return generator.create()
