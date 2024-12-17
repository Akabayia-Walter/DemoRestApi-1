from fastapi import APIRouter, Query
from app.configs.database import db

router = APIRouter(prefix="/api/v1", tags=["typemovie"])

@router.get("/typemovie")
async def TypeMovie(query:str = Query(), limit:int = 1, skip:int = 0):
    try:
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
        response = db['movies'].aggregate(pipeline)
        return {"message":list(response)}
    except Exception as e:
        return {"message":str(e)}
