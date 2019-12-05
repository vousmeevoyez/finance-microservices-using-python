"""
    Manage
    ___________________
    This is flask application entry
"""
import os

from flask_script import Manager, Shell

from app import blueprint
from app.api import create_app
from app.api.models.wallet import Wallet
from app.api.models.bank import Bank
from app.config.external.bank import MASTER_ACCOUNT

from task.investment.tasks import InvestmentTask

app = create_app(os.getenv("ENVIRONMENT") or 'dev')
app.register_blueprint(blueprint, url_prefix="/api/v1")

app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    """ function to start flask apps"""
    host = os.getenv("HOST") or '127.0.0.1'
    app.run(host=host)


@manager.command
def init():
    """ create init function here """
    escrow_wallet = Wallet.find_one({"label": "ESCROW"})
    if escrow_wallet is None:
        bank_accounts = []
        # virtual account here
        bank_accounts.append(MASTER_ACCOUNT["ESCROW"])
        bank = Bank.find_one({"name": MASTER_ACCOUNT["ESCROW"]["bank_name"]})

        wallet = Wallet(bank_accounts=bank_accounts)
        wallet.label = "ESCROW"
        wallet.bank_id = bank.id
        wallet.commit()

    profit_wallet = Wallet.find_one({"label": "PROFIT"})
    if profit_wallet is None:
        bank_accounts = []
        bank_accounts.append(MASTER_ACCOUNT["PROFIT"])
        bank = Bank.find_one({"name": MASTER_ACCOUNT["ESCROW"]["bank_name"]})

        wallet = Wallet(bank_accounts=bank_accounts)
        wallet.label = "PROFIT"
        wallet.bank_id = bank.id
        wallet.commit()


if __name__ == "__main__":
    manager.run()
