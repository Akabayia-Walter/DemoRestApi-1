from fastapi import APIRouter, Request
from hashlib import md5
from app.configs.database import db
from app.RedisConfigs.CacheDecorator import RedisCache
from app.configs.Redis_cache import redis_connection
import json
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/api/v1", tags=["upcoming"])

@router.get("/trending")
async def Trending(request:Request,limit:int = 5,skip:int = 0):
    try:
        r_url = str(request.url)
        cache_key  = md5(r_url.encode('utf-8')).hexdigest()
        check_cache = RedisCache(cache_key)
        if check_cache != None:
            return check_cache
        pipeline = [
    {
        '$lookup': {
            'from': 'movies', 
            'localField': '_ref', 
            'foreignField': '_id', 
            'as': 'movie_details'
        }
    }, {
        '$unwind': '$movie_details'
    }, {
        '$replaceRoot': {
            'newRoot': '$movie_details'
        }
    }
]
        
        response = db["TrendingMovies"].aggregate(pipeline)
        result = list(response)
        
        redis_connection.set(cache_key, json.dumps(result, default=str), ex=300)
        return JSONResponse(content=json.loads(json.dumps(result, default=str)),headers={"X-Cache-Status": "MISS"})
    except Exception as e:
        return {"message": str(e)}
    

