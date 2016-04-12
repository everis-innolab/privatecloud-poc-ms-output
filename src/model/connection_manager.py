from src.constants import *
from src.controller.singleton import Singleton
from playhouse.db_url import connect


class ConnectionManager(Singleton):

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self._db = None

    def get_database(self):
        self.__initialize_db_object_if_necessary()
        return self._db

    def __initialize_db_object_if_necessary(self):
        if self._db is None:
            self._db = connect('mysql://%s:%s@%s:%d/%s'%(
                MYSQL_USER,
                MYSQL_PASS,
                os.environ[MYSQL_HOST_ENV],
                int(os.environ[MYSQL_PORT_ENV]),
                MYSQL_DATABASE
            ))
