from fastapi import APIRouter, HTTPException,Response,Request
from fastapi.responses import JSONResponse
from app.RedisConfigs.RedisDecorator import Decorator
from app.configs.database import db
import logging
import json
from hashlib import md5
from app.RedisConfigs.CacheDecorator import RedisCache
from app.configs.Redis_cache import redis_connection

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/api/v1", tags=["getall"])
pipeline =[
     {
        '$project': {
            '_id': 0
        }
    }
]

@router.get("/getall")
async def get_all(request:Request,response:Response,skip:int = 0,limit:int = 1):
    try:
        r_url = str(request.url)
        cache_key  = md5(r_url.encode('utf-8')).hexdigest()
        check_cache = RedisCache(cache_key)
        if check_cache != None:
            return check_cache
        pipeline_querry = pipeline + [{"$skip":skip},{"$limit":limit}]
        response = db["movies"].aggregate(pipeline_querry)
        result = list(response)
        redis_connection.set(cache_key, json.dumps(result, default=str), ex=300)
        return JSONResponse(content=json.loads(json.dumps(result, default=str)),headers={"X-Cache-Status": "MISS"})
    except Exception as e:
        return {"message":str(e)}
    