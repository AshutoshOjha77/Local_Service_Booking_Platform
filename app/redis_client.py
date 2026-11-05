import redis.asyncio as redis
from app.config import setting

redis_client: redis.Redis | None = None

async def init_redis():
    global redis_client
    redis_client = redis.from_url(setting.REDIS_URL, encode="utf-8", decode_responses=True, connections=20)
    if redis_client.ping():
        print("Redis is intialized")

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        raise RuntimeError("Redis could'nt be intialized")
    return redis_client