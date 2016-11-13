#!/usr/bin/python

### GAE ###
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

### Basics ###
import json
import sys
sys.path.append('python/')

### Mine ###
from transaction_db import TransactionDB
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

class ExpensesHandler(webapp.RequestHandler):
    
    # User chose a class for a txn. Enter it into the db
    def post(self):
        txn_json = self.request.body
        json_py = json.loads(txn_json)
        '''
        id = str(json_py['date']) + str(json_py['amt'])
        print 'id: ' + id

        txn = TransactionDB(json_py['date'], json_py['desc'], json_py['amt'],  
                            json_py['txn_type'], id)
        print 'PUTTING ' + json_py['desc'] + ' as ' + json_py['classification']
        '''
        # txn.put()
        
    # Read csv, check that against db. Send 2 lists: 
    # 1. txns already entered (to be used for the chart)
    # 2. txns not yet entered / txns with no class (prompt user to enter).
    def get(self):
        savings_txn_list, checking_txn_list, credit_txn_list = get_txn_lists()
        
        serialized_entered = checking_txn_list.toJSON()
        serialized_unentered = savings_txn_list.toJSON()
        
        template_values = {
            'entered': serialized_entered,
            'unentered': serialized_unentered,
        }
        
        path = 'html/expenses.html'
        self.response.out.write(template.render(path, template_values)) 
       
'''
class ModExpensesHandler(webapp.RequestHandler):
    
    # User chose a class for a txn. Enter it into the db
    def post(self):
        txn_json = self.request.body
        json_py = json.loads(txn_json)
        
        txn = TransactionDB(json_py['date'], json_py['desc'], json_py['amt'],  
                            json_py['classification'], 
                            json_py['date'] + json_py['amt'])
        print 'PUTTING ' + json_py['desc'] + ' as ' + json_py['classification']
        txn.put()
        
    # Read csv, check that against db. Send 2 lists: 
    # 1. txns already entered (to be used for the chart)
    # 2. txns not yet entered / txns with no class (prompt user to enter).
    def get(self):
        savings_txn_list, checking_txn_list, credit_txn_list = get_txn_lists()
        
        serialized_entered = checking_txn_list.toJSON()
        serialized_unentered = savings_txn_list.toJSON()
        
        template_values = {
            'entered': serialized_entered,
            'unentered': serialized_unentered,
        }
        
        path = 'html/expenses.html'
        self.response.out.write(template.render(path, template_values)) 
 '''

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
                                      ('/expenses', ExpensesHandler)],
                                       debug=True)
                                     

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
