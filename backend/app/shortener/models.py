from sqlalchemy import Boolean, Column, Integer, String

from app.settings.database import Base


class Url(Base):
    """A model class for storing shortened URLs."""

    __tablename__ = 'url'

    id = Column(
        Integer,
        doc='The primary key of the model.',
        primary_key=True,
    )
    key = Column(
        String,
        doc='The shortened URL key.',
        unique=True,
        index=True,
    )
    secret_key = Column(
        String,
        doc='The secret key for verifying the shortened URL.',
        unique=True,
        index=True,
    )
    target_url = Column(
        String,
        doc='The original URL.',
        index=True,
    )
    is_active = Column(
        Boolean,
        doc='Whether the URL is active or not.',
        default=True,
    )
    clicks_count = Column(
        Integer,
        doc='The number of times the URL has been clicked.',
        default=0,
    )
