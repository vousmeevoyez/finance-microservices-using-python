"""
    TEST TRANSACTION MODEL
"""

from app.api.models.transaction import (
    Transaction,
    PaymentEmbed,
    ChildTransactionEmbed
)
from app.api.models.investor import Investor
from app.api.models.investment import Investment
from app.api.models.wallet import Wallet
from app.api.models.loan_request import LoanRequest


def test_set_collection():
    """ test method to retrieve right collection based on source / destination
    type """
    result = PaymentEmbed._set_collection("INVESTOR")
    assert result == Investor

    result = PaymentEmbed._set_collection("INVESTOR_BANK_ACC")
    assert result == Investor

    result = PaymentEmbed._set_collection("INVESTOR_RDL_ACC")
    assert result == Investor

    result = PaymentEmbed._set_collection("INVESTMENT")
    assert result == Investment

    result = PaymentEmbed._set_collection("ESCROW")
    assert result == Wallet

    result = PaymentEmbed._set_collection("PROFIT")
    assert result == Wallet

    result = PaymentEmbed._set_collection("MODANAKU")
    assert result == LoanRequest

    result = PaymentEmbed._set_collection("REPAYMENT")
    assert result == LoanRequest


def test_get_record(setup_investor, setup_investment_with_loan):
    """ test method based on model, and model primary key, we retrieve bank
    account for that particular models """
    investment, loan_request = setup_investment_with_loan

    result = PaymentEmbed._get_record(Investor, setup_investor.id, "INVESTOR")
    assert result["bn"]
    assert result["ano"]
    assert result["at"]
    assert result["an"]

    result = PaymentEmbed._get_record(Investment, investment.id, "INVESTMENT")
    assert result["bn"]
    assert result["ano"]
    assert result["at"]
    assert result["an"]

    # get some loan request id from investment
    result = PaymentEmbed._get_record(LoanRequest, loan_request.id, "MODANAKU")
    assert result["bn"]
    assert result["ano"]
    assert result["at"]
    assert result["an"]

    # get some loan request id from investment
    result = PaymentEmbed._get_record(LoanRequest, loan_request.id, "REPAYMENT")
    assert result["bn"]
    assert result["ano"]
    assert result["at"]
    assert result["an"]


def test_top_up_transaction(setup_flask_app, setup_investor, setup_investor_wallet):
    """
        CREDIT - TOP UP FROM RDL to Investor WALLET
        data flow would be from:
            investor rdl bank account to investor wallet
    """

    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR_RDL_ACC",
        destination_id=setup_investor.id,
        destination_type="INVESTOR",
        amount=1000000,
        transaction_type="TOP_UP_RDL",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_transaction_rdl_to_investment(
    setup_flask_app,
    setup_investor,
    setup_investor_wallet,
    setup_investment,
    setup_escrow_wallet,
):
    """
        test invest flow from rdl to investment va
    """

    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR",
        destination_id=setup_investment.id,
        destination_type="INVESTMENT",
        amount=-1000000,
        transaction_type="INVEST",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()

    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR",
        destination_id=setup_investment.id,
        destination_type="INVESTMENT",
        amount=1000000,
        transaction_type="RECEIVE_INVEST",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_investment_to_escrow(
    setup_flask_app, setup_escrow_wallet, setup_profit_wallet
):
    """
        test invest flow from rdl to investment va
    """

    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=-1000000,
        transaction_type="UPFRONT_FEE",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()

    transaction = Transaction(
        wallet_id=setup_profit_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=1000000,
        transaction_type="RECEIVE_UPFRONT_FEE",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_escrow_to_modanaku(
    setup_flask_app, setup_escrow_wallet, setup_investment_with_loan
):
    """
        test disburse flow from escrow to modanaku va
    """
    investment, loan_request = setup_investment_with_loan

    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=loan_request.id,
        destination_type="MODANAKU",
        amount=-1000000,
        transaction_type="DISBURSE",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_repayment_to_escrow(
    setup_flask_app, setup_escrow_wallet, setup_investment_with_loan
):
    """
        test disburse flow from escrow to modanaku va
    """
    investment, loan_request = setup_investment_with_loan

    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=loan_request.id,
        source_type="MODANAKU",
        destination_id=loan_request.id,
        destination_type="REPAYMENT",
        amount=1000000,
        transaction_type="RECEIVE_REPAYMENT",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_profit_to_escrow(setup_flask_app, setup_profit_wallet, setup_escrow_wallet):
    """
        test disburse flow from escrow to modanaku va
    """

    transaction = Transaction(
        wallet_id=setup_profit_wallet.id,
        source_id=setup_profit_wallet.id,
        source_type="PROFIT",
        destination_id=setup_escrow_wallet.id,
        destination_type="ESCROW",
        amount=-1000000,
        transaction_type="INVEST_FEE",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_receive_invest_fee(setup_flask_app, setup_profit_wallet, setup_escrow_wallet):
    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_profit_wallet.id,
        source_type="PROFIT",
        destination_id=setup_escrow_wallet.id,
        destination_type="ESCROW",
        amount=1000000,
        transaction_type="RECEIVE_INVEST_FEE",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_escrow_to_rdl(setup_flask_app, setup_investor, setup_escrow_wallet):
    """
        test disburse flow from escrow to modanaku va
    """

    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_investor.id,
        destination_type="INVESTOR_RDL_ACC",
        amount=-1000000,
        transaction_type="INVEST_REPAYMENT",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_rdl_to_withdraw(
    setup_flask_app, setup_investor, setup_investor_wallet, setup_escrow_wallet
):
    """
        test disburse flow from escrow to modanaku va
    """

    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR_RDL_ACC",
        destination_id=setup_investor.bank_accounts[1].id,
        destination_type="INVESTOR_BANK_ACC",
        amount=-1000000,
        transaction_type="WITHDRAW",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_adjustment(
    setup_flask_app, setup_investor, setup_investor_wallet, setup_escrow_wallet
):
    """
        test disburse flow from escrow to modanaku va
    """

    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR_RDL_ACC",
        destination_id=setup_investor.id,
        destination_type="INVESTOR",
        amount=1000000,
        transaction_type="CREDIT_ADJUSTMENT",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()

    transaction = Transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR_RDL_ACC",
        destination_id=setup_investor.id,
        destination_type="INVESTOR",
        amount=-1000000,
        transaction_type="DEBIT_ADJUSTMENT",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()

    # use this to correct a transaction !
    transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_escrow_wallet.id,
        destination_type="ESCROW",
        amount=-1000000,
        transaction_type="DEBIT_ADJUSTMENT",
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)

    transaction.payment = payment
    transaction.commit()


def test_investment_to_escrow_bulk(
    setup_flask_app, setup_escrow_wallet, setup_profit_wallet
):
    """
        test invest flow from rdl to investment va
    """

    child_trx = ChildTransactionEmbed(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=-1000,
        transaction_type="UPFRONT_FEE",
    )

    child_trx2 = ChildTransactionEmbed(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=-1000,
        transaction_type="UPFRONT_FEE",
    )
    transactions = []
    transactions.append(child_trx)
    transactions.append(child_trx2)

    parent_transaction = Transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=-2000,
        transaction_type="UPFRONT_FEE",
        transactions=transactions
    )

    payment = PaymentEmbed()
    payment.generate_payment_info(parent_transaction)

    parent_transaction.payment = payment
    parent_transaction.commit()

    assert len(parent_transaction.transactions) == 2
