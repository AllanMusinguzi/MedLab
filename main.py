import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import threading
from pages.login_signup import LoginSignup
from pages.user_page import UserPage
from pages.admin_page import AdminPage

class LoadingScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Loading")
        self.geometry("500x300")
        self.resizable(False, False)
        self.configure(bg='white')
        self.transient(master)
        self.grab_set()
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack(pady=20)
        self.progress.start()

class MedicalLabSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Medical Lab System")
        self.master.geometry("1366x768")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', font=('Ubuntu', 12))
        self.style.configure('TButton', anchor='center')

        self.db = None
        self.current_frame = None

        self.show_loading_screen()
        threading.Thread(target=self.connect_to_database, daemon=True).start()

    def show_loading_screen(self):
        self.loading_screen = LoadingScreen(self.master)

    def hide_loading_screen(self):
        self.loading_screen.destroy()

    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="imap",
                password="44@@44aa00@Allan",
                database="medical_labdb",
                port = 3307
            )
            print("Database connection successful!")
            self.master.after(0, self.initialize_app)
        except Error as err:
            print(f"Error: {err}")
            self.master.after(0, self.show_connection_error, str(err))

    def show_connection_error(self, error_message):
        self.hide_loading_screen()
        messagebox.showerror("Database Connection Error", 
                             f"Unable to connect to the database. Please check your connection settings.\n\nError: {error_message}")
        self.master.quit()

    def initialize_app(self):
        self.hide_loading_screen()
        if self.db:
            self.show_login_signup()

    def show_login_signup(self):
        self.clear_current_frame()
        self.current_frame = LoginSignup(self.master, self.db, self.login_callback)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_user_page(self, user_id):
        try:
            self.clear_current_frame()
            self.current_frame = UserPage(self.master, self.db, user_id, self.logout_callback)
            self.current_frame.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user page: {str(e)}")

    def show_admin_page(self, user_id, username, password, phone_number):
        try:
            self.clear_current_frame()
            self.current_frame = AdminPage(self.master, self.db, user_id, username, password, phone_number, self.logout_callback)
            self.current_frame.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load admin page: {str(e)}")

    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def login_callback(self, user_id, is_admin, username, password, phone_number):
        try:
            if is_admin:
                self.show_admin_page(user_id, username, password, phone_number)
            else:
                self.show_user_page(user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load page: {str(e)}")

    def logout_callback(self):
        self.show_login_signup()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.db:
                self.db.close()
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalLabSystem(root)
    root.mainloop()
