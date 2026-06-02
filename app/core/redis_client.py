# from redis.asyncio import Redis

# from app.config.settings import settings

# redis_client = Redis.from_url(
#     settings.REDIS_URL,
#     decode_responses=True,
# )



import redis.asyncio as redis

from app.config.settings import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

redis_connected = False


async def connect_redis():
    global redis_connected
    try:
        await redis_client.ping()
        redis_connected = True
        print("✅ Redis connected successfully")
        return True
    except Exception as e:
        redis_connected = False
        print(f"❌ Redis connection failed: {e}")
        return False


async def close_redis():
    if redis_connected:
        await redis_client.close()


async def redis_get(key):
    if not redis_connected:
        return None

    try:
        return await redis_client.get(key)
    except redis.exceptions.RedisError:
        return None


async def redis_setex(key, seconds, value):
    if not redis_connected:
        return None

    try:
        return await redis_client.setex(key, seconds, value)
    except redis.exceptions.RedisError:
        return None


async def redis_delete(key):
    if not redis_connected:
        return None

    try:
        return await redis_client.delete(key)
    except redis.exceptions.RedisError:
        return None