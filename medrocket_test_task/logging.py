"""Logging classes"""


class Logger:
    """Provides logging methods"""

    @classmethod
    def info(cls, message: str):
        """Prints info"""
        print(' [info]: ' + message)

    @classmethod
    def warn(cls, message: str):
        """Prints warning"""
        print('\033[93m [warn]: \033[00m' + message)

    @classmethod
    def error(cls, message: str):
        """Prints error"""
        print('\033[91m [error]: \033[00m' + message)
