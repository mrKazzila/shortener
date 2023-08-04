from pydantic import BaseModel


class UrlBase(BaseModel):
    target_url: str


class Url(UrlBase):
    is_active: bool
    clicks_count: int

    class Config:
        from_attributes = True


class UrlInfo(Url):
    url: str
    admin_url: str
