import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import threading
import configparser

from pages.login_signup import LoginSignup
from pages.user_page import UserPage
from pages.admin_page import AdminPage
#from pages.report_generate import ReportGenerate

class LoadingScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Loading")
        self.geometry("300x150")
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')
        self.transient(master)
        self.grab_set()
        
        self.label = tk.Label(self, text="Loading...", font=('Helvetica', 14), bg='#f0f0f0')
        self.label.pack(pady=20)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind('<Configure>', self.resize_frame)

    def resize_frame(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

class MedicalLabSystem:
    def __init__(self, master):
        self.master = master
        self.config = self.load_config()

        self.master.title(self.config['APP']['title'])
        self.master.geometry(f"{self.config['APP']['initial_width']}x{self.config['APP']['initial_height']}")
        self.master.minsize(int(self.config['APP']['min_width']), int(self.config['APP']['min_height']))
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.style = ttk.Style()
        self.style.theme_use(self.config['THEME']['style'])
        self.style.configure('.', font=(self.config['THEME']['font_family'], int(self.config['THEME']['font_size'])))
        self.style.configure('TButton', padding=int(self.config['THEME']['button_padding']))
        self.style.configure('TEntry', padding=int(self.config['THEME']['entry_padding']))
        self.style.configure('TLabel', padding=int(self.config['THEME']['label_padding']))

        # Apply colors
        self.master.configure(bg=self.config['COLORS']['background'])
        self.style.configure('.', background=self.config['COLORS']['background'], foreground=self.config['COLORS']['text'])
        self.style.configure('TButton', background=self.config['COLORS']['button'], foreground=self.config['COLORS']['button_text'])

        self.db = None
        self.current_frame = None

        self.show_loading_screen()
        threading.Thread(target=self.connect_to_database, daemon=True).start()

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    def show_loading_screen(self):
        self.loading_screen = LoadingScreen(self.master)

    def hide_loading_screen(self):
        self.loading_screen.destroy()

    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host=self.config['DATABASE']['host'],
                user=self.config['DATABASE']['user'],
                password=self.config['DATABASE']['password'],
                database=self.config['DATABASE']['database'],
                port=int(self.config['DATABASE']['port'])
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
        self.current_frame = ScrollableFrame(self.master)
        self.current_frame.pack(fill="both", expand=True)
        
        login_signup_frame = LoginSignup(self.current_frame.scrollable_frame, self.db, self.login_callback)
        login_signup_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_user_page(self, user_id):
        try:
            self.clear_current_frame()
            self.current_frame = ScrollableFrame(self.master)
            self.current_frame.pack(fill="both", expand=True)
            
            user_page_frame = UserPage(self.current_frame.scrollable_frame, self.db, user_id, self.logout_callback)
            user_page_frame.pack(fill="both", expand=True, padx=20, pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user page: {str(e)}")

    def show_admin_page(self, user_id, username, password, phone_number):
        try:
            self.clear_current_frame()
            self.current_frame = ScrollableFrame(self.master)
            self.current_frame.pack(fill="both", expand=True)
            
            admin_page_frame = AdminPage(self.current_frame.scrollable_frame, self.db, user_id, username, password, phone_number, self.logout_callback)
            admin_page_frame.pack(fill="both", expand=True, padx=20, pady=20)
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