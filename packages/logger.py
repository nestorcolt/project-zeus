from Cloud.packages.constants import constants
from Cloud.packages.settings import settings
import logging
import os


##############################################################################################

class Logger:

    def __init__(self, logger_name=None):
        self.logger_name = logger_name or __name__
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(settings.DEBUG_LEVEL)

        self.format = self.set_formatter()
        self.stream_handler = self.set_stream_handle()
        self.logger.addHandler(self.stream_handler)

        # for file logs
        self.file_handler = None

    def set_formatter(self, formatter_string=None):
        format_ = "%(name)s | %(message)s"
        format_ = formatter_string if formatter_string else format_
        return logging.Formatter(format_, "%Y-%m-%d %H:%M:%S")

    def set_file_handle(self, logging_level=logging.DEBUG, file_format=None, file_path=None):

        if not file_path:
            file_path = os.path.join(constants.ROOT_DIRECTORY, "logs", constants.LOG_FILE_NAME)

        if not file_format:
            file_format = "%(name)s | %(asctime)s | %(message)s:"

        self.file_handler = logging.FileHandler(file_path)
        self.file_handler.setLevel(logging_level)
        self.file_handler.setFormatter(self.set_formatter(file_format))
        self.logger.addHandler(self.file_handler)

    def set_stream_handle(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(settings.DEBUG_LEVEL)
        stream_handler.setFormatter(self.format)
        return stream_handler

##############################################################################################
