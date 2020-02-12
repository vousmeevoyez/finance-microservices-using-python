"""
    Callback Factory Pattern
"""
from app.api.lib.core.factory import Factory
from app.api.callback.factories.products import (
    WithdrawCallback,
    InvestCallback,
    ReceiveInvestCallback,
    UpfrontFeeCallback,
    ReceiveUpfrontFeeCallback,
    DisburseCallback,
    InvestFeeCallback,
    ReceiveInvestFeeCallback,
    InvestRepaymentCallback,
    DebitRefundCallback,
    CreditRefundCallback,
    DebitAdjustmentCallback,
    CreditAdjustmentCallback
)


class CallbackInfo:
    def __init__(self, transaction_id, transaction_type, status):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.status = status

    def load(self, generator):
        generator.set(self)


def generate_internal_callback(callback_info):
    """ factory interface to generate callback """
    factory = Factory()
    factory.register("INVEST", InvestCallback)
    factory.register("WITHDRAW", WithdrawCallback)
    factory.register("RECEIVE_INVEST", ReceiveInvestCallback)
    factory.register("UPFRONT_FEE", UpfrontFeeCallback)
    factory.register("RECEIVE_UPFRONT_FEE", ReceiveUpfrontFeeCallback)
    factory.register("DISBURSE", DisburseCallback)
    factory.register("INVEST_FEE", InvestFeeCallback)
    factory.register("RECEIVE_INVEST_FEE", ReceiveInvestFeeCallback)
    factory.register("INVEST_REPAYMENT", InvestRepaymentCallback)
    factory.register("CREDIT_REFUND", CreditRefundCallback)
    factory.register("DEBIT_REFUND", DebitRefundCallback)
    factory.register("CREDIT_ADJUSTMENT", CreditAdjustmentCallback)
    factory.register("DEBIT_ADJUSTMENT", DebitAdjustmentCallback)

    generator = factory.get(callback_info.transaction_type)
    callback_info.load(generator)
    return generator
