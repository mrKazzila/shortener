from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.config import settings
from app.shortener.router import router as shortener_router

app = FastAPI()
app.include_router(shortener_router)
origins = [
    f'{settings().DOMAIN}:{settings().DOMAIN_PORT}',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=['Content-Type'],
)
