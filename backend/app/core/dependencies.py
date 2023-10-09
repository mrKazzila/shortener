from typing import Annotated

from fastapi import Depends

from app.core.unit_of_work import ABCUnitOfWork, UnitOfWork

UOWDependencies = Annotated[ABCUnitOfWork, Depends(UnitOfWork)]
