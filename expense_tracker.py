import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from collections import defaultdict
from datetime import datetime

EXPENSE_FILE = 'expenses.json'

def initialize_file():
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'w') as f:
            json.dump([], f)

def load_expenses():
    with open(EXPENSE_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    if not (date and category and amount):
        messagebox.showwarning("Missing Info", "Please fill all required fields.")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a number.")
        return
    expenses = load_expenses()
    expenses.append({
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    })
    save_expenses(expenses)
    messagebox.showinfo("Success", "Expense added.")
    refresh_table()

def update_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Row", "Please select a row to update.")
        return
    idx = tree.index(selected[0])
    expenses = load_expenses()
    try:
        updated_amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a number.")
        return
    expenses[idx] = {
        "Date": date_entry.get(),
        "Category": category_entry.get(),
        "Amount": updated_amount,
        "Description": description_entry.get()
    }
    save_expenses(expenses)
    messagebox.showinfo("Updated", "Expense updated successfully.")
    refresh_table()

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Row", "Please select a row to delete.")
        return
    idx = tree.index(selected[0])
    expenses = load_expenses()
    removed = expenses.pop(idx)
    save_expenses(expenses)
    messagebox.showinfo("Deleted", f"Deleted expense: {removed}")
    refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for e in load_expenses():
        tree.insert('', 'end', values=(e['Date'], e['Category'], e['Amount'], e['Description']))

def view_report():
    expenses = load_expenses()
    if not expenses:
        messagebox.showinfo("No Data", "No expenses to report.")
        return
    total = sum(e['Amount'] for e in expenses)
    categories = defaultdict(float)
    months = defaultdict(float)
    for e in expenses:
        categories[e['Category']] += e['Amount']
        month = datetime.strptime(e['Date'], "%Y-%m-%d").strftime("%B %Y")
        months[month] += e['Amount']
    report = f"Total Expenses: ₹{total:.2f}\n\nBy Category:\n"
    for cat, amt in categories.items():
        report += f"{cat}: ₹{amt:.2f}\n"
    report += "\nBy Month:\n"
    for m, amt in months.items():
        report += f"{m}: ₹{amt:.2f}\n"
    messagebox.showinfo("Expense Report", report)

def filter_expenses():
    keyword = search_entry.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for e in load_expenses():
        if keyword in e['Category'].lower() or keyword in e['Date']:
            tree.insert('', 'end', values=(e['Date'], e['Category'], e['Amount'], e['Description']))

# GUI Setup
initialize_file()
root = tk.Tk()
root.title("💸 Expense Tracker")
root.geometry("900x600")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", font=("Helvetica", 11), rowheight=25)
style.configure("TButton", font=("Helvetica", 11), padding=6)

# Header
header = tk.Label(root, text="Expense Tracker", font=("Helvetica", 20, "bold"), bg="#f0f4f7", fg="#2c3e50")
header.pack(pady=10)

# Form Frame
form_frame = tk.Frame(root, bg="#f0f4f7")
form_frame.pack(pady=10)

labels = ["Date (YYYY-MM-DD)", "Category", "Amount", "Description"]
entries = []
for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, font=("Helvetica", 11), bg="#f0f4f7").grid(row=0, column=i, padx=5)
    entry = tk.Entry(form_frame, font=("Helvetica", 11), width=15)
    entry.grid(row=1, column=i, padx=5)
    entries.append(entry)

date_entry, category_entry, amount_entry, description_entry = entries
ttk.Button(form_frame, text="Add Expense", command=add_expense).grid(row=1, column=4, padx=10)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("Date", "Category", "Amount", "Description")
tree = ttk.Treeview(table_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.pack()

# Action Frame
action_frame = tk.Frame(root, bg="#f0f4f7")
action_frame.pack(pady=20)

ttk.Button(action_frame, text="✏️ Update Selected", command=update_expense).pack(side=tk.LEFT, padx=10)
ttk.Button(action_frame, text="🗑️ Delete Selected", command=delete_expense).pack(side=tk.LEFT, padx=10)
ttk.Button(action_frame, text="📊 View Report", command=view_report).pack(side=tk.LEFT, padx=10)

search_entry = tk.Entry(action_frame, font=("Helvetica", 11), width=20)
search_entry.pack(side=tk.LEFT, padx=10)
ttk.Button(action_frame, text="🔍 Filter", command=filter_expenses).pack(side=tk.LEFT, padx=10)

refresh_table()
root.mainloop()
