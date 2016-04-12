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
FILTER_ENDPOINT="/filter"

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

MYSQL_HOST_ENV="MYSQL_SERVICE_SERVICE_HOST"
MYSQL_PORT_ENV = "MYSQL_SERVICE_SERVICE_PORT"
DEV_MYSQL_HOST="192.168.56.102"
DEV_MYSQL_PORT = "3306"
MYSQL_DATABASE = "transactions"
MYSQL_USER = "innocloud"
MYSQL_PASS = "1234"

# Values to hard-code into env variables when launching in debug
DEV_EUREKA_HOST_ENV = "eureka-fd.cloud.everis.com"
DEV_EUREKA_PORT_ENV = "80"
# DEV_EUREKA_HOST_ENV = "192.168.56.102"
# DEV_EUREKA_PORT_ENV = "8080"

DEV_OUTPUT_HOST_ENV = "localhost"
DEV_OUTPUT_PORT_ENV = "9992"

OUTPUT_EXTERIOR_HOSTNAME = "ms-output-fd.cloud.everis.com"


