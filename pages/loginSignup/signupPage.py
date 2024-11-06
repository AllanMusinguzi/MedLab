import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil
from datetime import datetime
import bcrypt

class Signup(ctk.CTkFrame):
    def __init__(self, master, db, on_signup_success, on_switch_to_login):
        super().__init__(master)
        self.db = db
        self.on_switch_to_login = on_switch_to_login
        self.profile_picture_path = None
        
        # Configure the frame size and appearance
        self.configure(width=800, height=600)
        self.pack_propagate(False)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.create_signup_form()

    def create_signup_form(self):
        # Main scroll frame to hold signup form fields
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            width=700,
            height=450
        )
        self.main_frame.pack(pady=20, padx=40, fill='both', expand=False)

        # Configure grid columns
        self.main_frame.grid_columnconfigure(0, weight=1)  # Label column
        self.main_frame.grid_columnconfigure(1, weight=2)  # Entry column

        # Heading/Title - spans both columns
        heading_label = ctk.CTkLabel(
            self.main_frame,
            text="Create Your Account",
            font=("Ubuntu", 24, "bold")
        )
        heading_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Profile picture section
        profile_label = ctk.CTkLabel(
            self.main_frame,
            text="Profile Picture:",
            anchor="e"
        )
        profile_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")
        
        profile_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        profile_frame.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=10)
        
        self.profile_preview = ctk.CTkLabel(profile_frame, text="")
        self.profile_preview.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            profile_frame,
            text="Choose Picture",
            command=self.choose_profile_picture,
            width=120
        ).pack(side="left")
        
        # Form fields
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
        self.field_vars = {attr: ctk.StringVar() for _, attr in fields}

        # Create form fields
        for idx, (label, attr) in enumerate(fields, start=2):
            # Label
            field_label = ctk.CTkLabel(
                self.main_frame,
                text=label,
                anchor="e"
            )
            field_label.grid(row=idx, column=0, padx=(20, 10), pady=10, sticky="e")
            
            # Entry
            entry = ctk.CTkEntry(
                self.main_frame,
                width=300,
                placeholder_text=label.replace(":", ""),
                show="*" if "password" in attr else "",
                textvariable=self.field_vars[attr]
            )
            entry.grid(row=idx, column=1, sticky="w", padx=(10, 20), pady=10)
            setattr(self, attr, entry)
        '''
        # Password toggle button - placed below password fields
        self.password_visible = False
        toggle_btn = ctk.CTkButton(
            self.main_frame,
            text="Show/Hide Password",
            command=self.toggle_password_visibility,
            width=120
        )
        toggle_btn.grid(row=len(fields)+2, column=1, sticky="w", padx=(10, 20), pady=10)
        '''
        # Signup button
        signup_btn = ctk.CTkButton(
            self.main_frame,
            text="Sign Up",
            command=self.signup,
            width=200
        )
        signup_btn.grid(row=len(fields)+3, column=0, columnspan=2, pady=20)

        # Back to Login link
        login_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        login_frame.grid(row=len(fields)+4, column=0, columnspan=2, pady=10)
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account? "
        )
        login_label.pack(side="left")
        
        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            width=50,
            command=self.on_switch_to_login,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("blue", "light blue")
        )
        login_button.pack(side="left")

    def choose_profile_picture(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                uploads_dir = "uploads/profile_pictures"
                os.makedirs(uploads_dir, exist_ok=True)
                
                # Process and save the image
                image = Image.open(file_path)
                image.thumbnail((100, 100))  # Resize image
                
                # Generate new filename and save
                file_extension = os.path.splitext(file_path)[1]
                new_filename = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                new_file_path = os.path.join(uploads_dir, new_filename)
                
                # Save the resized image
                image.save(new_file_path)
                self.profile_picture_path = new_file_path
                
                # Display preview
                photo = ImageTk.PhotoImage(image)
                self.profile_preview.configure(image=photo)
                self.profile_preview.image = photo
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")

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

        if not '@' in email or not '.' in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists. Please choose another.")
                return

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
                'user'
            ))
            
            self.db.commit()
            
            # Show success in a modern window
            success_window = ctk.CTkToplevel(self)
            success_window.title("Success")
            success_window.geometry("400x200")
            success_window.lift()  # Bring window to front
            
            ctk.CTkLabel(
                success_window,
                text="Account created successfully!",
                font=("Ubuntu", 16, "bold")
            ).pack(pady=20)
            
            ctk.CTkLabel(
                success_window,
                text="You can now log in with your credentials."
            ).pack(pady=10)
            
            ctk.CTkButton(
                success_window,
                text="OK",
                command=lambda: [success_window.destroy(), self.on_switch_to_login()]
            ).pack(pady=20)
            
            self.clear_fields()
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.db.rollback()
        finally:
            cursor.close()

    def clear_fields(self):
        """Clear all signup fields and reset the profile picture"""
        for var in self.field_vars.values():
            var.set('')
        
        self.profile_picture_path = None
        self.profile_preview.configure(image='')
        self.profile_preview.image = None

    '''
    def toggle_password_visibility(self):
        """Toggle password visibility for both password fields"""
        self.password_visible = not self.password_visible
        show_char = "" if self.password_visible else "*"
        
        self.signup_password.configure(show=show_char)
        self.signup_confirm_password.configure(show=show_char)
    '''