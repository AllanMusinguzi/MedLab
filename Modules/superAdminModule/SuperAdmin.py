import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from datetime import datetime

from Modules.superAdminModule.Dashboard import DashboardView
from Modules.superAdminModule.Users import UsersView
from Modules.superAdminModule.Patients import PatientsView
from Modules.superAdminModule.Tests import TestsView
from Modules.superAdminModule.Results import ResultsView
from Modules.superAdminModule.Settings import SettingsView

class SuperAdminPage(ttk.Frame):
    def __init__(self, master, db, user_id, username, password, phone_number, logout_callback):
        super().__init__(master)
        
        # Store user data
        self.master = master
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.logout_callback = logout_callback
        
        # Configure window
        #self.title("Laboratory Management System - Super Admin")
        #self.geometry("1200x700")
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Initialize image dictionary
        self.images = {}
        
        # Load images and create frames
        self.load_images()
        self.create_navigation_frame()
        self.create_main_frame()
        
        # Initialize data
        #self.load_data()
        
        # Show initial dashboard view
        self.show_dashboard()
        
    def load_images(self):
        # Define image paths - replace with your actual image paths
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        self.home_image = ctk.CTkImage(Image.open(os.path.join(image_path, "home.png")), size=(20, 20))
        self.users_image = ctk.CTkImage(Image.open(os.path.join(image_path, "users.png")), size=(20, 20))
        self.patients_image = ctk.CTkImage(Image.open(os.path.join(image_path, "patients.png")), size=(20, 20))
        self.tests_image = ctk.CTkImage(Image.open(os.path.join(image_path, "tests.png")), size=(20, 20))
        self.results_image = ctk.CTkImage(Image.open(os.path.join(image_path, "results.png")), size=(20, 20))
        self.settings_image = ctk.CTkImage(Image.open(os.path.join(image_path, "settings.png")), size=(20, 20))
        
    def create_navigation_frame(self):
        # Navigation Frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.pack(side="left", fill="y", padx=10, pady=10)  # Use pack for the navigation frame

        # Logo Label
        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame, text="  LMS Admin", image=self.logo_image,
            compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.pack(side="top", fill="x", padx=20, pady=20)  # Use pack for logo label

        # Navigation Buttons
        self.dashboard_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
            text="Dashboard", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), image=self.home_image, anchor="w",
            command=self.show_dashboard)
        self.dashboard_button.pack(side="top", fill="x", padx=20)  # Use pack for dashboard button
        
        self.users_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
            text="Users", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), image=self.users_image, anchor="w",
            command=self.show_users)
        self.users_button.pack(side="top", fill="x", padx=20)  # Use pack for users button

        self.patients_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
            text="Patients", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), image=self.patients_image, anchor="w",
            command=self.show_patients)
        self.patients_button.pack(side="top", fill="x", padx=20)  # Use pack for patients button

        self.tests_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
            text="Tests", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), image=self.tests_image, anchor="w",
            command=self.show_tests)
        self.tests_button.pack(side="top", fill="x", padx=20)  # Use pack for tests button

        self.results_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
            text="Results", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), image=self.results_image, anchor="w",
            command=self.show_results)
        self.results_button.pack(side="top", fill="x", padx=20)  # Use pack for results button

        self.settings_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
            text="Settings", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), image=self.settings_image, anchor="w",
            command=self.show_settings)
        self.settings_button.pack(side="top", fill="x", padx=20)  # Use pack for settings button

        # Appearance mode menu
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event)
        self.appearance_mode_menu.pack(side="bottom", fill="x", padx=20, pady=20)  # Use pack for appearance menu

    def create_main_frame(self):
        # Main frame to hold different views
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Use pack for main frame

        # Set up column and row configurations for the main frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
    def show_dashboard(self):
        self.clear_main_frame()
        DashboardView(self.main_frame)
        self.select_frame_by_name("dashboard")
        
    def show_users(self):
        self.clear_main_frame()
        UsersView(self.main_frame, self.db)
        self.select_frame_by_name("users")
        
    def show_patients(self):
        self.clear_main_frame()
        PatientsView(self.main_frame)
        self.select_frame_by_name("patients")
        
    def show_tests(self):
        self.clear_main_frame()
        TestsView(self.main_frame)
        self.select_frame_by_name("tests")
        
    def show_results(self):
        self.clear_main_frame()
        ResultsView(self.main_frame)
        self.select_frame_by_name("results")
        
    def show_settings(self):
        self.clear_main_frame()
        SettingsView(self.main_frame)
        self.select_frame_by_name("settings")
        
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def select_frame_by_name(self, name):
        # Reset all button colors
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.users_button.configure(fg_color=("gray75", "gray25") if name == "users" else "transparent")
        self.patients_button.configure(fg_color=("gray75", "gray25") if name == "patients" else "transparent")
        self.tests_button.configure(fg_color=("gray75", "gray25") if name == "tests" else "transparent")
        self.results_button.configure(fg_color=("gray75", "gray25") if name == "results" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        
    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
