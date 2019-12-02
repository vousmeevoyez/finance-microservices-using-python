from firebase_admin import credentials, messaging, initialize_app


def push_notification(token, title, message):
    app = initialize_app()

    ntf_data = {"title": title, "message": message}

    # apns
    alert = messaging.ApsAlert(title=title, body=message)
    aps = messaging.Aps(alert=alert, sound="default")
    payload = messaging.APNSPayload(aps)

    # message
    msg = messaging.Message(
        data=ntf_data,
        token=token,
        apns=messaging.APNSConfig(payload=payload)
    )
    # send
    res = messaging.send(msg)
    return res


token = "fDrKNYt0JTU:APA91bEtTgIBR1jTgK0ZBeYujPe50uCOHS0V0oFxxG6Fbf3yoN4wgto08pDax8JrPUg05XJf4jexlimue-zBgfZl62_pUpPtxB4QOq63nONPisc4XO2NRyieAXOKk_8foHpUYhW2FAay"
result = push_notification(
    token,
    "Lorem Ipsum is simply dummy text of the printing and typesetting\
    Lorem Ipsum has been the industry's standard dummy text ever since the \
    1500s, when an unknown printer took a galley of type and scrambled it to \
    make a type specimen book. It has survived not only five centuries, but \
    also the leap into electronic typesetting, remaining essentially .\
    It was popularised in the 1960s with the release of Letraset sheets \
    containing Lorem Ipsum passages, and more recently with desktop publishin\
    software like Aldus PageMaker including versions of Lorem Ips",
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ips"
)
print(result)
