from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, Request
from redis.asyncio import Redis

from myproject.config import get_settings
from myproject.idempotency import RedisIdempotencyStore
from myproject.logging_config import configure_logging
from myproject.webhook import handle_webhook

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    redis = Redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )

    app.state.redis = redis
    app.state.idempotency_store = RedisIdempotencyStore(redis)

    try:
        yield
    finally:
        await redis.aclose()


app = FastAPI(
    title="myproject webhook server",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/example")
async def example_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
):
    return await handle_webhook(request, x_signature)
