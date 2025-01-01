from app.api import ROUTERS, MIDDLEWARES
from app.settings import create_app, routers_setup, middlewares_setup

app = create_app(
    title="ShortenerApi",
    description="Simple API for url shortener logic",
    version='0.0.1',
    contact={
        'autor': 'mrkazzila@gmail.com',
    },
)

routers_setup(app=app, endpoints=ROUTERS)
middlewares_setup(app=app, middlewares=MIDDLEWARES)
