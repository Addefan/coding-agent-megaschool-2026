import json
from enum import IntEnum

from settings import settings


class LogLevel(IntEnum):
    QUIET = 0
    ERROR = 1
    INFO = 2
    DEBUG = 3


class Logger:
    def __init__(self, level: LogLevel = None):
        if level is None:
            level = LogLevel.DEBUG if settings.debug else LogLevel.ERROR
        self.level = level

    def log(self, level, message, data=None):
        message = {
            "level": level,
            "message": message,
        }

        if data:
            message["data"] = data

        print(json.dumps(message))

    def debug(self, message, data=None):
        if self.level < LogLevel.DEBUG:
            return None
        return self.log(level="DEBUG", message=message, data=data)

    def info(self, message, data=None):
        if self.level < LogLevel.INFO:
            return None
        return self.log(level="INFO", message=message, data=data)

    def warn(self, message, data=None):
        if self.level < LogLevel.INFO:
            return None
        return self.log(level="WARN", message=message, data=data)

    def error(self, message, data=None):
        if self.level < LogLevel.ERROR:
            return None
        return self.log(level="ERROR", message=message, data=data)


logger = Logger()

if __name__ == "__main__":
    logger.debug("test")
