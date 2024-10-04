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
        
        # Configure the notebook style for centered tabs with center-aligned text
        self.style.configure('Custom.TNotebook', tabposition='n')
        self.style.configure('Custom.TNotebook.Tab', padding=[20, 5], width=20)

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.login_frame = ttk.Frame(self.notebook, padding="30 30 30 30")
        self.signup_frame = ttk.Frame(self.notebook, padding="30 30 30 30")

        self.notebook.add(self.login_frame, text='Login', padding=(10, 5), sticky='nsew')
        self.notebook.add(self.signup_frame, text='Sign Up', padding=(10, 5), sticky='nsew')

        self.create_login_form()
        self.create_signup_form()

    def create_login_form(self):
        main_frame = ttk.Frame(self.login_frame)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky=tk.E, pady=10)
        self.login_username = ttk.Entry(main_frame, width=30)
        self.login_username.grid(row=0, column=1, pady=10, padx=(10, 0))

        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky=tk.E, pady=10)
        self.login_password = ttk.Entry(main_frame, show="*", width=30)
        self.login_password.grid(row=1, column=1, pady=10, padx=(10, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Login", command=self.login).pack()

    def create_signup_form(self):
        main_frame = ttk.Frame(self.signup_frame)
        main_frame.pack(expand=True)

        fields = [
            ("Full Name:", "signup_full_name"),
            ("Email:", "signup_email"),
            ("Phone Number:", "signup_phone_number"),
            ("Username:", "signup_username"),
            ("Password:", "signup_password"),
            ("Confirm Password:", "signup_confirm_password")
        ]

        for i, (label, attr) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.E, pady=8)
            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, pady=8, padx=(10, 0))
            setattr(self, attr, entry)

            if "password" in attr:
                entry.config(show="*")

        self.is_admin_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Admin User", variable=self.is_admin_var).grid(row=len(fields), column=1, sticky=tk.W, pady=8)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Sign Up", command=self.signup).pack()

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT user_id, password, phone_number, is_admin FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                self.user_id = user[0]  # Set user_id
                self.username = username  # Set username
                self.phone_number = user[2]  # Set phone_number information
                
                # Call the login callback with relevant information
                self.login_callback(user[0], user[3], username, password, user[2])  # Pass username and password
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
