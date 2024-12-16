from fastapi import APIRouter, HTTPException
from configs.database import db,client
import logging

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
async def get_all(skip:int = 0,limit:int = 1):
    try:
        pipeline_querry = pipeline + [{"$skip":skip},{"$limit":limit}]
        response = db["movies"].aggregate(pipeline_querry)
        return {"message": list(response)}
    except Exception as e:
        logger.error(f"Internal Server Error: {e}", exc_info=True)
        
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred. Please try again later."
        )
    