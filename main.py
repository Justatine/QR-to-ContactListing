import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Toplevel, messagebox
import sqlite3
import qrcode
from PIL import Image, ImageTk

# Setup database function
def setup_database():
    conn = sqlite3.connect('Database/QRCDB.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tbContacts (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Firstname TEXT NOT NULL,
            Lastname TEXT NOT NULL,
            EmailAddress TEXT NOT NULL,
            MobileNumber INTEGER NOT NULL,
            CompanyName TEXT,
            CompanyAddress TEXT,
            CompanyNumber INTEGER NOT NULL,
            LinkedInAcc TEXT
        )
    ''')
    conn.commit()
    conn.close()

def show_message(title, message):
    messagebox.showinfo(
        title=title,
        message=message,
        parent=root 
    )

# Function to fetch data and populate Treeview
def fetch_data():
    for row in table.get_children():
        table.delete(row)

    try:
        conn = sqlite3.connect('Database/QRCDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbContacts")
        rows = cursor.fetchall()
        
        for row in rows:
            name = f"{row[1]} {row[2]}"
            table.insert("", "end", values=(
                row[0], row[1], row[2], row[3], ''.join(['0',str(row[4])]), row[5], row[6], row[7], row[8]
            ))

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {str(e)}")

def open_add_row_form():
    def submit_form():
        firstname = entry_firstname.get()
        lastname = entry_lastname.get()
        email = entry_email.get()
        mobile = entry_mobile.get()
        company = entry_company.get()
        address = entry_address.get()
        company_number = entry_company_number.get()
        linkedin = entry_linkedin.get()

        if firstname and lastname and email and mobile and company and address and company_number and linkedin:
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO tbContacts (Firstname, Lastname, EmailAddress, MobileNumber, CompanyName, CompanyAddress, CompanyNumber, LinkedInAcc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (firstname, lastname, email, mobile, company, address, company_number, linkedin))
            conn.commit()
            conn.close()

            table.insert("", "end", values=(firstname, lastname, email, mobile, company, address, company_number, linkedin))
            form.destroy()  
            
            show_message("Add Contact","Contact added")
            fetch_data()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    form = Toplevel(root)
    form.title("Add Contact")
    form.geometry("600x450") 
    form.resizable(False, False)

    # Center the form window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    form_width = 600
    form_height = 450

    # Calculate position for centering
    x = root_x + (root_width // 2) - (form_width // 2)
    y = root_y + (root_height // 2) - (form_height // 2)

    form.geometry(f"{form_width}x{form_height}+{x}+{y}")

    for i in range(3):
        form.columnconfigure(i, weight=1)

    # Personal Details
    ttk.Label(form, text="Personal Details", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10)
    ttk.Label(form, text="Firstname:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_firstname = ttk.Entry(form)
    entry_firstname.grid(row=2, column=0, padx=10, pady=5)

    ttk.Label(form, text="Lastname:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_lastname = ttk.Entry(form)
    entry_lastname.grid(row=4, column=0, padx=10, pady=5)

    # Contact Details
    ttk.Label(form, text="Contact Details", font=("Arial", 12, "bold")).grid(row=0, column=1, pady=10)
    ttk.Label(form, text="Email Address:").grid(row=1, column=1, sticky="w", padx=10, pady=5)
    entry_email = ttk.Entry(form)
    entry_email.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(form, text="Mobile Number:").grid(row=3, column=1, sticky="w", padx=10, pady=5)
    entry_mobile = ttk.Entry(form)
    entry_mobile.grid(row=4, column=1, padx=10, pady=5)

    # Company Details
    ttk.Label(form, text="Company Details", font=("Arial", 12, "bold")).grid(row=0, column=2, pady=10)
    ttk.Label(form, text="Company Name:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
    entry_company = ttk.Entry(form)
    entry_company.grid(row=2, column=2, padx=10, pady=5)

    ttk.Label(form, text="Company Address:").grid(row=3, column=2, sticky="w", padx=10, pady=5)
    entry_address = ttk.Entry(form)
    entry_address.grid(row=4, column=2, padx=10, pady=5)

    ttk.Label(form, text="Company Number:").grid(row=5, column=2, sticky="w", padx=10, pady=5)  # New label for company number
    entry_company_number = ttk.Entry(form)  # New entry for company number
    entry_company_number.grid(row=6, column=2, padx=10, pady=5)

    ttk.Label(form, text="LinkedIn Account:").grid(row=7, column=2, sticky="w", padx=10, pady=5)
    entry_linkedin = ttk.Entry(form)
    entry_linkedin.grid(row=8, column=2, padx=10, pady=5)

    # Submit button
    ttk.Button(form, text="Submit", command=submit_form).grid(row=9, column=1, pady=20)

def delete_row():
    selected_item = table.selection()
    if selected_item:
        user_data = table.item(selected_item[0], "values")
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete user {user_data[0]}?")
        if confirm:
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                DELETE FROM tbContacts WHERE Id=?
            ''', (user_data[0]))
            conn.commit()
            conn.close()

            table.delete(selected_item[0])
            show_message("Remove Contact","Contact removed")

            fetch_data()

def edit_contact():
    selected_item = table.selection()
    
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a contact to edit.")
        return

    user_data = table.item(selected_item[0], "values")

    def submit_form():
        firstname = entry_firstname.get()
        lastname = entry_lastname.get()
        email = entry_email.get()
        mobile = entry_mobile.get()
        company = entry_company.get()
        address = entry_address.get()
        company_number = entry_company_number.get()
        linkedin = entry_linkedin.get()

        if firstname and lastname and email and mobile and company and address and company_number and linkedin:
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                UPDATE tbContacts SET 
                Firstname = ?, 
                Lastname = ?, 
                EmailAddress = ?, 
                MobileNumber = ?, 
                CompanyName = ?, 
                CompanyAddress = ?, 
                CompanyNumber = ?, 
                LinkedInAcc = ? 
                WHERE Id = ?
            ''', (firstname, lastname, email, mobile, company, address, company_number, linkedin, user_data[0]))
            
            confirm = messagebox.askyesno(title="test", message="test")
            if confirm:
                conn.commit()
                conn.close()

                table.item(selected_item[0], values=(
                    user_data[0], firstname, lastname, email, mobile, company, address, company_number, linkedin
                ))

                form.destroy() 
                show_message("Update Contact","Contact updated")
            else:
                show_message("Update Contact","Update cancelled")

            fetch_data()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    form = Toplevel(root)
    form.title("Edit Contact")
    form.geometry("600x450")  
    form.resizable(False, False)

    # Center the form window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    form_width = 600
    form_height = 450

    # Calculate position for centering
    x = root_x + (root_width // 2) - (form_width // 2)
    y = root_y + (root_height // 2) - (form_height // 2)

    form.geometry(f"{form_width}x{form_height}+{x}+{y}")
    
    for i in range(3):
        form.columnconfigure(i, weight=1)

    # Personal Details
    ttk.Label(form, text="Personal Details", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10)
    ttk.Label(form, text="Firstname:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_firstname = ttk.Entry(form)
    entry_firstname.grid(row=2, column=0, padx=10, pady=5)
    entry_firstname.insert(0, user_data[1])  

    ttk.Label(form, text="Lastname:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_lastname = ttk.Entry(form)
    entry_lastname.grid(row=4, column=0, padx=10, pady=5)
    entry_lastname.insert(0, user_data[2])  

    # Contact Details
    ttk.Label(form, text="Contact Details", font=("Arial", 12, "bold")).grid(row=0, column=1, pady=10)
    ttk.Label(form, text="Email Address:").grid(row=1, column=1, sticky="w", padx=10, pady=5)
    entry_email = ttk.Entry(form)
    entry_email.grid(row=2, column=1, padx=10, pady=5)
    entry_email.insert(0, user_data[3])  

    ttk.Label(form, text="Mobile Number:").grid(row=3, column=1, sticky="w", padx=10, pady=5)
    entry_mobile = ttk.Entry(form)
    entry_mobile.grid(row=4, column=1, padx=10, pady=5)
    entry_mobile.insert(0, user_data[4])  

    # Company Details
    ttk.Label(form, text="Company Details", font=("Arial", 12, "bold")).grid(row=0, column=2, pady=10)
    ttk.Label(form, text="Company Name:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
    entry_company = ttk.Entry(form)
    entry_company.grid(row=2, column=2, padx=10, pady=5)
    entry_company.insert(0, user_data[5])  

    ttk.Label(form, text="Company Address:").grid(row=3, column=2, sticky="w", padx=10, pady=5)
    entry_address = ttk.Entry(form)
    entry_address.grid(row=4, column=2, padx=10, pady=5)
    entry_address.insert(0, user_data[6])  

    ttk.Label(form, text="Company Number:").grid(row=5, column=2, sticky="w", padx=10, pady=5)
    entry_company_number = ttk.Entry(form)
    entry_company_number.grid(row=6, column=2, padx=10, pady=5)
    entry_company_number.insert(0, user_data[7])  

    ttk.Label(form, text="LinkedIn Account:").grid(row=7, column=2, sticky="w", padx=10, pady=5)
    entry_linkedin = ttk.Entry(form)
    entry_linkedin.grid(row=8, column=2, padx=10, pady=5)
    entry_linkedin.insert(0, user_data[8])  

    # Submit button
    ttk.Button(form, text="Submit", command=submit_form).grid(row=9, column=1, pady=20)

def generate_qr_code_vcard(firstname, lastname, email, mobile, company, address, number, linkedIn):
    vcard_data = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"N:{lastname};{firstname}\n"
        f"FN:{firstname} {lastname}\n"
        f"EMAIL:{email}\n"
        f"TEL:{''.join(['0', str(mobile)])}\n"
        f"ORG:{company}\n"
        f"ADR:;;{address}\n"
        # f"ADR:;;{number}\n"
        # f"ADR:;;{linkedIn}\n"
        "END:VCARD"
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def open_qr():
    selected_item = table.selection()
    
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a contact to edit.")
        return

    user_data = table.item(selected_item[0], "values")
    contact_id = user_data[0]  

    try:
        conn = sqlite3.connect('Database/QRCDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbContacts WHERE Id=?", (contact_id,))
        contact = cursor.fetchone() 

        if contact:
            qr_img = generate_qr_code_vcard(
                contact[1], contact[2], contact[3], contact[4], contact[5], contact[6], contact[7], contact[8] 
            )
            modal = Toplevel(root)
            modal.title(f"QR Code for user {contact[1]} {contact[2]}")
            modal.geometry("350x350")

            # Center the modal window
            modal.update_idletasks() 
            screen_width = modal.winfo_screenwidth()
            screen_height = modal.winfo_screenheight()
            window_width = 350
            window_height = 350
            position_x = (screen_width // 2) - (window_width // 2)
            position_y = (screen_height // 2) - (window_height // 2)
            modal.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

            qr_image = ImageTk.PhotoImage(qr_img)
            label = ttk.Label(modal, image=qr_image)
            label.image = qr_image
            label.pack(pady=20)

            ttk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)
        else:
            print("No contact found with the given ID.")

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {str(e)}")

root = tk.Tk()
root.title("Contact QR Code Generator")
root.geometry("1500x400")

table_frame = ttk.Frame(root)
table_frame.pack(pady=20)

table_cols = (
    "Id", "Firstname", "Lastname", "Email Address", "Mobile Number", "Company Name",
    "Company Address", "Company Number", "LinkedIn Account"
)

table = ttk.Treeview(table_frame, columns=table_cols, show="headings", height=10)

for col in table_cols:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

table.pack()

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

add_button = ttk.Button(button_frame, text="Add Contact",command=open_add_row_form)
add_button.grid(row=0, column=0, padx=10)

edit_button = ttk.Button(button_frame, text="Edit Contact", command=edit_contact)
edit_button.grid(row=0, column=1, padx=10)

delete_button = ttk.Button(button_frame, text="Delete Contact",command=delete_row)
delete_button.grid(row=0, column=2, padx=10)

open_qr_button = ttk.Button(button_frame, text="Open QR Code", command=open_qr)
open_qr_button.grid(row=0, column=3, padx=10)
# Initialize database
setup_database()

# Automatically fetch data on startup
fetch_data()

# Start GUI loop
root.mainloop()
