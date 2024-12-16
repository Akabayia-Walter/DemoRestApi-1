from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["test"])  

@router.get("/test")
async def test():
    return {"message": "test hello again"}