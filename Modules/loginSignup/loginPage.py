import customtkinter as ctk
from tkinter import messagebox
import bcrypt

class Login(ctk.CTkFrame):
    def __init__(self, master, db, on_login_success, on_switch_to_signup):
        super().__init__(master)
        self.db = db
        self.login_callback = on_login_success
        self.switch_to_signup_callback = on_switch_to_signup
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create the main container frame with gray background
        self.configure(fg_color="#E5E5E5")  
        self.pack(fill="both", expand=True)

        self.create_login_form()

    def create_login_form(self):
        login_card = ctk.CTkFrame(
            self,
            fg_color="#2B2B2B",
            corner_radius=15,
            width=340, 
            height=380 
        )
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        login_card.pack_propagate(False) 


        title = ctk.CTkLabel(
            login_card,
            text="Welcome Back",
            font=("Inter", 24, "bold"),
            text_color="white"
        )
        title.pack(pady=(40, 20)) 

        # Username entry
        self.login_username = ctk.CTkEntry(
            login_card,
            width=280,
            height=35,
            placeholder_text="Username",
            corner_radius=5,
            border_color="#404040",
            fg_color="#1A1A1A"
        )
        self.login_username.pack(pady=10)

        # Password entry
        self.login_password = ctk.CTkEntry(
            login_card,
            width=280,
            height=35,
            placeholder_text="Password",
            show="•",
            corner_radius=5,
            border_color="#404040",
            fg_color="#1A1A1A"
        )
        self.login_password.pack(pady=10)

        # Login button
        login_button = ctk.CTkButton(
            login_card,
            text="Login",
            command=self.login,
            width=280,
            height=35,
            corner_radius=5,
            fg_color="#2D72D2",
            hover_color="#2159A5"
        )
        login_button.pack(pady=10)

        '''# Remember Me checkbox
        self.remember_me = ctk.CTkCheckBox(
            login_card,
            text="Remember Me",
            fg_color="#2D72D2",
            hover_color="#2159A5",
            border_color="#404040"
        )
        self.remember_me.pack(pady=10)'''

        # Sign Up section
        signup_frame = ctk.CTkFrame(
            login_card,
            fg_color="transparent",
        )
        signup_frame.pack(pady=10)

        signup_label = ctk.CTkLabel(
            signup_frame,
            text="Don't have an account?",
            text_color="#A0A0A0"
        )
        signup_label.pack(side="left", padx=2)
        
        signup_button = ctk.CTkLabel(
            signup_frame,
            text="Sign Up",
            text_color="#2D72D2",
            cursor="hand2"
        )
        signup_button.pack(side="left")
        signup_button.bind("<Button-1>", lambda e: self.switch_to_signup_callback())

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

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
                user_id, hashed_password, email, phone_number, username, role = user
                
                if role not in ['superadmin', 'admin', 'user']:
                    messagebox.showerror("Error", "Invalid user role.")
                    return
                
                self.login_callback(username, role)
                
                new_window = ctk.CTkToplevel(self)
                new_window.title("Login Successful")
                new_window.geometry("350x150")
                ctk.CTkLabel(
                    new_window,
                    text=f"Welcome {username}! Have Browsing",
                    font=("Inter", 16)
                ).pack(pady=20)
                
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

    def clear_fields(self):
        self.login_username.delete(0, ctk.END)
        self.login_password.delete(0, ctk.END)
        self.remember_me.deselect()