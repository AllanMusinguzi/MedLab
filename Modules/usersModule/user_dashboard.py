import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont
import os
from tkinter import PhotoImage, messagebox

class UserDashboard(ctk.CTkFrame):
    def __init__(self, master, db, user_id, username, **kwargs):
        super().__init__(master)
        self.initialize_dashboard(db, user_id, username)
        #self.role, self.full_name, self.phone_number, self.address, self.email = self.user_info(user_id)
        self.setup_ui()
        self.dropdown_state = False 
        self.show_dashboard()

    # ===============================
    # Initialization Methods
    # ===============================
    def initialize_dashboard(self, db, user_id, username, logout_callback=None):
        """Initialize dashboard attributes and settings"""
        self.db = db
        self.user_id = user_id
        self.username = username
        self.logout_callback = logout_callback
       
        
        # Configure the main window
        if isinstance(self.master, (ctk.CTk, ctk.CTkToplevel)):
            self.master.title("User Dashboard")
            self.master.geometry("1400x800")

        # Configure theme and styling
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configure fonts
        self.setup_fonts()

    def setup_fonts(self):
        """Initialize font configurations"""
        self.title_font = ctk.CTkFont(family="Ubuntu", size=24, weight="bold")
        self.header_font = ctk.CTkFont(family="Ubuntu", size=18, weight="bold")
        self.normal_font = ctk.CTkFont(family="Ubuntu", size=14)
        self.small_font = ctk.CTkFont(family="Ubuntu", size=12)

    def setup_ui(self):
        """Setup main UI container and layout"""
        # Main container
        self.main_container = ctk.CTkFrame(self.master, fg_color="#f0f0f0")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure grid
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        
        self.create_sidebar()
        self.create_main_area()

    # ===============================
    # Sidebar Components
    # ===============================
    def create_sidebar(self):
        """Create and setup sidebar"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            fg_color="#1a237e",
            width=280,
            corner_radius=15
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 10), pady=0)
        self.sidebar.grid_propagate(False)
        
        self.create_profile_section()
        self.create_navigation_menu()
        self.create_logout_button()

    def create_navigation_menu(self):
        """Create navigation menu buttons"""
        nav_items = [
            ("Dashboard", "home", self.show_dashboard),
            ("Patient Records", "user", self.show_patient_management),
            ("Lab Tests", "lab", self.show_test_management),
            ("Results", "chart", self.show_result_management),
            ("Inventory", "box", self.show_inventory_management),
            ("Quality Control", "shield", self.show_quality_control),
            ("Analytics", "graph", self.show_analytics)
        ]
        
        for text, icon, command in nav_items:
            self.create_nav_button(text, icon, command)

    def create_nav_button(self, text, icon_name, command):
        """Create individual navigation button"""
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            font=self.normal_font,
            fg_color="transparent",
            text_color="white",
            hover_color="#283593",
            anchor="w",
            height=45,
            command=command
        )
        btn.pack(fill="x", padx=10, pady=5)

    def create_logout_button(self):
        """Create logout button"""
        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            font=self.normal_font,
            fg_color="#f44336",
            hover_color="#d32f2f",
            height=40,
            command=self.logout
        ).pack(side="bottom", padx=20, pady=20, fill="x")

    # ===============================
    # Profile Picture Management
    # ===============================
    def create_profile_section(self):
        """Create profile section in sidebar with expandable details"""
        profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_frame.pack(fill="x", padx=20, pady=(30, 20))
        
        # Lab name
        ctk.CTkLabel(
            profile_frame,
            text="LLL Medical Laboratory",
            font=self.title_font,
            text_color="white"
        ).pack(pady=(0, 10))
        
        # Profile picture and details container
        self.profile_container = ctk.CTkFrame(profile_frame, fg_color="transparent")
        self.profile_container.pack(fill="x", expand=True)
        
        # Profile picture frame
        self.profile_pic_frame = ctk.CTkFrame(
            self.profile_container,
            width=80,
            height=80,
            fg_color="transparent"
        )
        self.profile_pic_frame.pack(pady=(0, 10))
        
        self.display_profile_picture()  # Display profile picture
        
        # Create expandable details section
        self.details_frame = ctk.CTkFrame(
            self.profile_container,
            fg_color="#283593",
            corner_radius=10
        )
        #self.create_user_details()
        self.details_frame.pack_forget()  # Initially hidden

    def display_profile_picture(self):
        """Display user profile picture"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT profile_picture, email, role, phone_number FROM users WHERE user_id = %s",
                (self.user_id,)
            )
            result = cursor.fetchone()
            
            if result and result[0] and os.path.exists(result[0]):
                self.load_profile_picture(result)
            else:
                self.profile_photo = self.create_default_profile_picture()
            
            self.create_profile_picture_label()
            
        except Exception as e:
            print(f"Error loading profile picture: {e}")
            self.profile_photo = self.create_default_profile_picture()

    def create_profile_picture_label(self):
        """Create and pack profile picture label"""
        self.profile_pic_label = ctk.CTkLabel(
            self.profile_pic_frame,
            image=self.profile_photo,
            text=""
        )
        self.profile_pic_label.pack(expand=True)
        
        # Bind profile picture to toggle user details
        self.profile_pic_label.bind("<Button-1>", self.toggle_user_details)

    def display_profile_picture(self):
        """Display user profile picture"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT profile_picture, email, role, phone_number, full_name, address FROM users WHERE user_id = %s",
                (self.user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                # If a result exists, load profile picture and details
                if result[0] and os.path.exists(result[0]):
                    self.load_profile_picture(result)
                else:
                    self.profile_photo = self.create_default_profile_picture()

                # Create and display profile picture label
                self.create_profile_picture_label()

                # Set user info for displaying details
                self.user_info = {
                    'email': result[1],
                    'role': result[2],
                    'phone_number': result[3],
                    'full_name': result[4],
                    'address': result[5]
                }
            else:
                # Handle the case where no result is found
                print("No user found with the given ID.")
                self.profile_photo = self.create_default_profile_picture()
                self.create_profile_picture_label()

        except Exception as e:
            print(f"Error loading profile picture: {e}")
            self.profile_photo = self.create_default_profile_picture()

    def load_profile_picture(self, result):
        """Load and process profile picture"""
        image_path = result[0]
        
        # Process the image to make it circular
        img = Image.open(image_path)
        img = img.resize((80, 80))
        
        # Create circular mask
        mask = Image.new('L', (80, 80), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 80, 80), fill=255)
        
        # Apply the mask to the image
        output = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        # Store the profile picture in the object
        self.profile_photo = ctk.CTkImage(
            light_image=output,
            dark_image=output,
            size=(80, 80)
        )

    def create_default_profile_picture(self):
        """Create default profile picture with initials"""
        img = Image.new('RGB', (80, 80), color='#2196f3')
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 80, 80), fill='#2196f3')
        
        try:
            font = ImageFont.truetype("Ubuntu", 32)
        except Exception as e:
            print(f"Font loading error: {e}")
            font = ImageFont.load_default()
        
        initials = self.username[0].upper()
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (80 - text_width) // 2
        y = (80 - text_height) // 2
        
        draw.text((x, y), initials, fill='white', font=font)
        
        return ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(80, 80)
        )

    def create_profile_picture_label(self):
        """Create and pack profile picture label"""
        self.profile_pic_label = ctk.CTkLabel(
            self.profile_pic_frame,
            image=self.profile_photo,
            text=""
        )
        self.profile_pic_label.pack(expand=True)
        self.profile_pic_label.bind("<Button-1>", self.toggle_user_details)

    def toggle_user_details(self, event=None):
        """Toggle the visibility of user details"""
        self.dropdown_state = not self.dropdown_state
        
        if self.dropdown_state:
            # Show details
            self.show_user_details()
            
            # Adjusting padding for horizontal space
            self.details_frame.pack(fill="x", padx=(10, 10), pady=(10, 10), anchor="w")
        else:
            # Hide details
            self.details_frame.pack_forget()

    def show_user_details(self):
        """Create and display the user details in the details frame"""
        # Check if labels are already created, if not, create them
        if not hasattr(self, 'user_id_label'):
            # Create labels if they don't exist
            self.user_id_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"User ID: {self.user_info.get(self.user_id, 'N/A')}", 
                font=self.normal_font, 
                text_color="white"
                )

            self.full_name_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"Full Name: {self.user_info.get('full_name', 'N/A')}", 
                font=self.normal_font, text_color="white"
                )

            self.username_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"Username: {self.user_info.get(self.username, 'N/A')}", 
                font=self.normal_font, text_color="white"
                )

            self.telephone_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"Phone: {self.user_info.get('phone_number', 'N/A')}", 
                font=self.normal_font, text_color="white"
                )

            self.email_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"Email: {self.user_info.get('email', 'N/A')}", 
                font=self.normal_font, 
                text_color="white"
                )

            self.address_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"Address: {self.user_info.get('address', 'N/A')}", 
                font=self.normal_font, text_color="white"
                )

            self.role_label = ctk.CTkLabel(
                self.details_frame, 
                text=f"Role: {self.user_info.get('role', 'N/A')}", 
                font=self.normal_font, 
                text_color="white"
                )
            
            # Pack the labels into the details frame with appropriate padding
            self.user_id_label.pack(pady=(10, 5), anchor="w")
            self.full_name_label.pack(pady=5, anchor="w")
            self.username_label.pack(pady=5, anchor="w")
            self.telephone_label.pack(pady=5, anchor="w")
            self.email_label.pack(pady=5, anchor="w")
            self.address_label.pack(pady=5, anchor="w")
            self.role_label.pack(pady=5, anchor="w")

        else:
            # If labels are already created, just pack them again
            self.user_id_label.pack(pady=(10, 5), anchor="w")
            self.full_name_label.pack(pady=5, anchor="w")
            self.username_label.pack(pady=5, anchor="w")
            self.telephone_label.pack(pady=5, anchor="w")
            self.email_label.pack(pady=5, anchor="w")
            self.address_label.pack(pady=5, anchor="w")
            self.role_label.pack(pady=5, anchor="w")

    # ===============================
    # Main Area Components
    # ===============================
    def create_main_area(self):
        """Create main content area"""
        self.main_area = ctk.CTkFrame(
            self.main_container,
            fg_color="#f5f5f5",
            corner_radius=15
        )
        self.main_area.pack(side="right", fill="both", expand=True, padx=(0, 0), pady=0)
        
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

    def create_stat_card(self, parent, title, value, icon_name, color):
        """Create statistics card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=self.small_font,
            text_color="gray"
        ).pack(padx=20, pady=(15, 5), anchor="w")
        
        ctk.CTkLabel(
            card,
            text=str(value),
            font=self.title_font,
            text_color=color
        ).pack(padx=20, pady=(0, 15), anchor="w")
        
        return card

    # ===============================
    # View Management
    # ===============================
    def show_dashboard(self):
        """Display dashboard view"""
        self.clear_main_area()
        
        # Header
        header = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        ctk.CTkLabel(
            header,
            text="Dashboard Overview",
            font=self.title_font
        ).pack(side="left")
        
        # Stats grid
        stats_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        stats_frame.pack(fill="both", padx=20, pady=20)
        
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        stats = [
            ("Total Patients", "1,234", "#2196f3"),
            ("Pending Tests", "45", "#ff9800"),
            ("Completed Tests", "789", "#4caf50"),
            ("Critical Results", "12", "#f44336")
        ]
        
        for idx, (title, value, color) in enumerate(stats):
            card = self.create_stat_card(stats_frame, title, value, "", color)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
        
        # Recent Activity
        activity_frame = ctk.CTkFrame(self.main_area, fg_color="white", corner_radius=15)
        activity_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            activity_frame,
            text="Recent Activity",
            font=self.header_font
        ).pack(padx=20, pady=20, anchor="w")

    def clear_main_area(self):
        """Clear main area content"""
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # Placeholder methods for other views
    def show_patient_management(self):
        self.clear_main_area()
        # Implementation needed

    def show_test_management(self):
        self.clear_main_area()
        # Implementation needed

    def show_result_management(self):
        self.clear_main_area()
        # Implementation needed

    def show_inventory_management(self):
        self.clear_main_area()
        # Implementation needed

    def show_quality_control(self):
        self.clear_main_area()
        # Implementation needed

    def show_analytics(self):
        self.clear_main_area()
        # Implementation needed

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if self.logout_callback:
                self.logout_callback()
            self.master.destroy()