from fastapi import APIRouter, Query,Response
from pydantic import BaseModel, Field
from app.configs.database import db
from fastapi_redis_cache import cache
router = APIRouter(prefix="/api/v1", tags=["search"])

@router.get("/search")
async def search(response:Response,query:str = Query(), skip:int = 0, limit:int  = 1):
    
    try:
        pipeline = [
    {
        '$match': {
            '$text': {
                '$search': query
            }
        }
    }, {
        '$sort': {
            'textScore': {
                '$meta': 'textScore'
            }
        }
    }, {
        '$unset': '_id'
    },
    {
        "$limit":limit
    }
]
        respon = db['movies'].aggregate(pipeline)
        result = list(respon)
        return {"message":result}
        
    except Exception as e:
        return {"message":str(e)}