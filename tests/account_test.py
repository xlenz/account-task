import pytest
import sys
from accountModule.account import Account


def test_initial_state():
    print('assert initial state')
    account = Account()
    assert account.is_balance_valid()
    assert account.get_balance() == 0
    assert account.get_transactions_count() == 0
    assert account.get_negative_transaction() == {'occurred': False}


@pytest.mark.parametrize("number,tr_type,output", [
    (33.333, 'Deposit', 33.33),
    (33.339, 'Deposit', 33.34),
    (0, 'Withdraw', 0.0),
    (0, 'Deposit', 0.0),
    (134, 'Withdraw', -134.0),
])
def test_update_balance(number, tr_type, output):
    print('assert update balance')
    account = Account()
    account.update_balance({'number': number, 'type': tr_type})
    assert account.get_balance() == output


@pytest.mark.parametrize("number", [-1, sys.float_info.max,
                                    -1 * sys.float_info.max,
                                    2 * sys.float_info.max,
                                    -2 * sys.float_info.max])
def test_is_balance_valid(number):
    print('assert is_balance_valid')
    account = Account()

    account.update_balance({'number': abs(number),
                            'type': 'Deposit' if number > 0 else 'Withdraw'})
    assert account.is_balance_valid() != float('Inf')


def test_is_balance_valid_negative():
    print('assert is_balance_valid_negative')
    account = Account()

    with pytest.raises(Exception) as excinfo:
        account.update_balance({'number': -1, 'type': 'Deposit'})
    excinfo.match(r'.* negative .*')

    with pytest.raises(Exception) as excinfo:
        account.update_balance({'number': 10, 'type': 'asdf'})
    excinfo.match(r'Invalid .*')


@pytest.mark.parametrize("path_to_file", ['', '//\\\//\//',
                                          'http://google.com'])
def test_read_file_negative(path_to_file):
    print('assert read_file - negative')
    account = Account()

    assert not account.read_file(path_to_file)


def test_check_negative_balance_occurrence():
    print('assert check_negative_balance_occurrence')
    account = Account()
    print(account.get_negative_transaction()['occurred'])

    # no effect
    account.update_balance({'number': 10, 'type': 'Deposit'})
    account.check_negative_balance_occurrence({'date': '...'}, 0)
    assert not account.get_negative_transaction()['occurred']


def test_read_file():
    print('assert read_file')
    account = Account()

    assert account.read_file('tests/transactions.txt')
    assert account.get_balance() == 35.67
    assert account.get_transactions_count() == 4
    assert account.get_negative_transaction() == {'occurred': True,
                                                  'balance': -0.46,
                                                  'date': '3-4-2012',
                                                  'line': 4}
    assert account.is_balance_valid()
    pass

# todo
# more test_read_file_negative, more test_read_file tests;
# test for process_line
