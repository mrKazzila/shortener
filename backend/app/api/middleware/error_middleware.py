import logging
from time import time
from typing import Any
from urllib import parse

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.datastructures import QueryParams
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

__all__ = ("ErrorMiddleware",)

logger = logging.getLogger(__name__)


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time()

        try:
            return await call_next(request)
        except Exception as exc:
            request_info = self._create_request_info_dict(
                request=request,
                start_time=start_time,
            )
            logger.error(exc)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": (
                        "An unexpected error occurred. "
                        f"Please try again later.\n{exc}"
                    ),
                    "ditail": request_info,
                },
                media_type="application/json",
            )

    def _create_request_info_dict(
        self,
        *,
        request: Request,
        start_time: float,
    ) -> dict[str, Any]:
        q_params = self._get_query_params_to_json(
            params=request.query_params,
        )
        return {
            "Start time": round(start_time, 0),
            "Duration": round(time() - start_time, 3),
            "Method": request.method,
            "Request path": str(request.url.path),
            "Path params": request.path_params,
            "Query params": q_params,
        }

    @staticmethod
    def _get_query_params_to_json(*, params: QueryParams) -> dict[str, Any]:
        return dict(parse.parse_qsl(str(params)))
