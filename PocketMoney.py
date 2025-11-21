import csv
import os

CATEGORIES = ["Bills", "Gas", "Entertainment", "Shopping"]
BUDGETS_FILE = "budgets.csv"
PURCHASES_FILE = "purchases.csv"

# --------------------------
# CSV helper functions
# --------------------------

def load_budgets():
    # Read budgets.csv and return a dict {category: budget}
    budgets = {cat: 0.0 for cat in CATEGORIES}

    try:
        with open(BUDGETS_FILE, newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # skip header
            for row in reader:
                if len(row) >= 2:
                    cat = row[0]
                    try:
                        amount = float(row[1])
                    except:
                        amount = 0.0
                    if cat in budgets:
                        budgets[cat] = amount
    except FileNotFoundError:
        # No budgets file yet, keep defaults (0.0)
        pass

    return budgets


def save_budgets(budgets):
    # Write the budgets dict to budgets.csv
    with open(BUDGETS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "budget"])
        for cat in CATEGORIES:
            writer.writerow([cat, budgets.get(cat, 0.0)])


def add_purchase_to_csv(category, amount):
    # Append one purchase to purchases.csv
    file_exists = os.path.exists(PURCHASES_FILE)
    write_header = (not file_exists) or os.path.getsize(PURCHASES_FILE) == 0

    with open(PURCHASES_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["category", "amount"])
        writer.writerow([category, amount])


def load_spending():
    # Read purchases.csv and return a dict {category: total_spent}
    spending = {cat: 0.0 for cat in CATEGORIES}

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

# --------------------------
# User interface helpers
# --------------------------

def display_menu():
    print("\nMenu:")
    print("1. Log a purchase")
    print("2. Set / update monthly budget")
    print("3. View budget")
    print("4. Reset for new month (HARD RESET)")
    print("5. Exit")


def get_user_choice():
    choice = input("Please select an option (1-5): ")
    return choice


def display_categories():
    print("\nChoose a category:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(str(i) + ". " + cat)


def get_category_choice():
    display_categories()
    choice = input("Select a category (1-" + str(len(CATEGORIES)) + "): ")

    try:
        index = int(choice) - 1
        if 0 <= index < len(CATEGORIES):
            return CATEGORIES[index]
    except:
        pass

    print("Invalid category. Using 'Bills' by default.")
    return "Bills"

# --------------------------
# Main features
# --------------------------

def setup_first_time():
    # Run when this is the first time or after a hard reset
    print("Welcome to the Budget App!")
    print("Let's set up your monthly budget.")

    total_str = input("How much money do you have for this month? ")
    try:
        total = float(total_str)
    except:
        total = 0.0

    budgets = {}
    remaining = total

    print("\nYou have $" + str(total) + " to spread across these categories.")
    for cat in CATEGORIES:
        while True:
            print("How much do you want to budget for " + cat + "?")
            if total > 0:
                print("Remaining (not enforced): $" + str(remaining))
            amount_str = input("Amount for " + cat + ": ")
            try:
                amount = float(amount_str)
                if amount < 0:
                    print("Budget cannot be negative. Try again.")
                else:
                    budgets[cat] = amount
                    remaining -= amount
                    break
            except:
                print("Please enter a number.")

    save_budgets(budgets)
    print("\nInitial budgets saved.")
    return budgets


def log_purchase():
    # Log one or more purchases
    while True:
        category = get_category_choice()
        amount_str = input("Enter purchase amount: ")

        try:
            amount = float(amount_str)
            if amount < 0:
                print("Amount cannot be negative.")
            else:
                add_purchase_to_csv(category, amount)
                print("Logged a purchase of $" + str(amount) + " in " + category)
        except:
            print("Invalid amount. Please enter a number.")

        more = input("Do you want to add another purchase? (y/n): ").lower()
        if more != "y":
            break


def set_monthly_budget(budgets):
    # Update the budget for one category
    category = get_category_choice()
    amount_str = input("Enter new monthly budget for " + category + ": ")

    try:
        amount = float(amount_str)
        if amount < 0:
            print("Budget cannot be negative.")
            return
        budgets[category] = amount
        save_budgets(budgets)
        print("Updated budget for " + category + " to $" + str(amount))
    except:
        print("Invalid amount. Please enter a number.")


def view_budget(budgets):
    # Show budget, spent, and percent for each category
    spending = load_spending()
    print("\nMonthly Budget Status:")

    for cat in CATEGORIES:
        budget = budgets.get(cat, 0.0)
        spent = spending.get(cat, 0.0)
        if budget > 0:
            percent = (spent / budget) * 100.0
        else:
            percent = 0.0

        # Example: Shopping $100.00/150.00 - 66.67%
        line = (
            cat + " $" +
            "{:.2f}".format(spent) + "/" +
            "{:.2f}".format(budget) +
            " - " +
            "{:.2f}".format(percent) + "%"
        )
        print(line)


def reset_database():
    # Hard reset: delete CSV files and start fresh like a brand new month
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

    # Now run setup again so it asks for:
    # - monthly income
    # - budget amounts for each category
    new_budgets = setup_first_time()
    print("New month setup complete.")
    return new_budgets

# --------------------------
# Main loop
# --------------------------

def main():
    budgets = load_budgets()

    # If all budgets are 0, treat as first-time setup
    if all(b == 0.0 for b in budgets.values()):
        budgets = setup_first_time()

    running = True
    while running:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            log_purchase()
        elif choice == "2":
            set_monthly_budget(budgets)
        elif choice == "3":
            view_budget(budgets)
        elif choice == "4":
            # HARD RESET
            new_budgets = reset_database()
            if new_budgets is not None:
                budgets = new_budgets
        elif choice == "5":
            print("Goodbye!")
            running = False
        else:
            print("Invalid choice. Please select 1-5.")

# Start the program
main()
