from logging.handlers import TimedRotatingFileHandler
import os, logging


def logger(service_name: str):
    log_filename = f"storage/log/{service_name}/{service_name}.log"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    logger_instance = logging.getLogger(service_name)

    if logger_instance.handlers:
        return logger_instance

    logger_instance.setLevel(logging.DEBUG)

    file_handler = TimedRotatingFileHandler(
        filename=log_filename,
        when="midnight",
        interval=1,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    color_formatter = CustomFormatter(service_name)  # console
    plain_formatter = logging.Formatter(
        "[%(levelname)s | %(asctime)s] [%(name)s:%(filename)s] %(message)s",
        "%d-%m-%Y %H:%M:%S"
    )  # arquivo

    file_handler.setFormatter(plain_formatter)
    console_handler.setFormatter(color_formatter)

    logger_instance.addHandler(file_handler)
    logger_instance.addHandler(console_handler)

    return logger_instance


class CustomFormatter(logging.Formatter):    
    LEVEL_COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name.upper()

    def format(self, record: logging.LogRecord) -> str:
        filename = record.filename
        timestamp = self.formatTime(record, "%d-%m-%Y %H:%M:%S")
        level_name = record.levelname
        
        color = self.LEVEL_COLORS.get(level_name, "")
        
        message = record.getMessage()
        
        formatted = (
            f"{color}[{level_name:8} | {timestamp}]{self.RESET} "
            f"[{self.service_name}:{filename}] {message}"
        )
        
        return formatted