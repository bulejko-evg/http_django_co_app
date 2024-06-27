from .paths import BASE_DIR


LOG_DIR = "log"
LOG_PATH = BASE_DIR / LOG_DIR
LOG_MAX_BYTES = 1024 * 1024 * 10  # 10Mb
LOG_BACKUP_COUNT = 10


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime}:{levelname}:{module}:{filename}:{lineno}:{message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "app": {  # common log
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / "app/app.log",
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "formatter": "verbose",
            "encoding": "UTF-8",
        },
        "auth": {  # auth log
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / "auth/auth.log",
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "formatter": "verbose",
            "encoding": "UTF-8",
        },
        "task": {  # celery task log
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / "task/task.log",
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "formatter": "verbose",
            "encoding": "UTF-8",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["app", "console"],
            "level": "DEBUG",
        },
        "auth": {
            "handlers": ["auth", "console"],
            "level": "DEBUG",
        },
        "task": {
            "handlers": ["task", "console"],
            "level": "DEBUG",
        },
    },
}
