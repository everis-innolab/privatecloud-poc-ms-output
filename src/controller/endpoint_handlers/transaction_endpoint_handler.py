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

    def handle_websocket_request(self):
        self._logger.info("handle websocket")
        # Here we do just the bare minimun to mantain the websocket active
        # until it's taken out of the active connections
        wsock = bottle.request.environ.get('wsgi.websocket')
        self.active_websockets.append(wsock)
        while True:
            if wsock not in self.active_websockets:
                break
            sleep(0.2)

    def handle_transaction_post_request(self):
        try:
            self._logger.info("Processing Transaction Request")
            transaction = self.__get_transaction_from_body()
            self._logger.info("Saving Transaction")
            TransactionDAO().save_transaction(transaction)
            self.__send_transaction_to_all_websockets(transaction)
            self._logger.info("Handled Transaction Request")
            return self.return_response("OK", 201)

        except MalformedTransactionException, e:
            self._logger.exception("Malformed Transaction, returning 400")
            return self.return_response(e.message, 400)
        except Exception, e:
            self._logger.exception("Error handling transaction. returning 500")
            return self.return_response(e.message, 500)

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

    def handle_filter_get_request(self):
        # params : page=1&count=5&pagination=true&sortBy=id&sortOrder=asc
        # paramsObj : {"pagination":true,"count":5,"sortBy":"name",
        # "sortOrder":"dsc","page":1}

        try:
            self._logger.info("Processing Filter Request")
            pagination, count, sort_by, sort_order, page = \
                self.__read_filter_query_params()

            response = TransactionDAO().get_query_as_json(
                pagination=pagination,
                count=count,
                sort_by=sort_by,
                sort_order=sort_order,
                page=page
            )
            self._logger.info("Handled Filter Request")
            bottle.response.content_type = 'application/json'
            return self.return_response(json.dumps(response), 200)
        except Exception, e:
            self._logger.exception("Exception handling filter request returning 500")
            return self.return_response(e.message, 500)


    def __read_filter_query_params(self):
        try:
            pagination = bottle.request.query.pagination or True
            count = int(bottle.request.query.count or '5')
            sort_by = bottle.request.query.sortBy or "id"
            sort_order = bottle.request.query.sortOrder or "asc"
            page = int(bottle.request.query.page or '1')

            string = "Read params pagination: %s, count: %s, sort_by: %s, " \
                     "sort_order: %s, page: %s"
            formatted_str = string%(pagination, count, sort_by, sort_order, page)
            self._logger.info(formatted_str)
            return pagination, count, sort_by, sort_order, page

        except Exception, e:
            self._logger.exception("Error parsing filter query params")
            raise e







