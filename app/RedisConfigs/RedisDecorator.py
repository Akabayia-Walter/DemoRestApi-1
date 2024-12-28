from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json
from hashlib import md5
from app.configs.Redis_cache import redis_connection

def Decorator(expire: int = 3600):  # Default expiration time set to 1 hour
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract URL for caching (excluding query parameters)
            request: Request = kwargs.get("request")
            if not request:
                raise ValueError("Request object not found in arguments.")
            
            # Create a cache key using the URL and query parameters
            query_params = str(request.query_params)
            url_path = str(request.url.path) + "?" + query_params
            print("Cache key source:", url_path)
            
            cache_key = md5(url_path.encode("utf-8")).hexdigest()
            print("Cache key:", cache_key)

            # Check if the response is in the cache
            Cache = redis_connection.get(cache_key)
            if Cache:
                print("Cache hit")
                print(Cache, "Cached Data")
                return JSONResponse(content=json.loads(Cache), headers={"X-Cache-Status": "HIT"})

            # Cache miss: Call the original function and serialize the response
            print("Cache miss")
            original_response = await func(*args, **kwargs)
            
            try:
                response_data = json.dumps(original_response, default=str)
            except Exception as e:
                print(f"Serialization error: {e}")
                return JSONResponse(content={"error": "Failed to serialize response"}, status_code=500)

            # Store the serialized response in the cache
            redis_connection.set(cache_key, response_data, ex=expire)

            # Return the original response
            return JSONResponse(content=original_response, headers={"X-Cache-Status": "MISS"})
        return wrapper
    return decorator
