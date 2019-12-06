from app.api.transactions.factories.helper import process_transaction
from app.api.models.transaction import Transaction


def test_process_top_up_transaction(
    setup_flask_app, setup_investor, setup_investor_wallet
):

    transaction_id = process_transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR_RDL_ACC",
        destination_id=setup_investor.id,
        destination_type="INVESTOR",
        amount=1000000,
        transaction_type="TOP_UP_RDL",
    )

    # make sure transaction propertly created with pending status
    result = Transaction.find_one({"_id": transaction_id})
    assert result.status == "PENDING"
    assert result.payment.method == "DEPOSIT_CALLBACK"
    assert result.payment.payment_type == "CREDIT"
    assert result.payment.provider == "BNI_RDL"
    assert result.payment.bank_code == "009"
    assert result.payment.source == "01231231312"
    assert result.payment.destination == "01231231312"


def test_process_rdl_to_investment_va(
    setup_flask_app,
    setup_investor,
    setup_investor_wallet,
    setup_investment,
    setup_escrow_wallet,
):

    investor_transaction_id = process_transaction(
        wallet_id=setup_investor_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR",
        destination_id=setup_investment.id,
        destination_type="INVESTMENT",
        amount=-1000000,
        transaction_type="INVEST",
    )

    # make sure transaction propertly created with pending status
    result = Transaction.find_one({"_id": investor_transaction_id})
    assert result.status == "PENDING"
    assert result.amount == -1000000
    assert result.payment.method == "INHOUSE_TRANSFER"
    assert result.payment.payment_type == "DEBIT"
    assert result.payment.provider == "BNI_RDL"
    assert result.payment.bank_code == "009"
    assert result.payment.source == "01231231312"  # RDL ACCOUNT
    assert result.payment.destination == "9889909612123123"  # INVESTMENT VA

    # should be triggered via callback
    escrow_trx_id = process_transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_investor.id,
        source_type="INVESTOR",
        destination_id=setup_investment.id,
        destination_type="INVESTMENT",
        amount=1000000,
        transaction_type="RECEIVE_INVEST",
    )

    # make sure transaction propertly created with pending status
    result = Transaction.find_one({"_id": escrow_trx_id})
    assert result.status == "PENDING"
    assert result.amount == 1000000
    assert result.payment.method == "DEPOSIT_CALLBACK"
    assert result.payment.payment_type == "CREDIT"
    assert result.payment.bank_code == "009"
    assert result.payment.provider == "BNI_VA"
    assert result.payment.source == "01231231312"  # FROM RDL ACCOUNT
    assert result.payment.destination == "9889909612123123"  # INVESTMENT VA


def test_process_investment_to_profit(
    setup_flask_app, setup_escrow_wallet, setup_profit_wallet
):

    escrow_trx_id = process_transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=-1000000,
        transaction_type="UPFRONT_FEE",
    )

    # make sure transaction propertly created with pending status
    result = Transaction.find_one({"_id": escrow_trx_id})
    assert result.status == "PENDING"
    assert result.amount == -1000000
    assert result.payment.method == "INHOUSE_TRANSFER"
    assert result.payment.payment_type == "DEBIT"
    assert result.payment.provider == "BNI_OPG"
    assert result.payment.bank_code == "009"
    assert result.payment.source == "111222334"  # ESCROW MASTER ACCOUNT
    assert result.payment.destination == "000022334555"  # PROFIT MASTER

    # should be triggered when the previous transaction success
    profit_trx_id = process_transaction(
        wallet_id=setup_profit_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=setup_profit_wallet.id,
        destination_type="PROFIT",
        amount=1000000,
        transaction_type="RECEIVE_UPFRONT_FEE",
    )

    # make sure transaction propertly created with pending status
    result = Transaction.find_one({"_id": profit_trx_id})
    assert result.status == "PENDING"
    assert result.amount == 1000000
    assert result.payment.method == "INHOUSE_TRANSFER"
    assert result.payment.payment_type == "CREDIT"
    assert result.payment.provider == "BNI_OPG"
    assert result.payment.bank_code == "009"
    assert result.payment.source == "111222334"  # FROM ESCROW MASTER ACCOUNT
    assert result.payment.destination == "000022334555"  # PROFI MASTER


def test_process_escrow_to_modanaku(
    setup_flask_app, setup_escrow_wallet, setup_investment_with_loan
):
    investment, loan_request = setup_investment_with_loan

    escrow_trx_id = process_transaction(
        wallet_id=setup_escrow_wallet.id,
        source_id=setup_escrow_wallet.id,
        source_type="ESCROW",
        destination_id=loan_request.id,
        destination_type="MODANAKU",
        amount=-1000000,
        transaction_type="DISBURSE",
    )

    # make sure transaction propertly created with pending status
    result = Transaction.find_one({"_id": escrow_trx_id})
    assert result.status == "PENDING"
    assert result.amount == -1000000
    assert result.payment.method == "INHOUSE_TRANSFER"
    assert result.payment.payment_type == "DEBIT"
    assert result.payment.provider == "BNI_OPG"
    assert result.payment.bank_code == "009"
    assert result.payment.source == "111222334"  # ESCROW MASTER ACCOUNT
    assert result.payment.destination == "9889909600023123"  # PROFIT MASTER
