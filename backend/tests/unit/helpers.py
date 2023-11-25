from typing import Any

from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from app.settings.database import Base


def select_by(*, model: type(Base), model_params: Any, value: str) -> Select:
    query = select(model).filter(model_params == value)
    return query
