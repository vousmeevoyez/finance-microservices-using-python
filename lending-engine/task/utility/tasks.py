import json
import random
import base64
import grpc
from bson import ObjectId

from flask import current_app
from google.protobuf.json_format import Parse
from celery.exceptions import (
    MaxRetriesExceededError
)

from task.tasks import BaseTask

from app.api import (
    celery
)


from app.config.worker import WORKER, RPC
from app.api.lib.utils import backoff
# RPC
from task.utility.rpc.email import (
    email_pb2_grpc,
    email_pb2
)
from task.utility.rpc.mobile import (
    mobile_pb2_grpc,
    mobile_pb2
)


def encode_content(payload):
    encoded_payload = json.dumps(payload).encode("utf-8")
    data = base64.b64encode(encoded_payload).decode("utf-8")
    return data


class UtilityTask(BaseTask):
    """Abstract base class for all tasks in my app."""

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def send_email(self, recipient, product_type="MOPINJAM",
                   email_type="INVESTOR_APPROVE", content=None):
        """ background task to create investor approval email """
        # send email via gRPC
        request = email_pb2.SendEmailRequest()
        request.recipient = recipient
        request.product_type = product_type
        request.email_type = email_type
        if content is not None:
            request.content = encode_content(content)

        try:
            channel = grpc.insecure_channel(RPC["NOTIFICATION"])
            stub = email_pb2_grpc.EmailNotificationStub(channel)
            stub.SendEmail(request)
        except grpc.RpcError:
            self.retry(countdown=backoff(self.request.retries))
        return True

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def send_push_notif(self, device_token, product_type="MOPINJAM",
                        notif_type="INVESTOR_APPROVE", content=None):
        """ background task to send push notification """
        # send email via gRPC
        request = mobile_pb2.SendPushNotificationRequest()
        request.device_token = device_token
        request.product_type = product_type
        request.notif_type = notif_type
        if content is not None:
            request.content = encode_content(content)

        try:
            channel = grpc.insecure_channel(RPC["NOTIFICATION"])
            stub = mobile_pb2_grpc.MobileNotificationStub(channel)
            stub.SendPushNotification(request)
        except grpc.RpcError:
            self.retry(countdown=backoff(self.request.retries))
        return True
