# modules/logger.py
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_file = "operations.log"

    def log(self, message):
        # Add the current timestamp to each log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {message}"
        with open(self.log_file, "a") as file:
            file.write(log_message + "\n")