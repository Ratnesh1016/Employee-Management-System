⭐ Employee Management System (Python + Tkinter + SQLite)
A desktop-based Employee Management System built using Python Tkinter for GUI and SQLite as the backend database.
This application allows HR/Admin users to add, update, delete, and view employee records through an easy-to-use and modern graphical interface.

🚀 Project Overview
This Employee Management System is designed to simplify and digitize employee data management in small businesses and organizations.
The system provides a clean GUI for maintaining employee information and performs all major CRUD operations efficiently.

🛠️ Technologies Used
Component	Technology
Programming Language	Python
GUI Framework	Tkinter & ttk
Database	SQLite
Validation	Regex (Email & Mobile)

✨ Features
✔ Add New Employees
✔ Update Existing Records
✔ Delete Employees
✔ View All Employees in a Table
✔ Auto-Fill Form When Selecting a Row
✔ Input Validation (Email, Salary, Mobile)
✔ Scrollable Treeview Table
✔ Colorful Modern GUI
✔ Persistent Storage Using SQLite

📂 Project Structure
Employee-Management-System/
│── Employee_Management_System.py
│── employee_management.db
│── README.md
│── /documentation
│     ├── Project_Description.pdf
│     ├── Screenshots/

🗃️ Database Structure
Table Name: employees
Column	Type	Description
id	INTEGER (PK)	Unique Employee ID
name	TEXT	Employee Name
position	TEXT	Job Role
salary	REAL	Salary Amount
dob	TEXT	Date of Birth
email	TEXT	Email Address
mobile_number	TEXT	Contact Number

▶️ How to Run the Project

Install Python 3.x

Run this command to install dependencies:

pip install tk


(tkinter comes pre-installed with Python)

Run the script:

python Employee_Management_System.py

🧪 Future Enhancements

🔹 Search bar & filters
🔹 Login system for admin
🔹 Export to Excel / PDF
🔹 Multi-table HRMS structure
🔹 Employee photo upload
🔹 Dark mode UI
