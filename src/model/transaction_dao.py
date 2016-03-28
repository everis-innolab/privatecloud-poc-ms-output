from peewee import Model, CharField, PrimaryKeyField, IntegerField, FloatField, \
    MySQLDatabase, IntegrityError
from src.controller.exceptions import MalformedTransactionException
from src.controller.singleton import Singleton
from playhouse.db_url import connect

from src.model.connection_manager import ConnectionManager
from src.model.transaction import Transaction


class TransactionDAO(Singleton):


    def __init__(self):
        super(TransactionDAO, self).__init__()
        self._db = ConnectionManager().get_database()

    def save_transaction(self, transaction):
        # Caution!! By default save does an update if primary key is specified, and an
        # insert if no PK was specified. To overcome this we can use insert or, maybe
        # better use the force_insert parameter of the save method.
        try:
            transaction.save(force_insert=True)
        except IntegrityError, e:
            transaction.save()

    def to_dict(self, peewee_dto):
        my_dict ={}
        my_dict["_id"] = peewee_dto.id
        my_dict["client_country"] = peewee_dto.client_country
        my_dict["client_id"] = peewee_dto.client_id
        my_dict["commerce_tpv"] = peewee_dto.commerce_tpv
        my_dict["client_credit_card"] = peewee_dto.client_credit_card
        my_dict["transaction_amount"] = peewee_dto.transaction_amount
        my_dict["commerce_id"] = peewee_dto.commerce_id
        my_dict["client_country_name"] = peewee_dto.client_country_name
        my_dict["commerce_country"] = peewee_dto.commerce_country
        my_dict["commerce_country_name"] = peewee_dto.commerce_country_name
        my_dict["commerce_account_iban"] = peewee_dto.commerce_account_iban
        my_dict["transaction_datetime"] = peewee_dto.transaction_datetime
        return my_dict

    def build_from_document(self, source_doc):
        try:
            id = source_doc.get("_id", None)
            client_country = source_doc["client_country"]
            client_id = source_doc["client_id"]
            commerce_tpv = source_doc.get("commerce_tpv", None)
            client_credit_card = source_doc["client_credit_card"]
            transaction_amount = source_doc["transaction_amount"]
            commerce_id = source_doc["commerce_id"]
            client_country_name = source_doc["client_country_name"]
            commerce_country = source_doc["commerce_country"]
            commerce_country_name = source_doc["commerce_country_name"]
            commerce_account_iban = source_doc["commerce_account_iban"]
            transaction_datetime = source_doc["transaction_datetime"]

            return Transaction(
                id = id,
                client_country = client_country,
                client_id = client_id,
                commerce_tpv = commerce_tpv,
                client_credit_card = client_credit_card,
                transaction_amount = transaction_amount,
                commerce_id = commerce_id,
                client_country_name = client_country_name,
                commerce_country = commerce_country,
                commerce_country_name = commerce_country_name,
                commerce_account_iban = commerce_account_iban,
                transaction_datetime = transaction_datetime
            )

        except Exception, e:
            raise MalformedTransactionException()
