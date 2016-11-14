# This handles the transaction type that is store in the database.
from google.appengine.ext import ndb

def make_key(date, desc, amt):
    return str(date) + str(desc[:5]) + str(float(amt))

# Key is equal to  str(date + amount)
class TransactionDB(ndb.Model):
    date = ndb.IntegerProperty()
    desc = ndb.StringProperty()
    amt = ndb.FloatProperty()
    txn_type = ndb.StringProperty(indexed=True)
