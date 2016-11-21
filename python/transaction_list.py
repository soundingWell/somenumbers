#!/usr/bin/python

import json
import csv

# These constants are the the column index for a given transaction.
DATE = 1
DESC = 3
AMT = 4
BALANCE = 5

# "10/31/2016" -> 20161031
# This is better for data. You can then compare dates sequetially.
def date_to_int(date_str):
    date_str = date_str.replace("/", "")
    year_first_date = date_str[4:] + date_str[0:4]
    return int(year_first_date)

class Transaction: 
    def __init__(self, date=0, desc='', amount=0, balance=0, txn_type=''):
        self.date = date
        self.desc = desc
        self.amount = amount
        self.balance = balance
        self.txn_type = txn_type
    
    def print_vals(self):
        print self.date + ', ' + self.description + ', ' + self.amount

class TransactionList(object):   
    
    def __init__(self):
        self.total = 0
        self.txns = []
        
    def init_from_tl(self, tl):
        self.txns=tl
    
    # tlr = transaction_list_raw
    def init_from_tlr(self, tlr):
        self.total= 0
        self.txns = []
        
        # These constants are the the column index for a given transaction.
        DATE = 1
        DESC = 2
        AMT = 3
        BALANCE = 5
        
        credit = False
        # Accessing the first column of the first transaction.
        # This tells us if it's a credit card or checking/savings.
        if tlr[0][0] == 'Sale' or tlr[0][0] == 'Payment':
            credit  = True
        if credit:
            DESC += 1
            AMT += 1
            
        for charge in tlr:
            # Charge is an arr with ['10/23/17', 'desript', '12399']
            amount = float(charge[AMT])
            
            # Credit has no balance.
            if credit:
                self.txns.insert(0, Transaction(date=date_to_int(charge[DATE]), 
                                                desc=charge[DESC], 
                                                amount=amount))
            else:
                self.txns.insert(0, Transaction(date=date_to_int(charge[DATE]), 
                                                desc=charge[DESC], 
                                                amount=amount,
                                                balance=charge[BALANCE]))
            self.total += amount
            
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


# Returns a TransactionList
def txn_list_from_csv(csv_file):
    transaction_list_raw = []
    with open(csv_file, 'rb') as csvfile:
        statemnt = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in statemnt:
            transaction_list_raw.append(row)

    read_first_line(transaction_list_raw)
    txn_list = TransactionList()
    txn_list.init_from_tlr(transaction_list_raw)
    return txn_list       
    