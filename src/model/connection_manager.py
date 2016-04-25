from peewee import MySQLDatabase
from playhouse.shortcuts import RetryOperationalError
from src.controller.singleton import Singleton


class ConnectionManager(Singleton):

    _constants_dto=None

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self._db = None

    def set_constants_dto(self, constants_dto):
        ConnectionManager._constants_dto=constants_dto

    def get_database(self):
        if self._db is None:
            self.reconnect()
        return self._db

    def close(self):
        if self._db is not None and not self._db.is_closed():
            self._db.close()

    def reconnect(self):
        self._db = MyRetryDB(
            database=ConnectionManager._constants_dto.mysql_database,
            host= ConnectionManager._constants_dto.mysql_host,
            port= ConnectionManager._constants_dto.mysql_port,
            user= ConnectionManager._constants_dto.mysql_user,
            password=ConnectionManager._constants_dto.mysql_pass
        )

class MyRetryDB(RetryOperationalError, MySQLDatabase):
    pass