import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, messagebox
import sqlite3
import qrcode
from PIL import Image, ImageTk

# Function to open the add-row form
def open_add_row_form():
    def submit_form():
        # Get values from the form fields
        col2 = entry_firstname.get()
        col3 = entry_lastname.get()
        col4 = entry_email.get()
        col5 = entry_mobile.get()
        col6 = entry_company.get()
        col7 = entry_address.get()
        col8 = entry_linkedin.get()

        # Ensure all fields are filled
        if col2 and col3 and col4 and col5 and col6 and col7 and col8:
            # Insert data into SQLite database
            conn = sqlite3.connect('Database/QRCDB.db')  # Updated to use QRCDB.db
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO tbContacts (Firstname, Lastname, EmailAddress, MobileNumber, CompanyName, CompanyAddress, LinkedInAcc)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (col2, col3, col4, col5, col6, col7, col8))
            conn.commit()
            conn.close()

            # Add data to the table in the UI
            table.insert("", "end", values=(col2, col3, col4, col5, col6, col7, col8, 'QR Code'))
            form.destroy()  # Close the form after adding the row
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    # Create a new Toplevel window for the form
    form = Toplevel(root)
    form.title("Add Row")
    form.geometry("300x500")

    ttk.Label(form, text="Firstname:").pack(pady=5)
    entry_firstname = ttk.Entry(form)
    entry_firstname.pack(pady=5)

    ttk.Label(form, text="Lastname:").pack(pady=5)
    entry_lastname = ttk.Entry(form)
    entry_lastname.pack(pady=5)

    ttk.Label(form, text="Email Address:").pack(pady=5)
    entry_email = ttk.Entry(form)
    entry_email.pack(pady=5)

    ttk.Label(form, text="Mobile Number:").pack(pady=5)
    entry_mobile = ttk.Entry(form)
    entry_mobile.pack(pady=5)

    ttk.Label(form, text="Company Name:").pack(pady=5)
    entry_company = ttk.Entry(form)
    entry_company.pack(pady=5)

    ttk.Label(form, text="Company Address:").pack(pady=5)
    entry_address = ttk.Entry(form)
    entry_address.pack(pady=5)

    ttk.Label(form, text="LinkedIn Account:").pack(pady=5)
    entry_linkedin = ttk.Entry(form)
    entry_linkedin.pack(pady=5)

    # Submit button
    ttk.Button(form, text="Submit", command=submit_form).pack(pady=10)

# Function to handle editing a row
def edit_row():
    selected_item = table.selection()
    if selected_item:
        # Retrieve user data from the selected row
        user_data = table.item(selected_item[0], "values")
        # Open edit form pre-filled with current data
        def submit_edit():
            col2 = entry_firstname.get()
            col3 = entry_lastname.get()
            col4 = entry_email.get()
            col5 = entry_mobile.get()
            col6 = entry_company.get()
            col7 = entry_address.get()
            col8 = entry_linkedin.get()

            if col2 and col3 and col4 and col5 and col6 and col7 and col8:
                # Update data in SQLite database
                conn = sqlite3.connect('Database/QRCDB.db')
                cursor = conn.cursor()
                cursor.execute(''' 
                    UPDATE tbContacts SET Firstname=?, Lastname=?, EmailAddress=?, MobileNumber=?, CompanyName=?, CompanyAddress=?, LinkedInAcc=?
                    WHERE Firstname=? AND Lastname=?
                ''', (col2, col3, col4, col5, col6, col7, col8, user_data[0], user_data[1]))
                conn.commit()
                conn.close()

                # Update data in the table UI
                table.item(selected_item[0], values=(col2, col3, col4, col5, col6, col7, col8, 'QR Code'))
                form.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required!")

        # Create a new Toplevel window for the edit form
        form = Toplevel(root)
        form.title("Edit Row")
        form.geometry("300x500")

        # Pre-fill form fields with current user data
        ttk.Label(form, text="Firstname:").pack(pady=5)
        entry_firstname = ttk.Entry(form)
        entry_firstname.insert(0, user_data[0])
        entry_firstname.pack(pady=5)

        ttk.Label(form, text="Lastname:").pack(pady=5)
        entry_lastname = ttk.Entry(form)
        entry_lastname.insert(0, user_data[1])
        entry_lastname.pack(pady=5)

        ttk.Label(form, text="Email Address:").pack(pady=5)
        entry_email = ttk.Entry(form)
        entry_email.insert(0, user_data[2])
        entry_email.pack(pady=5)

        ttk.Label(form, text="Mobile Number:").pack(pady=5)
        entry_mobile = ttk.Entry(form)
        entry_mobile.insert(0, user_data[3])
        entry_mobile.pack(pady=5)

        ttk.Label(form, text="Company Name:").pack(pady=5)
        entry_company = ttk.Entry(form)
        entry_company.insert(0, user_data[4])
        entry_company.pack(pady=5)

        ttk.Label(form, text="Company Address:").pack(pady=5)
        entry_address = ttk.Entry(form)
        entry_address.insert(0, user_data[5])
        entry_address.pack(pady=5)

        ttk.Label(form, text="LinkedIn Account:").pack(pady=5)
        entry_linkedin = ttk.Entry(form)
        entry_linkedin.insert(0, user_data[6])
        entry_linkedin.pack(pady=5)

        # Submit button
        ttk.Button(form, text="Submit", command=submit_edit).pack(pady=10)

# Function to handle deleting a row
def delete_row():
    selected_item = table.selection()
    if selected_item:
        user_data = table.item(selected_item[0], "values")
        # Confirm delete action
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {user_data[0]} {user_data[1]}?")
        if confirm:
            # Delete from database
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                DELETE FROM tbContacts WHERE Firstname=? AND Lastname=?
            ''', (user_data[0], user_data[1]))
            conn.commit()
            conn.close()

            # Delete from table
            table.delete(selected_item[0])

# Ensure to create the database and table if they don't exist
def setup_database():
    conn = sqlite3.connect('Database/QRCDB.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tbContacts (
            Id INTEGER NOT NULL,
            Firstname TEXT NOT NULL,
            Lastname TEXT NOT NULL,
            EmailAddress TEXT NOT NULL,
            MobileNumber INTEGER NOT NULL,
            CompanyName TEXT,
            CompanyAddress TEXT,
            LinkedInAcc INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to generate a QR code for a given user
def generate_qr_code(user_data, size=(300, 300)):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Resize the QR code to fit within the specified size
    img = img.resize(size)
    return img

# Function to fetch data from the database and display it in the table
def fetch_data():
    conn = sqlite3.connect('Database/QRCDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Firstname, Lastname, EmailAddress, MobileNumber, CompanyName, CompanyAddress, LinkedInAcc FROM tbContacts")
    rows = cursor.fetchall()
    conn.close()

    # Clear existing data in the table
    for row in table.get_children():
        table.delete(row)

    # Insert fetched data into the table
    for row in rows:
        user_data = f"Name: {row[0]} {row[1]}\nEmail: {row[2]}\nPhone: {row[3]}"
        qr_img = generate_qr_code(user_data)  # Generate QR code for user data

        # Convert the image to a format that Tkinter can display
        qr_image = ImageTk.PhotoImage(qr_img)

        # Insert data into the table, placeholder for QR code (last column)
        table.insert("", "end", values=row + ('QR Code',))
def show_qr_code_modal(user_data):
    # Generate the QR code image
    qr_img = generate_qr_code(user_data)

    # Create a modal window
    modal = Toplevel(root)
    modal.title("QR Code")
    modal.geometry("350x350")

    # Convert QR image for Tkinter
    qr_image = ImageTk.PhotoImage(qr_img)

    # Display the QR code in the modal
    label = ttk.Label(modal, image=qr_image)
    label.image = qr_image  # Keep a reference to avoid garbage collection
    label.pack(pady=20)

    ttk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)

def setup_treeview_buttons():
    def on_click(event):
        # Get the ID of the clicked row
        item_id = table.identify_row(event.y)
        if item_id:
            # Retrieve the 'values' field of the clicked row
            user_data = table.item(item_id, "values")
            if user_data:
                # Format the data to pass it to the QR code modal
                formatted_user_data = f"Name: {user_data[0]} {user_data[1]}\nEmail: {user_data[2]}\nPhone: {user_data[3]}"
                show_qr_code_modal(formatted_user_data)
            else:
                messagebox.showwarning("Warning", "No data found for the selected row.")
        else:
            messagebox.showwarning("Warning", "Please click on a valid row.")
    table.bind("<Button-1>", on_click)

# Main window
root = tk.Tk()
root.title("UI with Table and Add Button")
root.geometry("1500x400")

# Frame for Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=20)

# Table (Treeview widget)
columns = ("Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7", "Column 8")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

# Define column headings
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

# Add table to frame
table.pack()

# Add Buttons for Add, Edit, and Delete
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

add_button = ttk.Button(button_frame, text="Add Row", command=open_add_row_form)
add_button.grid(row=0, column=0, padx=10)

edit_button = ttk.Button(button_frame, text="Edit Row", command=edit_row)
edit_button.grid(row=0, column=1, padx=10)

delete_button = ttk.Button(button_frame, text="Delete Row", command=delete_row)
delete_button.grid(row=0, column=2, padx=10)

# Call the setup function before starting the main loop
setup_database()
fetch_data()  # Fetch and display data after setting up the database
setup_treeview_buttons() 

# Start the main event loop
root.mainloop()
