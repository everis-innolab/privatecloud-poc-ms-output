from peewee import Model, IntegerField, CharField, FloatField
from src.model.connection_manager import ConnectionManager


class BaseModel(Model):
    class Meta:
        database = ConnectionManager().get_database()
        auto_increment = False


class Transaction(BaseModel):
    # Carefull!! f you always want to have control over the primary key,
    # simply do not use the PrimaryKeyField field type, but use a normal
    # IntegerField (or other column type)
    # id = PrimaryKeyField()
    id = IntegerField(primary_key=True)
    client_country = CharField()
    client_id = IntegerField()
    commerce_tpv = CharField()
    client_credit_card = CharField(null= False)
    transaction_amount = FloatField(null= False)
    commerce_id = IntegerField()
    client_country_name = CharField()
    commerce_country = CharField()
    commerce_country_name = CharField()
    commerce_account_iban = CharField(null= False)
    transaction_datetime = CharField()
    fraud_code = IntegerField()
    client_name = CharField()
    client_last_name = CharField()


    def __eq__(self, other):
        return (
            self._id == other._id and
            self.client_country == other.client_country and
            self.client_id == other.client_id and
            self.commerce_tpv == other.commerce_tpv and
            self.client_credit_card == other.client_credit_card and
            self.transaction_amount == other.transaction_amount and
            self.commerce_id == other.commerce_id and
            self.client_country_name == other.client_country_name and
            self.commerce_country == other.commerce_country and
            self.commerce_country_name == other.commerce_country_name and
            self.commerce_account_iban == other.commerce_account_iban and
            self.transaction_datetime == other.transaction_datetime and
            self.fraud_code == other.fraud_code and
            self.client_name == other.client_name and
            self.client_last_name == other.client_laste_name
        )

    def __str__(self):
        return (
            '_id: %s\n'%str(self.id)+
            'client_country: %s\n'%str(self.client_country)+
            'client_id: %s\n'%str(self.client_id)+
            'commerce_tpv: %s\n'%str(self.commerce_tpv)+
            'client_credit_card: %s\n'%str(self.client_credit_card)+
            'transaction_amount: %s\n'%str(self.transaction_amount)+
            'commerce_id: %s\n'%str(self.commerce_id)+
            'client_country_name: %s\n'%str(self.client_country_name)+
            'commerce_country: %s\n'%str(self.commerce_country)+
            'commerce_country_name: %s\n'%str(self.commerce_country_name)+
            'commerce_account_iban: %s\n'%str(self.commerce_account_iban)+
            'transaction_datetime: %s\n'%str(self.transaction_datetime) +
            'client_name: %s\n'%str(self.client_name) +
            'client_last_name: %s\n'%str(self.client_last_name) +
            'fraud_code: %s\n'%str(self.fraud_code)
        )