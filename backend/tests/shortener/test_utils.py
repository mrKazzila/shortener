import pytest
from backend.app.shortener.utils import create_secret_key, generate_random_key


def test_generate_random_key_is_unique() -> None:
    """Test that generate_random_key is unique."""
    random_key_1 = generate_random_key(10)
    random_key_2 = generate_random_key(10)

    assert random_key_1 != random_key_2


def test_create_secret_key_with_valid_key() -> None:
    """Test that create_secret_key works with a valid key."""
    key = "my_key"
    secret_key = create_secret_key(key)

    assert secret_key.startswith(key)


@pytest.mark.parametrize('length, expected_result', [
    (1, 1),
    (5, 5),
    (10, 10),
])
def test_generate_random_key_with_difference_length(length: int, expected_result: int) -> None:
    random_key = generate_random_key(length)

    assert len(random_key) == expected_result


@pytest.mark.parametrize('length, expected_exception', [
    (0, ValueError),
    (-1, ValueError),
    (-10, ValueError),
])
def test_generate_random_key_with_invalid_length(length: int, expected_exception: type(Exception)) -> None:
    """Test that generate_random_key raise ValueError with invalid length."""
    with pytest.raises(expected_exception):
        generate_random_key(length)


def test_create_secret_key_with_empty_key() -> None:
    """Test that create_secret_key raises an error with an empty key."""
    with pytest.raises(ValueError):
        create_secret_key("")
