from fastapi import APIRouter, Query, Response,Request
import json
from fastapi.responses import JSONResponse
from app.RedisConfigs.RedisDecorator import Decorator
from app.configs.database import db
from hashlib import md5
from app.configs.Redis_cache import redis_connection
from app.RedisConfigs.CacheDecorator import RedisCache

router = APIRouter(prefix="/api/v1", tags=["genres"])

@router.get("/genres")
async def TypeMovie(request: Request,response:Response, query: str = Query(), limit: int = 1, skip: int = 0):
    try:
        pipeline = [
            {
                '$match': {
                    'genres': query
                }
            },
            {
                "$sort": {
                    "year": -1
                }
            },
            {
                "$unset": ["_id","released"]
            },
            {
                "$limit": limit
            },
            {
                "$skip": skip
            },
        ]
        r_url = str(request.url)
        cache_key  = md5(r_url.encode('utf-8')).hexdigest()
        check_cache = RedisCache(cache_key)
        if check_cache != None:
            return check_cache
        print("yes")
        response_data = db['movies'].aggregate(pipeline)
        result = list(response_data)
        redis_connection.set(cache_key, json.dumps(result, default=str), ex=300)
        return JSONResponse(content=json.loads(json.dumps(result, default=str)),headers={"X-Cache-Status": "MISS"})
    except Exception as e:
        return {"message": str(e)}