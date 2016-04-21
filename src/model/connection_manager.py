from peewee import MySQLDatabase
from playhouse.shortcuts import RetryOperationalError

from src.constants import *
from src.controller.singleton import Singleton
from playhouse.db_url import connect
from playhouse.pool import PooledMySQLDatabase




class ConnectionManager(Singleton):

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self._db = None
        self.reconnect()

    def get_database(self):
        return self._db

    def close(self):
        if self._db is not None and not self._db.is_closed():
            self._db.close()

    def reconnect(self):
        """
        This automatically manages a pool of connections.

        http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pool
        """
        # self._db = MySQLDatabase(
        self._db = MyRetryDB(
            database=MYSQL_DATABASE,
            host= os.environ[MYSQL_HOST_ENV],
            port= int(os.environ[MYSQL_PORT_ENV]),
            user= MYSQL_USER,
            password=MYSQL_PASS
        )
        # self._db.get_conn().ping(True)

class MyRetryDB(RetryOperationalError, MySQLDatabase):
    pass