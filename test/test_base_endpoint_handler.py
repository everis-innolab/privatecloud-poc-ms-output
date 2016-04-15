# -*- encoding: utf-8 -*-
import logging
import unittest
from mock import patch, Mock, mock_open, MagicMock
from src.controller.endpoint_handlers.base_endpoint_handler import \
    BaseEndpointHandler
from src.controller.logs.logger_factory import LoggerFactory


class TestBaseEndpointHandler(unittest.TestCase):

    def setUp(self ):
        logger = LoggerFactory.get_logger(
            # This path is set to be used with nosetests, so do not change.
            # Rather change the Pycharm launcher instead if needed and set it
            # to xxx\ms-cloud\python\OutputHandlerNode
            "./src/controller/logs/processing_node.log", logging.INFO
        )
        #We disable the stream logger so exceptions do not print
        logger.handlers = logger.handlers[:-1]
        self.handler = BaseEndpointHandler(None, logger)

    def tearDown(self ):
        pass

    def test_log_endpoint_reads_file(self):
        input = "Test\nstring\nfor\nlog\nfile"
        expected = "Test<br>string<br>for<br>log<br>file"

        m = self.get_mock_for_file_open(input, 28)
        with patch('__builtin__.open', m) as mock:
            result = self.handler.handle_log_get()
        self.assertEquals(expected, result)

    def get_mock_for_file_open(self, file_text, file_bytes):
        mock = MagicMock(spec=file)
        handle = MagicMock(spec=file)
        handle.write.return_value = None
        handle.read.return_value = file_text
        handle.tell.return_value = file_bytes
        handle.__enter__.return_value = handle
        """
        This is the tricky part. You have to specified a return_value to the
        mock intself. This way, when the test_subject calls open() the handle
        mock will be returned.

        If you do not assign a return_value to mock, then a random new mock
        will be returned to the test subject, which will have no values set
        for read() or tell().
        """
        mock.return_value = handle
        return mock

if __name__ == '__main__':
    unittest.main()