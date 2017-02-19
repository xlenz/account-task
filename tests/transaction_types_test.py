import pytest
from accountModule.transaction_types import *


def test_account():
    print('Assert transaction types')
    assert WITHDRAW == 'Withdraw'
    assert DEPOSIT == 'Deposit'
