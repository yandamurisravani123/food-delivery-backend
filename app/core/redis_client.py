# from redis.asyncio import Redis

# from app.config.settings import settings

# redis_client = Redis.from_url(
#     settings.REDIS_URL,
#     decode_responses=True,
# )



from redis.exceptions import RedisError
import redis.asyncio as redis

from app.config.settings import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)
redis_available = False


def available() -> bool:
    return redis_available



async def connect_redis():
    try:
        await redis_client.ping()
        print("✅ Redis connected successfully")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")


async def close_redis():
    await redis_client.close()