#!/usr/bin/env python3
"""
PocketMoney - A simple command-line budget tracker
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class PocketMoney:
    """Main class for managing personal finances"""
    
    def __init__(self, data_file: str = "pocketmoney_data.json"):
        self.data_file = data_file
        self.transactions: List[Dict] = []
        self.load_data()
    
    def load_data(self):
        """Load transaction data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.transactions = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not read {self.data_file}. Starting fresh.")
                self.transactions = []
        else:
            self.transactions = []
    
    def save_data(self):
        """Save transaction data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def add_income(self, amount: float, description: str, category: str = "Income"):
        """Add an income transaction"""
        transaction = {
            "type": "income",
            "amount": amount,
            "description": description,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
        self.save_data()
        print(f"✓ Added income: ${amount:.2f} - {description}")
    
    def add_expense(self, amount: float, description: str, category: str = "General"):
        """Add an expense transaction"""
        transaction = {
            "type": "expense",
            "amount": amount,
            "description": description,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
        self.save_data()
        print(f"✓ Added expense: ${amount:.2f} - {description}")
    
    def get_balance(self) -> float:
        """Calculate current balance"""
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        return income - expenses
    
    def list_transactions(self, limit: int = None):
        """List all transactions"""
        if not self.transactions:
            print("No transactions found.")
            return
        
        print("\nTransactions:")
        print("-" * 80)
        
        transactions = self.transactions[-limit:] if limit else self.transactions
        
        for i, trans in enumerate(transactions, 1):
            sign = "+" if trans["type"] == "income" else "-"
            print(f"{i}. [{trans['date']}] {sign}${trans['amount']:.2f} - "
                  f"{trans['description']} ({trans['category']})")
        print("-" * 80)
    
    def show_summary(self):
        """Show financial summary"""
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        balance = income - expenses
        
        print("\n" + "=" * 50)
        print("FINANCIAL SUMMARY")
        print("=" * 50)
        print(f"Total Income:   ${income:>10.2f}")
        print(f"Total Expenses: ${expenses:>10.2f}")
        print("-" * 50)
        print(f"Balance:        ${balance:>10.2f}")
        print("=" * 50)
        
        if self.transactions:
            categories = {}
            for trans in self.transactions:
                if trans["type"] == "expense":
                    cat = trans["category"]
                    categories[cat] = categories.get(cat, 0) + trans["amount"]
            
            if categories:
                print("\nExpenses by Category:")
                print("-" * 50)
                for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {cat:<20} ${amount:>10.2f}")
                print("-" * 50)


def main():
    """Main function to run the PocketMoney CLI"""
    import sys
    
    pm = PocketMoney()
    
    if len(sys.argv) < 2:
        print("PocketMoney - Personal Budget Tracker")
        print("\nUsage:")
        print("  python pocketmoney.py income <amount> <description> [category]")
        print("  python pocketmoney.py expense <amount> <description> [category]")
        print("  python pocketmoney.py balance")
        print("  python pocketmoney.py list [number]")
        print("  python pocketmoney.py summary")
        print("\nExamples:")
        print("  python pocketmoney.py income 1500 'Monthly salary' Salary")
        print("  python pocketmoney.py expense 50 'Groceries' Food")
        print("  python pocketmoney.py balance")
        print("  python pocketmoney.py list 10")
        print("  python pocketmoney.py summary")
        return
    
    command = sys.argv[1].lower()
    
    if command == "income":
        if len(sys.argv) < 4:
            print("Error: Please provide amount and description")
            return
        try:
            amount = float(sys.argv[2])
            description = sys.argv[3]
            category = sys.argv[4] if len(sys.argv) > 4 else "Income"
            pm.add_income(amount, description, category)
        except ValueError:
            print("Error: Invalid amount")
    
    elif command == "expense":
        if len(sys.argv) < 4:
            print("Error: Please provide amount and description")
            return
        try:
            amount = float(sys.argv[2])
            description = sys.argv[3]
            category = sys.argv[4] if len(sys.argv) > 4 else "General"
            pm.add_expense(amount, description, category)
        except ValueError:
            print("Error: Invalid amount")
    
    elif command == "balance":
        balance = pm.get_balance()
        print(f"\nCurrent Balance: ${balance:.2f}")
    
    elif command == "list":
        limit = None
        if len(sys.argv) > 2:
            try:
                limit = int(sys.argv[2])
            except ValueError:
                print("Error: Invalid number for limit")
                return
        pm.list_transactions(limit)
    
    elif command == "summary":
        pm.show_summary()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python pocketmoney.py' to see available commands")


if __name__ == "__main__":
    main()
