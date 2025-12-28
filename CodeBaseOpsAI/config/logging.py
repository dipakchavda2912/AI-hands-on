import logging
import logging.config
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "standard": {
      "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    },
    "json": {  # optional structured logging
      "format": '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
    },
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "standard",
      "level": LOG_LEVEL,
    },
    "file": {
      "class": "logging.FileHandler",
      "filename": "app.log",
      "formatter": "standard",
      "level": LOG_LEVEL,
    },
  },
  "root": {
    "handlers": ["console", "file"],
    "level": LOG_LEVEL,
  },
}


def setup_logging():
  logging.config.dictConfig(LOGGING_CONFIG)
