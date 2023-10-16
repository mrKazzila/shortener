from unittest import mock

pytest_plugins = [
    'tests.fixtures.database',
    'tests.fixtures.environment',
]

# issue: Unable to use pytest with cache
# https://github.com/long2ice/fastapi-cache/issues/49
mock.patch(
    "fastapi_cache.decorator.cache",
    lambda *args, **kwargs: lambda f: f,
).start()
