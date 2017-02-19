from accountModule.transaction_types import *
from datetime import datetime


def parse_line(line, line_num):
    transaction = {}
    tr_list = line.split(' ')

    # assert length
    if len(tr_list) != 3:
        set_error(transaction, 'Invalid transaction format', line_num, line)
        return transaction

    parse_date(line_num, tr_list[0], transaction)
    parse_type(line_num, tr_list[1], transaction)
    parse_number(line_num, tr_list[2], transaction)

    return transaction


def parse_date(line_num, date_str, transaction):
    try:
        datetime.strptime(date_str, '%m-%d-%Y')
        transaction['date'] = date_str
    except ValueError:
        set_error(transaction, 'Invalid date format', line_num, date_str)


def parse_type(line_num, type_str, transaction):
    if type_str != DEPOSIT and type_str != WITHDRAW:
        set_error(transaction, 'Invalid transaction type', line_num, type_str)
    else:
        transaction['type'] = type_str


def parse_number(line_num, num_str, transaction):
    # currency sign and length
    if len(num_str) < 2 or num_str[0] != '$':
        set_error(transaction, 'Invalid number format', line_num, num_str)
    else:
        num_str = num_str[1:]

    # convert to float
    try:
        number = float(num_str)
        # Note: seems like negative Deposit/Withdraw should not be allowed
        if number < 0:
            set_error(transaction, 'Negative number values are not allowed',
                      line_num, num_str)
        else:
            transaction['number'] = number
    except ValueError:
        set_error(transaction, 'Invalid number format', line_num, num_str)


def set_error(transaction, err, line_num, value):
    transaction['error'] = 'ERROR: %s (line %s): %s' % (err, line_num, value)
