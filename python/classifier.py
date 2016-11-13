#!/usr/bin/python

# from transaction_types import TransactionType

essential_keys = ['Skyline', 'STATE FARM', 'COMCAST', 'PGANDE']
income_keys = ['GOOGLE INC']

def search_for_substr(description_str, list_keys):
    for key in list_keys:
        if description_str.find(key) != -1:
            return True


def get_classification(description):
    return 'yeah'
    '''
    if search_for_substr(description, essential_keys):
        return TransactionType.essential
    elif search_for_substr(description, income_keys):
        return TransactionType.income
    else:
        return TransactionType.UNKNOWN
'''