# patient_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

class PatientManagement(ttk.Frame):
    def __init__(self, master, db, return_callback):
        super().__init__(master)
        self.db = db
        self.return_callback = return_callback
        
        self.setup_ui()
        self.load_patients()

    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header_frame, 
                 text="Patient Management",
                 font=('Ubuntu', 14, 'bold')).pack(side='left')
        
        ttk.Button(header_frame,
                  text="Back to Dashboard",
                  command=self.return_callback).pack(side='right')

        # Main content (split into left and right panes)
        content_frame = ttk.PanedWindow(self, orient='horizontal')
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left pane - Patient List
        self.create_patient_list(content_frame)
        
        # Right pane - Patient Details
        self.create_patient_details(content_frame)

    def create_patient_list(self, parent):
        list_frame = ttk.LabelFrame(parent, text="Patient List")
        parent.add(list_frame, weight=1)

        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_patients)
        ttk.Entry(search_frame, 
                 textvariable=self.search_var).pack(side='left', fill='x', expand=True)

        # Patient table
        columns = ("ID", "Name", "Phone", "Age", "Gender")
        self.patient_table = ttk.Treeview(list_frame, 
                                        columns=columns,
                                        show="headings",
                                        selectmode="browse")
        
        for col in columns:
            self.patient_table.heading(col, text=col)
            self.patient_table.column(col, width=100)

        self.patient_table.pack(fill='both', expand=True, padx=5, pady=5)
        self.patient_table.bind('<<TreeviewSelect>>', self.on_patient_select)

    def create_patient_details(self, parent):
        details_frame = ttk.LabelFrame(parent, text="Patient Details")
        parent.add(details_frame, weight=2)

        # Create form fields
        form_frame = ttk.Frame(details_frame)
        form_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Configure grid
        form_frame.columnconfigure(1, weight=1)

        # Add form fields
        self.create_form_field(form_frame, "Full Name:", 0)
        self.create_form_field(form_frame, "Phone:", 1)
        self.create_gender_field(form_frame, 2)
        self.create_dob_field(form_frame, 3)
        self.create_form_field(form_frame, "Address:", 4)
        self.create_medical_history_field(form_frame, 5)

        # Buttons
        button_frame = ttk.Frame(details_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, 
                  text="New Patient",
                  command=self.new_patient).pack(side='left', padx=5)
        
        ttk.Button(button_frame,
                  text="Save",
                  command=self.save_patient).pack(side='left', padx=5)
        
        ttk.Button(button_frame,
                  text="Delete",
                  command=self.delete_patient).pack(side='left', padx=5)

    # ... Additional methods for patient management ...