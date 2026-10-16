import os


def _bool_env(name: str, default: str = "False") -> bool:
  return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


class Config:
  DEBUG = _bool_env("DEBUG_MODE", "False")
  ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*")

  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")

  DATABASE_URL = os.getenv("DATABASE_URL", "")


class TestConfig(Config):
  TESTING = True
  DEBUG = False
  ALLOWED_HOSTS = "*"

  JWT_SECRET_KEY = "test-secret"

  DATABASE_URL = ""
