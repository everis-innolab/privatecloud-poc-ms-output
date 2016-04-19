# -*- encoding: utf8 -*-
import json
import bottle
from gevent import monkey, sleep
from src.controller.endpoint_handlers.base_endpoint_handler import \
    BaseEndpointHandler
from src.controller.exceptions import MalformedTransactionException
from src.model.connection_manager import ConnectionManager
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
            ConnectionManager().reconnect()
            self._logger.info("Processing Transaction Request")
            transaction = self.__get_transaction_from_body()
            self._logger.info("Saving Transaction")
            TransactionDAO().save_transaction(transaction)
            self._logger.info("Fraud Code: %s"%(transaction.fraud_code))
            if transaction.fraud_code is not 0:
                self.__send_transaction_to_all_websockets(transaction)

            self._logger.info("Handled Transaction Request")
            return self.return_response("OK", 201)

        except MalformedTransactionException, e:
            self._logger.exception("Malformed Transaction, returning 400")
            return self.return_response(e.message, 400)
        except Exception, e:
            self._logger.exception("Error handling transaction. returning 500")
            return self.return_response(e.message, 500)

        finally:
            ConnectionManager().close_connection()

    def __get_transaction_from_body(self):
        body_str = bottle.request.body.read()
        doc = json.loads(body_str)
        return TransactionDAO().build_from_document(doc)

    def __send_transaction_to_all_websockets(self, transaction_dto):
        self._logger.info(
            "Trying to send transaction to %s websockets"%
            str(len(self.active_websockets))
        )

        if len(self.active_websockets)>0:
            for wsock in self.active_websockets:
                self._logger.info("Sending Transaction to websocket")
                self.__send_transaction_to_websocket(wsock, transaction_dto)
            self.transaction_buffer = []

    def __send_transaction_to_websocket(self, websocket, transaction_dto):
        try:
            doc = TransactionDAO().to_dict(transaction_dto)
            websocket.send(json.dumps(doc))
            self._logger.info("Transaction sent")
        except Exception, e:
            self._logger.exception("Exception sending transaction, Websocket "
                                  "might have been closed by the other part.")
            self.active_websockets.remove(websocket)

    def handle_filter_get_request(self):
        # params : page=1&count=5&pagination=true&sortBy=id&sortOrder=asc
        # paramsObj : {"pagination":true,"count":5,"sortBy":"name",
        # "sortOrder":"dsc","page":1}

        try:
            ConnectionManager().reconnect()
            self._logger.info("Processing Filter Request")
            pagination, count, sort_by, sort_order, page, query = \
                self.__read_filter_query_params()

            response = TransactionDAO().get_query_as_json(
                pagination=pagination,
                count=count,
                sort_by=sort_by,
                sort_order=sort_order,
                page=page,
                query=query
            )
            self._logger.info("Handled Filter Request")
            bottle.response.content_type = 'application/json'
            # bottle.response.headers["Access-Control-Allow-Origin"] = "*.cloud.everis.com"
            bottle.response.headers["Access-Control-Allow-Origin"] = "*"
            bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
            bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            return self.return_response(json.dumps(response), 200)
        except Exception, e:
            self._logger.exception("Exception handling filter request returning 500")
            return self.return_response(e.message, 500)
        finally:
            ConnectionManager().close_connection()


    def __read_filter_query_params(self):
        try:
            pagination = bottle.request.query.pagination or True
            count = int(bottle.request.query.count or '5')
            sort_by = bottle.request.query.sortBy or "id"
            sort_order = bottle.request.query.sortOrder or "asc"
            page = int(bottle.request.query.page or '1')
            query = bottle.request.query.query or ""

            string = "Read params pagination: %s, count: %s, sort_by: %s, " \
                     "sort_order: %s, page: %s, query: %s"
            formatted_str = \
                string%(pagination, count, sort_by, sort_order, page, query)

            self._logger.info(formatted_str)
            return pagination, count, sort_by, sort_order, page, query

        except Exception, e:
            self._logger.exception("Error parsing filter query params")
            raise e