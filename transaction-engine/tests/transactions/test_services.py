import pytest
from bson import ObjectId

from app.api.transactions.services import (
    refund,
    bulk_transaction,
    aggregate_by_destination_id
)
from app.api.models.transaction import Transaction


def test_debit_refund(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction
    transaction = transactions[0]

    debit_refund_trx = refund(transaction.id)

    # make sure original transaction cancelled
    original_trx = Transaction.find_one({"_id": ObjectId(transaction.id)})
    assert original_trx.status == "CANCELLED"

    result = Transaction.find_one({"_id": ObjectId(debit_refund_trx[0])})
    assert result.status == "PENDING"
    assert result.amount == 500000
    assert result.transaction_type == "DEBIT_REFUND"
    assert result.payment.payment_type == "CREDIT"


def test_credit_refund(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction
    transaction = transactions[2]

    credit_refund_trx = refund(transaction.id)

    # make sure original transaction cancelled
    original_trx = Transaction.find_one({"_id": ObjectId(transaction.id)})
    assert original_trx.status == "CANCELLED"

    result = Transaction.find_one({"_id": ObjectId(credit_refund_trx[0])})
    assert result.status == "PENDING"
    assert result.amount == -1000000
    assert result.transaction_type == "CREDIT_REFUND"
    assert result.payment.payment_type == "DEBIT"


def test_aggregate_transactions():
    transactions = [
        {
            "wallet_id": "some-wallet-id",
            "source_id": "some-source-id",
            "source_type": "some-source-type",
            "destination_id": "some-destination-id",
            "destination_type": "some-destination-type",
            "amount": 100,
            "transaction_type": "some-transaction-type",
        },
        {
            "wallet_id": "some-wallet-id",
            "source_id": "some-source-id",
            "source_type": "some-source-type",
            "destination_id": "some-destination-id",
            "destination_type": "some-destination-type",
            "amount": 101,
            "transaction_type": "some-transaction-type",
        },
        {
            "wallet_id": "some-wallet-id",
            "source_id": "some-source-id",
            "source_type": "some-source-type",
            "destination_id": "some-destination-id",
            "destination_type": "some-destination-type",
            "amount": 102,
            "transaction_type": "some-transaction-type",
        },
        {
            "wallet_id": "some-wallet-id",
            "source_id": "some-source-id",
            "source_type": "some-source-type",
            "destination_id": "some-destination-id2",
            "destination_type": "some-destination-type",
            "amount": 101,
            "transaction_type": "some-transaction-type",
        },
        {
            "wallet_id": "some-wallet-id",
            "source_id": "some-source-id",
            "source_type": "some-source-type",
            "destination_id": "some-destination-id2",
            "destination_type": "some-destination-type",
            "amount": 11,
            "transaction_type": "some-transaction-type",
        },
        {
            "wallet_id": "some-wallet-id",
            "source_id": "some-source-id",
            "source_type": "some-source-type",
            "destination_id": "some-destination-id2",
            "destination_type": "some-destination-type",
            "amount": 99,
            "transaction_type": "some-transaction-type",
        }
    ]
    result = aggregate_by_destination_id(transactions)
    for trx in result:
        assert trx["source_id"]
        assert trx["source_type"]
        assert trx["destination_id"]
        assert trx["destination_type"]
        assert trx["transaction_type"]
        assert trx["amount"]
        assert trx["wallet_id"]


def test_bulk_transaction_upfront_fee(
        setup_escrow_wallet, setup_profit_wallet, make_transaction):
    """ test simulate bulk transfer upfront fee from escrow to profit"""
    transactions = [
        {
            "wallet_id": str(setup_escrow_wallet.id),
            "source_id": str(setup_escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(setup_profit_wallet.id),
            "destination_type": "PROFIT",
            "amount": -1,
            "transaction_type": "UPFRONT_FEE",
        },
        {
            "wallet_id": str(setup_escrow_wallet.id),
            "source_id": str(setup_escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(setup_profit_wallet.id),
            "destination_type": "PROFIT",
            "amount": -1,
            "transaction_type": "UPFRONT_FEE",
        },
        {
            "wallet_id": str(setup_escrow_wallet.id),
            "source_id": str(setup_escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(setup_profit_wallet.id),
            "destination_type": "PROFIT",
            "amount": -1,
            "transaction_type": "UPFRONT_FEE",
        },
    ]

    result = bulk_transaction(transactions)
    # make sure only 1 transaction created
    assert len(result) == 1

    transaction = Transaction.find_one({"id": ObjectId(result[0])})
    assert transaction.amount == -3
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "UPFRONT_FEE"
    assert transaction.payment.payment_type == "DEBIT"


def test_bulk_transaction_investor_fee(
        setup_escrow_wallet, setup_profit_wallet, make_transaction):
    """ test simulate bulk transfer upfront fee from profit to escrow"""
    transactions = [
        {
            "wallet_id": str(setup_profit_wallet.id),
            "source_id": str(setup_profit_wallet.id),
            "source_type": "PROFIT",
            "destination_id": str(setup_escrow_wallet.id),
            "destination_type": "ESCROW",
            "amount": -1,
            "transaction_type": "INVEST_FEE",
        },
        {
            "wallet_id": str(setup_profit_wallet.id),
            "source_id": str(setup_profit_wallet.id),
            "source_type": "PROFIT",
            "destination_id": str(setup_escrow_wallet.id),
            "destination_type": "ESCROW",
            "amount": -1,
            "transaction_type": "INVEST_FEE",
        },
        {
            "wallet_id": str(setup_profit_wallet.id),
            "source_id": str(setup_profit_wallet.id),
            "source_type": "PROFIT",
            "destination_id": str(setup_escrow_wallet.id),
            "destination_type": "ESCROW",
            "amount": -1,
            "transaction_type": "INVEST_FEE",
        }
    ]

    result = bulk_transaction(transactions)
    # make sure only 1 transaction created
    assert len(result) == 1

    transaction = Transaction.find_one({"id": ObjectId(result[0])})
    assert transaction.amount == -3
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "INVEST_FEE"
    assert transaction.payment.payment_type == "DEBIT"
