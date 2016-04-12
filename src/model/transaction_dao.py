import json
import pprint
from peewee import Model, CharField, PrimaryKeyField, IntegerField, FloatField, \
    MySQLDatabase, IntegrityError, Node
from src.controller.exceptions import MalformedTransactionException
from src.controller.singleton import Singleton
from src.model.connection_manager import ConnectionManager
from src.model.transaction import Transaction


class TransactionDAO(Singleton):

    def __init__(self):
        super(TransactionDAO, self).__init__()

    def save_transaction(self, transaction):
        # Caution!! By default save does an update if primary key is specified, and an
        # insert if no PK was specified. To overcome this we can use insert or, maybe
        # better use the force_insert parameter of the save method.
        try:
            transaction.save(force_insert=True)
        except IntegrityError, e:
            transaction.save()

    def to_dict(self, Transaction):
        dict= {}
        dict["_id"] = Transaction._id
        dict["client_country"] = Transaction.client_country
        dict["client_id"] = Transaction.client_id
        dict["commerce_tpv"] = Transaction.commerce_tpv
        dict["client_credit_card"] = Transaction.client_credit_card
        dict["transaction_amount"] = Transaction.transaction_amount
        dict["commerce_id"] = Transaction.commerce_id
        dict["client_country_name"] = Transaction.client_country_name
        dict["commerce_country"] = Transaction.commerce_country
        dict["commerce_country_name"] = Transaction.commerce_country_name
        dict["commerce_account_iban"] = Transaction.commerce_account_iban
        dict["transaction_datetime"] = Transaction.transaction_datetime
        dict["client_name"]=Transaction.client_name
        dict["client_last_name"]=Transaction.client_last_name
        return dict

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
            fraud_code = source_doc["fraud_code"]
            client_name=source_doc["client_name"]
            client_last_name=source_doc["client_last_name"]

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
                transaction_datetime = transaction_datetime,
                client_name=client_name,
                client_last_name=client_last_name,
                fraud_code=fraud_code
            )

        except Exception, e:
            raise MalformedTransactionException()
        pass

#===============================================================================
# JSON RESPONSE DATA GENERATION
#===============================================================================
    def get_query_as_json(self, pagination=True, count=10, sort_by="id",
                          sort_order="dsc", page=1):
        """
        The current method returns a query in a specific format that the
        front-end shows. The format specification can be seen at this link:
        http://zizzamia.com/ng-tasty/directive/table-server-side/pagination

        Reglas que aplicamos:
        * No se devuelve el id, el client_id, ni el commerce_id
        * Solo se devuelve el nombre del pais, nunca su codigo
        """
        data_dict = {}

        data_dict["pagination"] = self.__get_pagination_metadata(count, page)
        data_dict["header"]=self.__get_header()
        data_dict["rows"]=self.__get_data_rows(
            pagination, count, sort_by, sort_order, page
        )
        data_dict["sort-by"] = sort_by
        data_dict["sort-order"] = sort_order
        return data_dict

    def __get_pagination_metadata(self, items_per_page, current_page):
        meta_dict = {}
        meta_dict["size"]=Transaction.select().count()
        meta_dict["page"]=current_page
        meta_dict["count"]=items_per_page
        meta_dict["pages"] = \
            self.__get_page_count(meta_dict["size"], items_per_page)
        return meta_dict

    def __get_header(self):
        keys, names = self.__get_keys_and_names_for_projection()
        headers=[]
        for index, key in enumerate(keys):
            headers.append({"key": key, "name":names[index]})
        return headers

    def __get_keys_and_names_for_projection(self):
        keys = [
            "commerce_tpv","client_credit_card","transaction_amount",
            "client_country_name","commerce_country_name",
            "commerce_account_iban","transaction_datetime","fraud_code"
        ]
        names = [
            "Commerce Tpv","Client Credit Card","Amount","Client Country",
            "Commerce Country","Commerce Account","Transaction Date",
            "Fraud Code"
        ]
        return keys, names

    def __get_page_count(self, total_count, page_size):
        page_count = total_count / page_size
        if total_count % page_size >0:
            page_count +=1
        return page_count

    def __get_data_rows(self, pagination, count, sort_by, sort_order, page,
                        where=None):
        rows = []
        keys = self.__get_keys_and_names_for_projection()[0]
        iterable = self.__get_query_as_transaction_list(
            pagination, count, sort_by, sort_order, page
        )

        for transaction in iterable:
            rows.append(self.__project_transaction_into_dict(transaction, keys))

        return rows

    def __get_query_as_transaction_list(self, pagination, count, sort_by,
                                        sort_order, page, where=None):
        order_atribute = getattr(Transaction, sort_by)
        if sort_order == "desc":
            order_method = order_atribute.desc()
        else:
            order_method = order_atribute.asc()
        if pagination is False:
            skip = 0
            limit = 0
        else:
            skip = count * (page-1)
            limit = count

        iterable = Transaction.select().order_by(order_method)\
            .offset(skip).limit(limit)

        return iterable

    def __project_transaction_into_dict(self, transaction, keys):
        projection = {}
        for key in keys:
            projection[key]=getattr(transaction, key)
        return projection
