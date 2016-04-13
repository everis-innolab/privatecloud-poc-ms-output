import sys
import os
sys.path.append(os.getcwd())
from constants import *
#TODO This is necessary for dev, but it should be changed to a more formal way.
if sys.platform=="win32":
    os.environ[MYSQL_HOST_ENV]=DEV_MYSQL_HOST
    os.environ[MYSQL_PORT_ENV]=DEV_MYSQL_PORT
from src.controller.eureka_properties_factory import EurekaPropertiesFactory
from controller.logs.logger_factory import LoggerFactory
from eurekalab.client import EurekaClient
from controller.endpoint_handlers.transaction_endpoint_handler import \
    TransactionEndpointHandler
from controller.eureka_agent import EurekaAgent
from controller.service_runner import ServiceRunner
from model.transaction_dao import Transaction


class Main():

    def __init__(self, logger,eureka_server_dto, my_app_instace_dto):
        eureka_client = EurekaClient(eureka_server_dto, my_app_instace_dto)
        self.__eureka_agent = EurekaAgent(eureka_client, logger)
        self.__my_app_instance_dto = my_app_instace_dto
        self.__logger = logger


    def launch_server(self):
        try:
            handler = \
                TransactionEndpointHandler(self.__eureka_agent, self.__logger)


            wiring = [
                (TRANSACTION_ENDPOINT, "POST", handler.handle_transaction_post_request),
                (WEBSOCKET_ENDPOINT, "GET", handler.handle_websocket_request),
                (FILTER_ENDPOINT, "GET", handler.handle_filter_get_request())
            ]

            runner = ServiceRunner(
                handler, wiring, self.__eureka_agent, web_socket=True
            )

            runner.start()
        except Exception, e:
            self.__logger.exception("Exception Launching Server")
            raise e
        finally:
            self.__eureka_agent.de_register_in_eureka()
            self.__logger.info("De-register in eureka")

if __name__ == "__main__":
    # Lanzar con WorkingDirectory en ..../privatecloud-poc/ms-output

    logger = LoggerFactory.get_logger(LOG_FILE, DEFAULT_LOGGIN_LEVEL)

    factory = EurekaPropertiesFactory()
    if "--develop" in sys.argv or "--development" in sys.argv:
        eureka_dto = factory.get_development_eureka_server_dto()
        my_app_dto = factory.get_development_app_instance_dto()
        logger.info("Launching OutputHandler service in development mode")

    else:
        eureka_dto = factory.get_eureka_server_dto()
        my_app_dto = factory.get_app_instance_dto()
        logger.info("Launching OutputHandler service")

    Transaction.create_table(fail_silently=True)
    main_launcher = Main(logger, eureka_dto, my_app_dto)
    main_launcher.launch_server()



