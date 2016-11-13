# This handles the transaction type that is store in the database.
from google.appengine.ext import ndb

class TransactionDB(ndb.Model):
    date = ndb.IntegerProperty()
    desc = ndb.StringProperty()
    amt = ndb.IntegerProperty()
    txn_type = ndb.StringProperty()
    id = ndb.StringProperty(indexed=True)  # date + amount