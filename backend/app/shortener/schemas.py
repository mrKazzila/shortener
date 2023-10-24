from pydantic import BaseModel, HttpUrl


class SUrlBase(BaseModel):
    """
    Base URL schema.

    Args:
        target_url: The long target URL.
    """

    target_url: HttpUrl


class SUrl(SUrlBase):
    """
    URL schema.

    Args:
        id: ID.
        url: Short url for target URL.
    """

    id: int
    url: HttpUrl


class SUrlInfo(SUrl):
    """
    SUrlInfo schema.

    Args:
        is_active: Whether the URL is active.
        clicks_count: The number of clicks on the short URL.
    """

    is_active: bool
    clicks_count: int
