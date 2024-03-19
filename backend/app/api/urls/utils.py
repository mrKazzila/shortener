import logging
import secrets
from string import ascii_lowercase, ascii_uppercase, digits

from app.settings.config import settings

__all__ = ("generate_random_key",)

logger = logging.getLogger(__name__)
_LENGTH = settings().KEY_LENGTH


def generate_random_key(*, length: int = _LENGTH) -> str:
    """Generate a random key of the given length."""
    if length != _LENGTH:
        length = _LENGTH
        logger.warning(
            "Not correct length for key, arg auto changed to settings length!",
        )

    chars = ascii_lowercase + ascii_uppercase + digits
    return "".join(secrets.choice(chars) for _ in range(length))
