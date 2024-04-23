import os
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import logging
import configparser
from PIL import Image, ImageTk

from medical_assistant.main.speech_to_text import SpeechToTextConverter

class Runner:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config/config.ini')
        self.valid_users = self.config['valid_users']
        self.stt = None
        self.login_window = None

    def create_login_window(self):
        # Create the main window for login
        logging.info("Validating User login...")
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("1000x700")  # Adjust the window size

        # Set background image
        bg_image = Image.open("../../data/images/medical_assistant_logo.png")  # Change the path to your image
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.login_window, image=bg_photo)
        bg_label.place(relx=0.5, rely=0, anchor="n")  # Position at the center top

        # Create style for the labels and buttons
        style = ttk.Style()
        style.configure("TLabel", foreground="#007bff", font=("Arial", 16, "bold"))  # Adjust label font and color
        style.configure("TButton", foreground="#fff", background="#007bff", font=("Arial", 14, "bold"), padding=10)  # Adjust button font, color, and padding
        style.map("TButton", background=[("active", "#0056b3")])  # Adjust button color when active

        # Create heading
        login_heading = ttk.Label(self.login_window, text="Login", font=("Arial", 24, "bold"), foreground="#000000")  # Black color for heading
        login_heading.grid(row=1, columnspan=2, pady=20, sticky="ew")  # Adjust heading position and spacing

        # Create labels and entry fields for login
        username_label = ttk.Label(self.login_window, text="Username:")
        username_label.grid(row=2, column=0, pady=20, sticky="e")  # Adjust label position and spacing

        self.username_entry = ttk.Entry(self.login_window, font=("Arial", 14))
        self.username_entry.grid(row=2, column=1, pady=20, sticky="ew")  # Adjust entry position and spacing

        password_label = ttk.Label(self.login_window, text="Password:")
        password_label.grid(row=3, column=0, pady=20, sticky="e")  # Adjust label position and spacing

        self.password_entry = ttk.Entry(self.login_window, show="*", font=("Arial", 14))
        self.password_entry.grid(row=3, column=1, pady=20, sticky="ew")  # Adjust entry position and spacing

        # Create a login button
        login_button = ttk.Button(self.login_window, text="Login", command=self.check_login)
        login_button.grid(row=4, columnspan=2, pady=20, sticky="ew")  # Adjust button position and spacing

        # Center the widgets horizontally within the window
        for child in self.login_window.winfo_children():
            child.grid_configure(padx=20)
            child.grid_configure(sticky="ew")

        # Start the tkinter main loop for the login window
        self.login_window.mainloop()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.valid_users and self.config.get('valid_users', username) == password:
            # Close the login window
            self.login_window.destroy()

            # Open the data entry form
            self.open_record_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_record_window(self):
        root = tk.Tk()
        self.stt = SpeechToTextConverter(root)
        root.mainloop()

if __name__ == "__main__":
    runner_obj = Runner()
    runner_obj.create_login_window()
    os.system("exit 0")
