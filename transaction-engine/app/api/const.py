"""
    Constant used in lending engine
"""
import os


RESPONSE = {
    "INVALID_PARAMETER": {"TITLE": "INVALID_PARAMETER", "MESSAGE": "Invalid Parameter"},
    "INSUFFICIENT_BALANCE": {"TITLE": "INSUFFICIENT_BALANCE", "MESSAGE":
                             "Insufficient Balance"},
}


# this list of value used if this used as type we know which bank
# account to pick
TYPE_TO_BANK_TYPES = {
    "INVESTOR": "RDL_ACCOUNT",
    "INVESTOR_RDL_ACC": "RDL_ACCOUNT",
    "INVESTOR_BANK_ACC": "BANK_ACCOUNT",
    "INVESTMENT": "VIRTUAL_ACCOUNT",
    "MODANAKU": {"ACCOUNT_TYPE": "VIRTUAL_ACCOUNT", "LABEL": "MODANAKU"},
    "REPAYMENT": {"ACCOUNT_TYPE": "VIRTUAL_ACCOUNT", "LABEL": "REPAYMENT"},
    "ESCROW": "BANK_ACCOUNT",
    "PROFIT": "BANK_ACCOUNT",
}

# this list of value used if this used as type we know which model to use
TYPE_TO_MODELS = {
    "INVESTOR": "Investor",
    "INVESTMENT": "Investment",
    "INVESTOR_BANK_ACC": "Investor",
    "INVESTOR_RDL_ACC": "Investor",
    "ESCROW": "Wallet",
    "PROFIT": "Wallet",
    "MODANAKU": "LoanRequest",
    "REPAYMENT": "LoanRequest",
}

# using this variable we can decide what type of provider we select based on
# source
PROVIDER_ROUTES = {
    "RDL_ACCOUNT": "BNI_RDL",
    "BANK_ACCOUNT": "BNI_OPG",
    "VIRTUAL_ACCOUNT": "BNI_OPG",
}
# using this variable we can put conditional based on active or passive
# transaction
TRANSFER_TYPES = {
    "ACTIVE": [
        "INVEST",
        "DISBURSE",
        "UPFRONT_FEE",
        "INVEST_FEE",
        "INVEST_REPAYMENT",
        "WITHDRAW",
    ],
    "INTERNAL": ["DEBIT_REFUND", "CREDIT_REFUND", "DEBIT_ADJUSTMENT",
                 "CREDIT_ADJUSTMENT"],
    # this is all potential transaction that receive notification from BNI
    "PASSIVE": [
        "RECEIVE_INVEST", "RECEIVE_REPAYMENT", "TOP_UP_RDL"
    ],
    # because we dont receive any notif from BNI but we still need notification
    # we add new flag called custom passive
    "CUSTOM_PASSIVE": [
        "RECEIVE_INVEST_FEE", "RECEIVE_UPFRONT_FEE"
    ]
}

WORKER = {
    "MAX_RETRIES": os.getenv("WORKER_MAX_RETRY") or 5,
    "HARD_LIMIT": 15,
    "SOFT_LIMIT": 10,
    "ACKS_LATE": True,  # prevent executing task twice
}
