# -*- encoding: utf8 -*-
from datetime import datetime
import bottle
from src.controller.logs.utils import Utils
from src.controller.templates.status_page_template import STATUS_PAGE_TEMPLATE

class BaseEndpointHandler(object):
    """
    It's responsability is to provide the handlers necessary to answer the
    base endpoints (status, health, homepage and logs).
    """
    def __init__(self, eureka_agent, logger):
        # self._logger = LoggerFactory.get_logger()
        self._logger = logger
        self._eureka_agent = eureka_agent

    def handle_log_get(self):
        try:
            last_log_lines = Utils.get_last_n_lines_of_file_logger(10,self._logger)
            formatted_logs = last_log_lines.replace("\n","<br>")
            return self.return_response(formatted_logs, 200)

        except Exception, e:
            self._logger.exception("Error handling logs\n")
            return self.return_response(e.message, 400)

    def return_response(self, return_data, status):
        bottle.response.status = status
        return return_data

    def handle_status_get(self):
        try:
            self._logger.info("Handled Status Request")
            template = self.__get_filled_status_template()
            return self.return_response(template, 200)
        except:
            return self.return_response("Exception in status handler", 500)

    def __get_filled_status_template(self):
        now = datetime.now()
        return bottle.template(STATUS_PAGE_TEMPLATE, time=str(now))

    def handle_health_get(self):
        """
        De momento devolvemos exactamente lo mismo que para el status page. Si
        aparece una necesidad real para hacerlo de otro modo, se modificará
        entonces.
        :return:
        """
        try:
            self._logger.info("Handled Health Request")
            template = self.__get_filled_status_template()
            return self.return_response(template, 200)
        except:
            return self.return_response("Exception in Health handler", 500)

    def handle_homepage_get(self):
        try:
            self._logger.info("Handled Homepage Request")
            template = self.__get_filled_status_template()
            return self.return_response(template, 200)
        except:
            return self.return_response("Exception in Homepage handler", 500)