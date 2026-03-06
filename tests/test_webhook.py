import hashlib
import hmac

import pytest

from myproject.config import get_settings
from myproject.webhook import verify_signature


def sign(payload: bytes, secret: str) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()


@pytest.fixture(autouse=True)
def webhook_secret_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("WEBHOOK_SECRET", "dev-secret")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_verify_signature_accepts_valid_signature() -> None:
    payload = b'{"id":"evt_001","event":"payment.completed"}'
    signature = sign(payload, "dev-secret")

    assert verify_signature(payload, signature) is True


def test_verify_signature_rejects_invalid_signature() -> None:
    payload = b'{"id":"evt_001","event":"payment.completed"}'

    assert verify_signature(payload, "invalid-signature") is False


def test_verify_signature_rejects_missing_signature() -> None:
    payload = b'{"id":"evt_001","event":"payment.completed"}'

    assert verify_signature(payload, None) is False
