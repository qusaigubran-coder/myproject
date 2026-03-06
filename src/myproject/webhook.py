import hashlib
import hmac
import json
from typing import Any

from fastapi import Header, HTTPException, Request

from myproject.config import WEBHOOK_SECRET


def verify_signature(payload: bytes, signature: str | None) -> bool:
    if not signature:
        return False

    expected = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


async def handle_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
) -> dict[str, Any]:
    payload = await request.body()

    if not verify_signature(payload, x_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = json.loads(payload.decode("utf-8"))

    event_type = data.get("event")
    event_id = data.get("id")

    if not event_type or not event_id:
        raise HTTPException(status_code=400, detail="Missing required fields")

    # هنا منطق المعالجة الفعلي
    # مثال: حفظ الحدث، إرسال إشعار، تحديث قاعدة بيانات

    return {
        "status": "accepted",
        "event_id": event_id,
        "event_type": event_type,
    }
