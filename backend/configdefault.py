import os

# duplicate this file and rename to config.py and then set env vars there

class BaseConfig:
    # Common defaults
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # API / server
    HOST = os.getenv("BACKEND_HOST", "localhost")
    PORT = int(os.getenv("BACKEND_PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "TRUE")
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    