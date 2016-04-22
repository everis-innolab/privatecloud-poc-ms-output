import os
import sys
from src.controller.constants.constants_factory import ConstantsFactory
from src.model.connection_manager import ConnectionManager
from src.model.transaction import ProxyFactory

sys.path.append(os.getcwd())
from src.controller.eureka_properties_factory import EurekaPropertiesFactory
from controller.logs.logger_factory import LoggerFactory
from eurekalab.client import EurekaClient
from controller.endpoint_handlers.transaction_endpoint_handler import \
    TransactionEndpointHandler
from controller.eureka_agent import EurekaAgent
from controller.service_runner import ServiceRunner
from model.transaction_dao import Transaction


class Main():

    def __init__(self, logger,eureka_server_dto, my_app_instace_dto, constants_dto):
        eureka_client = EurekaClient(eureka_server_dto, my_app_instace_dto)
        self.__eureka_agent = EurekaAgent(
            eureka_client, logger, constants_dto.eureka_heartbeat_interval
        )

        self.__my_app_instance_dto = my_app_instace_dto
        self.__logger = logger
        self.__constants=constants_dto

    def launch_server(self):
        try:
            handler = \
                TransactionEndpointHandler(self.__eureka_agent, self.__logger)

            wiring = [
                (
                    self.__constants.transaction_endpoint,
                    "POST",
                    handler.handle_transaction_post_request
                ),(
                    self.__constants.webscket_endpoint,
                    "GET",
                    handler.handle_websocket_request
                ),(
                    self.__constants.filter_endpoint,
                    "GET",
                    handler.handle_filter_get_request
                )
            ]

            runner = ServiceRunner(
                handler, wiring, self.__eureka_agent, web_socket=True,
                constants_dto=self.__constants
            )

            runner.start()
        except Exception, e:
            self.__logger.exception("Exception Launching Server")
            raise e
        finally:
            self.__logger.info("De-register in eureka")
            try:
                self.__eureka_agent.de_register_in_eureka()
            except Exception:
                self.__logger.exception("Could not De-Register in eureka.")


if __name__ == "__main__":

    # Lanzar con WorkingDirectory en ..../privatecloud-poc/ms-output
    if "--develop" in sys.argv or "--development" in sys.argv:
        constants_dto = ConstantsFactory.get_constants_dto("development")
        logger = LoggerFactory.get_logger(
            constants_dto.log_file, constants_dto.default_loggin_level
        )
        logger.info("Launching OutputHandler service in development mode")
    else:
        constants_dto = ConstantsFactory.get_constants_dto("production")
        logger = LoggerFactory.get_logger(
            constants_dto.log_file, constants_dto.default_loggin_level
        )
        logger.info("Launching OutputHandler service")

    ConnectionManager().set_constants_dto(constants_dto)
    ProxyFactory.database_proxy.initialize(ConnectionManager().get_database())
    Transaction.create_table(fail_silently=True)
    eureka_factory = EurekaPropertiesFactory(constants_dto)
    main_launcher = Main(
        logger,
        eureka_factory.get_eureka_server_dto(),
        eureka_factory.get_app_instance_dto(),
        constants_dto
    )
    main_launcher.launch_server()
