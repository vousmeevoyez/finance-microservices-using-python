from rpc.models import VirtualAccount


def test_create_va(setup_flask_app):
    va = VirtualAccount(name="testing virtual account")
    trx_id = va.generate_trx_id()
    account_no = va.generate_va_number()
    va.save()

    va = VirtualAccount.objects.get(account_no=account_no)
    assert va.account_no
    assert va.name == "testing virtual account"
    assert va.trx_id
    assert va.expired_at


def test_custom_prefix_va(setup_flask_app):
    va = VirtualAccount(name="testing virtual account", va_type="REPAYMENT")
    trx_id = va.generate_trx_id()
    account_no = va.generate_va_number()
    va.save()

    va = VirtualAccount.objects.get(account_no=account_no)
    assert va.account_no[8:10] == "11"
    assert va.name == "testing virtual account"
    assert va.trx_id
    assert va.expired_at

    va = VirtualAccount(name="testing virtual account", va_type="INVESTMENT")
    trx_id = va.generate_trx_id()
    account_no = va.generate_va_number()
    va.save()

    va = VirtualAccount.objects.get(account_no=account_no)
    assert va.account_no[8:10] == "12"
    assert va.name == "testing virtual account"
    assert va.trx_id
    assert va.expired_at
