from bson import ObjectId
from app.api.models.transaction import Transaction
from tests.api_list import create_transaction


def test_api_top_up(setup_client, setup_investor, setup_investor_wallet):
    payload = {
        "wallet_id": str(setup_investor_wallet.id),
        "source_id": str(setup_investor.id),
        "source_type": "INVESTOR_RDL_ACC",
        "destination_id": str(setup_investor.id),
        "destination_type": "INVESTOR",
        "amount": 1000000,
        "transaction_type": "TOP_UP_RDL",
        "reference_no": "00712312312"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == 1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "TOP_UP_RDL"
    # make sure the actual payment is correct!
    assert transaction.payment.reference_no == "00712312312"
    assert transaction.payment.payment_type == "CREDIT"
    assert transaction.payment.provider == "BNI_RDL"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "COMPLETED"
    assert transaction.payment.method == "DEPOSIT_CALLBACK"
    assert transaction.payment.source == "01231231312"
    assert transaction.payment.destination == "01231231312"


def test_api_invest(setup_client, setup_investor, setup_investor_wallet,
                    setup_investment):
    payload = {
        "wallet_id": str(setup_investor_wallet.id),
        "source_id": str(setup_investor.id),
        "source_type": "INVESTOR",
        "destination_id": str(setup_investment.id),
        "destination_type": "INVESTMENT",
        "amount": -1000000,
        "transaction_type": "INVEST"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "INVEST"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.reference_no is None
    assert transaction.payment.provider == "BNI_RDL"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "01231231312"
    assert transaction.payment.destination == "01231231312123123"


def test_api_callback_investment(setup_client, setup_investor,
                                 setup_investor_wallet, setup_investment,
                                 setup_escrow_wallet):
    payload = {
        "wallet_id": str(setup_escrow_wallet.id),
        "source_id": str(setup_investor.id),
        "source_type": "INVESTOR",
        "destination_id": str(setup_investment.id),
        "destination_type": "INVESTMENT",
        "amount": 1000000,
        "transaction_type": "RECEIVE_INVEST",
        "reference_no": "12312312312"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == 1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "RECEIVE_INVEST"
    # make sure the actual payment is correct!
    assert transaction.payment.reference_no == "12312312312"
    assert transaction.payment.payment_type == "CREDIT"
    assert transaction.payment.provider == "BNI_VA"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "COMPLETED"
    assert transaction.payment.method == "DEPOSIT_CALLBACK"
    assert transaction.payment.source == "01231231312"
    assert transaction.payment.destination == "01231231312123123"


def test_api_send_upfront_fee(setup_client, setup_escrow_wallet,
                              setup_profit_wallet):
    payload = {
        "wallet_id": str(setup_escrow_wallet.id),
        "source_id": str(setup_escrow_wallet.id),
        "source_type": "ESCROW",
        "destination_id": str(setup_profit_wallet.id),
        "destination_type": "PROFIT",
        "amount": -1000000,
        "transaction_type": "UPFRONT_FEE"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "UPFRONT_FEE"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.reference_no is None
    assert transaction.payment.provider == "BNI_OPG"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "111222334"
    assert transaction.payment.destination == "000022334555"


def test_api_receive_upfront_fee(setup_client, setup_escrow_wallet,
                                 setup_profit_wallet):
    payload = {
        "wallet_id": str(setup_profit_wallet.id),
        "source_id": str(setup_escrow_wallet.id),
        "source_type": "ESCROW",
        "destination_id": str(setup_profit_wallet.id),
        "destination_type": "PROFIT",
        "amount": 1000000,
        "transaction_type": "RECEIVE_UPFRONT_FEE"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == 1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "RECEIVE_UPFRONT_FEE"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "CREDIT"
    assert transaction.payment.reference_no is None
    assert transaction.payment.provider == "BNI_OPG"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "111222334"
    assert transaction.payment.destination == "000022334555"


def test_api_disburse_modanaku(setup_client, setup_escrow_wallet,
                               setup_loan_request):
    payload = {
        "wallet_id": str(setup_escrow_wallet.id),
        "source_id": str(setup_escrow_wallet.id),
        "source_type": "ESCROW",
        "destination_id": str(setup_loan_request.id),
        "destination_type": "MODANAKU",
        "amount": -1000000,
        "transaction_type": "DISBURSE"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "DISBURSE"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.reference_no is None
    assert transaction.payment.provider == "BNI_OPG"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "111222334"
    assert transaction.payment.destination == "9888888128381123"


def test_api_callback_repayment(setup_client, setup_escrow_wallet,
                                setup_loan_request):
    payload = {
        "wallet_id": str(setup_escrow_wallet.id),
        "source_id": str(setup_loan_request.id),
        "source_type": "MODANAKU",
        "destination_id": str(setup_loan_request.id),
        "destination_type": "REPAYMENT",
        "amount": 1000000,
        "transaction_type": "RECEIVE_REPAYMENT",
        "reference_no": "00000000000000"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == 1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "RECEIVE_REPAYMENT"
    # make sure the actual payment is correct!
    assert transaction.payment.reference_no == "00000000000000"
    assert transaction.payment.payment_type == "CREDIT"
    assert transaction.payment.provider == "BNI_VA"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "COMPLETED"
    assert transaction.payment.method == "DEPOSIT_CALLBACK"
    assert transaction.payment.source == "9888888128381123"
    assert transaction.payment.destination == "9888888128000000"


def test_api_send_invest_fee(setup_client, setup_escrow_wallet,
                             setup_profit_wallet):
    payload = {
        "wallet_id": str(setup_profit_wallet.id),
        "source_id": str(setup_profit_wallet.id),
        "source_type": "PROFIT",
        "destination_id": str(setup_escrow_wallet.id),
        "destination_type": "ESCROW",
        "amount": -1000000,
        "transaction_type": "INVEST_FEE"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "INVEST_FEE"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.provider == "BNI_OPG"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "000022334555"
    assert transaction.payment.destination == "111222334"


def test_api_receive_invest_fee(
    setup_client, setup_escrow_wallet,
    setup_profit_wallet
):
    payload = {
        "wallet_id": str(setup_escrow_wallet.id),
        "source_id": str(setup_profit_wallet.id),
        "source_type": "PROFIT",
        "destination_id": str(setup_escrow_wallet.id),
        "destination_type": "ESCROW",
        "amount": 1000000,
        "transaction_type": "RECEIVE_INVEST_FEE",
        "reference_no": "123123333"
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == 1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "RECEIVE_INVEST_FEE"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "CREDIT"
    assert transaction.payment.provider == "BNI_OPG"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "000022334555"
    assert transaction.payment.destination == "111222334"


def test_api_invest_repayment(
    setup_client, setup_escrow_wallet,
    setup_investor
):
    payload = {
        "wallet_id": str(setup_escrow_wallet.id),
        "source_id": str(setup_escrow_wallet.id),
        "source_type": "ESCROW",
        "destination_id": str(setup_investor.id),
        "destination_type": "INVESTOR_RDL_ACC",
        "amount": -1000000,
        "transaction_type": "INVEST_REPAYMENT",
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "INVEST_REPAYMENT"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.provider == "BNI_OPG"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "111222334"
    assert transaction.payment.destination == "01231231312"


def test_api_investor_bni_withdraw(
    setup_client, setup_investor_wallet,
    setup_investor
):
    payload = {
        "wallet_id": str(setup_investor_wallet.id),
        "source_id": str(setup_investor.id),
        "source_type": "INVESTOR_RDL_ACC",
        "destination_id": str(setup_investor.bank_accounts[1].id),
        "destination_type": "INVESTOR_BANK_ACC",
        "amount": -1000000,
        "transaction_type": "WITHDRAW",
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "WITHDRAW"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.provider == "BNI_RDL"
    assert transaction.payment.bank_code == "009"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INHOUSE_TRANSFER"
    assert transaction.payment.source == "01231231312"
    assert transaction.payment.destination == "001122330011"


def test_api_investor_bca_withdraw(
    setup_client, setup_investor_wallet,
    setup_investor
):
    payload = {
        "wallet_id": str(setup_investor_wallet.id),
        "source_id": str(setup_investor.id),
        "source_type": "INVESTOR_RDL_ACC",
        "destination_id": str(setup_investor.bank_accounts[2].id),
        "destination_type": "INVESTOR_BANK_ACC",
        "amount": -1000000,
        "transaction_type": "WITHDRAW",
    }
    result = create_transaction(setup_client, payload)
    response = result.get_json()
    assert response["id"]
    # make sure the inserted transaction correct!
    transaction = Transaction.find_one({"_id": ObjectId(response["id"])})
    assert transaction.amount == -1000000
    assert transaction.status == "PENDING"
    assert transaction.transaction_type == "WITHDRAW"
    # make sure the actual payment is correct!
    assert transaction.payment.payment_type == "DEBIT"
    assert transaction.payment.provider == "BNI_RDL"
    assert transaction.payment.bank_code == "014"
    assert transaction.payment.status == "PENDING"
    assert transaction.payment.method == "INTERBANK_TRANSFER"
    assert transaction.payment.source == "01231231312"
    assert transaction.payment.destination == "009922113300"
