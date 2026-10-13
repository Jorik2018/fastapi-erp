from sqlalchemy import inspect

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict


T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="allow")

    data: list[T]

def to_entity(
    source: BaseModel | dict[str, Any],
    model: type,
    *,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
):
    include = set(include) if include is not None else None
    exclude = set(exclude or ())

    fields = {
        column.key
        for column in inspect(model).columns
    }

    if isinstance(source, BaseModel):
        data = source.model_dump(exclude_unset=True)
    else:
        data = dict(source)

    data = {
        key: value
        for key, value in data.items()
        if key in fields
        and key not in exclude
        and (include is None or key in include)
    }

    return model(**data)