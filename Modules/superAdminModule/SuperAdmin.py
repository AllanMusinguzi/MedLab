import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
import random
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image
from customtkinter import CTkImage

from Modules.superAdminModule.Dashboard import DashboardView
from Modules.superAdminModule.Users import UsersView
from Modules.superAdminModule.Patients import PatientsView
from Modules.superAdminModule.Tests import TestsView
from Modules.superAdminModule.Results import ResultsView
from Modules.superAdminModule.Settings import SettingsView

class SuperAdminPage(ctk.CTkFrame):
    def __init__(self, master, db, user_id, username, password, phone_number, logout_callback):
        super().__init__(master)
        
        # Store instance variables
        self.master = master
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.logout_callback = logout_callback
        
        # Initialize main frame
        self.main_frame = None
        
        # Configure master window grid
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        # Configure self (SuperAdminPage) to expand
        self.pack(fill="both", expand=True)
        
        # Configure grid layout for SuperAdminPage
        self.grid_columnconfigure(1, weight=1)  # Main content column
        self.grid_columnconfigure(0, weight=0)  # Sidebar column (no stretch)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize data
        self.metrics = {
            "Total Revenue": "$41,320",
            "Monthly Profit": "$1,221",
            "Conversion Rate": "88%"
        }
        
        # Create dashboard layout
        self.create_sidebar()
        self.show_dashboard()
    
    def clear_main_frame(self):
        """Clear the main content frame"""
        if self.main_frame:
            self.main_frame.destroy()
    
    def create_sidebar(self):
        """Create sidebar with navigation menu"""
        # Sidebar frame
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=10)
        sidebar.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        
        # Configure sidebar grid
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(7, weight=1)
        
        # Profile section
        profile_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        profile_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Configure profile frame grid
        profile_frame.grid_columnconfigure(0, weight=1)
        
        # Load profile picture from database
        profile_picture = self.load_profile_picture()
        
        # Profile image button
        profile_button = ctk.CTkButton(
            profile_frame,
            text=profile_picture or "👤",
            font=ctk.CTkFont(size=32),
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=self.show_profile_details
        )
        profile_button.grid(row=0, column=0, pady=(0, 10))
        
        ctk.CTkLabel(
            profile_frame,
            text=self.username or "Admin",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=0)
        
        # Navigation menu
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),           
            ("👥 Patients", self.show_patients),
            ("📋 Tests", self.show_tests),
            ("📈 Results", self.show_results),
            ("👥 Users", self.show_users),             
            ("⚙️ Settings", self.show_settings),
            ("Logout", self.logout)
        ]
        
        for idx, (label, command) in enumerate(menu_items):
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                height=40,
                command=command
            )
            btn.grid(row=idx+1, column=0, padx=10, pady=5, sticky="ew")

        '''# Logout button at the bottom
        logout_button = ctk.CTkButton(
            sidebar,
            text="Logout",
            height=45,
            font=("Ubuntu", 14),
            fg_color="#FF5252",
            hover_color="#FF1A1A",
            corner_radius=0,
            command=self.handle_logout
        )
        logout_button.pack(side="bottom", fill="x", padx=20, pady=20)'''


    def load_profile_picture(self):
        """Load profile picture of the logged-in user"""
        try:
            if not hasattr(self, 'user_id') or self.user_id is None:
                print("No user ID available")
                return "👤"

            cursor = self.db.cursor()
            query = "SELECT profile_picture FROM users WHERE user_id = ?"

            user_id = self.user_id
            cursor.execute(query, [user_id])
            result = cursor.fetchone()
            
            if result and result[0]:
                return result[0]
            return "👤"  # Default profile icon if no picture is found
        
        except Exception as e:
            print(f"Error loading profile picture: {e}")
            return "👤"  # Return default icon in case of error
        
        finally:
            if 'cursor' in locals():
                cursor.close()

    def show_profile_details(self):
        """Show profile details of the logged-in user"""
        try:
            if not hasattr(self, 'user_id') or self.user_id is None:
                print("No user ID available")
                return

            cursor = self.db.cursor()
            query = """
                SELECT username, phone_number, profile_picture
                FROM users 
                WHERE user_id = ?
            """
            
            user_id = self.user_id
            cursor.execute(query, [user_id])
            user_data = cursor.fetchone()
            cursor.close()
            
            if not user_data:
                print(f"No user data found for user_id: {self.user_id}")
                return
            
            # Update instance variables with fresh data
            username, phone_number, profile_picture = user_data
            self.username = username
            self.phone_number = phone_number
            
            # Create popup window
            popup = ctk.CTkToplevel(self)
            popup.title("My Profile")
            popup.geometry("400x300")
            popup.grab_set()
            
            # Center the popup on screen
            popup.update_idletasks()
            width = popup.winfo_width()
            height = popup.winfo_height()
            x = (popup.winfo_screenwidth() // 2) - (width // 2)
            y = (popup.winfo_screenheight() // 2) - (height // 2)
            popup.geometry(f'{width}x{height}+{x}+{y}')
            
            # Create main frame
            main_frame = ctk.CTkFrame(popup)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Profile picture
            profile_pic = ctk.CTkLabel(
                main_frame,
                text=profile_picture if profile_picture else "👤",
                font=ctk.CTkFont(size=48)
            )
            profile_pic.pack(pady=(0, 20))
            
            # User details
            details = [
                ("Username", self.username),
                ("Phone Number", self.phone_number)
            ]
            
            for label, value in details:
                detail_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
                detail_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    detail_frame,
                    text=f"{label}:",
                    font=ctk.CTkFont(weight="bold")
                ).pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    detail_frame,
                    text=str(value if value else "N/A")
                ).pack(side="right", padx=5)
            
            # Buttons Frame
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=(20, 0))
            
            # Edit Profile Button
            ctk.CTkButton(
                button_frame,
                text="Edit Profile",
                command=self.edit_profile,
                width=120
            ).pack(side="left", padx=5)
            
            # Close button
            ctk.CTkButton(
                button_frame,
                text="Close",
                command=popup.destroy,
                width=120
            ).pack(side="right", padx=5)
            
        except Exception as e:
            print(f"Error showing profile details: {e}")

    def edit_profile(self):
        """Open edit profile dialog"""
        try:
            if not hasattr(self, 'user_id') or self.user_id is None:
                print("No user ID available")
                return

            # Create edit popup window
            edit_popup = ctk.CTkToplevel(self)
            edit_popup.title("Edit Profile")
            edit_popup.geometry("400x400")
            edit_popup.grab_set()
            
            # Center the popup
            edit_popup.update_idletasks()
            width = edit_popup.winfo_width()
            height = edit_popup.winfo_height()
            x = (edit_popup.winfo_screenwidth() // 2) - (width // 2)
            y = (edit_popup.winfo_screenheight() // 2) - (height // 2)
            edit_popup.geometry(f'{width}x{height}+{x}+{y}')
            
            # Create main frame
            main_frame = ctk.CTkFrame(edit_popup)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Create form fields
            fields = [
                ("Username", self.username),
                ("Phone Number", self.phone_number)
            ]
            
            entries = {}
            for label, value in fields:
                # Label
                ctk.CTkLabel(
                    main_frame,
                    text=label,
                    font=ctk.CTkFont(weight="bold")
                ).pack(anchor="w", pady=(10, 0))
                
                # Entry with validation
                entry = ctk.CTkEntry(main_frame, width=300)
                entry.insert(0, value if value else "")
                entry.pack(anchor="w", pady=(0, 10))
                entries[label] = entry
            
            def validate_fields():
                """Validate form fields before saving"""
                username = entries["Username"].get().strip()
                phone = entries["Phone Number"].get().strip()
                
                if not username:
                    print("Username cannot be empty")
                    return False
                
                # Basic phone number validation
                if phone and not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                    print("Invalid phone number format")
                    return False
                
                return True
            
            def save_changes():
                """Save profile changes to database"""
                cursor = None
                try:
                    if not validate_fields():
                        return
                    
                    cursor = self.db.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET username = ?, phone_number = ?
                        WHERE user_id = ?
                    """, (
                        entries["Username"].get().strip(),
                        entries["Phone Number"].get().strip(),
                        self.user_id,
                    ))
                    self.db.commit()
                    
                    # Update instance variables
                    self.username = entries["Username"].get().strip()
                    self.phone_number = entries["Phone Number"].get().strip()
                    
                    # Close popup and refresh
                    edit_popup.destroy()
                    self.show_profile_details()
                    
                except Exception as e:
                    print(f"Error saving profile changes: {e}")
                
                finally:
                    if 'cursor' in locals():
                        cursor.close()
            
            # Buttons Frame
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=(20, 0))
            
            # Save button
            ctk.CTkButton(
                button_frame,
                text="Save Changes",
                command=save_changes,
                width=120
            ).pack(side="left", padx=5)
            
            # Cancel button
            ctk.CTkButton(
                button_frame,
                text="Cancel",
                command=edit_popup.destroy,
                width=120
            ).pack(side="right", padx=5)
            
        except Exception as e:
            print(f"Error opening edit profile: {e}")


    def setup_main_frame(self):
        """Setup new main frame with proper grid configuration"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        
        # Configure main frame grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Row 1 is content area
        return self.main_frame


    def show_dashboard(self):
        """Create and show dashboard content"""
        self.clear_main_frame()
        main_frame = self.setup_main_frame()
        
        # Create header
        self.create_header(main_frame)
        
        # Content section with grid layout
        content = ctk.CTkFrame(main_frame, fg_color="transparent")
        content.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure content grid
        content.grid_columnconfigure((0, 1, 2), weight=1)
        content.grid_rowconfigure(1, weight=1)
        
        # Metric cards
        self.create_metric_cards(content)
        
        # Charts section
        self.create_charts_section(content)

        
    def create_header(self, parent):
        """Create dashboard header"""
        header = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Configure header grid
        header.grid_columnconfigure(1, weight=1)
        
        # Title
        ctk.CTkLabel(
            header,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=10)
        
        # Search bar
        search_entry = ctk.CTkEntry(
            header,
            placeholder_text="Search...",
            width=200
        )
        search_entry.grid(row=0, column=1, padx=10, sticky="e")
        
        # User menu
        ctk.CTkButton(
            header,
            text="⚙️",
            width=40,
            fg_color="transparent",
            text_color=("gray10", "gray90")
        ).grid(row=0, column=2, padx=5)

        
    def create_metric_cards(self, parent):
        """Create metric cards row"""
        for idx, (metric, value) in enumerate(self.metrics.items()):
            card = ctk.CTkFrame(parent, corner_radius=10)
            card.grid(row=0, column=idx, padx=5, pady=10, sticky="nsew")
            
            # Configure card grid
            card.grid_columnconfigure(0, weight=1)
            card.grid_rowconfigure((0, 1), weight=1)
            
            # Metric value
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=24, weight="bold")
            ).grid(row=0, column=0, pady=(15, 5))
            
            # Metric label
            ctk.CTkLabel(
                card,
                text=metric,
                font=ctk.CTkFont(size=12),
                text_color=("gray40", "gray60")
            ).grid(row=1, column=0, pady=(0, 15))

            
    def create_charts_section(self, parent):
        """Create charts section"""
        # Configure the parent's grid for charts
        parent.grid_columnconfigure(0, weight=2)  # Main chart gets more space
        parent.grid_columnconfigure(2, weight=1)  # Stats get less space
        
        # Main chart
        chart_frame = ctk.CTkFrame(parent, corner_radius=10)
        chart_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        
        # Configure chart frame grid
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(0, weight=1)
        
        # Create sample line chart
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        x = list(range(7))
        y = [random.randint(1000, 5000) for _ in range(7)]
        
        ax.plot(x, y, marker='o')
        ax.set_title("Weekly Revenue")
        ax.set_xlabel("Day")
        ax.set_ylabel("Revenue ($)")
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Side stats
        stats_frame = ctk.CTkFrame(parent, corner_radius=10)
        stats_frame.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")
        
        # Configure stats frame grid
        stats_frame.grid_columnconfigure(0, weight=1)
        
        stats = [
            ("Total Users", "1,234"),
            ("Active Users", "892"),
            ("New Users", "+121"),
            ("Bounce Rate", "32%")
        ]
        
        for idx, (label, value) in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color=("gray40", "gray60")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w")


    def show_users(self):
        self.clear_main_frame()
        main_frame = self.setup_main_frame()
        UsersView(main_frame, self.db)

    def show_patients(self):
        self.clear_main_frame()
        main_frame = self.setup_main_frame()
        PatientsView(main_frame)

    def show_tests(self):
        self.clear_main_frame()
        main_frame = self.setup_main_frame()
        TestsView(main_frame)

    def show_results(self):
        self.clear_main_frame()
        main_frame = self.setup_main_frame()
        ResultsView(main_frame)

    def show_settings(self):
        self.clear_main_frame()
        main_frame = self.setup_main_frame()
        SettingsView(main_frame)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if self.logout_callback:
                self.logout_callback()
            self.master.destroy()