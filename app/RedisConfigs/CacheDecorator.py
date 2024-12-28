from fastapi.responses import JSONResponse
import json
from app.configs.Redis_cache import redis_connection
def RedisCache(cache_key):
    Cache = redis_connection.get(cache_key)
    if Cache:
        print("from cache")
        return JSONResponse(content=json.loads(Cache),headers={"X-Cache-Status": "HIT"})
    return None