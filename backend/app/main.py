from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.config import settings
from app.settings.redis_setup import redis_setup
from app.shortener.router import router as shortener_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Service started')
    await redis_setup()
    yield
    print('Service exited')


app = FastAPI(lifespan=lifespan)
app.include_router(shortener_router)

origins = [
    f'{settings().DOMAIN}:{settings().DOMAIN_PORT}',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=[
        'Content-Type',
        'Access-Control-Allow-Origin',
    ],
)
