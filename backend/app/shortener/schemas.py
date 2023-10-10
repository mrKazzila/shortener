from pydantic import BaseModel, HttpUrl


class SUrlBase(BaseModel):
    """
    Base URL model.

    Args:
        target_url: The target URL of the URL.
    """

    target_url: HttpUrl


class SUrl(SUrlBase):
    """
    URL model.

    Args:
        is_active: Whether the URL is active.
        clicks_count: The number of clicks on the URL.
    """

    is_active: bool
    clicks_count: int


class SUrlInfo(SUrl):
    """
    URL info model.

    Args:
        url: The full URL of the URL, including the protocol and domain name.
    """

    url: HttpUrl


class SAddUrl(BaseModel):
    id: int
    url: HttpUrl
    target_url: HttpUrl


class STargetUrl(BaseModel):
    id: int
    is_active: bool
    clicks_count: int
    target_url: HttpUrl
