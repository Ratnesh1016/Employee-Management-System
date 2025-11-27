import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

DB_FILE = "employee_management.db"

# ----------------- Database functions -----------------
def connect_db():
    return sqlite3.connect(DB_FILE)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile_number TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_employee(name, position, salary, dob, email, mobile_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, position, salary, dob, email, mobile_number) VALUES (?, ?, ?, ?, ?, ?)",
        (name, position, salary, dob, email, mobile_number)
    )
    conn.commit()
    conn.close()

def view_employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_employee(emp_id, name, position, salary, dob, email, mobile_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees
        SET name = ?, position = ?, salary = ?, dob = ?, email = ?, mobile_number = ?
        WHERE id = ?
    """, (name, position, salary, dob, email, mobile_number, emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()

# ----------------- Validation helpers -----------------
def is_valid_email(email):
    # Simple regex — fine for basic validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_mobile(mobile):
    # Accepts digits, length between 7 and 15
    return re.match(r"^\d{7,15}$", mobile) is not None

# ----------------- GUI logic -----------------
def display_employees():
    for row in tree.get_children():
        tree.delete(row)
    for emp in view_employees():
        tree.insert("", tk.END, values=emp)

def clear_form():
    entry_name.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_salary.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_mobile.delete(0, tk.END)

def get_form_values():
    return (
        entry_name.get().strip(),
        entry_position.get().strip(),
        entry_salary.get().strip(),
        entry_dob.get().strip(),
        entry_email.get().strip(),
        entry_mobile.get().strip()
    )

def validate_form(name, position, salary, dob, email, mobile):
    if not (name and position and salary and dob and email and mobile):
        messagebox.showerror("Error", "All fields must be filled!")
        return False
    # salary numeric
    try:
        float(salary)
    except ValueError:
        messagebox.showerror("Error", "Salary must be a number.")
        return False
    # simple email/mobile validation
    if not is_valid_email(email):
        messagebox.showerror("Error", "Enter a valid email address.")
        return False
    if not is_valid_mobile(mobile):
        messagebox.showerror("Error", "Enter a valid mobile number (digits only).")
        return False
    return True

def add_employee_gui():
    name, position, salary, dob, email, mobile = get_form_values()
    if not validate_form(name, position, salary, dob, email, mobile):
        return
    add_employee(name, position, float(salary), dob, email, mobile)
    messagebox.showinfo("Success", "Employee added successfully!")
    clear_form()
    display_employees()

def update_employee_gui():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select an employee to update!")
        return

    emp_id = tree.item(selected_items[0])['values'][0]   # <-- fixed: index first element
    name, position, salary, dob, email, mobile = get_form_values()
    if not validate_form(name, position, salary, dob, email, mobile):
        return
    update_employee(emp_id, name, position, float(salary), dob, email, mobile)
    messagebox.showinfo("Success", "Employee updated successfully!")
    clear_form()
    display_employees()

def delete_employee_gui():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select an employee to delete!")
        return

    emp_id = tree.item(selected_items[0])['values'][0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected employee?")
    if confirm:
        delete_employee(emp_id)
        messagebox.showinfo("Deleted", "Employee deleted successfully!")
        clear_form()
        display_employees()

def on_tree_select(event):
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(selected[0])['values']
    # values: (id, name, position, salary, dob, email, mobile)
    entry_name.delete(0, tk.END); entry_name.insert(0, values[1])
    entry_position.delete(0, tk.END); entry_position.insert(0, values[2])
    entry_salary.delete(0, tk.END); entry_salary.insert(0, values[3])
    entry_dob.delete(0, tk.END); entry_dob.insert(0, values[4])
    entry_email.delete(0, tk.END); entry_email.insert(0, values[5])
    entry_mobile.delete(0, tk.END); entry_mobile.insert(0, values[6])

# ----------------- Build GUI -----------------
create_table()  # ensure table exists (does NOT drop existing data)

root = tk.Tk()
root.title("Employee Management System")
root.geometry("940x660")
root.configure(bg="#eef6ff")

# Header
header = tk.Label(root, text="EMPLOYEE MANAGEMENT SYSTEM",
                  font=("Segoe UI", 20, "bold"), bg="#0b5ea8", fg="white", pady=12)
header.pack(fill="x")

main_frame = tk.Frame(root, bg="#eef6ff")
main_frame.pack(pady=12, padx=12, fill="both", expand=True)

# Left: Form
form_frame = tk.LabelFrame(main_frame, text="Employee Details", bg="#f7fbff", fg="#0b5ea8",
                           font=("Segoe UI", 11, "bold"), padx=16, pady=12)
form_frame.pack(side="left", fill="y", padx=(0,12))

lbl_width = 26

tk.Label(form_frame, text="Employee Name:", bg="#f7fbff", anchor="w", width=lbl_width).grid(row=0, column=0, sticky="w", pady=6)
entry_name = tk.Entry(form_frame, width=36); entry_name.grid(row=0, column=1, pady=6)

tk.Label(form_frame, text="Position:", bg="#f7fbff", anchor="w", width=lbl_width).grid(row=1, column=0, sticky="w", pady=6)
entry_position = tk.Entry(form_frame, width=36); entry_position.grid(row=1, column=1, pady=6)

tk.Label(form_frame, text="Salary:", bg="#f7fbff", anchor="w", width=lbl_width).grid(row=2, column=0, sticky="w", pady=6)
entry_salary = tk.Entry(form_frame, width=36); entry_salary.grid(row=2, column=1, pady=6)

tk.Label(form_frame, text="Date of Birth (YYYY-MM-DD):", bg="#f7fbff", anchor="w", width=lbl_width).grid(row=3, column=0, sticky="w", pady=6)
entry_dob = tk.Entry(form_frame, width=36); entry_dob.grid(row=3, column=1, pady=6)

tk.Label(form_frame, text="Email:", bg="#f7fbff", anchor="w", width=lbl_width).grid(row=4, column=0, sticky="w", pady=6)
entry_email = tk.Entry(form_frame, width=36); entry_email.grid(row=4, column=1, pady=6)

tk.Label(form_frame, text="Mobile Number:", bg="#f7fbff", anchor="w", width=lbl_width).grid(row=5, column=0, sticky="w", pady=6)
entry_mobile = tk.Entry(form_frame, width=36); entry_mobile.grid(row=5, column=1, pady=6)

# Buttons
button_frame = tk.Frame(form_frame, bg="#f7fbff")
button_frame.grid(row=6, column=0, columnspan=2, pady=(12,0))

btn_add = tk.Button(button_frame, text="Add Employee", width=16, bg="#28a745", fg="white",
                    font=("Segoe UI", 10, "bold"), command=add_employee_gui)
btn_add.grid(row=0, column=0, padx=6, pady=4)

btn_update = tk.Button(button_frame, text="Update Employee", width=16, bg="#007bff", fg="white",
                       font=("Segoe UI", 10, "bold"), command=update_employee_gui)
btn_update.grid(row=0, column=1, padx=6, pady=4)

btn_delete = tk.Button(button_frame, text="Delete Employee", width=16, bg="#dc3545", fg="white",
                       font=("Segoe UI", 10, "bold"), command=delete_employee_gui)
btn_delete.grid(row=0, column=2, padx=6, pady=4)

btn_clear = tk.Button(button_frame, text="Clear Form", width=12, bg="#6c757d", fg="white",
                      font=("Segoe UI", 10), command=clear_form)
btn_clear.grid(row=0, column=3, padx=6, pady=4)

# Right: Table
table_frame = tk.Frame(main_frame)
table_frame.pack(side="right", fill="both", expand=True)

columns = ("ID", "Name", "Position", "Salary", "DOB", "Email", "Mobile")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
tree.pack(side="left", fill="both", expand=True, padx=(0,4))

# Configure scrollbars
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")
tree.configure(yscrollcommand=vsb.set)

for col in columns:
    tree.heading(col, text=col)
    # sensible widths
    if col == "ID":
        tree.column(col, width=50, anchor="center")
    elif col in ("Salary", "DOB"):
        tree.column(col, width=90, anchor="center")
    elif col == "Email":
        tree.column(col, width=220, anchor="w")
    else:
        tree.column(col, width=140, anchor="w")

# Bind selection
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Populate table
display_employees()

# Start GUI loop
root.mainloop()
