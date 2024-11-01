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
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Ubuntu', 12))
        self.style.configure('TEntry', font=('Ubuntu', 12))
        self.style.configure('TButton', font=('Ubuntu', 12))
        self.style.configure('Title.TLabel', font=('Ubuntu', 14, 'bold'))
        
        # Configure notebook style for better visibility
        self.style.configure('Custom.TNotebook', tabposition='n')
        self.style.configure('Custom.TNotebook.Tab', padding=[40, 10], width=20, font=('Ubuntu', 12))

        self.create_widgets()

    def create_widgets(self):
        # Configure grid weights for proper expansion
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create main notebook with increased padding
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=40, pady=30)

        # Create frames with increased padding
        self.login_frame = ttk.Frame(self.notebook, padding=20)
        self.signup_frame = ttk.Frame(self.notebook, padding=20)

        self.notebook.add(self.login_frame, text='Login')
        self.notebook.add(self.signup_frame, text='Sign Up')

        # Configure login and signup frames to expand properly
        for frame in (self.login_frame, self.signup_frame):
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

        self.create_login_form()
        self.create_signup_form()


    def create_login_form(self):
        # Configure the login frame to allow for centering
        self.login_frame.columnconfigure(0, weight=1)
        self.login_frame.columnconfigure(1, weight=1)

        # Create main frame with reduced padding
        main_frame = ttk.Frame(self.login_frame, padding="10 5 10 5")
        main_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        # Configure main_frame columns to allow stretching
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Login fields with reduced spacing
        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky=tk.E, pady=5)
        self.login_username = ttk.Entry(main_frame, width=40)
        self.login_username.grid(row=0, column=1, sticky='w', pady=5, padx=(5, 0))

        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky=tk.E, pady=5)
        self.login_password = ttk.Entry(main_frame, show="*", width=40)
        self.login_password.grid(row=1, column=1, sticky='w', pady=5, padx=(5, 0))

        # Login button with reduced padding
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Center the button
        ttk.Button(button_frame, text="Login", command=self.login, padding=(15, 5)).pack()

        # Center the button frame within the main frame
        button_frame.grid_columnconfigure(0, weight=1)
        

    def create_signup_form(self):
        self.signup_frame.columnconfigure(0, weight=1)
        self.signup_frame.columnconfigure(1, weight=1)

        # Create main frame with reduced padding
        main_frame = ttk.Frame(self.signup_frame, padding="10 5 10 5")
        main_frame.grid(row=1, column=0, sticky='nsew')
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        current_row = 0

        # Profile picture section
        ttk.Label(main_frame, text="Profile Picture:").grid(row=current_row, column=0, sticky=tk.E, pady=5)
        profile_frame = ttk.Frame(main_frame)
        profile_frame.grid(row=current_row, column=1, sticky='w', pady=5, padx=(5, 0))
        self.profile_preview = ttk.Label(profile_frame)
        self.profile_preview.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(profile_frame, text="Choose Picture", command=self.choose_profile_picture).pack(side=tk.LEFT)

        current_row += 1

        # Main fields with reduced spacing
        fields = [
            ("Full Name:", "signup_full_name"),
            ("Email:", "signup_email"),
            ("Phone Number:", "signup_phone_number"),
            ("Username:", "signup_username"),
            ("Password:", "signup_password"),
            ("Confirm Password:", "signup_confirm_password"),
            ("Address:", "signup_address")
        ]

        for label, attr in fields:
            ttk.Label(main_frame, text=label).grid(row=current_row, column=0, sticky=tk.E, pady=5)
            entry = ttk.Entry(main_frame, width=40 if attr != "signup_address" else 50)
            entry.grid(row=current_row, column=1, sticky='w', pady=5, padx=(5, 0))
            setattr(self, attr, entry)

            if "password" in attr:
                entry.config(show="*")

            current_row += 1

        # Role selection
        ttk.Label(main_frame, text="Role:").grid(row=current_row, column=0, sticky=tk.E, pady=5)
        self.role_var = tk.StringVar(value="User")  # Default role
        role_options = ["User", "Admin"]
        self.role_combobox = ttk.Combobox(main_frame, textvariable=self.role_var, values=role_options, state="readonly")
        self.role_combobox.grid(row=current_row, column=1, sticky='w', pady=5, padx=(5, 0))

        current_row += 1

        # Preferences section with reduced spacing
        ttk.Label(main_frame, text="Preferences:").grid(row=current_row, column=0, sticky=tk.E, pady=5)
        self.preferences_frame = ttk.Frame(main_frame)
        self.preferences_frame.grid(row=current_row, column=1, sticky='w', pady=5, padx=(5, 0))

        self.pref_vars = {
            'notifications': tk.BooleanVar(),
            'newsletter': tk.BooleanVar(),
            'dark_mode': tk.BooleanVar()
        }

        for i, (pref, var) in enumerate(self.pref_vars.items()):
            ttk.Checkbutton(self.preferences_frame, text=pref.title(), variable=var).grid(row=0, column=i, padx=5)

        current_row += 1

        # Signup button with reduced padding
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Sign Up", command=self.signup, padding=(15, 5)).pack()


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
        full_name = self.signup_full_name.get()
        email = self.signup_email.get()
        phone_number = self.signup_phone_number.get()
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()
        address = self.signup_address.get()
        role = self.role_var.get()

        if not all([full_name, email, phone_number, username, password, confirm_password, address]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        preferences = {
            'notifications': self.pref_vars['notifications'].get(),
            'newsletter': self.pref_vars['newsletter'].get(),
            'dark_mode': self.pref_vars['dark_mode'].get()
        }

        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (full_name, email, phone_number, username, password, 
                                   profile_picture, address, role, preferences) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (full_name, email, phone_number, username, hashed_password.decode('utf-8'), 
                      self.profile_picture_path, address, role, json.dumps(preferences)))
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
        self.signup_full_name.delete(0, tk.END)
        self.signup_email.delete(0, tk.END)
        self.signup_phone_number.delete(0, tk.END)
        self.signup_username.delete(0, tk.END)
        self.signup_password.delete(0, tk.END)
        self.signup_confirm_password.delete(0, tk.END)
        self.signup_address.delete(0, tk.END)
        self.role_var.set("User")
        self.profile_picture_path = None
        self.profile_preview.configure(image='')

# Example usage (commented out)
# root = tk.Tk()
# db = create_database_connection()  # Define your database connection function
# app = LoginSignup(root, db, login_callback=lambda user_data: print(user_data))
# app.pack(fill='both', expand=True)
# root.mainloop()
