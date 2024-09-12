LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
            "qualname": "uvicorn",
        },
        "uvicorn.develop": {
            "level": "DEBUG",
            "handlers": ["debug"],
            "propagate": False,
        },
        "track": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
            "qualname": "track",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "debug": {
            "formatter": "debug",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s [%(asctime)s] %(message)s %(module)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": (
                '%(levelprefix)s %(client_addr)s'
                ' - "%(request_line)s" %(status_code)s'),
        },
        "debug": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": (
                '%(levelprefix)s [%(asctime)s] [%(filename)s/'
                '%(funcName)s:%(lineno)d] %(message)s'),
        },
    },
}
