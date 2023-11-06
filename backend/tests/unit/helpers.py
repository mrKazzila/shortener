from sqlalchemy import select
from sqlalchemy.sql.selectable import Select


def select_by(*, model, model_params, value: str) -> Select:
    query = (
        select(model)
        .filter(model_params == value)
    )
    return query
