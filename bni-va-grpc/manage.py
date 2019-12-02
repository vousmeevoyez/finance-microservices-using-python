import os

from rpc.server import start
from rpc import create_app

if __name__ == "__main__":
    app = create_app(os.environ.get("ENVIRONMENT") or "test")
    app.app_context().push()
    start(
        os.environ.get("GRPC_HOST", "0.0.0.0"),
        os.environ.get("GRPC_PORT", "5001")
    )
