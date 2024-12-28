import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
import redis
from app.configs.Redis_cache import redis_connection
from app.RedisConfigs.RedisDecorator import Decorator

router = APIRouter(prefix="/api/v1", tags=["test"])  

# def Decorator(expire: int):
#     def decorator(func):
#         async def wrapper(request: Request, response: Response):
#             # URL from the request
#             url_path = str(request.url)
#             # Ensure that the correct response is awaited and passed through the decorator
#             print(expire)
#             Cache = redis_connection.get(url_path)
#             if Cache:
#                 print("from cache")
#                 return JSONResponse(content=json.loads(Cache))
            
#             print("cache not found")
#             original_response = await func(request, response)
#             redis_connection.set(url_path, json.dumps(original_response), ex=expire)
            
#             # Print the response from the original function
#             # print(original_response.get("message"))
#             print("from decorator")
            
#             # Return the modified response back to the client
#             return original_response
#         return wrapper
#     return decorator

@router.get("/test")
@Decorator(expire=60)
async def test(
    request: Request,
    response: Response,
    skip:int = 0,limit:int = 1
):
    try:
        n = 9
        print("from test")
        # Your actual function logic
        item = [{"name": "item1"}, {"name": "item2"}]
        return {"message": item}
    except Exception as e:
        return {"message": str(e)}
