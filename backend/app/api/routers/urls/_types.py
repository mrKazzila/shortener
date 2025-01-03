from typing import Annotated

from fastapi import Depends, Path, Query
from pydantic import HttpUrl

from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

__all__ = (
    "PathUrlKey",
    "QueryLongUrl",
    "Uow",
)

QueryLongUrl = Annotated[
    HttpUrl,
    Query(description="Initial long URL for shortening"),
]
PathUrlKey = Annotated[str, Path(description="The shortened URL key")]
Uow = Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)]
