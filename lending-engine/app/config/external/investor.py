import os

INVESTOR_BE = {
    "BASE_URL": os.environ.get("INVESTOR_BASE_URL") or "http://localhost:8000/",
    "ENDPOINTS": {
        "REFRESH_TOKEN": "api/v1/sio/refresh_token",
    },
    "SOCKETIO_KEY": os.environ.get("SOCKETIO_KEY") or "SOCKETIO_KEY",
}
