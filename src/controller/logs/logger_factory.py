import logging
import os
from logging.handlers import RotatingFileHandler
from logging import Formatter
from src.controller.singleton import Singleton


class LoggerFactory():

    logger = None

    @staticmethod
    def get_logger(file_path, logging_level):

        logger = logging.getLogger(__name__)
        logger.setLevel(logging_level)

        # Clear File and Create Rotatin File Handler
        LoggerFactory.__clear_log_file(file_path)

        # add the handlers to the logger
        handlers = LoggerFactory.__get_handlers(file_path, logging_level)
        for handler in handlers:
            logger.addHandler(handler)
        return logger

    @staticmethod
    def __get_handlers(file_path, logging_level):
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handlers = [
            RotatingFileHandler(file_path, maxBytes=1000000, backupCount=1),
            logging.StreamHandler()
        ]

        for handler in handlers:
            handler.setLevel(logging_level)
            handler.setFormatter(formatter)

        return handlers

    @staticmethod
    def __clear_log_file(log_file_path):
        f = open(log_file_path, 'w')
        f.write(u'LOG FILE START\n')
        f.close()


