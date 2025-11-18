# PocketMoney 💰

A simple and elegant command-line budget tracker to manage your personal finances.

## Features

- 📊 Track income and expenses
- 💵 View current balance
- 📝 List transaction history
- 📈 Generate financial summaries
- 🏷️ Categorize transactions
- 💾 Automatic data persistence

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Amangal1/PocketMoney.git
cd PocketMoney
```

2. No external dependencies required! PocketMoney uses only Python standard library.

## Usage

### Add Income

```bash
python pocketmoney.py income <amount> <description> [category]
```

Example:
```bash
python pocketmoney.py income 1500 "Monthly salary" Salary
python pocketmoney.py income 50 "Freelance work" Freelance
```

### Add Expense

```bash
python pocketmoney.py expense <amount> <description> [category]
```

Example:
```bash
python pocketmoney.py expense 50 "Groceries" Food
python pocketmoney.py expense 30 "Gas" Transportation
python pocketmoney.py expense 100 "Electricity bill" Utilities
```

### Check Balance

```bash
python pocketmoney.py balance
```

### List Transactions

```bash
# List all transactions
python pocketmoney.py list

# List last 10 transactions
python pocketmoney.py list 10
```

### View Summary

```bash
python pocketmoney.py summary
```

This displays:
- Total income
- Total expenses
- Current balance
- Expenses breakdown by category

## Example Session

```bash
# Add some income
$ python pocketmoney.py income 2000 "Salary" Work
✓ Added income: $2000.00 - Salary

# Add expenses
$ python pocketmoney.py expense 500 "Rent" Housing
✓ Added expense: $500.00 - Rent

$ python pocketmoney.py expense 100 "Groceries" Food
✓ Added expense: $100.00 - Groceries

$ python pocketmoney.py expense 50 "Gas" Transportation
✓ Added expense: $50.00 - Gas

# Check balance
$ python pocketmoney.py balance
Current Balance: $1350.00

# View summary
$ python pocketmoney.py summary

==================================================
FINANCIAL SUMMARY
==================================================
Total Income:   $   2000.00
Total Expenses: $    650.00
--------------------------------------------------
Balance:        $   1350.00
==================================================

Expenses by Category:
--------------------------------------------------
  Housing              $     500.00
  Food                 $     100.00
  Transportation       $      50.00
--------------------------------------------------
```

## Data Storage

All transactions are automatically saved to `pocketmoney_data.json` in the current directory. This file is created automatically when you add your first transaction.

## Requirements

- Python 3.6 or higher

## License

MIT License - Feel free to use and modify as needed!