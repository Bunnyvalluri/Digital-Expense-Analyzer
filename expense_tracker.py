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
    messagebox.showinfo("Success", "✅ Expense added.")
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
    messagebox.showinfo("Updated", "✅ Expense updated successfully.")
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
    messagebox.showinfo("Deleted", f"🗑️ Deleted expense: {removed}")
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
root.geometry("1000x650")
root.configure(bg="#f3e5f5")  # Soft lavender background

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#d81b60", foreground="white")
style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.map("TButton", background=[("active", "#880e4f")])

# Header
header = tk.Label(root, text="💸 Expense Tracker", font=("Segoe UI", 26, "bold"), bg="#f3e5f5", fg="#d81b60")
header.pack(pady=10)

# Form Frame
form_frame = tk.LabelFrame(root, text="📝 Add / Edit Expense", font=("Segoe UI", 12, "bold"), bg="#fce4ec", padx=10, pady=10)
form_frame.pack(fill="x", padx=20, pady=10)

labels = ["Date (YYYY-MM-DD)", "Category", "Amount", "Description"]
entries = []
for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, font=("Segoe UI", 11), bg="#fce4ec").grid(row=0, column=i, padx=5, pady=5)
    entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=18)
    entry.grid(row=1, column=i, padx=5, pady=5)
    entries.append(entry)

date_entry, category_entry, amount_entry, description_entry = entries
ttk.Button(form_frame, text="➕ Add Expense", command=add_expense).grid(row=1, column=4, padx=10, pady=5)

# Table Frame
table_frame = tk.LabelFrame(root, text="📋 Expense Records", font=("Segoe UI", 12, "bold"), bg="#fce4ec", padx=10, pady=10)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Date", "Category", "Amount", "Description")
tree = ttk.Treeview(table_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)

# Action Frame
action_frame = tk.LabelFrame(root, text="⚙️ Actions", font=("Segoe UI", 12, "bold"), bg="#fce4ec", padx=10, pady=10)
action_frame.pack(fill="x", padx=20, pady=10)

ttk.Button(action_frame, text="✏️ Update Selected", command=update_expense).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(action_frame, text="🗑️ Delete Selected", command=delete_expense).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(action_frame, text="📊 View Report", command=view_report).grid(row=0, column=2, padx=10, pady=5)

search_entry = tk.Entry(action_frame, font=("Segoe UI", 11), width=25)
search_entry.grid(row=0, column=3, padx=10, pady=5)
ttk.Button(action_frame, text="🔍 Filter", command=filter_expenses).grid(row=0, column=4, padx=10, pady=5)

refresh_table()
root.mainloop()
