import bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from src.constants import *
from src.model.connection_manager import ConnectionManager


class ServiceRunner():
    """
    This class is in charge of the endpoint --> handler wiring and starting the
    server. Furthermore, it needs to take into account whether or not the
    server needs to support websockets. Base on this specification, it has to
    launch one type or Python server or another
    """

    def __init__(self, base_endpoint_handler, route_wiring_list,
                 eureka_agent, web_socket = False):

        self._app = bottle.Bottle()
        self.__handler=base_endpoint_handler
        self.eureka_agent = eureka_agent
        self.__web_socket = web_socket
        self.__wire_standard_routes()
        self.__wire_routes_to_methods(route_wiring_list)
        self.__add_hooks()




    def __wire_standard_routes(self):
        wiring = [
            (STATUS_ENDPOINT, "GET",self.__handler.handle_status_get),
            (HEALTH_ENDPOINT, "GET",self.__handler.handle_status_get),
            (HOMEPAGE_ENDPOINT, "GET",self.__handler.handle_homepage_get),
            (LOG_ENDPOINT, "GET",self.__handler.handle_log_get)
        ]
        self.__wire_routes_to_methods(wiring)

    def __wire_routes_to_methods(self, route_wiring_list):
        if route_wiring_list is not None and len(route_wiring_list)>0:
            for endpoint, method, callback in route_wiring_list:
                self._app.route(endpoint, method, callback)
        pass

#===============================================================================
# BEFORE AND AFTER REQUEST HOOKS
#===============================================================================
    def __connect(self):
        ConnectionManager().connect()

    def __disconnect(self):
        ConnectionManager().close()

    def __add_hooks(self):
        self._app.add_hook('before_request',self.__connect )
        self._app.add_hook('after_request',self.__disconnect )

    def start(self):
        self.eureka_agent.register_in_eureka()
        port=self.eureka_agent.ec_client.app.port
        if self.__web_socket is False:
            self._app.run(host="0.0.0.0", port=port)
        else:
            server = WSGIServer(
                ("0.0.0.0", port), self._app, handler_class=WebSocketHandler
            )
            server.serve_forever()


