class ConstantsDTO(object):

    def __init__(self, transaction_endpoint=None, log_endpoint=None,
                 health_endpoint=None, status_endpoint=None,
                 homepage_endpoint=None, webscket_endpoint=None,
                 filter_endpoint=None, log_file=None, default_loggin_level=None,
                 eureka_app_name=None, eureka_heartbeat_interval=None,
                 eureka_host=None, eureka_port=None, output_host=None,
                 output_port=None, output_exterior_hostname=None,
                 mysql_host=None, mysql_port=None, mysql_database=None,
                 mysql_user=None, mysql_pass=None):

        self.__transaction_endpoint = transaction_endpoint
        self.__log_endpoint = log_endpoint
        self.__health_endpoint = health_endpoint
        self.__status_endpoint = status_endpoint
        self.__homepage_endpoint = homepage_endpoint
        self.__webscket_endpoint = webscket_endpoint
        self.__filter_endpoint = filter_endpoint
        self.__log_file = log_file
        self.__default_loggin_level = default_loggin_level
        self.__eureka_app_name = eureka_app_name
        self.__eureka_heartbeat_interval = eureka_heartbeat_interval
        self.__eureka_host = eureka_host
        self.__eureka_port = eureka_port
        self.__output_host = output_host
        self.__output_port = output_port
        self.__output_exterior_hostname = output_exterior_hostname
        self.__mysql_host = mysql_host
        self.__mysql_port = mysql_port
        self.__mysql_database = mysql_database
        self.__mysql_user = mysql_user
        self.__mysql_pass = mysql_pass

##DC:==========================================================================
##DC: GETTERS
##DC:==========================================================================

    @property
    def transaction_endpoint(self):
        return self.__transaction_endpoint

    @property
    def log_endpoint(self):
        return self.__log_endpoint

    @property
    def health_endpoint(self):
        return self.__health_endpoint

    @property
    def status_endpoint(self):
        return self.__status_endpoint

    @property
    def homepage_endpoint(self):
        return self.__homepage_endpoint

    @property
    def webscket_endpoint(self):
        return self.__webscket_endpoint

    @property
    def filter_endpoint(self):
        return self.__filter_endpoint

    @property
    def log_file(self):
        return self.__log_file

    @property
    def default_loggin_level(self):
        return self.__default_loggin_level

    @property
    def eureka_app_name(self):
        return self.__eureka_app_name

    @property
    def eureka_heartbeat_interval(self):
        return self.__eureka_heartbeat_interval

    @property
    def eureka_host(self):
        return self.__eureka_host

    @property
    def eureka_port(self):
        return self.__eureka_port

    @property
    def output_host(self):
        return self.__output_host

    @property
    def output_port(self):
        return self.__output_port

    @property
    def output_exterior_hostname(self):
        return self.__output_exterior_hostname

    @property
    def mysql_host(self):
        return self.__mysql_host

    @property
    def mysql_port(self):
        return self.__mysql_port

    @property
    def mysql_database(self):
        return self.__mysql_database

    @property
    def mysql_user(self):
        return self.__mysql_user

    @property
    def mysql_pass(self):
        return self.__mysql_pass

##DC:==========================================================================
##DC: SETTERS
##DC:==========================================================================

    @transaction_endpoint.setter
    def transaction_endpoint(self, transaction_endpoint):
        self.__transaction_endpoint = transaction_endpoint

    @log_endpoint.setter
    def log_endpoint(self, log_endpoint):
        self.__log_endpoint = log_endpoint

    @health_endpoint.setter
    def health_endpoint(self, health_endpoint):
        self.__health_endpoint = health_endpoint

    @status_endpoint.setter
    def status_endpoint(self, status_endpoint):
        self.__status_endpoint = status_endpoint

    @homepage_endpoint.setter
    def homepage_endpoint(self, homepage_endpoint):
        self.__homepage_endpoint = homepage_endpoint

    @webscket_endpoint.setter
    def webscket_endpoint(self, webscket_endpoint):
        self.__webscket_endpoint = webscket_endpoint

    @filter_endpoint.setter
    def filter_endpoint(self, filter_endpoint):
        self.__filter_endpoint = filter_endpoint

    @log_file.setter
    def log_file(self, log_file):
        self.__log_file = log_file

    @default_loggin_level.setter
    def default_loggin_level(self, default_loggin_level):
        self.__default_loggin_level = default_loggin_level

    @eureka_app_name.setter
    def eureka_app_name(self, eureka_app_name):
        self.__eureka_app_name = eureka_app_name

    @eureka_heartbeat_interval.setter
    def eureka_heartbeat_interval(self, eureka_heartbeat_interval):
        self.__eureka_heartbeat_interval = eureka_heartbeat_interval

    @eureka_host.setter
    def eureka_host(self, eureka_host):
        self.__eureka_host = eureka_host

    @eureka_port.setter
    def eureka_port(self, eureka_port):
        self.__eureka_port = eureka_port

    @output_host.setter
    def output_host(self, output_host):
        self.__output_host = output_host

    @output_port.setter
    def output_port(self, output_port):
        self.__output_port = output_port

    @output_exterior_hostname.setter
    def output_exterior_hostname(self, output_exterior_hostname):
        self.__output_exterior_hostname = output_exterior_hostname

    @mysql_host.setter
    def mysql_host(self, mysql_host):
        self.__mysql_host = mysql_host

    @mysql_port.setter
    def mysql_port(self, mysql_port):
        self.__mysql_port = mysql_port

    @mysql_database.setter
    def mysql_database(self, mysql_database):
        self.__mysql_database = mysql_database

    @mysql_user.setter
    def mysql_user(self, mysql_user):
        self.__mysql_user = mysql_user

    @mysql_pass.setter
    def mysql_pass(self, mysql_pass):
        self.__mysql_pass = mysql_pass

    def __eq__(self, other):
        return (
            self.transaction_endpoint == other.transaction_endpoint and
            self.log_endpoint == other.log_endpoint and
            self.health_endpoint == other.health_endpoint and
            self.status_endpoint == other.status_endpoint and
            self.homepage_endpoint == other.homepage_endpoint and
            self.webscket_endpoint == other.webscket_endpoint and
            self.filter_endpoint == other.filter_endpoint and
            self.log_file == other.log_file and
            self.default_loggin_level == other.default_loggin_level and
            self.eureka_app_name == other.eureka_app_name and
            self.eureka_heartbeat_interval == other.eureka_heartbeat_interval and
            self.eureka_host == other.eureka_host and
            self.eureka_port == other.eureka_port and
            self.output_host == other.output_host and
            self.output_port == other.output_port and
            self.output_exterior_hostname == other.output_exterior_hostname and
            self.mysql_host == other.mysql_host and
            self.mysql_port == other.mysql_port and
            self.mysql_database == other.mysql_database and
            self.mysql_user == other.mysql_user and
            self.mysql_pass == other.mysql_pass
        )

    def __str__(self):
        return (
            'transaction_endpoint: %s\n'%str(self.__transaction_endpoint)+
            'log_endpoint: %s\n'%str(self.__log_endpoint)+
            'health_endpoint: %s\n'%str(self.__health_endpoint)+
            'status_endpoint: %s\n'%str(self.__status_endpoint)+
            'homepage_endpoint: %s\n'%str(self.__homepage_endpoint)+
            'webscket_endpoint: %s\n'%str(self.__webscket_endpoint)+
            'filter_endpoint: %s\n'%str(self.__filter_endpoint)+
            'log_file: %s\n'%str(self.__log_file)+
            'default_loggin_level: %s\n'%str(self.__default_loggin_level)+
            'eureka_app_name: %s\n'%str(self.__eureka_app_name)+
            'eureka_heartbeat_interval: %s\n'%str(self.__eureka_heartbeat_interval)+
            'eureka_host: %s\n'%str(self.__eureka_host)+
            'eureka_port: %s\n'%str(self.__eureka_port)+
            'output_host: %s\n'%str(self.__output_host)+
            'output_port: %s\n'%str(self.__output_port)+
            'output_exterior_hostname: %s\n'%str(self.__output_exterior_hostname)+
            'mysql_host: %s\n'%str(self.__mysql_host)+
            'mysql_port: %s\n'%str(self.__mysql_port)+
            'mysql_database: %s\n'%str(self.__mysql_database)+
            'mysql_user: %s\n'%str(self.__mysql_user)+
            'mysql_pass: %s\n'%str(self.__mysql_pass)
        )