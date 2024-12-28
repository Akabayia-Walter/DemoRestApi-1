from fastapi import APIRouter, HTTPException
from app.configs.database import db
from dotenv import load_dotenv
import os
import httpx
import asyncio
import logging
from time import sleep

router = APIRouter(prefix="/api/v1",tags=["upcoming"]) # Add this line
load_dotenv()

bearer = os.getenv("TMDB")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

top_ranking = []
delay = 7 * 24 * 60 * 60
async def TMDB():
   try:
        while True:
            url = f"https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
            headers = {
                "accept": "application/json",
                "Authorization": f"{bearer}"
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    d_data = response.json()
                    ranklist = d_data['results']
                    for result in ranklist:
                        if 'title' in result and 'vote_average' in result:
                            get_title = result.get('title')
                            get_language = result.get("original_language")
                            get_overview = result.get("overview")
                            get_release_date = result.get("release_date")
                            get_vote_average = result.get('vote_average')
                            get_poster_path = result.get("poster_path")
                            top_ranking.append({"title": get_title, "language":get_language, "average_rating": get_vote_average,"release_date":get_release_date,"overview":get_overview,"poster_path":f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{get_poster_path}"})
                        else:
                            pass
                    await Insert_ranklist()
                else:
                    logger.info(f"Failed to fetch data from TMDB. Status code: {response.status_code}")
            await asyncio.sleep(delay+180)    # Sleep for 1wk
   except Exception as e:
       logger.info(e) 
async def Insert_ranklist():
    try:
        collection = db["Upcoming"] # Replace with your collection name
        delete_response = collection.delete_many({}) # Delete all existing documents
        if delete_response.acknowledged: # Check if any documents were deleted
            insert_response = collection.insert_many(top_ranking) # Insert new documents
            if insert_response.acknowledged: # Check if the insertion was successful
                logger.info("inserted successfully!")
            top_ranking.clear()
    except Exception as e: # Handle any exceptions
        logger.info(e)
@router.on_event("startup")
def background():
    try:
        asyncio.create_task(TMDB())
        logger.info("Background Upcoming task started")
    except Exception as e:
        logger.info(e)