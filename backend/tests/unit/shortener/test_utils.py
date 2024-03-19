import logging

import pytest
from tests.unit.shortener.parametrize_data import key_length

from app.api.urls.utils import generate_random_key

logger = logging.getLogger(__name__)


@pytest.mark.unit()
def test_generate_random_key_return_str() -> None:
    """Test that generate_random_key returned not empty string."""
    key = generate_random_key()

    assert type(key) == str
    assert key != ""


@pytest.mark.unit()
def test_generate_random_key_is_unique() -> None:
    """Test that generate_random_key is unique."""
    random_key_1 = generate_random_key()
    random_key_2 = generate_random_key()

    assert random_key_1 != random_key_2


@pytest.mark.unit()
@pytest.mark.parametrize(
    ("length", "expected_result"),
    key_length,
    ids=str,
)
def test_generate_random_key_with_default_length(
    length: int,
    expected_result: int,
) -> None:
    """Test function for generate_random_key with default length."""
    logger.info("TEST LOGS")
    random_key = generate_random_key(length=length)

    assert len(random_key) == expected_result
