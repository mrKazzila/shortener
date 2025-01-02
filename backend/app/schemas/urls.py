from pydantic import BaseModel, ConfigDict, HttpUrl

__all__ = (
    "SUrlBase",
    "SUrl",
    "SUrlInfo",
    "SReturnUrl",
)


class SUrlBase(BaseModel):
    """Base URL schema."""

    target_url: HttpUrl
    model_config = ConfigDict(from_attributes=True)


class SReturnUrl(SUrlBase):
    key: str


class SUrl(SUrlBase):
    """URL schema."""

    id: int


class SUrlInfo(SUrl):
    """SUrlInfo schema."""

    is_active: bool
    clicks_count: int
