import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import threading
import configparser
from datetime import datetime
import os
import sys

from Modules.loginSignup.loginPage import Login
from Modules.loginSignup.signupPage import Signup
from Modules.usersModule.user_page import UserPage
from Modules.adminModule.dashboard import AdminDashboard
from Modules.superAdminModule.SuperAdmin import SuperAdminPage

class LoadingScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Loading")
        self.geometry("300x250")
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')
        self.transient(master)
        self.grab_set()

        # Configure root window grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.label = tk.Label(self, text="Loading...", font=('Ubuntu', 14), bg='#f0f0f0')
        self.label.pack(pady=20)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()


class MedicalLabSystem:
    def __init__(self, master):
        self.master = master
        self.config = self.load_config()
        self.current_frame = None
        self.login_frame = None
        self.signup_frame = None

        # Set main window attributes
        self.master.title(self.config['APP']['title'])
        self.master.geometry(f"{self.config['APP']['initial_width']}x{self.config['APP']['initial_height']}")
        self.master.minsize(int(self.config['APP']['min_width']), int(self.config['APP']['min_height']))
        self.master.configure(bg=self.config['COLORS']['background'])

        # Configure grid weights for root window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Initialize styles
        self.init_styles()
        
        # Other initialization code
        self.db = None
        self.show_loading_screen()
        threading.Thread(target=self.connect_to_database, daemon=True).start()

    def init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use(self.config['THEME']['style'])
        self.style.configure('.', font=(self.config['THEME']['font_family'], int(self.config['THEME']['font_size'])))
        
        # Button styling
        self.style.configure('TButton', 
                           background=self.config['COLORS']['button_bg'], 
                           foreground=self.config['COLORS']['button_fg'],
                           padding=int(self.config['THEME']['button_padding']))
        self.style.map('TButton',
                      background=[('active', self.config['COLORS']['button_active']),
                                ('disabled', self.config['COLORS']['button_disabled'])])

        # Entry styling
        self.style.configure('TEntry', 
                           fieldbackground=self.config['COLORS']['entry_bg'],
                           foreground=self.config['COLORS']['entry_fg'],
                           bordercolor=self.config['COLORS']['entry_border'])
        
        # Label styling
        self.style.configure('TLabel', 
                           background=self.config['COLORS']['background'], 
                           foreground=self.config['COLORS']['label_fg'])

        # Treeview styling
        self.style.configure('Treeview', 
                           background=self.config['COLORS']['table_bg'],
                           foreground=self.config['COLORS']['table_fg'],
                           fieldbackground=self.config['COLORS']['table_bg'])
        self.style.map('Treeview', 
                      background=[('selected', self.config['COLORS']['table_selected_bg'])],
                      foreground=[('selected', self.config['COLORS']['table_selected_fg'])])
        
        self.style.configure('Treeview.Heading', 
                           background=self.config['COLORS']['table_header_bg'], 
                           foreground=self.config['COLORS']['table_header_fg'])

    def load_config(self):
        config = configparser.ConfigParser()
        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            messagebox.showerror("Configuration Error", f"Config file not found: {config_path}")
            self.master.quit()
            return None
        config.read(config_path)
        return config

    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, 'config.ini')
        else:
            return 'config.ini'

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
            self.show_login()

    def show_login(self):
        # Clear any existing frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create a new frame with master as parent
        self.current_frame = tk.Frame(self.master)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for the current frame
        self.current_frame.grid_rowconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)
        
        self.login_frame = Login(
            master=self.current_frame,
            db=self.db,
            on_login_success=self.login_callback,  
            on_switch_to_signup=self.show_signup  
        )
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def show_signup(self):
        # Clear any existing frame
        if self.current_frame:
            self.current_frame.destroy()
            
        # Create a new frame with master as parent
        self.current_frame = tk.Frame(self.master)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for the current frame
        self.current_frame.grid_rowconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)
        
        self.signup_frame = Signup(
            master=self.current_frame,
            db=self.db,
            on_signup_success=self.show_login,    
            on_switch_to_login=self.show_login   
        )
        self.signup_frame.grid(row=0, column=0, sticky="nsew")

    def login_callback(self, username, role):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT user_id, phone_number, password
                FROM users
                WHERE username = %s
            """, (username,))
            
            user_details = cursor.fetchone()
            
            if user_details:
                user_id = user_details[0]
                phone_number = user_details[1]
                password = user_details[2]
                
                self.current_session = {
                    'user_id': user_id,
                    'username': username,
                    'role': role,
                    'phone_number': phone_number,
                    'password': password,
                    'login_time': datetime.now()
                }
                
                if role == 'superadmin':
                    self.show_superadmin_page(
                        user_id=user_id,
                        username=username,
                        password=password,
                        phone_number=phone_number
                    )
                elif role == 'admin':
                    self.show_admin_page(
                        user_id=user_id,
                        username=username,
                        password=password,
                        phone_number=phone_number
                    )
                elif role == 'user':
                    self.show_user_page(
                        user_id=user_id,
                        username=username,
                        password=password,
                        phone_number=phone_number
                    )
                else:
                    messagebox.showerror("Error", "Invalid user role.")
                    
            else:
                messagebox.showerror("Error", "User details not found.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load page: {str(e)}")
            
        finally:
            cursor.close()

    def show_user_page(self, user_id, username, password, phone_number):
        try:
            self.clear_current_frame()
            
            # Create new frame with master as parent
            self.current_frame = tk.Frame(self.master)
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            
            user_page_frame = UserPage(
                master=self.current_frame,
                db=self.db,
                user_id=user_id,
                username=username,
                password=password,
                phone_number=phone_number,
                logout_callback=self.logout_callback
            )
            user_page_frame.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user page: {str(e)}")

    def show_admin_page(self, user_id, username, password, phone_number):
        try:
            self.clear_current_frame()
            
            # Create new frame with master as parent
            self.current_frame = tk.Frame(self.master)
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            
            admin_page_frame = AdminDashboard(
                master=self.current_frame,
                db=self.db,
                user_id=user_id,
                username=username,
                password=password,
                phone_number=phone_number,
                logout_callback=self.logout_callback
            )
            admin_page_frame.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load adminDashboard: {str(e)}")

    def show_superadmin_page(self, user_id, username, password, phone_number):
        try:
            self.clear_current_frame()
            
            # Create new frame with master as parent
            self.current_frame = tk.Frame(self.master)
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            
            superadmin_page_frame = SuperAdminPage(
                master=self.current_frame,
                db=self.db,
                user_id=user_id,
                username=username,
                password=password,
                phone_number=phone_number,
                logout_callback=self.logout_callback
            )
            superadmin_page_frame.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load superadmin page: {str(e)}")

    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def logout_callback(self):
        self.show_login()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.db:
                self.db.close()
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalLabSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()