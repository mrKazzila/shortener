from typing import Annotated

from fastapi import Depends, Path

from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

__all__ = (
    "PathUrlKey",
    "Uow",
)

PathUrlKey = Annotated[str, Path(description="The shortened URL key")]
Uow = Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)]
