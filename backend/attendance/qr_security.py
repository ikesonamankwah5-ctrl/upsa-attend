from django.core import signing
from django.utils import timezone


QR_VALIDITY_SECONDS = 60

QR_SALT = "upsa-attend-rotating-qr-v1"


def generate_qr_token(session_id):

    current_time = int(timezone.now().timestamp())

    time_slot = current_time // QR_VALIDITY_SECONDS

    payload = {
        "session_id": session_id,
        "time_slot": time_slot,
    }

    return signing.dumps(
        payload,
        salt=QR_SALT
    )


def verify_qr_token(token, session_id):

    try:
        payload = signing.loads(
            token,
            salt=QR_SALT,
            max_age=60
        )

    except signing.SignatureExpired:
        return False

    except signing.BadSignature:
        return False

    current_time = int(timezone.now().timestamp())

    current_slot = current_time // QR_VALIDITY_SECONDS

    return (
        payload.get("session_id") == session_id
        and payload.get("time_slot") == current_slot
    )