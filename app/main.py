from fastapi import FastAPI
from src.app.routers.test import router as test_router
from src.app.routers.getAll import router as getall_router
from src.app.routers.Search import router as search_router
from src.app.routers.Movie import router as typemovie_router
from src.app.routers.Genres import router as genres_router

app = FastAPI()

app.include_router(test_router)
app.include_router(getall_router)
app.include_router(search_router)
app.include_router(typemovie_router)
app.include_router(genres_router)