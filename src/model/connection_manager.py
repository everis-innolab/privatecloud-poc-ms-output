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

    def connect(self):
        self._db.connect()

    def close(self):
         self._db.close()

    def reconnect(self):
        """
        This automatically manages a pool of connections.

        http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pool
        """
        self._db = PooledMySQLDatabase(
            database=MYSQL_DATABASE,
            max_connections=4,
            stale_timeout=300,
            **{
                'host': os.environ[MYSQL_HOST_ENV],
                'port': int(os.environ[MYSQL_PORT_ENV]),
                'user': MYSQL_USER,
                'password':MYSQL_PASS
            }
        )



