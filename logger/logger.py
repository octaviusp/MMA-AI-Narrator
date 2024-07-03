from datetime import datetime

class logger:
    """
    Static class Logger to handle logging across an application.
    This class provides static methods to log messages of various severity levels.

    The log format is "[DD/MM/YYYY] - [LEVEL] - [FILE] - MESSAGE",
    where LEVEL is one of INFO, DEBUG, CRITICAL, or ERROR.

    Methods:
        info(message: str, file: str) - Logs an information message.
        debug(message: str, file: str) - Logs a debug message.
        critical(message: str, file: str) - Logs a critical error message.
        error(message: str, file: str) - Logs an error message.
    """

    def __init__(self):
        self.on = True
   
    def _log(self, level: str, message: str, file: str):
        if self.on:
            log_message = f"[{datetime.now().strftime('%d/%m/%Y')}] - [{level}] - [{file}] - {message}"
            print(log_message)  # Assuming log output to console; replace with file write if needed

    def info(self, message: str, file: str):
        """
        Logs an informational message.

        Args:
            message (str): The message to log.
            file (str): The file where the log is triggered.
        """
        self._log('INFO', message, file)

   
    def debug(self, message: str, file: str):
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
            file (str): The file where the log is triggered.
        """
        self._log('DEBUG', message, file)

   
    def critical(self, message: str, file: str):
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
            file (str): The file where the log is triggered.
        """
        self._log('CRITICAL', message, file)

   
    def error(self, message: str, file: str):
        """
        Logs an error message.

        Args:
            message (str): The message to log.
            file (str): The file where the log is triggered.
        """
        self._log('ERROR', message, file)

Logger = logger()
