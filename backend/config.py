import os

class BaseConfig:
    # Common defaults
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # API / server
    HOST = os.getenv("BACKEND_HOST", "localhost")
    PORT = int(os.getenv("BACKEND_PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "TRUE")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    