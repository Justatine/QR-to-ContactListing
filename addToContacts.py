import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import sqlite3
import qrcode
from PIL import Image, ImageTk


# Function to open the add-row form
def open_add_row_form():
    def submit_form():
        col2 = entry_firstname.get()
        col3 = entry_lastname.get()
        col4 = entry_email.get()
        col5 = entry_mobile.get()
        col6 = entry_company.get()
        col7 = entry_address.get()
        col8 = entry_linkedin.get()

        if col2 and col3 and col4 and col5 and col6 and col7 and col8:
            # Insert data into SQLite database
            conn = sqlite3.connect('Database/QRCDB.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO tbContacts (Firstname, Lastname, EmailAddress, MobileNumber, CompanyName, CompanyAddress, LinkedInAcc)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (col2, col3, col4, col5, col6, col7, col8))
            conn.commit()
            conn.close()

            # Add data to the table in the UI
            table.insert("", "end", values=(col2, col3, col4, col5, col6, col7, col8, 'QR Code'))
            form.destroy()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

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

    ttk.Button(form, text="Submit", command=submit_form).pack(pady=10)


# Function to generate a QR code with vCard data
def generate_qr_code_vcard(firstname, lastname, email, mobile, company, address):
    vcard_data = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"N:{lastname};{firstname}\n"
        f"FN:{firstname} {lastname}\n"
        f"EMAIL:{email}\n"
        f"TEL:{mobile}\n"
        f"ORG:{company}\n"
        f"ADR:;;{address}\n"
        "END:VCARD"
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


# Function to display QR code for a contact
def show_qr_code_modal(user_data):
    qr_img = generate_qr_code_vcard(
        user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5]
    )
    modal = Toplevel(root)
    modal.title("QR Code")
    modal.geometry("350x350")

    qr_image = ImageTk.PhotoImage(qr_img)
    label = ttk.Label(modal, image=qr_image)
    label.image = qr_image
    label.pack(pady=20)

    ttk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)


def setup_treeview_buttons():
    def on_click(event):
        item_id = table.identify_row(event.y)
        if item_id:
            user_data = table.item(item_id, "values")
            if user_data:
                show_qr_code_modal(user_data)
            else:
                messagebox.showwarning("Warning", "No data found for the selected row.")
        else:
            messagebox.showwarning("Warning", "Please click on a valid row.")

    table.bind("<Button-1>", on_click)


# Main window
root = tk.Tk()
root.title("Contact Management")
root.geometry("1500x400")

# Table
columns = ("Firstname", "Lastname", "Email", "Mobile", "Company", "Address", "LinkedIn", "QR Code")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

table.pack(pady=20)

# Buttons
add_button = ttk.Button(root, text="Add Contact", command=open_add_row_form)
add_button.pack()

setup_treeview_buttons()

root.mainloop()
