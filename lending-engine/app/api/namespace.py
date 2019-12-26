"""
    Flask Restplus Namespace
"""
from flask_restplus import Namespace


class InvestorNamespace:
    api = Namespace("investor")


class CallbackNamespace:
    api = Namespace("callback")


class InvestmentNamespace:
    api = Namespace("investment")


class ReportNamespace:
    api = Namespace("report")
