from pydantic import BaseModel


class UrlBase(BaseModel):
    """
    Base URL model.

    Args:
        target_url: The target URL of the URL.
    """
    target_url: str


class Url(UrlBase):
    """
    URL model.

    Args:
        is_active: Whether the URL is active.
        clicks_count: The number of clicks on the URL.
    """
    is_active: bool
    clicks_count: int

    class Config:
        from_attributes = True


class UrlInfo(Url):
    """
    URL info model.

    Args:
        url: The full URL of the URL, including the protocol and domain name.
        admin_url: The URL of the admin page for the URL.
    """
    url: str
    admin_url: str
