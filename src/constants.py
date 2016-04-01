# -*- encoding: utf-8 -*-
## ENDPOINTS
import logging
import os

TRANSACTION_ENDPOINT="/transactions"
LOG_ENDPOINT="/logs"
HEALTH_ENDPOINT="/health"
STATUS_ENDPOINT="/status"
HOMEPAGE_ENDPOINT="/"
WEBSOCKET_ENDPOINT="/websocket"

# Do not change, the python path of execution is xxx\OutputHandlerNode
LOG_FILE = "./src/controller/logs/processing_node.log"
DEFAULT_LOGGIN_LEVEL = logging.INFO
EUREKA_APP_NAME = "OutputHandler"
EUREKA_HEARTBEAT_INTERVAL = 25

#Kubernetes Enviroment Variables
EUREKA_HOST_ENV = "EUREKA_SERVICE_SERVICE_HOST"
EUREKA_PORT_ENV = "EUREKA_SERVICE_SERVICE_PORT"
OUTPUT_HOST_ENV = "MS_OUTPUT_SERVICE_SERVICE_HOST"
OUTPUT_PORT_ENV = "MS_OUTPUT_SERVICE_SERVICE_PORT"

#Values to hard-code into env variables when launching in debug
DEV_EUREKA_HOST_ENV = "eureka-fd.cloud.everis.com"
DEV_EUREKA_PORT_ENV = "80"
DEV_OUTPUT_HOST_ENV = "localhost"
DEV_OUTPUT_PORT_ENV = "9992"

OUTPUT_EXTERIOR_HOSTNAME = "ms-output-fd.cloud.everis.com"

"""
MySQL - Es probable que el MySQL este fuera de openshift. Lo que sí es seguro
es que no estará registrado en Eureka. Por lo tanto podemos:
    * Asignarle la IP del servicio MySQL (172.30.75.11 por ej.)
    * Utilizar la variable de entorno del contenedor MYSQL_SERVICE_SERVICE_HOST
"""

# MYSQL_HOST = "################### --> SET-ME <-- ##############################"
# MYSQL_PORT = 3306

MYSQL_HOST=os.environ.get("MYSQL_SERVICE_SERVICE_HOST")
MYSQL_PORT = int(os.environ.get("MYSQL_SERVICE_SERVICE_PORT"))
MYSQL_DATABASE = "transactions"
MYSQL_USER = "innocloud"
MYSQL_PASS = "1234"
