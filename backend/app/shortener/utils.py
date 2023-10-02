import secrets
from string import ascii_lowercase, ascii_uppercase, digits

import app.shortener.services as services
from app.settings.config import settings


async def create_unique_random_key() -> str:
    """
    Creates a unique random key.

    Returns:
        A unique random key.
    """
    key = generate_random_key()

    while await services.get_active_long_url_by_key(key=key):
        key = generate_random_key()

    return key


def generate_random_key(length: int = settings().KEY_LENGTH) -> str:
    """
    Generate a random key of the given length.

    Args:
        length (int, optional): The length of the key. Defaults to 5.

    Returns:
        str: The random key.
    """
    if length <= 2:
        length = settings().KEY_LENGTH
        print('Not correct length, changed to settings length!')  # TODO: log

    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(secrets.choice(chars) for _ in range(length))
