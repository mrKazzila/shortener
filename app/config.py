from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Path settings
ROOT_DIR = Path(__file__).resolve().parent.parent  # корень репозитория
ENV_DIR = Path(ROOT_DIR / 'env').resolve()

# Load env from file
dotenv_path = Path(ENV_DIR / '.env').resolve()
load_dotenv(dotenv_path=dotenv_path)

# Database settings
DB_DRIVER = environ['DB_DRIVER']
DB_HOST = environ['DB_HOST']
DB_PORT = environ['DB_PORT']
DB_NAME = environ['DB_NAME']
DB_USER = environ['DB_USER']
DB_PASSWORD = environ['DB_PASSWORD']
