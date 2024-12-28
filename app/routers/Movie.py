import json
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from app.RedisConfigs.RedisDecorator import Decorator
from app.configs.database import db
from app.configs.Redis_cache import redis_connection
from app.RedisConfigs.CacheDecorator import RedisCache
from hashlib import md5
router = APIRouter(prefix="/api/v1", tags=["typemovie"])

@router.get("/typemovie")
async def TypeMovie(request:Request,query: str = Query(...), limit: int = 1, skip: int = 0):
    try:
        r_url = str(request.url)
        cache_key  = md5(r_url.encode('utf-8')).hexdigest()
        check_cache = RedisCache(cache_key)
        if check_cache != None:
            return check_cache
        print("yes")
        pipeline = [
    {
        '$match': {
            'type': query
        }
    },
     {
    "$sort": {
      "year":-1
    }
  },
     
    {'$set':{
        'released': {
            '$dateToString': {
                'format': '%Y-%m-%d', 
                'date': '$released'
            }
        }
    }},

    {
        "$unset":["_id"]
    },
    {
        "$limit":limit
    },
    {
        "$skip":skip
    },
]
        
        respon = db['movies'].aggregate(pipeline)
        result = list(respon)
        redis_connection.set(cache_key, json.dumps(result, default=str), ex=300)
        return JSONResponse(content=json.loads(json.dumps(result, default=str)),headers={"X-Cache-Status": "MISS"})
    except Exception as e:
        return {"message":str(e)}
