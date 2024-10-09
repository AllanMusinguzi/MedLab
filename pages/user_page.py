import tkinter as tk
from tkinter import ttk, messagebox
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

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('.', font=('Ubuntu', 11))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabelframe', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', background='#4a7abc', foreground='white')
        self.style.map('TButton', background=[('active', '#3a5a8c')])
        self.style.configure('Header.TLabel', font=('Ubuntu', 12, 'bold'))

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

        # Patient Table
        self.patient_table = ttk.Treeview(patient_frame, columns=("Patient ID","Test ID", "Name", "Phone", "Gender", "Age"), show="headings")
        self.patient_table.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.patient_table.heading("Patient ID", text="Patient ID")
        self.patient_table.heading("Test ID", text="Test ID")
        self.patient_table.heading("Name", text="Name")
        self.patient_table.heading("Phone", text="Phone")
        self.patient_table.heading("Gender", text="Gender")
        self.patient_table.heading("Age", text="Age")
        self.load_patients()

        # Binding selection event
        self.patient_table.bind("<<TreeviewSelect>>", self.on_patient_select)

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
        self.tests_tree = ttk.Treeview(self.tests_frame, columns=("ID", "Name", "Description"), show="headings")
        self.tests_tree.heading("ID", text="ID")
        self.tests_tree.heading("Name", text="Test Name")
        self.tests_tree.heading("Description", text="Description")
        self.tests_tree.grid(row=0, column=0, sticky="nsew")

        # Bind the selection event
        self.tests_tree.bind("<<TreeviewSelect>>", self.on_test_select)

        self.load_tests()

        # Results Frame
        self.results_frame = ttk.LabelFrame(tests_results_frame, text="Test Results", padding="10", style='TLabelframe', labelanchor="n")
        self.results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.results_frame.columnconfigure(1, weight=1)

        ttk.Label(self.results_frame, text="Patient ID:").grid(row=0, column=0, sticky="w")
        self.patient_id_var = tk.StringVar()
        self.patient_id_entry = ttk.Entry(self.results_frame, textvariable=self.patient_id_var, state="readonly")
        self.patient_id_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Test ID:").grid(row=1, column=0, sticky="w")
        self.test_id_var = tk.StringVar()
        self.test_id_entry = ttk.Entry(self.results_frame, textvariable=self.test_id_var, state="normal")
        self.test_id_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Result:").grid(row=2, column=0, sticky="w")
        self.result_var = tk.StringVar(value="Select Result")
        self.result_combobox = ttk.Combobox(self.results_frame, textvariable=self.result_var, values=["Positive", "Negative", "Normal", "Abnormal"], state="readonly")
        self.result_combobox.grid(row=2, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Description:").grid(row=3, column=0, sticky="w")
        self.description_text = tk.Text(self.results_frame, height=3, width=30)
        self.description_text.grid(row=3, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Date of Test:").grid(row=4, column=0, sticky="w")
        self.date_entry = DateEntry(self.results_frame, width=12, background='#4a7abc', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=4, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Doctor/Technician:").grid(row=5, column=0, sticky="w")
        self.doctor_entry = ttk.Entry(self.results_frame)
        self.doctor_entry.grid(row=5, column=1, sticky="ew")

        ttk.Label(self.results_frame, text="Comments:").grid(row=6, column=0, sticky="w")
        self.comments_text = tk.Text(self.results_frame, height=3, width=30)
        self.comments_text.grid(row=6, column=1, sticky="ew")

        ttk.Button(self.results_frame, text="Submit Result", command=self.submit_result).grid(row=7, column=0, columnspan=2, pady=(10, 0))

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

    def load_patients(self):
        cursor = self.db.cursor()

        # Modify the query to get patient details and associated tests
        query = """
        SELECT p.patient_id, GROUP_CONCAT(pt.test_id) AS test_ids, p.full_name, p.phone_number, p.gender, p.age
        FROM patients p
        LEFT JOIN patient_tests pt ON p.patient_id = pt.patient_id
        GROUP BY p.patient_id
        """
        
        cursor.execute(query)
        patients = cursor.fetchall()
        cursor.close()

        # Clear the table before loading new data
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
            # Get the selected item
        selected_item = self.patient_table.selection()
        if selected_item:
                # Fetch the values from the selected row
            patient_data = self.patient_table.item(selected_item)['values']
            if patient_data:
                    # Set Patient ID and Test ID in the results frame
                self.patient_id_var.set(patient_data[0])  # Patient ID is the first column
                self.test_id_var.set(patient_data[1] if patient_data[1] else '')  # Test ID is the second column

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

        selected_items = self.tests_tree.selection([0])
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

            self.patient_id_var.set(patient[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, patient[2])
            self.gender_var.set(patient[3])
            self.dob_entry.set_date(patient[4])
            self.age_var.set(patient[5])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, patient[6])
            self.history_entry.delete(0, tk.END)
            self.history_entry.insert(0, patient[7])

            # Fetch and display patient's tests
            cursor.execute("""
                SELECT t.test_id 
                FROM patient_tests pt
                JOIN tests t ON pt.test_id = t.test_id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            tests = [test[0] for test in cursor.fetchall()]

            # Clear previous selection and select patient's tests
            self.tests_tree.selection_clear(0, tk.END)
            for item in self.tests_tree.get_children():
                if self.tests_tree.item(item)['values'][0] in tests:
                    self.tests_tree.selection_add(item)

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
            cursor.execute("SELECT * FROM patients WHERE phone_number = %s", (phone,))
            patient = cursor.fetchone()

            if not patient:
                messagebox.showerror("Error", "Patient not found.")
                return

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

            patient_data = {
                "name": patient[2],
                "phone": patient[1],
                "gender": patient[3],
                "dob": patient[4],
                "age": patient[5],
                "address": patient[6],
                "medical_history": patient[7],
                "tests": [(row[9], (row[10] or "Pending", row[11] or "N/A", row[12] or "N/A")) for row in results]
            }

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
        description = self.description_text.get("1.0", tk.END).strip()
        test_date = self.date_entry.get_date()
        doctor_technician = self.doctor_entry.get()
        comments = self.comments_text.get("1.0", tk.END).strip()

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
            self.clear_result_fields()
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
        self.description_text.delete("1.0", tk.END)
        self.date_entry.set_date(date.today())
        self.doctor_entry.delete(0, tk.END)
        self.comments_text.delete("1.0", tk.END)

    def update_patient_table(self):
        for item in self.patient_table.get_children():
            self.patient_table.delete(item)
        self.load_patients()

    def logout(self):
        self.logout_callback()