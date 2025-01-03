from app.api.middleware.error_middleware import ErrorMiddleware

MIDDLEWARES = {ErrorMiddleware}

__all__ = ("MIDDLEWARES",)
