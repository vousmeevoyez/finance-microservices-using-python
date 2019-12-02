"""
    Flask Restplus Namespace
"""
from flask_restplus import Namespace


class TransactionNamespace:
    api = Namespace("transactions")


class InvestorNamespace:
    api = Namespace("investor")


class InvestmentNamespace:
    api = Namespace("investment")
