from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from app.configs.database import db

router = APIRouter(prefix="/api/v1", tags=["search"])

@router.get("/search")
async def search(query:str = Query(), skip:int = 0, limit:int  = 1):
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
        response = db['movies'].aggregate(pipeline)
        return {"message":list(response)}
        
    except Exception as e:
        return {"message":str(e)}