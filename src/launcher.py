import sys
import os
sys.path.append(os.getcwd())
from src.controller.eureka_properties_factory import EurekaPropertiesFactory
import constants
from controller.logs.logger_factory import LoggerFactory
from eurekalab.client import EurekaClient
from constants import *
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
            my_handler = \
                TransactionEndpointHandler(self.__eureka_agent, self.__logger)
            wiring = [
                (TRANSACTION_ENDPOINT, "POST", my_handler.handle_transaction_post),
                (WEBSOCKET_ENDPOINT, "GET", my_handler.handle_websocket)
            ]
            runner = ServiceRunner(
                my_handler, wiring, self.__eureka_agent, web_socket=True
            )
            runner.start()
        except Exception, e:
            self.__logger.exception("Exception Launching Server")
            raise e
        finally:
            self.__eureka_agent.de_register_in_eureka()
            self.__logger.info("De-register in eureka")

if __name__ == "__main__":
    # Lanzar con WorkingDirectory en ms-cloud\python\OutputHandlerNode

    logger = LoggerFactory.get_logger(
        constants.LOG_FILE, constants.DEFAULT_LOGGIN_LEVEL
    )

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



