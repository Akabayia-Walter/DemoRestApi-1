from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend as RedisBackend
import uvicorn
from app.routers.test import router as test_router
from app.routers.getAll import router as getall_router
from app.routers.Search import router as search_router
from app.routers.Movie import router as typemovie_router
from app.routers.Genres import router as genres_router
from app.routers.BackgroudTasks.TrendingAll import router as trendingalltasks_router
from app.routers.game import router as game_router
from app.routers.BackgroudTasks.TopRanking import router as toprank_router
from app.routers.BackgroudTasks.Upcoming import router as upcoming_router
from app.routers.Upcoming import router as upcoming_router
from app.routers.Trendingall import router as trendingall_router
app = FastAPI()
# background tasks
app.include_router(trendingalltasks_router)
app.include_router(upcoming_router)
# others
app.include_router(test_router)
app.include_router(getall_router)
app.include_router(search_router)
app.include_router(typemovie_router)
app.include_router(genres_router)
app.include_router(upcoming_router)
app.include_router(trendingall_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)