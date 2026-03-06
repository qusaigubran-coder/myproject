from fastapi import FastAPI, Header, Request

from myproject.logging_config import configure_logging
from myproject.webhook import handle_webhook

configure_logging()

app = FastAPI(title="myproject webhook server")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/example")
async def example_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
):
    return await handle_webhook(request, x_signature)
