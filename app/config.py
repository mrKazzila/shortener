from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Path settings
ROOT_DIR = Path(__file__).resolve().parent.parent  # Root project dir
ENV_DIR = Path(ROOT_DIR / 'env').resolve()

# Load env from file
dotenv_path = Path(ENV_DIR / '.env').resolve()
load_dotenv(dotenv_path=dotenv_path)

# Base settings
BASE_URL = environ['BASE_URL']
origins = [
    'http://localhost:8000',
]

# Database settings
DB_DRIVER = environ['DB_DRIVER']
DB_HOST = environ['DB_HOST']
DB_PORT = environ['DB_PORT']
DB_NAME = environ['DB_NAME']
DB_USER = environ['DB_USER']
DB_PASSWORD = environ['DB_PASSWORD']
DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Test database settings
TEST_DB_DRIVER = environ['TEST_DB_DRIVER']
TEST_DB_HOST = environ['TEST_DB_HOST']
TEST_DB_PORT = environ['TEST_DB_PORT']
TEST_DB_NAME = environ['TEST_DB_NAME']
TEST_DB_USER = environ['TEST_DB_USER']
TEST_DB_PASSWORD = environ['TEST_DB_PASSWORD']
TEST_DB_URL = f"{TEST_DB_DRIVER}://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
