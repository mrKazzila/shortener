from fastapi import FastAPI

from app.shortener.router import router as shortener_router

app = FastAPI()
app.include_router(shortener_router)
