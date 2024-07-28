import tkinter as tk
from tkinter import ttk
import sqlite3
from encrypt import Encryptor
import utilities

# Create an instance of Encryptor
encryptor = Encryptor('C:/Users/bbabi/OneDrive/Desktop/Password Manager/key.txt')

# Function to create a new user account and store it in the SQLite database
def create_account():
    # Clear any previous error message
    error_label.config(text="")
    
    username = username_entry.get()
    password = password_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_number = phone_number_entry.get()

    # Check if any field is empty
    if not username or not password or not first_name or not last_name or not phone_number:
        error_label.config(text="All fields are required.")
        return

    # Capitalize first letter of names
    first_name = utilities.capitalize_first_letter(first_name)
    last_name = utilities.capitalize_first_letter(last_name)

    # Clean and validate phone number
    cleaned_phone_number = utilities.clean_number(phone_number)
    if not utilities.is_valid_phone_number(cleaned_phone_number):
        error_label.config(text="Invalid phone number format.")
        return

    # Encrypt the username and phone number for comparison
    encrypted_username = encryptor.encrypt(username)
    encrypted_phone_number = encryptor.encrypt(cleaned_phone_number)

    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the username already exists
    c.execute('''SELECT 1 FROM users WHERE username = ?''', (encrypted_username,))
    if c.fetchone():
        error_label.config(text="Username already exists. Try again.")
        conn.close()
        return

    # Check if the phone number already exists
    c.execute('''SELECT 1 FROM users WHERE phone_number = ?''', (encrypted_phone_number,))
    if c.fetchone():
        error_label.config(text="Phone number already exists. Try again.")
        conn.close()
        return

    # Encrypt the rest of the user data
    encrypted_password = encryptor.encrypt(password)
    encrypted_first_name = encryptor.encrypt(first_name)
    encrypted_last_name = encryptor.encrypt(last_name)

    # Create a table for user accounts if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL
                )''')

    # Insert new user account into the database
    c.execute('''INSERT INTO users (username, password, first_name, last_name, phone_number)
                 VALUES (?, ?, ?, ?, ?)''', (encrypted_username, encrypted_password, encrypted_first_name, encrypted_last_name, encrypted_phone_number))
    conn.commit()

    conn.close()
    print("Account created successfully!")
    # Go back to the main menu
    show_main_menu()

# Function to handle user login
def login():
    # Clear any previous error message
    error_label.config(text="")
    
    username = username_entry.get()
    password = password_entry.get()

    # Check if any field is empty
    if not username or not password:
        error_label.config(text="All fields are required.")
        return

    # Encrypt the username for comparison
    encrypted_username = encryptor.encrypt(username)

    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the username and password match a record in the database
    c.execute('''SELECT password FROM users WHERE username = ?''', (encrypted_username,))
    result = c.fetchone()

    conn.close()

    if result:
        encrypted_password = result[0]
        decrypted_password = encryptor.decrypt(encrypted_password)
        if password == decrypted_password:
            print("Login successful!")
            # Optionally, you can navigate to the next screen here
        else:
            error_label.config(text="Invalid username or password.")
    else:
        error_label.config(text="Invalid username or password.")

# Function to switch to the create account screen
def show_create_account_screen():
    clear_screen()
    first_name_label.pack(pady=5)
    first_name_entry.pack(pady=5)
    last_name_label.pack(pady=5)
    last_name_entry.pack(pady=5)
    phone_number_label.pack(pady=5)
    phone_number_entry.pack(pady=5)
    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    create_account_btn.pack(pady=10)
    back_to_menu_btn.pack(pady=10)
    error_label.pack(pady=5)

# Function to switch to the login screen
def show_login_screen():
    clear_screen()
    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_btn.pack(pady=10)
    back_to_menu_btn.pack(pady=10)
    error_label.pack(pady=5)

# Function to clear the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.pack_forget()

# Function to show the main menu
def show_main_menu():
    clear_screen()
    ttk.Label(root, text="Welcome to the Password Manager", style='Title.TLabel').pack(pady=20)
    signup_btn.pack(pady=10)
    main_login_btn.pack(pady=10)
    exit_btn.pack(pady=10)

# Create the main menu window
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x500")  # Set window size

# Define styles
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12))
style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
style.configure('TButton', font=('Helvetica', 12))

# Main menu label
ttk.Label(root, text="Welcome to the Password Manager", style='Title.TLabel').pack(pady=20)

# First Name Entry
first_name_label = ttk.Label(root, text="First Name:", style='TLabel')
first_name_entry = ttk.Entry(root, font=('Helvetica', 12))

# Last Name Entry
last_name_label = ttk.Label(root, text="Last Name:", style='TLabel')
last_name_entry = ttk.Entry(root, font=('Helvetica', 12))

# Phone Number Entry
phone_number_label = ttk.Label(root, text="Phone Number:", style='TLabel')
phone_number_entry = ttk.Entry(root, font=('Helvetica', 12))

# Username Entry
username_label = ttk.Label(root, text="Username:", style='TLabel')
username_entry = ttk.Entry(root, font=('Helvetica', 12))

# Password Entry
password_label = ttk.Label(root, text="Password:", style='TLabel')
password_entry = ttk.Entry(root, show="*", font=('Helvetica', 12))

# Create Account Button
create_account_btn = ttk.Button(root, text="Create Account", command=create_account, style='TButton')

# Login Button
login_btn = ttk.Button(root, text="Login", command=login, style='TButton')

# Main Menu Buttons
signup_btn = ttk.Button(root, text="Signup", command=show_create_account_screen, style='TButton')
main_login_btn = ttk.Button(root, text="Login", command=show_login_screen, style='TButton')

# Exit Button
exit_btn = ttk.Button(root, text="Exit", command=root.destroy, style='TButton')
back_to_menu_btn = ttk.Button(root, text="Back to Menu", command=show_main_menu, style='TButton')

# Error Label
error_label = ttk.Label(root, text="", style='TLabel', foreground='red')

# Show the main menu
show_main_menu()

# Run the main loop
root.mainloop()