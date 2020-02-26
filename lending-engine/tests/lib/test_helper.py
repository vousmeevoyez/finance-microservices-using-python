from app.api.lib.helper import send_notif

def test_send_notif(setup_borrower):
    email_notif, in_app_notif = send_notif(
        recipient=setup_borrower.email,
        user_id=setup_borrower.user_id,
        notif_type="REMINDER_BEFORE_DUEDATE",
        platform="mobile",
        custom_content={
            "loan_request_code": "123456"
        }
    )
    assert email_notif["recipient"]
    assert email_notif["product_type"]
    assert email_notif["email_type"]
    assert email_notif["content"]["loan_request_code"]

    assert in_app_notif["user_id"]
    assert in_app_notif["template"]["subject"]
    assert in_app_notif["template"]["message"].find("123456")
    assert in_app_notif["type_"]
    assert in_app_notif["platform"]

    email_notif, in_app_notif = send_notif(
        recipient=setup_borrower.email,
        user_id=setup_borrower.user_id,
        notif_type="REMINDER_AFTER_DUEDATE",
        platform="mobile",
        custom_content={
            "loan_request_code": "123456"
        }
    )

    assert email_notif["recipient"]
    assert email_notif["product_type"]
    assert email_notif["email_type"]
    assert email_notif["content"]["loan_request_code"]

    assert in_app_notif["user_id"]
    assert in_app_notif["template"]["subject"]
    assert in_app_notif["template"]["message"].find("123456")
    assert in_app_notif["type_"]
    assert in_app_notif["platform"]

    email_notif, in_app_notif = send_notif(
        recipient=setup_borrower.email,
        user_id=setup_borrower.user_id,
        notif_type="LOAN_REQUEST_CANCEL",
        platform="mobile",
        custom_content={
            "loan_request_code": "123456"
        }
    )

    assert email_notif["recipient"]
    assert email_notif["product_type"]
    assert email_notif["email_type"]
    assert email_notif["content"]["loan_request_code"]

    assert in_app_notif["user_id"]
    assert in_app_notif["template"]["subject"]
    assert in_app_notif["template"]["message"].find("123456")
    assert in_app_notif["type_"]
    assert in_app_notif["platform"]
