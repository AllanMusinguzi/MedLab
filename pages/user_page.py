import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import report_generate
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

        self.tests_frame = ttk.LabelFrame(tests_results_frame, text="Tests", padding="10", style='TLabelframe', labelanchor="n")
        self.tests_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.tests_frame.columnconfigure(0, weight=1)
        self.tests_frame.rowconfigure(0, weight=1)

        # Create a Treeview for tests
        self.tests_tree = ttk.Treeview(self.tests_frame, columns=("ID", "Name", "Price"), show="headings")
        self.tests_tree.heading("ID", text="ID")
        self.tests_tree.heading("Name", text="Test Name")
        self.tests_tree.heading("Price", text="Price")
        self.tests_tree.grid(row=0, column=0, sticky="nsew")

        # Bind the selection event
        self.tests_tree.bind("<<TreeviewSelect>>", self.on_test_select)

        self.load_tests()

        # Modify the Results Frame
        self.results_frame = ttk.LabelFrame(tests_results_frame, text="Test Results", padding="10", style='TLabelframe', labelanchor="n")
        self.results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(1, weight=1)

        ttk.Label(self.results_frame, text="Test ID:").grid(row=0, column=0, sticky="w")
        self.test_id_var = tk.StringVar()
        ttk.Entry(self.results_frame, textvariable=self.test_id_var, state="readonly").grid(row=0, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Patient ID:").grid(row=1, column=0, sticky="w")
        self.patient_id_var = tk.StringVar()
        ttk.Entry(self.results_frame, textvariable=self.patient_id_var, state="readonly").grid(row=1, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Result:").grid(row=2, column=0, sticky="w")
        self.result_var = tk.StringVar(value="Select Result")
        self.result_combobox = ttk.Combobox(self.results_frame, textvariable=self.result_var, values=["Positive", "Negative", "Normal", "Abnormal"], state="readonly")
        self.result_combobox.grid(row=2, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Description:").grid(row=3, column=0, sticky="w")
        self.description_text = tk.Text(self.results_frame, height=5, width=20, background='white')
        self.description_text.grid(row=3, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Date of Test:").grid(row=4, column=0, sticky="w")
        self.date_entry = DateEntry(self.results_frame, width=17, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=4, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Doctor/Technician:").grid(row=5, column=0, sticky="w")
        self.doctor_entry = ttk.Entry(self.results_frame)
        self.doctor_entry.grid(row=5, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Comments:").grid(row=6, column=0, sticky="w")
        self.comments_text = tk.Text(self.results_frame, height=5, width=20, background='white')
        self.comments_text.grid(row=6, column=1, sticky="ew")

        ttk.Button(self.results_frame, text="Submit Result", command=self.submit_result).grid(row=7, column=0, columnspan=2, pady=(10, 0))

    def load_tests(self):
        # Clear existing items
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)

        # Fetch tests from the database
        cursor = self.db.cursor()
        cursor.execute("SELECT id, name, price FROM tests")
        tests = cursor.fetchall()
        cursor.close()

        # Insert tests into the Treeview
        for test in tests:
            self.tests_tree.insert("", "end", values=test)

    def on_test_select(self, event):
        selected_items = self.tests_tree.selection()
        if selected_items:
            item = selected_items[0]
            test_id = self.tests_tree.item(item)['values'][0]
            self.test_id_var.set(test_id)
            
            # Get the current patient ID (you need to implement this based on your UI structure)
            current_patient_id = self.get_current_patient_id()
            self.patient_id_var.set(current_patient_id)

            # Clear previous results
            self.clear_result_fields()

            # Prompt user to input test results
            messagebox.showinfo("Input Required", f"Please input the results for Test ID: {test_id}")

    def get_current_patient_id(self):
        # Implement this method to return the current patient ID
        # For now, we'll return a placeholder value
        return self.patient_id_entry.get()  # Assuming phone number is used as patient ID

    def clear_result_fields(self):
        self.result_var.set("Select Result")
        self.description_text.delete("1.0", tk.END)
        self.date_entry.set_date(date.today())
        self.doctor_entry.delete(0, tk.END)
        self.comments_text.delete("1.0", tk.END)

    def submit_result(self):
        # Gather result information
        test_id = self.test_id_var.get()
        patient_id = self.patient_id_var.get()
        result = self.result_var.get()
        description = self.description_text.get("1.0", tk.END).strip()
        test_date = self.date_entry.get_date()
        doctor_technician = self.doctor_entry.get()
        comments = self.comments_text.get("1.0", tk.END).strip()

        # Validate result information
        if not all([test_id, patient_id, result, description, test_date, doctor_technician]):
            messagebox.showerror("Error", "All fields except Comments are required.")
            return

        cursor = self.db.cursor()
        try:
            # Insert results into 'results' table
            cursor.execute("""
                INSERT INTO results (patient_id, test_id, result, description, test_date, doctor_technician, comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, test_id, result, description, test_date, doctor_technician, comments))

            # Commit the changes to the database
            self.db.commit()
            messagebox.showinfo("Success", "Test result submitted successfully.")
            self.clear_result_fields()
        except Exception as e:
            # Rollback the transaction if an error occurs
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to submit test result: {str(e)}")
            print(f"Error details: {e}")  # Log the error for debugging
        finally:
            cursor.close()

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

        self.result_var = tk.StringVar()
        self.result_value_entry = tk.Entry(self)
        self.description_entry = tk.Entry(self)
        self.date_picker = DateEntry(self)  # Date picker widget
        self.doctor_entry = tk.Entry(self)
        self.comments_entry = tk.Entry(self)        

    def add_patient(self):
        # Gather patient information
        phone = self.phone_entry.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get_date()
        age = self.age_var.get()
        address = self.address_entry.get()
        history = self.history_entry.get()

        # Validate patient information
        if not all([phone, name, gender, dob, age, address]):
            messagebox.showerror("Error", "All fields except Medical History are required.")
            return

        # Validate that at least one test is selected
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one test.")
            return

        cursor = self.db.cursor()
        try:
            # Insert patient information into 'patients' table
            cursor.execute("""
                INSERT INTO patients (phone_number, full_name, gender, dob, age, address, medical_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (phone, name, gender, dob, age, address, history))

            # Get the last inserted patient_id
            patient_id = cursor.lastrowid

            # Loop through each selected test and insert into 'patient_tests' table
            for item in selected_items:
                test_id = self.tree.item(item)['values'][0]  # Get test ID from selected test
                
                # Insert the selected test into 'patient_tests' table
                cursor.execute("INSERT INTO patient_tests (patient_id, test_id) VALUES (%s, %s)", (patient_id, test_id))

            # Commit all changes to the database
            self.db.commit()
            
            # Display patient_id and test_id in the results frame (assumed to have corresponding entry fields)
            self.patient_id_entry.delete(0, tk.END)
            self.patient_id_entry.insert(0, patient_id)

            # Assuming the first selected test is the one to display in results frame
            self.test_id_entry.delete(0, tk.END)
            self.test_id_entry.insert(0, test_id)

            messagebox.showinfo("Success", "Patient and tests added successfully.")
            self.clear_fields()

        except Exception as e:
            # Rollback the transaction if an error occurs and provide more detailed error context
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to add patient or tests: {str(e)}")
            raise

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
            # First, delete existing tests for the patient
            cursor.execute("DELETE FROM patient_tests WHERE patient_id = %s", (patient[0],))

            # Then, add selected tests
            selected_items = self.tree.selection()  
            for item in selected_items:
                test_id = self.tree.item(item)['values'][0]  # Assuming test ID is in the first column
                cursor.execute("INSERT INTO patient_tests (patient_id, test_id) VALUES (%s, %s)", (patient[0], test_id))

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

            # Create a popup dialog
            popup = tk.Toplevel(self.master)
            popup.title("Patient Information")

            # Create a Treeview to display patient information
            tree = ttk.Treeview(popup, columns=("Attribute", "Value"), show="headings")
            tree.heading("Attribute", text="Attribute")
            tree.heading("Value", text="Value")
            tree.column("Attribute", anchor="w")
            tree.column("Value", anchor="w")

            # Insert patient data into the Treeview
            patient_data = [
                ("Patient ID", patient[0]),
                ("Name", patient[2]),
                ("Gender", patient[3]),
                ("Date of Birth", patient[4]),
                ("Contact", patient[1]),
                ("Age", patient[5]),
                ("Address", patient[6]),
                ("History", patient[7])
            ]

            for item in patient_data:
                tree.insert("", tk.END, values=item)

            # Fetch and display patient's tests
            cursor.execute("""
                SELECT t.test_name 
                FROM patient_tests pt
                JOIN tests t ON pt.test_id = t.test_id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            tests = [test[0] for test in cursor.fetchall()]

            # Display tests in the same table
            if tests:
                tree.insert("", tk.END, values=("Tests", ", ".join(tests)))

            tree.pack(padx=10, pady=10)

            # Button to close the popup
            close_button = tk.Button(popup, text="Close", command=popup.destroy)
            close_button.pack(pady=10)

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

            # Fetch patient's tests and results
            cursor.execute("""
                SELECT t.test_name, t.description, tr.result, tr.test_date, tr.comment
                FROM patient_tests pt
                JOIN tests t ON pt.test_id = t.test_id
                JOIN test_results tr ON pt.test_id = tr.test_id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            test_results = cursor.fetchall()

            # Prepare data for the PDF report
            patient_data = {
                "name": patient[2],
                "phone": patient[1],
                "gender": patient[3],
                "dob": patient[4],
                "age": patient[5],
                "address": patient[6],
                "medical_history": patient[7],
                "tests": [(test_name, (result, test_date, comment)) for test_name, description, result, test_date, comment in test_results]
            }

            # Call the report_generate function to create a PDF
            pdf_file_path = report_generate.generate_report(patient_data)

            # Open the PDF file with the default PDF viewer
            os.startfile(pdf_file_path)

            messagebox.showinfo("Success", "Patient information PDF has been generated and opened.")
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