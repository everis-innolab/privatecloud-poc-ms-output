# -*- encoding: utf8 -*-
import json
import bottle
from gevent import monkey, sleep
from src.controller.endpoint_handlers.base_endpoint_handler import \
    BaseEndpointHandler
from src.controller.exceptions import MalformedTransactionException
from src.model.transaction_dao import TransactionDAO
monkey.patch_all()


class TransactionEndpointHandler(BaseEndpointHandler):

    def __init__(self, eureka_agent, logger):
        super(TransactionEndpointHandler, self).__init__(eureka_agent, logger)
        self.active_websockets = []

    def handle_websocket(self):
        self._logger.info("handle websocket")
        # Here we do just the bare minimun to mantain the websocket active
        # until it's taken out of the active connections
        wsock = bottle.request.environ.get('wsgi.websocket')
        self.active_websockets.append(wsock)
        while True:
            if wsock not in self.active_websockets:
                break
            sleep(0.2)

    def handle_transaction_post(self):
        try:
            self._logger.info("Processing Transaction Request")
            transaction = self.__get_transaction_from_body()
            self._logger.info("Saving Transaction exception")
            TransactionDAO().save_transaction(transaction)
            self.__send_transaction_to_all_websockets(transaction)
            self._logger.info("Handled Transaction Request")
            return self.return_response("OK", 201)

        except MalformedTransactionException, e:
            self._logger.info("Malformed Transaction, returnin 400")
            return self.return_response(e.message, 400)

    def __get_transaction_from_body(self):
        body_str = bottle.request.body.read()
        doc = json.loads(body_str)
        return TransactionDAO().build_from_document(doc)

    def __send_transaction_to_all_websockets(self, transaction_dto):
        if len(self.active_websockets)>0:
            for wsock in self.active_websockets:
                self.__send_transaction_to_websocket(wsock, transaction_dto)
            self.transaction_buffer = []

    def __send_transaction_to_websocket(self, websocket, transaction_dto):
        try:
            doc = TransactionDAO().to_dict(transaction_dto)
            websocket.send(json.dumps(doc))
        except Exception, e:
            self.active_websockets.remove(websocket)




