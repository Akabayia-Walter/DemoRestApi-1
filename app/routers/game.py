import asyncio
from fastapi import APIRouter, HTTPException

router = APIRouter()

async def background_task():
    while True:
        print('Running background task...')
        await asyncio.sleep(50)  # Sleep for 5 seconds

@router.on_event("startup")
async def startup_event():
    asyncio.create_task(background_task())

