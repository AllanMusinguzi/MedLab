import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

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

        # Enable scrolling if needed
        scrollbar = ttk.Scrollbar(self.tests_frame, orient="vertical", command=self.tests_tree.yview)
        self.tests_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

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

        ttk.Button(self.results_frame, text="Submit Result", command=self.submit_result).grid(row=6, column=0, columnspan=2, pady=(10, 0))

    def calculate_age(self, event):
        dob = self.dob_entry.get_date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        self.age_var.set(age)

    def load_tests(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, name, price FROM tests")
            for row in cursor.fetchall():
                self.tests_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tests: {e}")

    def on_test_select(self, event):
        selected_item = self.tests_tree.selection()
        if selected_item:
            item = self.tests_tree.item(selected_item)
            test_id = item['values'][0]
            self.test_id_var.set(test_id)

    def add_patient(self):
        phone = self.phone_entry.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get()
        age = self.age_var.get()
        address = self.address_entry.get()
        history = self.history_entry.get()

        if not (phone and name and gender and dob and age and address):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO patients (phone_number, full_name, gender, date_of_birth, age, address, medical_history)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (phone, name, gender, dob, age, address, history))
            self.db.commit()
            messagebox.showinfo("Success", "Patient added successfully.")
            self.clear_patient_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient: {e}")

    def modify_patient(self):
        # Implement modification logic here
        pass

    def view_patient(self):
        # Implement viewing logic here
        pass

    def print_info(self):
        # Implement printing logic here
        pass

    def submit_result(self):
        test_id = self.test_id_var.get()
        patient_id = self.patient_id_var.get()
        result = self.result_var.get()
        description = self.description_text.get("1.0", tk.END).strip()
        date_of_test = self.date_entry.get_date()
        doctor = self.doctor_entry.get()

        if not (test_id and patient_id and result and date_of_test and doctor):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO test_results (test_id, patient_id, result, description, date_of_test, doctor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (test_id, patient_id, result, description, date_of_test, doctor))
            self.db.commit()
            messagebox.showinfo("Success", "Test result submitted successfully.")
            self.clear_result_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit test result: {e}")

    def clear_patient_entries(self):
        self.phone_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.dob_entry.set_date(date.today())
        self.age_var.set("")
        self.address_entry.delete(0, tk.END)
        self.history_entry.delete(0, tk.END)

    def clear_result_entries(self):
        self.test_id_var.set("")
        self.patient_id_var.set("")
        self.result_var.set("Select Result")
        self.description_text.delete("1.0", tk.END)
        self.date_entry.set_date(date.today())
        self.doctor_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserPage(root, user_id=1, logout_callback=root.quit)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
