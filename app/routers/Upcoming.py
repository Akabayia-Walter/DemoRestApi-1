from fastapi import APIRouter, Request
from hashlib import md5
from app.configs.database import db
from app.RedisConfigs.CacheDecorator import RedisCache
from app.configs.Redis_cache import redis_connection
import json
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/api/v1", tags=["upcoming"])

@router.get("/upcoming")
async def UpcomingMovies(request:Request,limit:int = 5,skip:int = 0):
    try:
        r_url = str(request.url)
        cache_key  = md5(r_url.encode('utf-8')).hexdigest()
        check_cache = RedisCache(cache_key)
        if check_cache != None:
            return check_cache
        pipeline = [
    {
        '$project': {
            '_id': 0, 
            'overview': 1, 
            'release_date': 1, 
            'language': 1, 
            'average_rating': 1, 
            'title': 1, 
            'poster_path': 1
        }
    }, {
        '$sort': {
            'release_date': 1
        }
    }
]
        response = db["Upcoming"].aggregate(pipeline)
        result = list(response)
        
        redis_connection.set(cache_key, json.dumps(result, default=str), ex=300)
        return JSONResponse(content=json.loads(json.dumps(result, default=str)),headers={"X-Cache-Status": "MISS"})
    except Exception as e:
        return {"message": str(e)}
    

