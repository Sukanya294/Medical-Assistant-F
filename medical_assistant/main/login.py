import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import logging
import configparser


# Create a dictionary to store valid username-password pairs (you can replace this with a database)
class Runner:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # fetching valid users from config.ini
        self.config.read('../config/config.ini')
        self.valid_users = self.config['valid_users']

    # Function to check login credentials
    def check_login(self):
        username = username_entry.get()
        password = password_entry.get()

        if username in self.valid_users and self.config.get('valid_users', username) == password:
            # Close the login window
            login_window.destroy()

            # Open the data entry form
            self.open_data_entry_form()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Function to open the data entry form
    @staticmethod
    def open_data_entry_form():
        data_entry_window = tk.Tk()
        data_entry_window.title("Data Entry Form")

        # Create labels and entry fields for data
        name_label = tk.Label(data_entry_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(data_entry_window)
        name_entry.pack()

        age_label = tk.Label(data_entry_window, text="Age:")
        age_label.pack()
        age_entry = tk.Entry(data_entry_window)
        age_entry.pack()

        height_label = tk.Label(data_entry_window, text="Height (cm):")
        height_label.pack()
        height_entry = tk.Entry(data_entry_window)
        height_entry.pack()

        # Function to save the data to an Excel file
        def save_data():
            data = {
                "Name": [name_entry.get()],
                "Age": [age_entry.get()],
                "Height (cm)": [height_entry.get()]
            }

            df = pd.DataFrame(data)

            # Save the data to an Excel file
            df.to_excel('../../data/user_data.xlsx', index=False)
            messagebox.showinfo("Data Saved", "Data has been saved to data/user_data.xlsx")

        # Create a button to save the data
        save_button = tk.Button(data_entry_window, text="Save", command=save_data)
        save_button.pack()

        data_entry_window.mainloop()


if __name__ == "__main__":
    runner_obj = Runner()

    # Create the main window for login
    logging.info("Validating User login...")
    login_window = tk.Tk()
    login_window.title("Login")

    # Create labels and entry fields for login
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")  # Show asterisks for password
    password_entry.pack()

    # Create a login button
    login_button = tk.Button(login_window, text="Login", command=runner_obj.check_login)
    login_button.pack()

    # Start the tkinter main loop for the login window
    login_window.mainloop()
    os.system("exit 0")
