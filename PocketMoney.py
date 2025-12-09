import csv
import os

BUDGETS_FILE = "budgets.csv"
PURCHASES_FILE = "purchases.csv"

# CSV helper functions
def load_budgets():
    # Read budgets.csv and return a dict {category: budget}
    budgets = {}

    try:
        with open(BUDGETS_FILE, newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    cat = row[0].strip()
                    try:
                        amount = float(row[1])
                    except:
                        amount = 0.0
                    budgets[cat] = amount
    except FileNotFoundError:
        pass

    return budgets

def save_budgets(budgets):
    # Write the budgets dict to budgets.csv
    with open(BUDGETS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "budget"])
        for cat, amount in budgets.items():
            writer.writerow([cat, amount])

def add_purchase_to_csv(category, amount):
    # Append one purchase to purchases.csv
    file_exists = os.path.exists(PURCHASES_FILE)
    write_header = (not file_exists) or os.path.getsize(PURCHASES_FILE) == 0

    with open(PURCHASES_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["category", "amount"])
        writer.writerow([category, amount])

def load_spending(budgets):
    # Read purchases.csv and return a dict {category: total_spent}
    spending = {cat: 0.0 for cat in budgets.keys()}

    if not os.path.exists(PURCHASES_FILE):
        return spending

    with open(PURCHASES_FILE, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2:
                cat = row[0]
                try:
                    amount = float(row[1])
                except:
                    amount = 0.0
                if cat in spending:
                    spending[cat] += amount
    
    return spending

# User interface helpers
def display_menu():
    print("\nMenu:")
    print("1. Log a purchase")
    print("2. Set / update monthly budget")
    print("3. View budget")
    print("4. Add budget group")
    print("5. Reset for new month (HARD RESET)")
    print("6. Exit")

def get_user_choice():
    choice = input("Please select an option (1-6): ")
    return choice

def display_categories(budgets):
    print("\nChoose a category:")
    cats = list(budgets.keys())
    for i, cat in enumerate(cats, start=1):
        print(f"{i}. {cat}")

def get_category_choice(budgets):
    while True:
        cats = list(budgets.keys())
        if not cats:
            print("No categories defined. Add a budget group first.")
            return None
        display_categories(budgets)
        choice = input(f"Select a category (1-{len(cats)}): ")

        try:
            index = int(choice) - 1
            if 0 <= index < len(cats):
                return cats[index]
        except:
            pass

# Main features
def setup_first_time():
    # Run when this is the first time or after a hard reset
    print("Welcome to Pocket Money!")
    print("Let's set up your monthly budget.")

    while True:
        total_str = input("How much money do you have for this month? ")
        try:
            total = float(total_str)
            if total <= 0:
                print("Enter a positive amount.")
                continue
            elif total != round(total, 2):
                print("Please enter a valid monetary amount.")
                continue
            break
        except:
            print("Please enter a number.")
    
    budgets = {}
    remaining = total

    # Ask how many groups the user wants, then names, and amounts
    while True:
        count_str = input("How many budget groups do you want to create? ")
        try:
            count = int(count_str)
            if count <= 0:
                print("Enter a positive number.")
            else:
                break
        except:
            print("Please enter a whole number.")

    print(f"\nYou have ${total:.2f} to spread across these categories.")
    for i in range(count):
        while True:
            cat = input(f"Name for group #{i+1}: ").strip()
            if not cat:
                print("Name cannot be empty.")
                continue
            if cat in budgets:
                print("That name already exists. Choose a different name.")
                continue

            while True:
                print("How much do you want to budget for " + cat + "?")
                if total > 0:
                    print(f"${remaining:.2f} Remaining")
                amount_str = input("Amount for " + cat + ": ")
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("Enter a positive number.")
                        continue
                    elif amount != round(amount, 2):
                        print("Please enter a valid monetary amount.")
                        continue
                    elif amount > remaining:
                        print(f"You only have ${remaining:.2f} remaining.")
                        continue
                    elif amount == remaining and i < count - 1:
                        print("You should leave some budget for the other groups.")
                        continue
                    budgets[cat] = amount
                    remaining -= amount
                    break
                except:
                    print("Please enter a number.")
            break

    save_budgets(budgets)
    print("\nInitial budgets saved.")
    return budgets, remaining

def log_purchase(budgets):
    # Log purchases
    while True:
        cat = get_category_choice(budgets)
        if cat is None:
            continue
        spending = load_spending(budgets)
        budget = budgets.get(cat, 0.0)
        spent = spending.get(cat, 0.0)
        remaining = budget - spent
        amount_str = input("Enter purchase amount: ")

        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Enter a positive number.")
                continue
            if amount != round(amount, 2):
                print("Please enter a valid monetary amount.")
                continue
            else:
                if amount > remaining:
                    print(f"*** This purchase exceeds your remaining budget of ${remaining:.2f} for {cat} ***")
                add_purchase_to_csv(cat, amount)
                print(f"Logged a purchase of ${amount:.2f} in {cat}")
        except:
            print("Invalid amount.")

        more = input("Do you want to add another purchase? (y/n): ").lower()
        if more != "y":
            break

def set_monthly_budget(budgets, remaining):
    # Update the budget for a category
    category = get_category_choice(budgets)

    while True:
        try:
            print(f"${remaining:.2f} Remaining")
            amount_str = input("Enter new monthly budget for " + category + ": ")
            amount = float(amount_str)
            if amount <= 0:
                print("Enter a positive number.")
                continue
            elif amount != round(amount, 2):
                print("Please enter a valid monetary amount.")
                continue
            elif remaining <= 0 and amount > budgets.get(category, 0.0):
                print("No remaining funds to allocate to budgets.")
                return remaining
            elif amount - budgets.get(category, 0.0) > remaining:
                print(f"You only have ${remaining:.2f} remaining.")
                continue
            remaining -= (amount - budgets.get(category, 0.0))
            budgets[category] = amount
            save_budgets(budgets)
            print(f"Updated budget for {category} to ${amount:.2f}")
        except:
            print("Invalid amount. Please enter a number.")
        break
    return remaining

def view_budget(budgets):
    # Show budget, spent, and percent for each category
    spending = load_spending(budgets)
    print("\nMonthly Budget Status:")

    for cat in budgets.keys():
        budget = budgets.get(cat, 0.0)
        spent = spending.get(cat, 0.0)
        if budget > 0:
            percent = (spent / budget) * 100.0
        else:
            percent = 0.0

        line = (f"{cat:15s} $" + "{:.2f}".format(spent) + "/" +
            "{:.2f}".format(budget) + " - " +
            "{:.2f}".format(percent) + "%"
        )
        print(line)

def add_budget_group(budgets, remaining):
    if remaining <= 0:
        print("No remaining funds to allocate to a new budget group.")
        return remaining

    while True:
        cat = input("Name for group: ").strip()
        if not cat:
            print("Name cannot be empty.")
            continue
        if cat in budgets:
            print("That name already exists. Choose a different name.")
            continue

        while True:
            print("How much do you want to budget for " + cat + "?")
            print(f"${remaining:.2f} Remaining")
            amount_str = input("Amount for " + cat + ": ")
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Enter a positive number.")
                elif amount != round(amount, 2):
                    print("Please enter a valid monetary amount.")
                    continue
                elif amount > remaining:
                    print(f"You only have ${remaining:.2f} remaining.")
                    continue
                else:
                    budgets[cat] = amount
                    remaining -= amount
                    break
            except:
                print("Please enter a number.")
        break
    
    save_budgets(budgets)
    print("Added new budget group:", cat)
    return remaining

def reset_database():
    # Hard reset: delete CSV files and start fresh (new month)
    print("\nRESET FOR NEW MONTH (HARD RESET)")
    print("This will DELETE all budgets and all purchases and start over.")
    confirm = input("Are you sure you want to reset? (y/n): ").lower()

    if confirm != "y":
        print("Reset cancelled.")
        return None

    # Delete purchases file if it exists
    if os.path.exists(PURCHASES_FILE):
        os.remove(PURCHASES_FILE)
        print("All purchases cleared.")
    else:
        print("No purchases file found. Nothing to clear.")

    # Delete budgets file if it exists
    if os.path.exists(BUDGETS_FILE):
        os.remove(BUDGETS_FILE)
        print("Old budgets cleared.")
    else:
        print("No budgets file found. Nothing to clear.")

    # Run setup again
    new_budgets, remaining = setup_first_time()
    print("New month setup complete.")
    return new_budgets, remaining

# Main loop
def main():
    budgets = load_budgets()

    # If all budgets are 0, treat as first-time setup
    if not budgets:
        budgets, remaining = setup_first_time()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            log_purchase(budgets)
        elif choice == "2":
            remaining = set_monthly_budget(budgets, remaining)
        elif choice == "3":
            view_budget(budgets)
        elif choice == "4":
            remaining = add_budget_group(budgets, remaining)
        elif choice == "5":
            # HARD RESET
            budgets, remaining = reset_database()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")

# Start the program
main()
