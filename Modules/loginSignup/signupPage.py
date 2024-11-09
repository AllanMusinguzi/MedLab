import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime
import bcrypt

class Signup(ctk.CTkFrame):
    def __init__(self, master, db, on_signup_success, on_switch_to_login):
        super().__init__(master)
        self.db = db
        self.on_signup_success = on_signup_success
        self.on_switch_to_login = on_switch_to_login
        self.profile_picture_path = None
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create the main container frame with gray background
        self.configure(fg_color="#E5E5E5")
        self.pack(fill="both", expand=True)

        '''
            self.DEFAULT_BG = 'white'
            self.ERROR_BG = '#ffe6e6'  # Light red background
            
        def reset_field_colors(self):
            """Reset all fields to default background color"""
            for field in self.entry.values():
                field.configure(bg=self.DEFAULT_BG)

        def highlight_field(self, field_name):
            """Highlight a specific field in error color"""
            self.entry[field_name].configure(bg=self.ERROR_BG)
        '''    

        self.create_signup_form()

    def create_signup_form(self):
        # Main card frame
        signup_card = ctk.CTkFrame(
            self,
            fg_color="#2B2B2B",
            corner_radius=15,
            width=400,
            height=680
        )
        signup_card.place(relx=0.5, rely=0.5, anchor="center")
        signup_card.pack_propagate(False)

        # Title
        title = ctk.CTkLabel(
            signup_card,
            text="Create Account",
            font=("Inter", 24, "bold"),
            text_color="white"
        )
        title.pack(pady=(30, 20))

        # Profile picture section
        profile_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        profile_frame.pack(pady=10)
        
        self.profile_preview = ctk.CTkLabel(
            profile_frame, 
            text="No image selected",
            text_color="#A0A0A0"
        )
        self.profile_preview.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            profile_frame,
            text="Choose Picture",
            command=self.choose_profile_picture,
            width=200,
            height=35,
            corner_radius=5,
            fg_color="#2D72D2",
            hover_color="#2159A5"
        ).pack(side="left")

        # Form fields with inline labels
        fields = [
            ("Full Name", "signup_full_name", "📛 John Doe"),
            ("Email", "signup_email", "📧 example@email.com"),
            ("Phone Number", "signup_phone_number", "📱 +1 (555) 123-4567"),
            ("Username", "signup_username", "👤 Choose a unique username"),
            ("Address", "signup_address", "🏠 123 Main St, City, Country"),
            ("Password", "signup_password", "🔒 Min. 8 characters"),
            ("Confirm Password", "signup_confirm_password", "🔒 Re-enter your password")
        ]

        # Create StringVar for each field
        self.field_vars = {attr: ctk.StringVar() for _, attr, _ in fields}

        # Create form fields with inline labels
        for label, attr, placeholder in fields:
            # Create a frame for each field group
            field_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
            field_frame.pack(pady=8, padx=40, fill="x")
            
            # Label
            field_label = ctk.CTkLabel(
                field_frame,
                text=label,
                text_color="#A0A0A0",
                width=130,  # Fixed width for alignment
                anchor="e"  # Right-align the label
            )
            field_label.pack(side="left", padx=(0, 10))
            
            # Entry field
            entry = ctk.CTkEntry(
                field_frame,
                placeholder_text=placeholder,
                textvariable=self.field_vars[attr],
                show="•" if "password" in attr else "",
                corner_radius=5,
                border_color="#404040",
                fg_color="#1A1A1A",
                text_color="#FFFFFF",
                placeholder_text_color="#666666",
                height=35
            )
            entry.pack(side="left", fill="x", expand=True)
            setattr(self, attr, entry)

        # Signup button
        signup_btn = ctk.CTkButton(
            signup_card,
            text="Sign Up",
            command=self.signup,
            width=320,
            height=35,
            corner_radius=5,
            fg_color="#2D72D2",
            hover_color="#2159A5"
        )
        signup_btn.pack(pady=15)

        # Login link section
        login_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        login_frame.pack(pady=10)
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account?",
            text_color="#A0A0A0"
        )
        login_label.pack(side="left", padx=2)
        
        login_button = ctk.CTkLabel(
            login_frame,
            text="Login",
            text_color="#2D72D2",
            cursor="hand2"
        )
        login_button.pack(side="left")
        login_button.bind("<Button-1>", lambda e: self.on_switch_to_login())

    # Rest of the methods remain the same...
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
                self.profile_preview.configure(image=photo, text="")
                self.profile_preview.image = photo
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")

    def signup(self):
        # Reset all field colors at the start
        #self.reset_field_colors()
        
        # Get values and strip whitespace
        full_name = self.signup_full_name.get().strip()
        email = self.signup_email.get().strip()
        phone_number = self.signup_phone_number.get().strip()
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        address = self.signup_address.get().strip()
        confirm_password = self.signup_confirm_password.get()

        # Check if all fields are filled
        empty_fields = []
        for field_name, value in {
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
            'address': address
        }.items():
            if not value:
                empty_fields.append(field_name)
                #self.highlight_field(field_name)
        
        if empty_fields:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            #self.highlight_field('email')
            messagebox.showerror("Invalid Email", 
                "Please enter a valid email address.\n\n"
                "Valid format: username@domain.com\n"
                "• Must contain '@' symbol\n"
                "• Must contain domain name and extension\n"
                "• Cannot contain spaces"
            )
            return

        # Phone number validation
        cleaned_phone = re.sub(r'[\s\(\)\+\-]', '', phone_number)
        if not cleaned_phone.isdigit():
            #self.highlight_field('phone_number')
            messagebox.showerror("Invalid Phone Number",
                "Phone number can only contain:\n"
                "• Numbers (0-9)\n"
                "• Plus sign (+)\n"
                "• Parentheses ()\n"
                "• Spaces\n"
                "• Hyphens (-)"
            )
            return
        
        if not (10 <= len(cleaned_phone) <= 15):
            #self.highlight_field('phone_number')
            messagebox.showerror("Invalid Phone Number",
                "Phone number must be between 10 and 15 digits.\n\n"
                "Examples:\n"
                "• +1 (555) 123-4567\n"
                "• (555) 123-4567\n"
                "• +44 20 7123 4567"
            )
            return

        # Password validation
        if len(password) < 8:
            #self.highlight_field('password')
            messagebox.showerror("Weak Password",
                "Password must be at least 8 characters long.\n"
                "Current length: " + str(len(password))
            )
            return

        # Password strength validation
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        password_requirements = []
        if not has_upper:
            password_requirements.append("• At least one uppercase letter (A-Z)")
        if not has_lower:
            password_requirements.append("• At least one lowercase letter (a-z)")
        if not has_digit:
            password_requirements.append("• At least one number (0-9)")
        if not has_special:
            password_requirements.append("• At least one special character (!@#$%^&*...)")
        
        if password_requirements:
            #self.highlight_field('password')
            messagebox.showerror("Weak Password",
                "Password must contain:\n" + "\n".join(password_requirements)
            )
            return

        # Password match validation
        if password != confirm_password:
            #self.highlight_field('password')
            #self.highlight_field('confirm_password')
            messagebox.showerror("Password Mismatch", 
                "Passwords do not match.\n"
                "Please make sure both passwords are identical."
            )
            return

        # Username validation
        if len(username) < 3:
            #self.highlight_field('username')
            messagebox.showerror("Invalid Username",
                "Username must be at least 3 characters long.\n"
                "Current length: " + str(len(username))
            )
            return
        
        if not username.replace("_", "").isalnum():
            #self.highlight_field('username')
            messagebox.showerror("Invalid Username",
                "Username can only contain:\n"
                "• Letters (a-z, A-Z)\n"
                "• Numbers (0-9)\n"
                "• Underscores (_)"
            )
            return

        # If all validations pass, hash password and continue with signup
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # ... rest of the signup code ...
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during password hashing: {str(e)}")
            return

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
            success_window.geometry("350x150")
            success_window.lift()
            
            # Center the success window
            success_window.update_idletasks()
            width = success_window.winfo_width()
            height = success_window.winfo_height()
            x = (success_window.winfo_screenwidth() // 2) - (width // 2)
            y = (success_window.winfo_screenheight() // 2) - (height // 2)
            success_window.geometry(f'{width}x{height}+{x}+{y}')
            
            ctk.CTkLabel(
                success_window,
                text="Account created successfully!",
                font=("Inter", 16, "bold")
            ).pack(pady=20)
            
            ctk.CTkButton(
                success_window,
                text="OK",
                command=lambda: [success_window.destroy(), self.on_switch_to_login()],
                width=200,
                height=35,
                corner_radius=5,
                fg_color="#2D72D2",
                hover_color="#2159A5"
            ).pack(pady=15)
            
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
        self.profile_preview.configure(image='', text="No image selected")
        self.profile_preview.image = None