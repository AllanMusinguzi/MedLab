import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import bcrypt
from PIL import Image, ImageTk
import os
import shutil
from datetime import datetime
import json

class LoginSignup(ttk.Frame):
    def __init__(self, master, db, login_callback):
        super().__init__(master)
        self.db = db
        self.login_callback = login_callback
        self.profile_picture_path = None
        
        # Configure the frame size instead of window size
        self.configure(width=650, height=600)
        self.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Setup style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Ubuntu', 12))
        self.style.configure('TEntry', font=('Ubuntu', 12))
        self.style.configure('TButton', font=('Ubuntu', 12))
        self.style.configure('Title.TLabel', font=('Ubuntu', 14, 'bold'))
        self.style.configure('Custom.TNotebook', tabposition='n')
        self.style.configure('Custom.TNotebook.Tab', padding=[40, 10], width=20, font=('Ubuntu', 12), anchor="center")
        
        self.create_widgets()

    def create_widgets(self):
        # Configure grid weights for proper expansion
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Custom style to hide notebook tabs
        style = ttk.Style()
        style.layout("Custom.TNotebook.Tab", [])  # Removes tabs from the notebook

        # Notebook with hidden tabs
        self.notebook = ttk.Notebook(self, style="Custom.TNotebook")
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Frames for login and signup forms
        self.login_frame = ttk.Frame(self.notebook, padding=20)
        self.signup_frame = ttk.Frame(self.notebook, padding=20)

        # Add frames to notebook without visible tabs
        self.notebook.add(self.login_frame)
        self.notebook.add(self.signup_frame)

        # Configure frame for central alignment
        for frame in (self.login_frame, self.signup_frame):
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

        # Create login and signup forms
        self.create_login_form()
        self.create_signup_form()

    def create_login_form(self):
        # Main frame for login fields
        main_frame = ttk.Frame(self.login_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Heading/Title for the login form
        heading_label = ttk.Label(main_frame, text="Login to Your Account", font=('Ubuntu', 16, 'bold'))
        heading_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")

        # Username and Password fields with reduced spacing
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=10)
        self.login_username = ttk.Entry(main_frame, width=30)
        self.login_username.grid(row=1, column=1, sticky="w", pady=10, padx=(5, 0))
        
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=10)
        self.login_password = ttk.Entry(main_frame, show="*", width=30)
        self.login_password.grid(row=2, column=1, sticky="w", pady=10, padx=(5, 0))

        # Login button with padding
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        button_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(button_frame, text="Login", command=self.login, padding=(10, 5)).pack()

        # "Switch to Sign Up" text with clickable "Right here" link
        switch_to_signup_label = ttk.Label(main_frame, text="Don't have an account?")
        switch_to_signup_label.grid(row=4, column=0, sticky="e", pady=10)
        
        switch_to_signup_link = ttk.Label(main_frame, text="Right here", cursor="hand2", font=('Ubuntu'))
        switch_to_signup_link.grid(row=4, column=1, sticky="w", pady=10)
        switch_to_signup_link.bind("<Button-1>", lambda e: self.notebook.select(self.signup_frame))


    def create_signup_form(self):
        # Configure column weights for centering
        self.signup_frame.columnconfigure(0, weight=1)
        self.signup_frame.columnconfigure(1, weight=1)
        
        # Main frame to hold signup form fields, centered within signup frame
        main_frame = ttk.Frame(self.signup_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

                # Heading/Title for the login form
        heading_label = ttk.Label(main_frame, text="Create Your Account", font=('Ubuntu', 16, 'bold'))
        heading_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")

        current_row = 1
        
        # Profile picture section
        ttk.Label(main_frame, text="Profile Picture:").grid(
            row=current_row, column=0, sticky=tk.E, pady=5
        )
        profile_frame = ttk.Frame(main_frame)
        profile_frame.grid(row=current_row, column=1, sticky='w', pady=5, padx=(5, 0))
        
        # Profile preview and choose picture button
        self.profile_preview = ttk.Label(profile_frame)
        self.profile_preview.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            profile_frame,
            text="Choose Picture",
            command=self.choose_profile_picture,
            width=15
        ).pack(side=tk.LEFT)
        
        current_row += 1
        
        # Fields for form inputs
        fields = [
            ("Full Name:", "signup_full_name"),
            ("Email:", "signup_email"),
            ("Phone Number:", "signup_phone_number"),
            ("Username:", "signup_username"),
            ("Address:", "signup_address"),            
            ("Password:", "signup_password"),
            ("Confirm Password:", "signup_confirm_password")
        ]
        
        # Create StringVar for each field
        self.field_vars = {attr: tk.StringVar() for _, attr in fields}

        # Create form fields
        for label, attr in fields:
            ttk.Label(main_frame, text=label).grid(
                row=current_row, column=0, sticky=tk.E, pady=5
            )
            
            # Special handling for password fields
            if "password" in attr:
                entry = ttk.Entry(
                    main_frame,
                    width=30,
                    show="*",
                    textvariable=self.field_vars[attr]
                )
            else:
                entry = ttk.Entry(
                    main_frame,
                    width=30 if attr == "signup_address" else 30,
                    textvariable=self.field_vars[attr]
                )
            
            entry.grid(row=current_row, column=1, sticky='w', pady=5, padx=(5, 0))
            setattr(self, attr, entry)
            current_row += 1
            
            # Password visibility toggle after confirm password field
            if attr == "signup_confirm_password":
                toggle_frame = ttk.Frame(main_frame)
                toggle_frame.grid(
                    row=current_row,
                    column=1,
                    sticky='w',
                    pady=(0, 5),
                    padx=(5, 0)
                )
                self.toggle_password_btn = ttk.Button(
                    toggle_frame,
                    text="Show/Hide",
                    command=self.toggle_password_visibility,
                    width=7.5
                )
                self.toggle_password_btn.pack(side=tk.LEFT)
                current_row += 1
        
        # Initialize password visibility state
        self.password_visible = False
        
        # Signup button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=15)
        ttk.Button(
            button_frame,
            text="Sign Up",
            command=self.signup,
            padding=(7.5, 5),
            width=15  
        ).pack()

        # "Back to Login" link
        login_link = ttk.Label(
            button_frame,
            text="Already have an account? Login",
            cursor="hand2"
        )
        login_link.pack(pady=(10, 0))
        login_link.bind("<Button-1>", lambda e: self.notebook.select(self.login_frame))


    def choose_profile_picture(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                # Create uploads directory if it doesn't exist
                uploads_dir = "uploads/profile_pictures"
                os.makedirs(uploads_dir, exist_ok=True)
                
                # Copy and rename file
                file_extension = os.path.splitext(file_path)[1]
                new_filename = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                new_file_path = os.path.join(uploads_dir, new_filename)
                
                shutil.copy2(file_path, new_file_path)
                self.profile_picture_path = new_file_path
                
                # Show preview
                image = Image.open(file_path)
                image.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(image)
                self.profile_preview.configure(image=photo)
                self.profile_preview.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        # Input validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT user_id, password, email, phone_number, username, role
                FROM users
                WHERE (username = %s OR email = %s)
            """, (username, username))
            
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                # Unpack user details
                user_id, hashed_password, email, phone_number, username, role = user
                
                # Validate role against your existing roles
                if role not in ['superadmin', 'admin', 'user']:
                    messagebox.showerror("Error", "Invalid user role.")
                    return
                
                # Call login_callback with just username and role
                self.login_callback(username, role)
                
                # Show appropriate welcome message
                messagebox.showinfo("Success", f"Welcome {username}!")
                
                # Log to your existing login_logs table if you have one
                cursor.execute("""
                    INSERT INTO login_logs 
                    (username, success, role, timestamp)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """, (username, True, role))
                self.db.commit()
                    
            else:
                messagebox.showerror("Error", "Invalid username or password.")
                
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
        finally:
            cursor.close()

    def signup(self):
        # Get values and strip whitespace
        full_name = self.signup_full_name.get().strip()
        email = self.signup_email.get().strip()
        phone_number = self.signup_phone_number.get().strip()
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        address = self.signup_address.get().strip()        
        confirm_password = self.signup_confirm_password.get()

        # Validation
        if not all([full_name, email, phone_number, username, password, confirm_password, address]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Basic email validation
        if not '@' in email or not '.' in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = self.db.cursor()
        try:
            # Check if username already exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists. Please choose another.")
                return

            # Insert new user
            cursor.execute("""
                INSERT INTO users (
                    full_name, 
                    email, 
                    phone_number, 
                    username, 
                    password,
                    profile_picture, 
                    address, 
                    role
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                full_name,
                email,
                phone_number,
                username,
                hashed_password.decode('utf-8'),
                self.profile_picture_path,
                address,
                'user'  # Default role for offline application
            ))
            
            self.db.commit()
            messagebox.showinfo("Success", "Account created successfully. You can now log in.")
            self.notebook.select(self.login_frame)
            self.clear_signup_fields()
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.db.rollback()
        finally:
            cursor.close()

    def clear_signup_fields(self):
        """Clear all signup fields and reset the profile picture"""
        entries = [
            self.signup_full_name,
            self.signup_email,
            self.signup_phone_number,
            self.signup_username,
            self.signup_password,
            self.signup_confirm_password,
            self.signup_address
        ]
        
        # Clear all entry widgets
        for entry in entries:
            if hasattr(entry, 'set'):  # If it's a StringVar
                entry.set('')
            else:  # If it's an Entry widget
                entry.delete(0, tk.END)
        
        # Reset profile picture if it exists
        if hasattr(self, 'profile_picture_path'):
            self.profile_picture_path = None
        
        # Reset profile preview if it exists
        if hasattr(self, 'profile_preview'):
            self.profile_preview.configure(image='')
            self.profile_preview.image = None  # Keep a reference to prevent garbage collection

    def toggle_password_visibility(self):
        """Toggle password visibility for both password fields"""
        self.password_visible = not self.password_visible
        show_char = "" if self.password_visible else "*"
        
        # Update password fields
        if isinstance(self.signup_password, tk.Entry):
            self.signup_password.configure(show=show_char)
        if isinstance(self.signup_confirm_password, tk.Entry):
            self.signup_confirm_password.configure(show=show_char)

# Example usage (commented out)
# root = tk.Tk()
# db = create_database_connection()  # Define your database connection function
# app = LoginSignup(root, db, login_callback=lambda user_data: print(user_data))
# app.pack(fill='both', expand=True)
# root.mainloop()
