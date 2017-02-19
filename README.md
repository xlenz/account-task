account-task
============

**Account** is a simple command line accounting tool that takes a text file
as input. The input file consists of one or more lines, each of which is in
the following format:

1. mm-dd-yyyy Deposit $xx.xx
2. mm-dd-yyyy Withdraw $xx.xx

NOTE:
* format provided above is the only one supported;
* $ sign is mandatory and the only one allowed;
* negative values for deposit/withdraw are not allowed;

When you run the command "Account transaction.txt" it reads the input data
from the transactions.txt file and outputs the following information:


1. The number of total transactions
2. The account balance including all transactions
3. the date and balance for the first transaction that results in a negative account balance

Running
--

NOTE: `python3` is required

1. Account tool: `python3 account`
2. Tests: `python3 setup.py tests`
