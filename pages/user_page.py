import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import tempfile
import os

class UserPage(ttk.Frame):
    def __init__(self, master, db, user_id, logout_callback):
        super().__init__(master)
        self.db = db
        self.user_id = user_id
        self.logout_callback = logout_callback

        self.style = ttk.Style()
        self.style.theme_use('clam')

        tests_results_frame = ttk.Frame(self)
        tests_results_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.style.configure('.', font=('Ubuntu', 11))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabelframe', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', background='#4a7abc', foreground='white')
        self.style.map('TButton', background=[('active', '#3a5a8c')])
        self.style.configure('Header.TLabel', font=('Ubuntu', 12, 'bold')) #, foreground='#2c3e50'

        self.create_widgets()

    def create_widgets(self):
        self.configure(style='TFrame')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding="10", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Header
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        ttk.Label(header_frame, text="Patient Management", style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Logout", command=self.logout_callback).pack(side=tk.RIGHT)

        # Patient Information Frame
        patient_frame = ttk.LabelFrame(main_frame, text="Patient Information", padding="10", style='TLabelframe', labelanchor="n")
        patient_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(0, 20))
        patient_frame.columnconfigure(1, weight=1)

        labels = ["Phone Number:", "Full Name:", "Gender:", "Date of Birth:", "Age:", "Address:", "Medical History:"]
        for i, label in enumerate(labels):
            ttk.Label(patient_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)

        self.phone_entry = ttk.Entry(patient_frame)
        self.phone_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        self.name_entry = ttk.Entry(patient_frame)
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        gender_frame = ttk.Frame(patient_frame, style='TFrame')
        gender_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.gender_var = tk.StringVar()
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT)

        self.dob_entry = DateEntry(patient_frame, width=12, background='#4a7abc', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.dob_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        self.dob_entry.bind("<<DateEntrySelected>>", self.calculate_age)

        self.age_var = tk.StringVar()
        ttk.Label(patient_frame, textvariable=self.age_var).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)

        self.address_entry = ttk.Entry(patient_frame)
        self.address_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)

        self.history_entry = ttk.Entry(patient_frame)
        self.history_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)

        # Tests and Results Frame
        tests_results_frame = ttk.Frame(main_frame, style='TFrame')
        tests_results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(0, 20))
        tests_results_frame.columnconfigure(0, weight=1)
        tests_results_frame.rowconfigure(1, weight=1)

        # Define self.tests_frame inside tests_results_frame
        self.tests_frame = ttk.LabelFrame(tests_results_frame, text="Tests", padding="10", style='TLabelframe', labelanchor="n")
        self.tests_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.tests_frame.columnconfigure(0, weight=1)
        self.tests_frame.rowconfigure(0, weight=1)
        self.load_tests()

        # Results Frame
        results_frame = ttk.LabelFrame(tests_results_frame, text="Test Results", padding="10", style='TLabelframe', labelanchor="n")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = tk.Text(results_frame, height=10, width=40, background='white')
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Buttons
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)

        buttons = [
            ("Add Patient", self.add_patient),
            ("Modify Patient", self.modify_patient),
            ("View Patient", self.view_patient),
            ("Print Info", self.print_info)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=5, sticky=(tk.W, tk.E))

    def calculate_age(self, event=None):
        birth_date = self.dob_entry.get_date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        self.age_var.set(str(age))

    def load_tests(self):
        # Create Treeview widget inside the tests_frame
        self.tree = ttk.Treeview(self.tests_frame, columns=("Test ID", "Test Name", "Description"), show="headings")
        
        # Define headings
        self.tree.heading("Test ID", text="Test ID")
        self.tree.heading("Test Name", text="Test Name")
        self.tree.heading("Description", text="Description")

        # Set column widths (optional)
        self.tree.column("Test ID", width=50)
        self.tree.column("Test Name", width=100)
        self.tree.column("Description", width=300)

        # Add Treeview to the grid inside the tests_frame
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Enable scrolling if needed
        scrollbar = ttk.Scrollbar(self.tests_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Load data from the database
        cursor = self.db.cursor()
        cursor.execute("SELECT test_id, test_name, description FROM tests")

        # Insert data into the Treeview
        for test in cursor.fetchall():
            self.tree.insert("", tk.END, values=(test[0], test[1], test[2]))

        cursor.close()

    def add_patient(self):
        # Gather patient information
        phone = self.phone_entry.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get_date()
        age = self.age_var.get()
        address = self.address_entry.get()
        history = self.history_entry.get()

        # Validate input
        if not all([phone, name, gender, dob, age, address]):
            messagebox.showerror("Error", "All fields except Medical History are required.")
            return

        # Insert patient into the database
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO patients (phone_number, full_name, gender, dob, age, address, medical_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (phone, name, gender, dob, age, address, history))
            
            patient_id = cursor.lastrowid

            """"    

                # Add selected tests to patient_tests table
                selected_items = self.tree.selection()  
                selected_tests = [self.tree.item(item)['values'][0] for item in selected_items]  # Adjust index as needed

                for test in selected_tests:
                    cursor.execute("SELECT test_id FROM tests WHERE test_name = %s", (test,))
                    result = cursor.fetchone()
                    if result is None:
                        raise ValueError(f"Test '{test}' not found in the database")
                    
                    test_id = result[0]
                    cursor.execute("INSERT INTO patient_tests (patient_id, test_id) VALUES (%s, %s)", (patient_id, test_id))

            """

            self.db.commit()
            messagebox.showinfo("Success", "Patient and tests added successfully")
            self.clear_fields()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to add patient: {str(e)}")
        finally:
            cursor.close()

    def modify_patient(self):
        # Get patient phone number
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number to modify a patient.")
            return

        # Fetch patient data
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
        patient = cursor.fetchone()

        if not patient:
            messagebox.showerror("Error", "Patient not found.")
            return

        # Update patient information
        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get_date()
        age = self.age_var.get()
        address = self.address_entry.get()
        history = self.history_entry.get()

        try:
            cursor.execute("""
                UPDATE patients 
                SET full_name = %s, gender = %s, dob = %s, age = %s, address = %s, medical_history = %s
                WHERE phone_number = %s
            """, (name, gender, dob, age, address, history, phone))

            # Update tests
            cursor.execute("DELETE FROM tests WHERE patient_id = %s", (patient[0],))
            selected_tests = [self.tree.get(i) for i in self.tree.selection()]
            for test in selected_tests:
                cursor.execute("SELECT test_id FROM tests WHERE test_name = %s", (test,))
                test_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO tests (patient_id, test_id) VALUES (%s, %s)", (patient[0], test_id))

            self.db.commit()
            messagebox.showinfo("Success", "Patient information updated successfully")
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
        finally:
            cursor.close()

    def view_patient(self):
        # Get patient phone number
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number to view a patient.")
            return

        # Fetch patient data
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
            patient = cursor.fetchone()

            if not patient:
                messagebox.showerror("Error", "Patient not found.")
                return

            # Populate fields with patient data
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, patient[2]) 
            self.gender_var.set(patient[3])  
            self.dob_entry.set_date(patient[4])  
            self.age_var.set(patient[5])  
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, patient[6]) 
            self.history_entry.delete(0, tk.END)
            self.history_entry.insert(0, patient[7]) 

            # Fetch and select patient's tests
            cursor.execute("""
                SELECT t.test_name 
                FROM tests pt
                JOIN tests t ON pt.test_id = t.id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            tests = [test[0] for test in cursor.fetchall()]
            
            self.tree.selection_clear(0, tk.END)
            for i in range(self.tree.size()):
                if self.tree.get(i) in tests:
                    self.tree.selection_set(i)

            messagebox.showinfo("Success", "Patient information loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient: {str(e)}")
        finally:
            cursor.close()

    def print_info(self):
        # Get patient phone number
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number to print patient information.")
            return

        # Fetch patient data
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
            patient = cursor.fetchone()

            if not patient:
                messagebox.showerror("Error", "Patient not found.")
                return

            # Fetch patient's tests
            cursor.execute("""
                SELECT t.test_name 
                FROM tests pt
                JOIN tests t ON pt.test_id = t.id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            tests = [test[0] for test in cursor.fetchall()]

            # Create a temporary file to store patient information
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write(f"Patient Information:\n")
                temp_file.write(f"Name: {patient[2]}\n")
                temp_file.write(f"Phone: {patient[1]}\n")
                temp_file.write(f"Gender: {patient[3]}\n")
                temp_file.write(f"Date of Birth: {patient[4]}\n")
                temp_file.write(f"Age: {patient[5]}\n")
                temp_file.write(f"Address: {patient[6]}\n")
                temp_file.write(f"Medical History: {patient[7]}\n")
                temp_file.write(f"\nTests:\n")
                for test in tests:
                    temp_file.write(f"- {test}\n")

            # Open the file with the default text editor
            os.startfile(temp_file.name)

            messagebox.showinfo("Success", "Patient information has been prepared for printing.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print patient information: {str(e)}")
        finally:
            cursor.close()

    def clear_fields(self):
        self.phone_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.dob_entry.set_date(date.today())
        self.age_var.set("")
        self.address_entry.delete(0, tk.END)
        self.history_entry.delete(0, tk.END)
        self.tree.selection_clear(0, tk.END)
        self.results_text.delete('1.0', tk.END)
    
    def logout(self):
        self.logout_callback()