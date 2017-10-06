#!/usr/bin/python

import csv
import json
import logging


# Google
from google.appengine.ext import ndb

### Mine ###
from transaction_db import TransactionDB
from transaction_db import make_key

# These constants are the the column index for a given transaction.
DATE = 1
DESC = 2
AMT = 3
BALANCE = 5

# "10/31/2016" -> 20161031
# This is better for data. You can then compare dates sequentially.
def date_to_int(date_str):
    date_str = date_str.replace("/", "")
    year_first_date = date_str[4:] + date_str[0:4]
    return int(year_first_date)


class Transaction: 
    def __init__(self, date=0, desc='', amount=0, balance=0, txn_type=''):
        self.amount = amount
        if balance is None:
            balance = 0
        self.balance = balance
        self.date = date
        self.desc = desc
        self.txn_type = txn_type
    

    def print_vals(self):
        print self.date + ', ' + self.description + ', ' + self.amount


class TransactionList(object):   
    def __init__(self):
        self.txns = []
        global DATE, DESC, AMT, BALANCE        
        
    def init_from_tl(self, tl):
        self.txns=tl
        
    # Used by mod expenses.
    def add_txn_to_end(self, txn_raw, is_credit):
        amount = 0
        balance = 0
        if not is_credit:
            try: 
                amount = float(txn_raw[AMT])
            except ValueError:
                #logging.info("failed to read txn: " + txn_raw[DATE] + " " + txn_raw[DESC])
                return
            try: 
                balance = float(txn_raw[BALANCE])
            except ValueError:
                #logging.info("failed to read txn: " + txn_raw[DATE] + " " + txn_raw[DESC])
                return
            
        self.txns.append(Transaction(date=date_to_int(txn_raw[DATE]), 
                                     desc=txn_raw[DESC], 
                                     amount=amount,
                                     balance=balance))

        
    # Used by main.
    def add_txn_to_front(self, txn_raw, is_credit):
        amount = 0
        balance = 0
        if not is_credit:
            try: 
                amount = float(txn_raw[AMT])
            except ValueError:
                logging.info("failed to read txn: " + txn_raw[DATE] + " " + txn_raw[DESC])
                return
            try: 
                balance = float(txn_raw[BALANCE])
            except ValueError:
                logging.info("failed to read txn: " + txn_raw[DATE] + " " + txn_raw[DESC])
                return

        self.txns.insert(0, Transaction(date=date_to_int(txn_raw[DATE]), 
                                        desc=txn_raw[DESC], 
                                        amount=amount,
                                        balance=balance))
    
    # tlr = transaction_list_raw
    def init_from_tlr(self, tlr, desc_dates=False):
        self.txns = []
        
        # Bad, but if I made these members, they would need 'self.' prefix.
        global DATE, DESC, AMT, BALANCE   
        
        is_credit = False
        # Accessing the first column of the first transaction.
        # This tells us if it's a credit card or checking/savings.
        if tlr[0][0] == 'Sale' or tlr[0][0] == 'Payment' or tlr[0][0] == 'Return':
            is_credit  = True
            DESC = 3
            AMT = 4
        else:
            DESC = 2
            AMT = 3
            
        for txn_raw in tlr:
            # Newest txn at back.           
            if desc_dates:
                self.add_txn_to_end(txn_raw, is_credit)
            else:
                self.add_txn_to_front(txn_raw, is_credit)

            
    def get_txns_by_class(self, txn_class):
        set_of_txns = []
        for txn in self.txns:
            if txn.txn_type == txn_class:
                set_of_txns.append(txn)
            
        return set_of_txns
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, skipkeys=False, indent=2, separators=(',', ':'))

      
def read_first_line(list_of_transactions):
    top_line = list_of_transactions[0]
    list_of_transactions.remove(top_line)   


# Returns a TransactionList. top_down.
def txn_list_from_csv(csv_file, desc_dates=False):
    transaction_list_raw = []
    with open(csv_file, 'rb') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in statement:
            transaction_list_raw.append(row)

    read_first_line(transaction_list_raw)
    txn_list = TransactionList()
    txn_list.init_from_tlr(transaction_list_raw, desc_dates)
    return txn_list       

# Returns a TransactionList. top_down.
def store_txns_from_csv(csv_file):
    transaction_list_raw = []
    with open(csv_file, 'rb') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in statement:
            transaction_list_raw.append(row)

    read_first_line(transaction_list_raw)
    txn_list = TransactionList()
    txn_list.init_from_tlr(transaction_list_raw, True)
    
    for txn in txn_list.txns:
        txn_db = TransactionDB(date=txn.date, 
                               desc=txn.desc, 
                               amt=txn.amount,  
                               txn_type="")
        
        txn_key = make_key(txn.date, txn.desc, txn.amount)
        txn_db.key = ndb.Key(TransactionDB, txn_key)
        txn_db.put()
    
    
    return txn_list  
    