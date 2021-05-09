import logging
import os
from logging import handlers  # noqa F401

import environ


class GroupWriteRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """https://stackoverflow.com/questions/1407474"""

    def _open(self):
        prevumask = os.umask(0o002)
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv


env = environ.Env()
env.read_env(str((environ.Path(__file__) - 1).path(".env")))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(module)s"
            + "%(name)s %(process)d %(thread)d: %(message)s"
        },
        "simple": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "settings.GroupWriteRotatingFileHandler",
            "filename": env("LOG_PATH_REQUEST"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "simple",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
