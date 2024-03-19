from pydantic import BaseModel, HttpUrl

__all__ = (
    "SUrlBase",
    "SUrl",
    "SUrlInfo",
)


class SUrlBase(BaseModel):
    """Base URL schema."""

    target_url: HttpUrl

    class Config:
        from_attributes = True


class SUrl(SUrlBase):
    """URL schema."""

    id: int
    key: str


class SUrlInfo(SUrl):
    """SUrlInfo schema."""

    is_active: bool
    clicks_count: int
