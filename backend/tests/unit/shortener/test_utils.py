from typing import Any

import pytest

from app.shortener.utils import generate_random_key

# TODO: add docstrings

_key_length = [
    # length, expected_result
    (-1, 5),
    (0, 5),
    (5, 5),
    (10, 5),
]

_wrong_key_length_type = [
    # invalid key_length
    ('',),
    (1.1,),
    (None,),
    (True,),
    ('test',),
    ([1],),
    ([1, 2, 3, 4, 5],),
]


@pytest.mark.unit
def test_generate_random_key_return_str() -> None:
    """Test that generate_random_key returned not empty string."""
    key = generate_random_key()

    assert type(key) == str
    assert key != ''


@pytest.mark.unit
def test_generate_random_key_is_unique() -> None:
    """Test that generate_random_key is unique."""
    random_key_1 = generate_random_key()
    random_key_2 = generate_random_key()

    assert random_key_1 != random_key_2


@pytest.mark.unit
@pytest.mark.parametrize(
    'length, expected_result',
    _key_length,
    ids=str,
)
def test_generate_random_key_with_default_length(length: int, expected_result: int) -> None:
    random_key = generate_random_key(length=length)
    assert len(random_key) == expected_result


@pytest.mark.unit
@pytest.mark.parametrize(
    'key_length',
    _wrong_key_length_type,
    ids=str,
)
def test_generate_random_key_raise_value_error(key_length: Any) -> None:
    with pytest.raises(ValueError):
        generate_random_key(length=key_length)
