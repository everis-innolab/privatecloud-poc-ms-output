import os
from eurekalab.model.app_instance_dto import AppInstanceDTO
from eurekalab.model.eureka_server_dto import EurekaServerDTO
from src.controller.singleton import Singleton

class EurekaPropertiesFactory(Singleton):

    def __init__(self, constants_dto):
        super(EurekaPropertiesFactory, self).__init__()
        self.__constants_dto = constants_dto

    def get_eureka_server_dto(self):
        host = self.__constants_dto.eureka_host
        port = self.__constants_dto.eureka_port
        return EurekaServerDTO(
            eureka_url="http://%s"%host,
            eureka_domain_name="none",
            data_center="MyOwn",
            eureka_port=port,
            endpoint="eureka"
        )

    def get_app_instance_dto(self):
        host = self.__constants_dto.output_host
        port = self.__constants_dto.output_port
        return AppInstanceDTO(
            vip_address="none",
            secure_vip_address="none",
            port=port,
            host_name=host,
            secure_port=443,
            ip_addr=host,
            home_page_url="http://%s:%s"%(host, port),
            health_check_url="http://%s:%s/health"%(host, port),
            status_page_url="http://%s:%s/status"%(host, port),
            status="STARTING",
            app_name=self.__constants_dto.eureka_app_name
        )