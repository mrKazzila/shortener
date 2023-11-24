import logging
import secrets
from string import ascii_lowercase, ascii_uppercase, digits

from app.settings.config import settings

logger = logging.getLogger(__name__)


def generate_random_key(*, length: int = settings().KEY_LENGTH) -> str:
    """
    Generate a random key of the given length.

    Args:
        length (int, optional): The length of the key. Defaults to 5.

    Returns:
        str: The random key.
    """
    if length != settings().KEY_LENGTH:
        length = settings().KEY_LENGTH
        logger.warning(
            'Not correct length for key, arg auto changed to settings length!',
        )

    chars = ascii_lowercase + ascii_uppercase + digits
    key_ = ''.join(secrets.choice(chars) for _ in range(length))
    return key_
