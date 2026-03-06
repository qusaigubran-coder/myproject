import hashlib
import hmac
import json
import logging
from typing import Any

from fastapi import Header, HTTPException, Request, status

from myproject.config import get_settings
from myproject.idempotency import register_event

logger = logging.getLogger(__name__)


def verify_signature(payload: bytes, signature: str | None) -> bool:
    if not signature:
        return False

    secret = get_settings().webhook_secret.encode("utf-8")
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()

    return hmac.compare_digest(expected, signature)


async def handle_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
) -> dict[str, Any]:
    payload = await request.body()

    if not verify_signature(payload, x_signature):
        logger.warning("Webhook rejected: invalid_signature")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature",
        )

    try:
        data = json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError as exc:
        logger.warning("Webhook rejected: invalid_json")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON",
        ) from exc

    event_id = data.get("id")
    event_type = data.get("event")

    if not event_id or not event_type:
        logger.warning("Webhook rejected: missing_fields")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields",
        )

    if not register_event(str(event_id)):
        logger.info(
            "Webhook duplicate ignored: event_id=%s event_type=%s",
            event_id,
            event_type,
        )
        return {
            "status": "duplicate",
            "event_id": event_id,
            "event_type": event_type,
        }

    logger.info(
        "Webhook accepted: event_id=%s event_type=%s",
        event_id,
        event_type,
    )
    return {
        "status": "accepted",
        "event_id": event_id,
        "event_type": event_type,
    }
