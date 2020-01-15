import pytest
from bson import ObjectId
import random

from app.api.lib.helper import encrypt
from app.config.external.bank import (
    BNI_ECOLLECTION,
    BNI_RDL
)

from tests.api_list import (
    va_deposit_callback,
    rdl_deposit_callback,
    internal_callback
)
from app.api.models.batch import Schedule, TransactionQueue
from app.api.models.investment import Investment
from app.api.models.loan_request import LoanRequest


def test_callback_repayment(setup_client,
                            setup_investment_with_loan):
    """ Callback Virtual Account """
    investment, loan_request = setup_investment_with_loan
    trx_id = str(random.randint(111111111, 9999999999))

    data = {
        "virtual_account": loan_request.bank_accounts[0].account_no,
        "customer_name": "jennie",
        "trx_id": trx_id,
        "trx_amount": "0",
        "payment_amount": "500000",
        "cumulative_payment_amount": "500000",
        "payment_ntb": "12345",
        "datetime_payment": "2018-12-20 11:16:00",
    }
    # generate encrypted data using BNI encryption
    encrypted_data = encrypt(
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        BNI_ECOLLECTION["CREDIT_SECRET_KEY"],
        data
    )

    fake_callback_request = {
        "client_id": BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        "data": encrypted_data
    }
    result = va_deposit_callback(setup_client, fake_callback_request)
    response = result.get_json()
    assert response["status"] == "000"


def test_callback_deposit_va(setup_client,
                             setup_investment_with_loan):
    """ Callback Virtual Account """
    investment, loan_request = setup_investment_with_loan
    trx_id = str(random.randint(111111111, 9999999999))

    data = {
        "virtual_account": investment.bank_accounts[0].account_no,
        "customer_name": "jennie",
        "trx_id": trx_id,
        "trx_amount": "0",
        "payment_amount": "50000",
        "cumulative_payment_amount": "50000",
        "payment_ntb": "12345",
        "datetime_payment": "2018-12-20 11:16:00",
    }
    # generate encrypted data using BNI encryption
    encrypted_data = encrypt(
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        BNI_ECOLLECTION["CREDIT_SECRET_KEY"],
        data
    )

    fake_callback_request = {
        "client_id": BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        "data": encrypted_data
    }
    result = va_deposit_callback(setup_client, fake_callback_request)
    response = result.get_json()
    assert response["status"] == "000"


def test_callback_deposit_va_not_found(setup_client,
                                       setup_investment_with_loan):
    """ Callback Virtual Account """
    trx_id = str(random.randint(111111111, 9999999999))

    data = {
        "virtual_account": "9889909611123000",
        "customer_name": "jennie",
        "trx_id": trx_id,
        "trx_amount": "0",
        "payment_amount": "50000",
        "cumulative_payment_amount": "50000",
        "payment_ntb": "12345",
        "datetime_payment": "2018-12-20 11:16:00",
    }
    # generate encrypted data using BNI encryption
    encrypted_data = encrypt(
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        BNI_ECOLLECTION["CREDIT_SECRET_KEY"],
        data
    )

    fake_callback_request = {
        "client_id": BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        "data": encrypted_data
    }
    result = va_deposit_callback(setup_client, fake_callback_request)
    assert result.status_code == 404


def test_callback_deposit_invalid_va(setup_client,
                                     setup_investment_with_loan):
    """ Callback Virtual Account """
    trx_id = str(random.randint(111111111, 9999999999))

    data = {
        "virtual_account": "9889909600023000",
        "customer_name": "jennie",
        "trx_id": trx_id,
        "trx_amount": "0",
        "payment_amount": "50000",
        "cumulative_payment_amount": "50000",
        "payment_ntb": "12345",
        "datetime_payment": "2018-12-20 11:16:00",
    }
    # generate encrypted data using BNI encryption
    encrypted_data = encrypt(
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        BNI_ECOLLECTION["CREDIT_SECRET_KEY"],
        data
    )

    fake_callback_request = {
        "client_id": BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        "data": encrypted_data
    }
    result = va_deposit_callback(setup_client, fake_callback_request)
    assert result.status_code == 400


def test_callback_deposit_rdl(setup_client,
                              setup_investor, setup_investor_wallet):
    """ Callback Virtual Account """
    data = {
        "p2p_id": BNI_RDL["COMPANY"],
        "account_number": setup_investor.bank_accounts[0].account_no,
        "payment_amount": "50000.000",
        "accounting_flag": "C",
        "journal_number": "123456789",
        "datetime_payment": "2018-12-20 11:16:00",
    }
    # generate encrypted data using BNI encryption
    encrypted_data = encrypt(
        BNI_RDL["COMPANY"],
        BNI_RDL["CALLBACK_SECRET_KEY"],
        data
    )

    fake_callback_request = {
        "p2p_id": BNI_RDL["COMPANY"],
        "data": encrypted_data
    }
    result = rdl_deposit_callback(setup_client, fake_callback_request)
    response = result.get_json()
    assert response["status"] == "000"


def test_internal_callback(setup_client, setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction
    """ test internal callback update """
    data = {
        "transaction_id": str(transactions[0].id),
        "transaction_type": transactions[0].transaction_type,
        "status": "SUCCESS",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 200
    assert response["status"] == "SEND_TO_INVESTMENT_SUCCESS"


def test_internal_callback_receive_upfront(
    setup_client,
    setup_investment_with_transaction
):
    """ test internal callback for indicating upfront received """
    investment, loan_request, transactions = setup_investment_with_transaction

    receive_upfront_trx = transactions[2]

    data = {
        "transaction_id": str(receive_upfront_trx.id),
        "transaction_type": receive_upfront_trx.transaction_type,
        "status": "SUCCESS",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 200
    assert response["status"] == "RECEIVE_FROM_ESCROW_SUCCESS"


def test_internal_callback_not_found(
    setup_client
):
    """ test internal callback update when trx is not found """
    fake_trx_id = str(ObjectId())
    data = {
        "transaction_id": fake_trx_id,
        "transaction_type": "INVEST",
        "status": "SUCCESS",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 404
    assert response["error"]


def test_internal_callback_upfront_fee(
    setup_client,
    setup_investment_with_transaction
):
    """ test internal callback for indicating succesfully send upfront fee  """
    investment, loan_request, transactions = setup_investment_with_transaction
    # append transaction into batch to simulate the batch already exexuted
    upfront_fee_trx = transactions[1]

    data = {
        "transaction_id": str(upfront_fee_trx.id),
        "transaction_type": "UPFRONT_FEE",
        "status": "COMPLETED",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 200
    assert response["status"] == "SEND_TO_PROFIT_COMPLETED"

    investment = Investment.find_one({"id": investment.id})
    assert any("SEND_TO_PROFIT_COMPLETED" in iv.status for iv in investment.list_of_status)


def test_internal_callback_disburse(setup_client,
                                    setup_investment_with_transaction):
    """ test internal callback for indiciating disburse success """
    investment, loan_request, transactions = setup_investment_with_transaction

    data = {
        "transaction_id": str(transactions[3].id),
        "transaction_type": transactions[3].transaction_type,
        "status": "COMPLETED",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 200
    assert response["status"] == "SEND_TO_MODANAKU_COMPLETED"

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert any("SEND_TO_MODANAKU_COMPLETED" in lr.status for lr in loan_request.list_of_status)
    assert loan_request.status == "DISBURSED"

def test_internal_callback_invest_fee(
        setup_client,
        setup_investment_with_transaction
):
    """ test internal callback after we successfully send escrow investor
    profit to escrow"""
    investment, loan_request, transactions = setup_investment_with_transaction

    invest_fee_trx = transactions[4]

    data = {
        "transaction_id": str(invest_fee_trx.id),
        "transaction_type": invest_fee_trx.transaction_type,
        "status": "COMPLETED",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 200
    assert response["status"] == "SEND_FEE_TO_ESCROW_COMPLETED"

    loan_request = LoanRequest.find_one(
        {"id": loan_request.id}
    )
    assert any("SEND_FEE_TO_ESCROW_COMPLETED" in lr.status for lr in loan_request.list_of_status)


def test_internal_callback_receive_invest_fee(
        setup_client,
        setup_investment_with_transaction
):
    """ test internal callback after we successfully send escrow investor
    profit to escrow"""
    investment, loan_request, transactions = setup_investment_with_transaction

    data = {
        "transaction_id": str(transactions[5].id),
        "transaction_type": transactions[5].transaction_type,
        "status": "COMPLETED",
    }
    result = internal_callback(setup_client, data)
    response = result.get_json()
    assert result.status_code == 200
    assert response["status"] == "RECEIVE_FEE_FROM_PROFIT_COMPLETED"

    loan_request = LoanRequest.find_one(
        {"id": loan_request.id}
    )
    assert any("RECEIVE_FEE_FROM_PROFIT_COMPLETED" in lr.status for lr in loan_request.list_of_status)
