from fastapi import APIRouter, HTTPException
from app.configs.database import db
from dotenv import load_dotenv
import os
import httpx
import asyncio
import logging

router = APIRouter(prefix="/api/v1",tags=["topranking"])

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
            page_num = 1
            while page_num  < 3:
                url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page_num}"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"{bearer}"
                }
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers)
                    d_data = response.json()
                    ranklist = d_data['results']
                    for result in ranklist:
                        if 'title' in result and 'vote_average' in result:
                            get_title = result.get('title')
                            get_vote_average = result.get('vote_average')
                            top_ranking.append({"title": get_title, "average_rating": get_vote_average})
                        else:
                            pass
                page_num += 1
            await Insert_ranklist()
            await asyncio.sleep(delay+120)    # Sleep for 1wk
   except Exception as e:
       logger.info(e) 
async def Insert_ranklist():
    try:
        for _results in top_ranking:
            collection = db['movies'].find_one({"title": _results.get("title")})
            if collection is None:
                pass
            else:
                update_collection = db['TopRanking'].update_one({"title":_results.get("title")},{"$set":{"average_rating":_results['average_rating']}},upsert=True)
                if update_collection.acknowledged:
                    pass
        logger.info("done")
    except Exception as e:
        logger.info(e)
@router.on_event("startup")
async def background():
    try:
        asyncio.create_task(TMDB())
        logger.info("Background TopRanking task started")
    except HTTPException as http_err:
        logger.error(f"HTTP error occurred: {http_err.detail}")
    except Exception as err:
        logger.error(f"Unexpected error occurred: {err}")