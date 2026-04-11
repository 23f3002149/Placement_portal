import json

try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print(" Redis connected - Caching ON!")
except Exception:
    redis_client = None
    print(" Redis nahi chala - direct DB se chalega (caching off)")


def cache_get(key):
    """Redis se value fetch karo, nahi mili to None return karo"""
    if redis_client is None:
        return None
    try:
        val = redis_client.get(key)
        return json.loads(val) if val else None
    except:
        return None


def cache_set(key, value, ttl=300):
    """Redis mein value save karo (default 5 min)"""
    if redis_client is None:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value, default=str))
    except:
        pass


def cache_delete(*keys):
    """Redis se ek ya zyada keys delete karo (cache invalidate)"""
    if redis_client is None:
        return
    try:
        redis_client.delete(*keys)
    except:
        pass
