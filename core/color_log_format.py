import logging

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[37m",   # White
        "INFO": "\033[36m",    # Cyan
        "WARNING": "\033[33m", # Yellow
        "ERROR": "\033[31m",   # Red
        "CRITICAL": "\033[41m" # Red background
    }

    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"