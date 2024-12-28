from fastapi import APIRouter, HTTPException
from app.configs.database import db, client
from dotenv import load_dotenv
import os
import httpx
import asyncio
import logging

router = APIRouter()

load_dotenv()

bearer = os.getenv("TMDB")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
treding_movies = []
async def TMDB():
    delay = 7 * 24 * 60 * 60
    url = "https://api.themoviedb.org/3/trending/all/week?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"{bearer}"
    }
    while True:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                d_data = response.json()
                _results = d_data['results']
                for result in _results:
                    if 'title' in result:
                        _check = result.get('title')
                        treding_movies.append(_check)
                    elif 'name' in result:
                        _check = result.get('original_name')
                        treding_movies.append(_check)
                await generate_cursor()
            else:
                logger.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        await asyncio.sleep(delay+60)  # Sleep for 1 wk

async def generate_cursor():
    for result in treding_movies:
        collection = db['movies'].find_one({"title": result})
        if collection is None:
            pass
        else:
            update_result = db["TrendingMovies"].update_one(
                {"title": result},
                {"$setOnInsert": {"title": result, "_ref": collection.get("_id")}},
                upsert=True
            )
            if update_result.upserted_id is not None:
                logger.info(f"Inserted document with id {update_result.upserted_id}")
            else:
                logger.info("Document already exists")
    treding_movies.clear()
@router.on_event("startup")
async def background():
    try:
        asyncio.create_task(TMDB())
        logger.info("Background task started")
    except HTTPException as http_err:
        logger.error(f"HTTP error occurred: {http_err.detail}")
    except Exception as err:
        logger.error(f"Unexpected error occurred: {err}")