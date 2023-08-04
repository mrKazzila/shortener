from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Url(Base):
    __tablename__ = 'url'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks_count = Column(Integer, default=0)
