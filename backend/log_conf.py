LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": '%(levelprefix)s [%(asctime)s] %(message)s %(module)s',
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
        "debug": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": '%(levelprefix)s [%(asctime)s] [%(filename)s/%(funcName)s:%(lineno)d] %(message)s',
        },
    },
    "handlers": {
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
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.develop": {
            "handlers": ["debug"],
            "level": "DEBUG",
            "propagate": False
        },
    },
}
