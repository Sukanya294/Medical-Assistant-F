import configparser
import logging
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from customtkinter import CTkFont

from medical_assistant.main.speech_to_text import SpeechToTextConverter


# Create a dictionary to store valid username-password pairs (you can replace this with a database)
class Runner:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # fetching valid users from config.ini
        self.config.read('../config/config.ini')
        self.valid_users = self.config['valid_users']
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.stt = None

    # Function to check login credentials
    def check_login(self):
        username = username_entry.get()
        password = password_entry.get()

        if username in self.valid_users and self.config.get('valid_users', username) == password:
            # Close the login window
            login_window.destroy()

            # Open the data entry form
            self.open_record_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_record_window(self):
        root = ctk.CTk()
        root.state('zoomed')
        self.stt = SpeechToTextConverter(root)
        root.mainloop()


if __name__ == "__main__":
    runner_obj = Runner()

    # Create the main window for login
    logging.info("Validating User login...")
    login_window = ctk.CTk()
    login_window.geometry("700x500")
    login_window.title("Medical Assistant")
    login_window.state('zoomed')
    # login_window.attributes('-fullscreen', True)

    label = ctk.CTkLabel(login_window, text="Login to Medical Assistant", font=("Arial", 30))
    label.pack(pady=20)
    frame = ctk.CTkFrame(master=login_window)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    # Create labels and entry fields for login
    username_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=300, height=50)
    username_entry.pack(pady=12, padx=10)

    password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", width=300, height=50)
    password_entry.pack(pady=12, padx=10)

    # Create a login button
    login_button = ctk.CTkButton(master=frame, text='Login', command=runner_obj.check_login, width=300, height=50)
    login_button.pack(pady=12, padx=10)

    # Start the tkinter main loop for the login window
    login_window.mainloop()
    os.system("exit 0")
