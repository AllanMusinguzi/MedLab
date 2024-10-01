# user_page.py
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
        self.style.configure('.', font=('Ubuntu', 10))

        self.create_widgets()

    # ... (previous code for create_widgets and other methods remains the same)

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

        # Insert patient into database
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO patients (phone_number, full_name, gender, dob, age, address, medical_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (phone, name, gender, dob, age, address, history))
            
            patient_id = cursor.lastrowid

            # Add selected tests
            selected_tests = [self.tests_listbox.get(i) for i in self.tests_listbox.curselection()]
            for test in selected_tests:
                cursor.execute("SELECT id FROM tests WHERE test_name = %s", (test,))
                test_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO patient_tests (patient_id, test_id) VALUES (%s, %s)", (patient_id, test_id))

            self.db.commit()
            messagebox.showinfo("Success", "Patient added successfully")
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
            cursor.execute("DELETE FROM patient_tests WHERE patient_id = %s", (patient[0],))
            selected_tests = [self.tests_listbox.get(i) for i in self.tests_listbox.curselection()]
            for test in selected_tests:
                cursor.execute("SELECT id FROM tests WHERE test_name = %s", (test,))
                test_id = cursor.fetchone()[0]
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

            # Populate fields with patient data
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, patient[2])  # full_name
            self.gender_var.set(patient[3])  # gender
            self.dob_entry.set_date(patient[4])  # dob
            self.age_var.set(patient[5])  # age
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, patient[6])  # address
            self.history_entry.delete(0, tk.END)
            self.history_entry.insert(0, patient[7])  # medical_history

            # Fetch and select patient's tests
            cursor.execute("""
                SELECT t.test_name 
                FROM patient_tests pt
                JOIN tests t ON pt.test_id = t.id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            patient_tests = [test[0] for test in cursor.fetchall()]
            
            self.tests_listbox.selection_clear(0, tk.END)
            for i in range(self.tests_listbox.size()):
                if self.tests_listbox.get(i) in patient_tests:
                    self.tests_listbox.selection_set(i)

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
                FROM patient_tests pt
                JOIN tests t ON pt.test_id = t.id
                WHERE pt.patient_id = %s
            """, (patient[0],))
            patient_tests = [test[0] for test in cursor.fetchall()]

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
                for test in patient_tests:
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
        self.tests_listbox.selection_clear(0, tk.END)
        self.results_text.delete('1.0', tk.END)