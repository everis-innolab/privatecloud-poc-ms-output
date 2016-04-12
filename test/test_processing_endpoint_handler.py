# -*- encoding: utf-8 -*-
import copy
import json
import unittest
import sys
from mock import patch, Mock
from constants import *
#TODO This is necessary for dev, but it should be changed to a more formal way.
if sys.platform=="win32":
    os.environ[MYSQL_HOST_ENV]=DEV_MYSQL_HOST
    os.environ[MYSQL_PORT_ENV]=DEV_MYSQL_PORT
from src.controller.endpoint_handlers.transaction_endpoint_handler import \
    TransactionEndpointHandler
from src.controller.exceptions import MalformedTransactionException
from src.controller.logs.logger_factory import LoggerFactory
from src.model.transaction_dao import TransactionDAO


class TestProcessingEndpointHandler(unittest.TestCase):

    def setUp(self ):
        logger = LoggerFactory.get_logger(
            # This path is set to be used with nosetests, so do not change.
            # Rather change the Pycharm launcher instead if needed and set it
            # to xxx\ms-cloud\python\OutputHandlerNode
            "./src/controller/logs/processing_node.log", logging.INFO
        )
        #We disable the stream logger so exceptions do not print
        logger.handlers = logger.handlers[:-1]
        self.processing = TransactionEndpointHandler(None, logger)
        self.transaction_document = {
            "_id" : 0,
            "client_country" : "SK",
            "client_id" : 35,
            "commerce_tpv" : "805348991287",
            "client_credit_card" : "4756310296329932",
            "transaction_amount" : 384.1,
            "commerce_id" : 100,
            "client_country_name" : "Slovakia",
            "commerce_country" : "ES",
            "commerce_country_name" : "Spain",
            "commerce_account_iban" : "ES7231011409805348991287",
            "transaction_datetime" : "2015-06-15T18:01:32.000+0000",
            "client_name":"foo",
            "client_last_name": "bar",
            "fraud_code":1
        }

        self.transaction_dto = \
            TransactionDAO().build_from_document(self.transaction_document)

    def tearDown(self ):
        pass

    def test_malformed_transaction_return_exception_message(self):
        with patch('bottle.request', self.get_read_mock()):
            expected = MalformedTransactionException().message
            result = self.processing.handle_transaction_post_request()
            self.assertEquals(result, expected)

    def get_read_mock(self):
        transaction_dict = copy.deepcopy(self.transaction_document)
        transaction_dict.pop("client_country", None)
        m = Mock()
        m.body.read.return_value = json.dumps(transaction_dict)
        return m

if __name__ == '__main__':
    unittest.main ()
