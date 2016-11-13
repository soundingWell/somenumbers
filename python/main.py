#!/usr/bin/python

### GAE ###
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

### Basics ###
import json
import sys
sys.path.append('python/')

### Mine ###
from transaction_db import TransactionDB
from transaction_db import make_key
import transaction_list


SAVINGS_FILE = 'statements/savings/Chase0256_Activity_20161111.CSV'
CHECKING_FILE = 'statements/checking/Chase5851_Activity_20161111.CSV'
CREDIT_FILE = 'statements/card/Chase9147_Activity_20161106.CSV'

# Returns savings, checking, credit txn lists in json form.
def get_txn_lists():
    savings_txn_list = transaction_list.txn_list_from_csv(SAVINGS_FILE)
    checking_txn_list = transaction_list.txn_list_from_csv(CHECKING_FILE)
    credit_txn_list = transaction_list.txn_list_from_csv(CREDIT_FILE)

    return savings_txn_list, checking_txn_list, credit_txn_list

# Displays pie charts of expenses..
class ExpensesHandler(webapp.RequestHandler):
        
    # Send list of entered txns.
    def get(self):
        db_txns = TransactionDB.query()
        txn_list = transaction_list.TransactionList()
        for db_txn in db_txns:
            if db_txn.txn_type is not '':
                txn_list.txns.append(transaction_list.Transaction(date=db_txn.date,
                                                                  desc=db_txn.desc,
                                                                  amount=db_txn.amt,
                                                                  balance=0,
                                                                  txn_type=db_txn.txn_type))
        
        template_values = {
            'db_txns': txn_list.toJSON(),
            'length': json.dumps(len(txn_list.txns))
        }
        
        path = 'html/expenses.html'
        self.response.out.write(template.render(path, template_values)) 
       

class ModExpensesHandler(webapp.RequestHandler):
    # User chose a type for a txn. Enter it into the db.
    # If that type = 'Remove', remove the txn from the db.
    def post(self):
        txn_json = self.request.body
        json_py = json.loads(txn_json)
        
        txn_db = TransactionDB(date=int(json_py['date']), 
                               desc=str(json_py['desc']), 
                               amt=int(json_py['amt']),  
                               txn_type=str(json_py['txn_type']))
        
        txn_key = make_key(json_py['date'], json_py['desc'], json_py['amt'])
        txn_db.key = ndb.Key(TransactionDB, txn_key)
        txn_db.put()
            
        
    # Read db, send list of entries in the db. Allow user to change txn_type
    def get(self):
        savings_txn_list, checking_txn_list, credit_txn_list = get_txn_lists()
        self.check_db(savings_txn_list)
        self.check_db(checking_txn_list)
        self.check_db(credit_txn_list)
        
        '''
        db_txns = TransactionDB.query()
        
        txn_list = transaction_list.TransactionList()
        for db_txn in db_txns:
            if db_txn.txn_type is not '':
                txn_list.txns.append(transaction_list.Transaction(date=db_txn.date,
                                                                  desc=db_txn.desc,
                                                                  amount=db_txn.amt,
                                                                  balance=0,
                                                                  txn_type=db_txn.txn_type))
        '''
        
        template_values = {
            'savings': savings_txn_list.toJSON(),
            'checking': checking_txn_list.toJSON(),
            'credit': credit_txn_list.toJSON()
        }   
        
        path = 'html/mod_expenses.html'
        self.response.out.write(template.render(path, template_values)) 
            
    # Check each entry of txn_list against db. Fill in txn_type when needed.
    def check_db(self, txn_list):
        for txn in txn_list.txns:
            key_str = make_key(txn.date, txn.desc, txn.amount)
            db_txn_key = ndb.Key(TransactionDB, key_str)
            db_txn = db_txn_key.get()
            if db_txn:
                print 'Found txn ' + key_str
                txn.txn_type = db_txn.txn_type
            

class MainPage(webapp.RequestHandler):
    
    def get(self):
        savings_txn_list, checking_txn_list, credit_txn_list = get_txn_lists()
        
        serialized_savings = savings_txn_list.toJSON()
        serialized_checking = checking_txn_list.toJSON()
        serialized_credit = credit_txn_list.toJSON()
    
        template_values = {
            'savings': serialized_savings,
            'checking': serialized_checking,
            'credit': serialized_credit
        }
        path = 'html/main.html'
        self.response.out.write(template.render(path, template_values))    
    

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/expenses', ExpensesHandler),
                                      ('/mod_expenses', ModExpensesHandler)],
                                       debug=True)
                                     

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
