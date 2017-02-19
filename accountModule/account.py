import os.path
import sys

from accountModule import transaction_parser
from accountModule.transaction_types import *


class Account:
    __balance = 0.0
    __transactionsCount = 0
    __firstNegativeTransaction = {'occurred': False}

    def read_file(self, path_to_file):
        print('Processing file: %s' % path_to_file)

        if not os.path.isfile(path_to_file):
            print('File not found: %s' % path_to_file)
            return False

        idx = 0
        try:
            with open(path_to_file, "r") as file:
                for line in file:
                    idx += 1

                    # skip empty lines
                    line = line.strip()
                    if not line:
                        continue

                    if not self.process_line(line, idx):
                        return False
        except IOError:
            print('File read error')
            return False

        print('Done.')
        return True

    def process_line(self, line, idx):
        # parse line
        transaction = transaction_parser.parse_line(line, idx)
        if 'error' in transaction:
            print(transaction['error'])
            return False

        # transactions count
        self.__transactionsCount += 1

        # update balance and validate
        self.update_balance(transaction)
        if not self.is_balance_valid():
            print('ERROR: Balance is outside supported range. Line %s.' % idx)
            print('Maximum balance value is %s' % sys.float_info.max)
            return False

        # first negative transaction
        self.check_negative_balance_occurrence(transaction, idx)
        return True

    def update_balance(self, tr):
        if tr['number'] < 0:
            raise Exception('ERROR: negative numbers not allowed.')

        if tr['type'] == DEPOSIT:
            self.__balance += tr['number']
        elif tr['type'] == WITHDRAW:
            self.__balance -= tr['number']
        else:
            raise Exception('Invalid transaction type: %s' % tr['type'])

    def is_balance_valid(self):
        return abs(self.__balance) != float('Inf')

    def check_negative_balance_occurrence(self, transaction, line):
        occurred = self.get_negative_transaction()['occurred']
        if not occurred and self.__balance < 0:
            self.__firstNegativeTransaction['occurred'] = True
            self.__firstNegativeTransaction['date'] = transaction['date']
            self.__firstNegativeTransaction['balance'] = self.get_balance()
            self.__firstNegativeTransaction['line'] = line

    def get_balance(self):
        return round(self.__balance, 2)

    def get_transactions_count(self):
        return self.__transactionsCount

    def get_negative_transaction(self):
        return self.__firstNegativeTransaction
