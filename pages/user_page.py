import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry
from tkcalendar import DateEntry
from datetime import date
from report_generate import ReportGenerate
import subprocess

class UserPage(ttk.Frame):
    def __init__(self, master, db, user_id, logout_callback):
        super().__init__(master)
        self.db = db
        self.user_id = user_id
        self.logout_callback = logout_callback

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', font=('Ubuntu', 11))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabelframe', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', background='#4a7abc', foreground='white')
        self.style.map('TButton', background=[('active', '#3a5a8c')])
        self.style.configure('Header.TLabel', font=('Ubuntu', 12, 'bold'))

    def create_widgets(self):
        self.configure(style='TFrame')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding="10", style='TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.create_header(main_frame)
        self.create_patient_frame(main_frame)
        self.create_tests_results_frame(main_frame)
        self.create_buttons(main_frame)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent, style='TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        ttk.Label(header_frame, text="Patient Management", style='Header.TLabel').grid(row=0, column=0, sticky="w")
        ttk.Button(header_frame, text="Logout", command=self.logout_callback).grid(row=0, column=1, sticky="e")

    def create_patient_frame(self, parent):
        patient_frame = ttk.LabelFrame(parent, text="Patient Information", padding="10", style='TLabelframe')
        patient_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5), pady=(0, 10))
        patient_frame.columnconfigure(1, weight=1)
        patient_frame.rowconfigure(7, weight=1)

        labels = ["Phone Number:", "Full Name:", "Gender:", "Date of Birth:", "Age:", "Address:", "Medical History:"]
        self.patient_entries = {}

        for i, label in enumerate(labels):
            ttk.Label(patient_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            
            self.phone_entry = ttk.Entry(patient_frame)
            self.phone_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

            self.name_entry = ttk.Entry(patient_frame)
            self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

            self.address_entry = ttk.Entry(patient_frame)
            self.address_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)

            self.history_entry = ttk.Entry(patient_frame)
            self.history_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)

            if label == "Gender:":
                gender_frame = ttk.Frame(patient_frame, style='TFrame')
                gender_frame.grid(row=i, column=1, sticky="ew", pady=5)
                self.gender_var = tk.StringVar()
                ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT, padx=(0, 10))
                ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT)
                self.patient_entries[label] = self.gender_var
            elif label == "Date of Birth:":
                self.dob_entry = DateEntry(patient_frame, width=12, background='#4a7abc', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                self.dob_entry.grid(row=i, column=1, sticky="ew", pady=5)
                self.dob_entry.bind("<<DateEntrySelected>>", self.calculate_age)
                self.patient_entries[label] = self.dob_entry
            elif label == "Age:":
                self.age_var = tk.StringVar()
                ttk.Label(patient_frame, textvariable=self.age_var).grid(row=i, column=1, sticky="ew", pady=5)
                self.patient_entries[label] = self.age_var
            else:
                entry = ttk.Entry(patient_frame)
                entry.grid(row=i, column=1, sticky="ew", pady=5)
                self.patient_entries[label] = entry

        self.create_patient_table(patient_frame)

    def create_patient_table(self, parent):
        columns = ("Patient ID", "Test ID", "Name", "Phone", "Gender", "Age")
        self.patient_table = ttk.Treeview(parent, columns=columns, show="headings")
        self.patient_table.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=10)
        
        for col in columns:
            self.patient_table.heading(col, text=col)
            self.patient_table.column(col, width=100)  # Adjust width as needed

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.patient_table.yview)
        scrollbar.grid(row=8, column=2, sticky="ns")
        self.patient_table.configure(yscrollcommand=scrollbar.set)

        self.patient_table.bind("<<TreeviewSelect>>", self.on_patient_select)
        self.load_patients()

    def create_tests_results_frame(self, parent):
        tests_results_frame = ttk.Frame(parent, style='TFrame')
        tests_results_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0), pady=(0, 10))
        tests_results_frame.columnconfigure(0, weight=1)
        tests_results_frame.rowconfigure(1, weight=1)

        self.create_tests_frame(tests_results_frame)
        self.create_results_frame(tests_results_frame)

    def create_tests_frame(self, parent):
        tests_frame = ttk.LabelFrame(parent, text="Tests", padding="10", style='TLabelframe')
        tests_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        tests_frame.columnconfigure(0, weight=1)
        tests_frame.rowconfigure(0, weight=1)

        columns = ("ID", "Name", "Description")
        self.tests_tree = ttk.Treeview(tests_frame, columns=columns, show="headings")
        self.tests_tree.grid(row=0, column=0, sticky="nsew")
        
        for col in columns:
            self.tests_tree.heading(col, text=col)
            self.tests_tree.column(col, width=100)  # Adjust width as needed

        scrollbar = ttk.Scrollbar(tests_frame, orient="vertical", command=self.tests_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tests_tree.configure(yscrollcommand=scrollbar.set)

        self.tests_tree.bind("<<TreeviewSelect>>", self.on_test_select)
        self.load_tests()

    def create_results_frame(self, parent):
        results_frame = ttk.LabelFrame(parent, text="Test Results", padding="10", style='TLabelframe')
        results_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        results_frame.columnconfigure(1, weight=1)

        labels = ["Patient ID:", "Test ID:", "Result:", "Description:", "Date of Test:", "Doctor/Technician:", "Comments:"]
        self.result_entries = {}

        for i, label in enumerate(labels):
            ttk.Label(results_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Patient ID:":
                self.patient_id_var = tk.StringVar()
                entry = ttk.Entry(results_frame, textvariable=self.patient_id_var, state="readonly")
            elif label == "Test ID:":
                self.test_id_var = tk.StringVar()
                entry = ttk.Entry(results_frame, textvariable=self.test_id_var, state="normal")
            elif label == "Result:":
                self.result_var = tk.StringVar(value="Select Result")
                entry = ttk.Combobox(results_frame, textvariable=self.result_var, values=["Positive", "Negative", "Normal", "Abnormal"], state="readonly")
            elif label == "Date of Test:":
                entry = DateEntry(results_frame, width=12, background='#4a7abc', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            elif label in ["Description:", "Comments:"]:
                entry = tk.Text(results_frame, height=3, width=30)
            else:
                entry = ttk.Entry(results_frame)
            
            entry.grid(row=i, column=1, sticky="ew", pady=5)
            self.result_entries[label] = entry

        ttk.Button(results_frame, text="Submit Result", command=self.submit_result).grid(row=len(labels), column=0, columnspan=2, pady=(10, 0))

    def create_buttons(self, parent):
        button_frame = ttk.Frame(parent, style='TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        buttons = [
            ("Add Patient", self.add_patient),
            ("Update Patient", self.modify_patient),
            ("View Patient", self.view_patient),
            ("Print Info", self.print_info)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=5, sticky="ew")

    def load_patients(self):
        cursor = self.db.cursor()

        #Query to get patient details and associated tests
        query = """
        SELECT p.patient_id, GROUP_CONCAT(pt.test_id) AS test_ids, p.full_name, p.phone_number, p.gender, p.age
        FROM patients p
        LEFT JOIN patient_tests pt ON p.patient_id = pt.patient_id
        GROUP BY p.patient_id
        """
        
        cursor.execute(query)
        patients = cursor.fetchall()
        cursor.close()

        for patient in self.patient_table.get_children():
            self.patient_table.delete(patient)

        # Insert fetched patient data into the table (test_ids as concatenated string)
        for patient in patients:
            reordered_patient = (patient[0], patient[1] if patient[1] else 'None', patient[2], patient[3], patient[4], patient[5])
            self.patient_table.insert("", "end", values=reordered_patient)

    def load_tests(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT test_id, test_name, description FROM tests")
        tests = cursor.fetchall()
        cursor.close()

        for test in tests:
            self.tests_tree.insert("", "end", values=test)

    def on_test_select(self, event):
        selected_items = self.tests_tree.selection()
        if selected_items:
            item = selected_items[0]
            test_id = self.tests_tree.item(item)['values'][0]
            self.test_id_var.set(test_id)

        # Define the on_patient_select method
    def on_patient_select(self, event):
        selected_item = self.patient_table.selection()
        if selected_item:
                # Fetch the values from the selected row
            patient_data = self.patient_table.item(selected_item)['values']
            if patient_data:
                    # Set Patient ID and Test ID in the results frame
                self.patient_id_var.set(patient_data[0])
                self.test_id_var.set(patient_data[1] if patient_data[1] else '') 

    def calculate_age(self, event=None):
        birth_date = self.dob_entry.get_date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        self.age_var.set(str(age))

    def add_patient(self):
        phone = self.phone_entry.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get_date()
        age = self.age_var.get()
        address = self.address_entry.get()
        history = self.history_entry.get()

        if not all([phone, name, gender, dob, age, address]):
            messagebox.showerror("Error", "All fields except Medical History are required.")
            return

        selected_items = self.tests_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one test.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO patients (phone_number, full_name, gender, dob, age, address, medical_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (phone, name, gender, dob, age, address, history))

            patient_id = cursor.lastrowid

            for item in selected_items:
                test_id = self.tests_tree.item(item)['values'][0]
                cursor.execute("INSERT INTO patient_tests (patient_id, test_id) VALUES (%s, %s)", (patient_id, test_id))

            self.db.commit()
            self.patient_table.insert("", "end", values=(patient_id, name, phone, gender, age))
            messagebox.showinfo("Success", "Patient and tests added successfully.")
            self.clear_fields()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to add patient or tests: {str(e)}")
        finally:
            cursor.close()


    def modify_patient(self):
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number to modify a patient.")
            return

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
        patient = cursor.fetchone()

        if not patient:
            messagebox.showerror("Error", "Patient not found.")
            return

        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get_date()
        age = self.age_var.get()
        address = self.address_entry.get()
        history = self.history_entry.get()

        selected_items = self.tests_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one test.")
            return

        try:
            cursor.execute("""
                UPDATE patients 
                SET full_name = %s, gender = %s, dob = %s, age = %s, address = %s, medical_history = %s
                WHERE phone_number = %s
            """, (name, gender, dob, age, address, history, phone))

            # Update tests
            cursor.execute("DELETE FROM patient_tests WHERE patient_id = %s", (patient[0],))

            for item in selected_items:
                test_id = self.tests_tree.item(item)['values'][0]
                cursor.execute("INSERT INTO patient_tests (patient_id, test_id) VALUES (%s, %s)", (patient[0], test_id))

            self.db.commit()
            self.update_patient_table()
            messagebox.showinfo("Success", "Patient information updated successfully")
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
        finally:
            cursor.close()

    def view_patient(self):
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number to view a patient.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
            patient = cursor.fetchone()

            if not patient:
                messagebox.showerror("Error", "Patient not found.")
                return

            # Create a responsive dialog to display patient information
            dialog = Toplevel(self)
            dialog.title("Patient Information")
            dialog.geometry("400x400")  # default size 
            dialog.grab_set()  # making the dialog modal

            # labels and entries
            Label(dialog, text="Patient ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[0]).grid(row=0, column=1, sticky="w", padx=10, pady=5)

            Label(dialog, text="Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[2]).grid(row=1, column=1, sticky="w", padx=10, pady=5)

            Label(dialog, text="Gender:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[3]).grid(row=2, column=1, sticky="w", padx=10, pady=5)

            Label(dialog, text="Date of Birth:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[4]).grid(row=3, column=1, sticky="w", padx=10, pady=5)

            Label(dialog, text="Age:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[5]).grid(row=4, column=1, sticky="w", padx=10, pady=5)

            Label(dialog, text="Address:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[6]).grid(row=5, column=1, sticky="w", padx=10, pady=5)

            Label(dialog, text="History:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
            Label(dialog, text=patient[7]).grid(row=6, column=1, sticky="w", padx=10, pady=5)

            # Fetch and display patient's tests
            cursor.execute("""
                SELECT t.test_id, t.test_name 
                FROM patient_tests pt
                JOIN tests t ON pt.test_id = t.test_id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            tests = cursor.fetchall()

            # Add a section for displaying patient's tests
            Label(dialog, text="Tests to be carried out:", font=("Ubuntu", 12, "bold")).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

            for index, test in enumerate(tests, start=8):  # Start after patient details
                Label(dialog, text=f"Test {index-7}: {test[1]}").grid(row=index, column=0, columnspan=2, padx=10, pady=2)

            # Success message
            messagebox.showinfo("Success", "Patient information loaded successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient: {str(e)}")
        finally:
            cursor.close()

    def print_info(self):
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number to print patient information.")
            return

        cursor = self.db.cursor()
        try:
            # Fetch patient details
            cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
            patient = cursor.fetchone()

            if not patient:
                messagebox.showerror("Error", "Patient not found.")
                return

            # Fetch patient test results
            cursor.execute("""
                SELECT 
                    p.patient_id, p.full_name, p.phone_number, p.gender, p.dob, p.age, p.address, p.medical_history,
                    t.test_id, t.test_name, 
                    r.status, r.test_date, r.comments
                FROM 
                    patients p
                JOIN 
                    patient_tests pt ON p.patient_id = pt.patient_id
                JOIN 
                    tests t ON pt.test_id = t.test_id
                LEFT JOIN 
                    results r ON pt.patient_id = r.patient_id AND pt.test_id = r.test_id
                WHERE 
                    p.patient_id = %s
            """, (patient[0],))
            results = cursor.fetchall()

            # Construct the patient data dictionary
            patient_data = {
                "name": patient[1],  
                "phone": patient[2], 
                "gender": patient[3],
                "dob": patient[4],
                "age": patient[5],
                "address": patient[6],
                "medical_history": patient[7],
                "tests": [
                    {
                        "test_name": row[9],  # Test name
                        #"description": row[8],
                        "status": row[10] or "Pending",  # Test status
                        "test_date": row[11] or "N/A",  # Test date
                        "comments": row[12] or "N/A"  # Test comments
                    } for row in results
                ]
            }

            # Debug: Print patient_data to see the structures
            print("Patient Data:", patient_data)

            # Assuming ReportGenerate is a function that creates a PDF from the data
            pdf_file_path = ReportGenerate(patient_data)
            subprocess.call(['xdg-open', pdf_file_path])

            messagebox.showinfo("Success", "Patient information PDF has been generated and opened.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print patient information: {str(e)}")
        finally:
            cursor.close()

    def submit_result(self):
        patient_id = self.patient_id_var.get()
        test_id = self.test_id_var.get()
        result = self.result_var.get()
        description = self.result_entries["Description:"].get("1.0", tk.END).strip()
        test_date = self.result_entries["Date of Test:"].get_date()
        doctor_technician = self.result_entries["Doctor/Technician:"].get()
        comments = self.result_entries["Comments:"].get("1.0", tk.END).strip()

        # Validate that required fields are filled
        if not all([patient_id, test_id, result, description, test_date, doctor_technician]):
            messagebox.showerror("Error", "All fields except Comments are required.")
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO results (patient_id, test_id, status, description, test_date, doctor_technician, comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                status = VALUES(status),
                description = VALUES(description),
                test_date = VALUES(test_date),
                doctor_technician = VALUES(doctor_technician),
                comments = VALUES(comments)
            """, (patient_id, test_id, result, description, test_date, doctor_technician, comments))

            self.db.commit()
            messagebox.showinfo("Success", "Test result submitted successfully.")
            self.clear_result_fields()  # Clear fields after successful submission
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to submit test result: {str(e)}")
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
        self.tests_tree.selection_clear(0, tk.END)
        self.clear_result_fields()

    def clear_result_fields(self):
        self.patient_id_var.set("")
        self.test_id_var.set("")
        self.result_var.set("Select Result")
        self.result_entries["Description:"].delete("1.0", tk.END)
        self.result_entries["Comments:"].delete("1.0", tk.END)        
        self.result_entries["Date of Test:"].set_date(date.today())
        self.result_entries["Doctor/Technician:"].delete(0, tk.END)

    def update_patient_table(self):
        for item in self.patient_table.get_children():
            self.patient_table.delete(item)
        self.load_patients()

    def logout(self):
        self.logout_callback()