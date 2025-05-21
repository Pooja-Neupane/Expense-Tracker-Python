import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to SQLite database and create expenses table
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()

def add_expense(amount, category, date):
    """Add a new expense record"""
    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, date)
    )
    conn.commit()

def view_expenses_by_date(start_date, end_date):
    """Fetch and print expenses in the date range"""
    cursor.execute(
        "SELECT amount, category, date FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date",
        (start_date, end_date)
    )
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found for the selected date range.")
        return []
    print(f"Expenses from {start_date} to {end_date}:")
    for amount, category, date in rows:
        print(f"Date: {date}, Category: {category}, Amount: {amount}")
    return rows

def plot_expenses_over_time(start_date, end_date):
    """Plot total expenses per day as a line chart"""
    cursor.execute(
        "SELECT date, SUM(amount) FROM expenses WHERE date BETWEEN ? AND ? GROUP BY date ORDER BY date",
        (start_date, end_date)
    )
    data = cursor.fetchall()
    if not data:
        print("No data to plot for the selected date range.")
        return

    dates, amounts = zip(*data)
    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o', linestyle='-', color='blue')
    plt.title("Total Expenses Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount Spent")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_expense_distribution_by_category(start_date, end_date):
    """Plot expense distribution by category as a pie chart"""
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE date BETWEEN ? AND ? GROUP BY category",
        (start_date, end_date)
    )
    data = cursor.fetchall()
    if not data:
        print("No data to plot for the selected date range.")
        return

    categories, amounts = zip(*data)

    plt.figure(figsize=(7,7))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution by Category")
    plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular.
    plt.show()

# Example Usage
if __name__ == "__main__":
    #Adding some example expenses (uncomment to add)
    add_expense(100.50, "Groceries", "2025-05-18")
    add_expense(40.00, "Transport", "2025-05-18")
    add_expense(20.75, "Snacks", "2025-05-19")
    add_expense(150.00, "Rent", "2025-05-20")
    # add_expense(60.00, "Entertainment", "2025-05-21")
    add_expense(90.00, "Groceries", "2025-05-21")

    start = "2025-05-18"
    end = "2025-05-21"

    view_expenses_by_date(start, end)
    plot_expenses_over_time(start, end)
    plot_expense_distribution_by_category(start, end)

    conn.close()
