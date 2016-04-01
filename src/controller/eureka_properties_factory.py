import os

from eurekalab.model.app_instance_dto import AppInstanceDTO
from eurekalab.model.eureka_server_dto import EurekaServerDTO

from src.constants import *
from src.controller.exceptions import EnviromentVariablesNotSet
from src.controller.singleton import Singleton

class EurekaPropertiesFactory(Singleton):

    def __init__(self):
        super(EurekaPropertiesFactory, self).__init__()

    def get_eureka_server_dto(self):
        host, port = self.__read_eureka_host_and_port_from_env()
        return EurekaServerDTO(
            eureka_url="http://%s"%host,
            eureka_domain_name="none",
            data_center="MyOwn",
            eureka_port=port,
            endpoint="eureka"
        )

    def __read_eureka_host_and_port_from_env(self):
        # TO-DO. Para futuras versiones esto leera las variables globales
        # para el primer despliegue usamos los valores "Hardcodeados"

        # host = os.environ.get(EUREKA_HOST_ENV)
        # port = int(os.environ.get(EUREKA_PORT_ENV))
        # if host is None or port is None:
        #     raise EnviromentVariablesNotSet()
        # return host, port
        return DEV_EUREKA_HOST_ENV, int(DEV_EUREKA_PORT_ENV)

    def get_app_instance_dto(self):
        host, port = self.__read_output_host_and_port_from_env()
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
            app_name=EUREKA_APP_NAME
        )

    def __read_output_host_and_port_from_env(self):
        # host = os.environ.get(OUTPUT_HOST_ENV)
        # El hostname debe ser accesible desde el exterior (El codigo del
        # web-frontend se ejecuta en el navegador del cliente, por lo que tiene
        # que pode abrir una conexion desde fuera)
        host = OUTPUT_EXTERIOR_HOSTNAME
        port = int(os.environ.get(OUTPUT_PORT_ENV))
        if host is None or port is None:
            raise EnviromentVariablesNotSet()
        return host, port

    def get_development_eureka_server_dto(self):
        host, port = DEV_EUREKA_HOST_ENV, int(DEV_EUREKA_PORT_ENV)
        return EurekaServerDTO(
            eureka_url="http://%s"%host,
            eureka_domain_name="none",
            data_center="MyOwn",
            eureka_port=port,
            endpoint="eureka"
        )

    def get_development_app_instance_dto(self):
        host, port = DEV_OUTPUT_HOST_ENV, int(DEV_OUTPUT_PORT_ENV)
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
            app_name=EUREKA_APP_NAME
        )
