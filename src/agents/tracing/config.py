import os

path_to_outputlog = "src/agents/tracing"

LOGGING_CONFIG = {
    "version" : 1,
    "formatters": {
        "simple": {
            "format": "[{levelname} {name} {asctime}] {message}",
            "style": "{",
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
            "level": "DEBUG",
            "formatter": "simple",
            "filename": os.path.join(path_to_outputlog,"output.log"),
        },
    },
    "loggers": {
        "": {"handlers": ["stdout", "file"], "level": "INFO", "propagate": False},
        "__main__": {
            "handlers": ["stdout", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "src.agents": {"level": "DEBUG"},
        # ddgs logs "Error in engine ..." at INFO for every search backend
        # it tries and fails over from - noisy even at the default level.
        "ddgs": {"level": "WARNING"},
        "primp": {"level": "WARNING"},
    },
}