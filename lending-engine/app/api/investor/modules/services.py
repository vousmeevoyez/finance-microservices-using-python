from bson import ObjectId

from celery import chain
from celery.exceptions import TimeoutError

from app.api.models.investor import Investor
from app.api.models.wallet import Wallet

from task.investor.tasks import InvestorTask
from task.utility.tasks import UtilityTask
from task.transaction.tasks import TransactionTask


def approve_investor(investor_id):
    result = InvestorTask().create_rdl.apply_async(args=[investor_id], queue="investor")
    return {"id": result.id}, 202


def withdraw(investor_id, destination_id, amount):
    investor = Investor.find_one({"id": ObjectId(investor_id)})
    investor_wallet = Wallet.find_one({"user_id": investor.user_id})

    withdraw_payload = {
        "wallet_id": str(investor_wallet.id),
        "source_id": investor_id,
        "source_type": "INVESTOR_RDL_ACC",
        "destination_id": destination_id,
        "destination_type": "INVESTOR_BANK_ACC",
        "amount": -amount,
        "transaction_type": "WITHDRAW",
    }

    result = TransactionTask().send_transaction.apply_async(
        kwargs=withdraw_payload, queue="transaction"
    )
    return {"id": result.id}, 202


def sync_balance(investor_id):
    """
        sync RDL balance internal and BNI Rdl
    """
    result = InvestorTask().sync_rdl.apply_async(args=[investor_id], queue="investor")

    # if differences more than zero
    # it means we have less than we suppose so we need to add balance
    # if differences less than zero
    # it means we have more than we suppose so we need to deduct balance
    try:
        payload = result.get(timeout=15)
    except TimeoutError:
        return {"error": "TIMEOUT"}, 422

    if payload is not None:
        result = TransactionTask().send_transaction.apply_async(
            kwargs=payload, queue="transaction"
        )

    return {"message": "synced"}
