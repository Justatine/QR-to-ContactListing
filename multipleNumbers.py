import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Toplevel, messagebox
import sqlite3
import qrcode
from PIL import Image, ImageTk
from tkinter import Listbox

# Setup database function
def setup_database():
    conn = sqlite3.connect('Database/QRCDB.db')
    cursor = conn.cursor()
    
    # tbContacts Table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tbContacts (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Firstname TEXT NOT NULL,
            Lastname TEXT NOT NULL,
            EmailAddress TEXT NOT NULL,
            CompanyName TEXT,
            CompanyAddress TEXT,
            CompanyNumber INTEGER NOT NULL,
            LinkedInAcc TEXT
        )
    ''')
    
    # tbContactNos Table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tbContactNos (
            contactId INTEGER PRIMARY KEY AUTOINCREMENT,
            Id INTEGER NOT NULL,
            MobileNumber INTEGER NOT NULL
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

def fetch_data():
    # Clear the table
    for row in table.get_children():
        table.delete(row)

    try:
        conn = sqlite3.connect('Database/QRCDB.db')
        cursor = conn.cursor()

        # Select only the columns you need
        cursor.execute('''
            SELECT *
            FROM tbContacts
        ''')
        rows = cursor.fetchall()

        for row in rows:
            if row:
                table.insert("", "end", values=(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
                ))
            else:
                messagebox.showerror("Data Error", f"Incomplete row data: {row}")

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {str(e)}")

def add_contact():
    def add_mobile_number():
        number = entry_mobile.get()
        if number:
            mobile_list.insert("end", number)
            entry_mobile.delete(0, "end")
        else:
            messagebox.showwarning("Warning", "Mobile number cannot be empty!")

    def remove_mobile_number():
        selected = mobile_list.curselection()
        if selected:
            mobile_list.delete(selected)
        else:
            messagebox.showwarning("Warning", "Please select a mobile number to remove!")

    def submit_form():
        firstname = entry_firstname.get()
        lastname = entry_lastname.get()
        email = entry_email.get()
        company = entry_company.get()
        address = entry_address.get()
        company_number = entry_company_number.get()
        linkedin = entry_linkedin.get()
        mobile_numbers = list(mobile_list.get(0, "end"))

        if firstname and lastname and email and mobile_numbers and company and address and company_number and linkedin:
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO tbContacts (Firstname, Lastname, EmailAddress, CompanyName, CompanyAddress, CompanyNumber, LinkedInAcc)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (firstname, lastname, email, company, address, company_number, linkedin))
            contact_id = cursor.lastrowid

            for mobile in mobile_numbers:
                cursor.execute('''
                    INSERT INTO tbContactNos (Id, MobileNumber)
                    VALUES (?, ?)
                ''', (contact_id, mobile))

            conn.commit()
            conn.close()

            table.insert("", "end", values=(firstname, lastname, email, ", ".join(mobile_numbers), company, address, company_number, linkedin))
            form.destroy()  

            show_message("Add Contact", "Contact added")
            fetch_data()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    form = Toplevel(root)
    form.title("Add Contact")
    form.geometry("600x600")
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

    # Layout and labels
    ttk.Label(form, text="Firstname:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_firstname = ttk.Entry(form)
    entry_firstname.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(form, text="Lastname:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_lastname = ttk.Entry(form)
    entry_lastname.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(form, text="Email Address:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = ttk.Entry(form)
    entry_email.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(form, text="Mobile Numbers:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_mobile = ttk.Entry(form)
    entry_mobile.grid(row=3, column=1, padx=10, pady=5)

    ttk.Button(form, text="Add Number", command=add_mobile_number).grid(row=3, column=2, padx=10, pady=5)
    mobile_list = Listbox(form, height=5)
    mobile_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    ttk.Button(form, text="Remove Selected", command=remove_mobile_number).grid(row=4, column=2, padx=10, pady=5)

    ttk.Label(form, text="Company Name:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_company = ttk.Entry(form)
    entry_company.grid(row=5, column=1, padx=10, pady=5)

    ttk.Label(form, text="Company Address:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_address = ttk.Entry(form)
    entry_address.grid(row=6, column=1, padx=10, pady=5)

    ttk.Label(form, text="Company Number:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    entry_company_number = ttk.Entry(form)
    entry_company_number.grid(row=7, column=1, padx=10, pady=5)

    ttk.Label(form, text="LinkedIn Account:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    entry_linkedin = ttk.Entry(form)
    entry_linkedin.grid(row=8, column=1, padx=10, pady=5)

    ttk.Button(form, text="Submit", command=submit_form).grid(row=9, column=0, columnspan=3, pady=20)

def edit_contact():
    selected_item = table.selection()

    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a contact to edit.")
        return

    user_data = table.item(selected_item[0], "values")

    def update_contact():
        firstname = entry_firstname.get()
        lastname = entry_lastname.get()
        email = entry_email.get()
        company = entry_company.get()
        address = entry_address.get()
        company_number = entry_company_number.get()
        linkedin = entry_linkedin.get()
        mobile_numbers = list(mobile_list.get(0, "end"))

        if firstname and lastname and email and mobile_numbers and company and address and company_number and linkedin:
            try:
                conn = sqlite3.connect('Database/QRCDB.db')
                cursor = conn.cursor()

                # Update the tbContacts table
                cursor.execute(''' 
                    UPDATE tbContacts SET 
                    Firstname = ?, 
                    Lastname = ?, 
                    EmailAddress = ?, 
                    CompanyName = ?, 
                    CompanyAddress = ?, 
                    CompanyNumber = ?, 
                    LinkedInAcc = ? 
                    WHERE Id = ?
                ''', (firstname, lastname, email, company, address, company_number, linkedin, user_data[0]))

                cursor.execute('DELETE FROM tbContactNos WHERE Id = ?', (user_data[0],))
                for mobile in mobile_numbers:
                    cursor.execute('''INSERT INTO tbContactNos (Id, MobileNumber) VALUES (?, ?)''', 
                                   (user_data[0], int(mobile) ))

                conn.commit()
                conn.close()

                # Refresh the table
                fetch_data()

                form.destroy()
                show_message("Update Contact", "Contact updated successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error updating contact: {str(e)}")
        else:
            messagebox.showwarning("Validation Error", "All fields are required!")

    def add_mobile_number():
        number = entry_mobile.get()
        if number:
            mobile_list.insert("end", number)
            entry_mobile.delete(0, "end")
        else:
            messagebox.showwarning("Input Error", "Mobile number cannot be empty!")

    def remove_mobile_number():
        selected = mobile_list.curselection()
        if selected:
            mobile_list.delete(selected)
        else:
            messagebox.showwarning("Selection Error", "Please select a number to remove!")

    # Create the edit form
    form = Toplevel(root)
    form.title("Edit Contact")
    form.geometry("600x600")
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
    
    ttk.Label(form, text="Firstname:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_firstname = ttk.Entry(form)
    entry_firstname.grid(row=0, column=1, padx=10, pady=5)
    entry_firstname.insert(0, user_data[1])

    ttk.Label(form, text="Lastname:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_lastname = ttk.Entry(form)
    entry_lastname.grid(row=1, column=1, padx=10, pady=5)
    entry_lastname.insert(0, user_data[2])

    ttk.Label(form, text="Email Address:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = ttk.Entry(form)
    entry_email.grid(row=2, column=1, padx=10, pady=5)
    entry_email.insert(0, user_data[3])

    ttk.Label(form, text="Mobile Numbers:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_mobile = ttk.Entry(form)
    entry_mobile.grid(row=3, column=1, padx=10, pady=5)
    ttk.Button(form, text="Add Number", command=add_mobile_number).grid(row=3, column=2, padx=10, pady=5)
    mobile_list = Listbox(form, height=5)
    mobile_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    ttk.Button(form, text="Remove Selected", command=remove_mobile_number).grid(row=4, column=2, padx=10, pady=5)

    # Pre-populate mobile numbers
    conn = sqlite3.connect('Database/QRCDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MobileNumber FROM tbContactNos WHERE Id = ?', (user_data[0],))
    mobile_numbers = cursor.fetchall()
    conn.close()

    for mobile in mobile_numbers:
        mobile_list.insert("end", mobile[0])

    ttk.Label(form, text="Company Name:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_company = ttk.Entry(form)
    entry_company.grid(row=5, column=1, padx=10, pady=5)
    entry_company.insert(0, user_data[4])

    ttk.Label(form, text="Company Address:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_address = ttk.Entry(form)
    entry_address.grid(row=6, column=1, padx=10, pady=5)
    entry_address.insert(0, user_data[5])

    ttk.Label(form, text="Company Number:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    entry_company_number = ttk.Entry(form)
    entry_company_number.grid(row=7, column=1, padx=10, pady=5)
    entry_company_number.insert(0, user_data[6])

    ttk.Label(form, text="LinkedIn Account:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    entry_linkedin = ttk.Entry(form)
    entry_linkedin.grid(row=8, column=1, padx=10, pady=5)
    entry_linkedin.insert(0, user_data[7])

    ttk.Button(form, text="Update", command=update_contact).grid(row=9, column=0, columnspan=3, pady=20)

def delete_row():
    selected_item = table.selection()
    if selected_item:
        user_data = table.item(selected_item[0], "values")
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete user {user_data[0]}?")
        if confirm:
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM tbContactNos WHERE Id=?
            ''', (user_data[0]))

            cursor.execute(''' 
                DELETE FROM tbContacts WHERE Id=?
            ''', (user_data[0]))
            
            conn.commit()
            conn.close()

            table.delete(selected_item[0])
            show_message("Remove Contact","Contact removed")

            fetch_data()

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
root.resizable(True,True)

table_frame = ttk.Frame(root)
table_frame.pack(pady=20)

table_cols = (
    "Id", "Firstname", "Lastname", "Email Address", "Company Name",
    "Company Address", "Company Number", "LinkedIn Account"
)

table = ttk.Treeview(table_frame, columns=table_cols, show="headings", height=10)

for col in table_cols:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

table.pack()

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

add_button = ttk.Button(button_frame, text="Add Contact",command=add_contact)
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
