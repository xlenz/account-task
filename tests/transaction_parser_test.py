import pytest
from accountModule.transaction_parser import parse_type, parse_number, \
    parse_line, parse_date, set_error


@pytest.mark.parametrize("item,value", [
    ("type", ''),
    ("type", 'qwe'),
    ("type", 'Deposi'),

    ("number", ''),
    ("number", '1.1.1'),
    ("number", '$-1'),
    ("number", 'x1'),
    ("number", '$$'),
    ("number", '{'),
    ("number", '100,100.00'),

    ("date", ''),
    ("date", '1-1-01'),
    ("date", '1-32-2001'),
    ("date", '1-4-201'),
    ("date", '3-3-20012'),
    ("date", '13-14-2012'),
    ("date", '-2-3-2012'),
    ("date", '--2012'),
    ("date", 'sdasdfasdfasf'),
])
def test_parse_type_negative(item, value):
    print('Assert parser (negative)')
    dictionary = {}
    print(item)
    if item == 'type':
        parse_type(0, value, dictionary)
    elif item == 'number':
        parse_number(0, value, dictionary)
    elif item == 'date':
        parse_date(0, value, dictionary)

    assert 'error' in dictionary


@pytest.mark.parametrize("transaction_type", ['Deposit', 'Withdraw'])
def test_parse_type(transaction_type):
    print('Assert type parser')
    dictionary = {}
    parse_type(0, transaction_type, dictionary)
    assert 'error' not in dictionary
    assert dictionary['type'] == transaction_type


@pytest.mark.parametrize("date", ['1-1-2001', '3-3-8888',
                                  '01-01-1970', '12-31-2017'])
def test_parse_date(date):
    print('Assert type parser')
    dictionary = {}
    parse_date(0, date, dictionary)
    assert 'error' not in dictionary
    assert dictionary['date'] == date


@pytest.mark.parametrize("number,output", [
    ('$2', 2.0),
    ('$0', 0.0),
    ('$58.25325252352345', 58.25325252352345),
    ('$9999999999999999999999999999999999', 1e+34),
])
def test_parse_number(number, output):
    print('Assert number parser')
    dictionary = {}
    parse_number(0, number, dictionary)
    assert 'error' not in dictionary
    assert dictionary['number'] == output


@pytest.mark.parametrize("line,output", [
    ('3-3-2003 Deposit $33.33', {'date': '3-3-2003',
                                 'type': 'Deposit', 'number': 33.33}),
    ('3-3-2003 Withdraw $33.33', {'date': '3-3-2003',
                                  'type': 'Withdraw', 'number': 33.33})
])
def test_parse_line(line, output):
    print('Assert line parser')
    dictionary = {}
    assert parse_line(line, 0) == output


@pytest.mark.parametrize("line", ['', '1 2 3 4', '1 2', '1',
                                  '0-0-2010 Deposit $1',
                                  '1-1-2010 Deposits $1',
                                  '1-1-2010 Deposit $-1'])
def test_parse_line_negative(line):
    print('Assert line parser (negative)')
    dictionary = {}
    assert 'error' in parse_line(line, 0)


def test_parse_error():
    print('Assert set error')
    dictionary = {}
    set_error(dictionary, 'EE', 333, 'VV')
    assert dictionary['error'] == 'ERROR: EE (line 333): VV'
