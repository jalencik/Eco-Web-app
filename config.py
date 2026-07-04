"""Application configuration.

All secrets come from environment variables so nothing sensitive
is ever committed to the repository.
"""
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///ecopulse.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # How long fetched weather/air-quality data is reused before calling
    # the API again (seconds). Keeps us well inside free API limits.
    CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", 600))

    # Set DEMO_DATA=1 to run without internet access (development only).
    # The UI clearly labels demo data so it can never be mistaken for real.
    DEMO_DATA = os.environ.get("DEMO_DATA") == "1"
