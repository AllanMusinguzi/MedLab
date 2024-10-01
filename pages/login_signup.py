# login_signup.py
import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt

class LoginSignup(ttk.Frame):
    def __init__(self, master, db, login_callback):
        super().__init__(master)
        self.db = db
        self.login_callback = login_callback

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Ubuntu', 12))
        self.style.configure('TEntry', font=('Ubuntu', 12))
        self.style.configure('TButton', font=('Ubuntu', 12))
        self.style.configure('TNotebook.Tab', font=('Ubuntu', 12))

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.login_frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        self.signup_frame = ttk.Frame(self.notebook, padding="20 20 20 20")

        self.notebook.add(self.login_frame, text='Login')
        self.notebook.add(self.signup_frame, text='Sign Up')

        self.create_login_form()
        self.create_signup_form()

    def create_login_form(self):
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.login_username = ttk.Entry(self.login_frame, width=30)
        self.login_username.grid(row=0, column=1, pady=5)

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.login_password = ttk.Entry(self.login_frame, show="*", width=30)
        self.login_password.grid(row=1, column=1, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=1, sticky=tk.E, pady=10)

    def create_signup_form(self):
        ttk.Label(self.signup_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.signup_username = ttk.Entry(self.signup_frame, width=30)
        self.signup_username.grid(row=0, column=1, pady=5)

        ttk.Label(self.signup_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.signup_password = ttk.Entry(self.signup_frame, show="*", width=30)
        self.signup_password.grid(row=1, column=1, pady=5)

        ttk.Label(self.signup_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.signup_confirm_password = ttk.Entry(self.signup_frame, show="*", width=30)
        self.signup_confirm_password.grid(row=2, column=1, pady=5)

        self.is_admin_var = tk.BooleanVar()
        ttk.Checkbutton(self.signup_frame, text="Admin User", variable=self.is_admin_var).grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Button(self.signup_frame, text="Sign Up", command=self.signup).grid(row=4, column=1, sticky=tk.E, pady=10)

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT user_id, password, is_admin FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                self.login_callback(user[0], user[2], username, password)  # Pass username and password
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
        finally:
            cursor.close()

    def signup(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()
        is_admin = self.is_admin_var.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
                return

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)",
                           (username, hashed_password, is_admin))
            self.db.commit()
            messagebox.showinfo("Success", "User registered successfully.")
            self.notebook.select(0)  # Switch to login tab
            self.signup_username.delete(0, tk.END)
            self.signup_password.delete(0, tk.END)
            self.signup_confirm_password.delete(0, tk.END)
            self.is_admin_var.set(False)
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
        finally:
            cursor.close()
