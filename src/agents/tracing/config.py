import os

path_to_outputlog = "src/agents/tracing"

LOGGING_CONFIG = {
    "version" : 1,
    "formatters": {
        "simple": {
            "fmt": "[{levelname} {name} {asctime}] {message}", # this is not working
            "datefmt": "%H:%M:%S",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": os.path.join(path_to_outputlog,"output.log"),
        },
    },
    "loggers": {
        "": {"hanlders": ["stdout", "file"], "level": "DEBUG", "propagate": False},
        "__main__": {
            "handlers": ["stdout", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}