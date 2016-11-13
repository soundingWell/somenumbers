#!/usr/bin/python

'''
Any enums related to charging.
'''

# If food/fun/essentials can be positive if I was reimbursed.

from enum import Enum

class TransactionType(Enum):
    essential = 1
    food = 2
    fun = 3
    income = 4
    UNKNOWN = 4