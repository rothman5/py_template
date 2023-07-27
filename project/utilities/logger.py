""" Logger module. """

import os
import sys
import logging

from .singleton import Singleton


class Logger(Singleton, logging.Logger):
    """Logger class."""

    def __init__(self, identifier: str = "root") -> None:
        super().__init__(name=identifier)
        self.add_file_handler()
        self.add_console_handler()

    def get_path(self, relative_path: str) -> str:
        """Utility function used to get the absolute path of a file.

        Args:
            relative_path (str): Relative path (usually the file name).

        Returns:
            str: Absolute path.
        """

        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS  # pylint: disable=no-member,protected-access
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_formatter(self) -> logging.Formatter:
        """Create a logging formatter.

        Returns:
            logging.Formatter: Logging formatter.
        """

        text_format = "%(levelname).1s (%(asctime)s) %(message)s"
        date_format = "%H:%M:%S"
        return logging.Formatter(fmt=text_format, datefmt=date_format)

    def add_file_handler(self) -> None:
        """Add a file handler to the logger to enable file logging."""

        file_handler = logging.FileHandler(self.get_path("debug.log"), "w")
        file_handler.setFormatter(self.get_formatter())
        file_handler.setLevel(logging.DEBUG)
        self.addHandler(file_handler)

    def add_console_handler(self) -> None:
        """Add a console handler to the logger to enable console logging."""

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.get_formatter())
        console_handler.setLevel(logging.INFO)
        self.addHandler(console_handler)
