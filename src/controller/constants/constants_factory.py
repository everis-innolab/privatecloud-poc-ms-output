import logging
import os

from src.controller.constants.constants_dto import ConstantsDTO


class ConstantsFactory():

    @staticmethod
    def get_constants_dto(enviroment=None):
        if enviroment=="development":
            return ConstantsFactory.__get_development_constants()
        elif enviroment=="production":
            return ConstantsFactory.__get_production_constants()
        else:
            return None

    @staticmethod
    def __get_production_constants():
        return ConstantsDTO(
            transaction_endpoint="/transactions",
            log_endpoint="/logs",
            health_endpoint="/health",
            status_endpoint="/status",
            homepage_endpoint="/",
            webscket_endpoint="/websocket",
            filter_endpoint="/filter",
            log_file="./src/controller/logs/processing_node.log",
            default_loggin_level=logging.INFO,
            eureka_app_name="OutputHandler",
            eureka_heartbeat_interval=15,
            eureka_host= os.environ.get("EUREKA_SERVICE_SERVICE_HOST"),
            eureka_port=int(os.environ.get("EUREKA_SERVICE_SERVICE_PORT")),
            output_host="ms-output-fd.cloud.everis.com",
            output_port=80,
            mysql_host=os.environ.get("MYSQL_SERVICE_SERVICE_HOST"),
            mysql_port=int(os.environ.get("MYSQL_SERVICE_SERVICE_PORT")),
            mysql_database="transactions",
            mysql_user="innocloud",
            mysql_pass="1234"
        )

    @staticmethod
    def __get_development_constants():
        return ConstantsDTO(
            transaction_endpoint="/transactions",
            log_endpoint="/logs",
            health_endpoint="/health",
            status_endpoint="/status",
            homepage_endpoint="/",
            webscket_endpoint="/websocket",
            filter_endpoint="/filter",
            log_file="./src/controller/logs/processing_node.log",
            default_loggin_level=logging.INFO,
            eureka_app_name="OutputHandler",
            eureka_heartbeat_interval=15,
            eureka_host= "192.168.56.102",
            eureka_port=8080,
            output_host="localhost",
            output_port=9992,
            mysql_host="192.168.56.102",
            mysql_port=3306,
            mysql_database="transactions",
            mysql_user="innocloud",
            mysql_pass="1234"
        )
