from redis.asyncio import Redis
from redis.exceptions import RedisError


class IdempotencyUnavailableError(Exception):
    pass


class RedisIdempotencyStore:
    def __init__(self, redis: Redis, prefix: str = "webhook:event") -> None:
        self.redis = redis
        self.prefix = prefix

    def _key(self, event_id: str) -> str:
        return f"{self.prefix}:{event_id}"

    async def register_event(self, event_id: str, ttl_seconds: int) -> bool:
        key = self._key(event_id)

        try:
            created = await self.redis.set(
                key,
                "1",
                ex=ttl_seconds,
                nx=True,
            )
        except RedisError as exc:
            raise IdempotencyUnavailableError(
                "Redis idempotency store unavailable"
            ) from exc

        return bool(created)
