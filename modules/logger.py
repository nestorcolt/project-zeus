import logging


class Logger:

    def __init__(self, logger_name=None):
        self.logger_name = logger_name or __name__
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)

        self.format = self.set_formatter()
        self.file_format = self.format
        self.stream_handler = self.set_stream_handle()
        self.logger.addHandler(self.stream_handler)

        # for file logs
        self.file_handler = None

    def set_formatter(self, formatter_string=None):
        format_ = "%(name)s: %(message)s"
        format_ = formatter_string if formatter_string else format_
        return logging.Formatter(format_)

    def set_file_handle(self, file_path, logging_level, file_format):
        self.file_handler = logging.FileHandler(file_path)
        self.file_handler.setLevel(logging_level)
        self.file_format = file_format
        self.file_handler.setFormatter(file_format)
        return self.file_handler

    def set_stream_handle(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(self.format)
        return stream_handler

##############################################################################################
