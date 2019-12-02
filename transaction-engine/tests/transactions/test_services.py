import pytest
from bson import ObjectId

from app.api.transactions.services import refund
from app.api.models.transaction import Transaction


def test_debit_refund(setup_debit_transaction):
    debit_refund_trx = refund(setup_debit_transaction.id)

    # make sure original transaction cancelled
    original_trx = Transaction.find_one({"_id": ObjectId(setup_debit_transaction.id)})
    assert original_trx.status == "CANCELLED"

    result = Transaction.find_one({"_id": ObjectId(debit_refund_trx[0])})
    assert result.status == "PENDING"
    assert result.amount == 100
    assert result.transaction_type == "DEBIT_REFUND"
    assert result.payment.payment_type == "CREDIT"


def test_credit_refund(setup_credit_transaction):
    credit_refund_trx = refund(setup_credit_transaction.id)

    # make sure original transaction cancelled
    original_trx = Transaction.find_one({"_id": ObjectId(setup_credit_transaction.id)})
    assert original_trx.status == "CANCELLED"

    result = Transaction.find_one({"_id": ObjectId(credit_refund_trx[0])})
    assert result.status == "PENDING"
    assert result.amount == -1000000
    assert result.transaction_type == "CREDIT_REFUND"
    assert result.payment.payment_type == "DEBIT"
