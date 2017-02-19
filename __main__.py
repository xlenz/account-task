import sys
import time

from accountModule.account import Account


def print_results(account):
    # total transactions
    print('Total transactions count: %s' % account.get_transactions_count())

    # balance
    print('Balance: %s' % account.get_balance())

    # first negative transaction
    negative_transaction = account.get_negative_transaction()
    if negative_transaction['occurred']:
        # Note: is is not required to print line, but it's helpful
        negative_balance = account.get_negative_transaction()
        print('First negative balance occurrence: %s at %s (line %s)' %
              (negative_balance['balance'],
               negative_balance['date'],
               negative_balance['line']))
    else:
        print("Account balance didn't become negative.")


def main():
    print('Program started...')
    start = time.time()

    acc = Account()

    # command line arguments
    if len(sys.argv) != 2:
        print('Program requires one argument: path to file with transactions.')
        sys.exit(2)

    # read file
    path_to_file = sys.argv[1]
    if not acc.read_file(path_to_file):
        sys.exit(1)

    # print results
    print('----------')
    print_results(acc)
    print('----------')

    # end
    print('The end, time spent: %s' % round(time.time() - start, 3))
    sys.exit(0)


if __name__ == "__main__":
    main()
