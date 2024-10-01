# admin_page.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class AdminPage(ttk.Frame):
    def __init__(self, master, db, admin_id, logout_callback):
        super().__init__(master)
        self.db = db
        self.admin_id = admin_id
        self.logout_callback = logout_callback

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', font=('Ubuntu', 10))

        self.create_widgets()

    # ... (previous code remains the same)

    def load_users(self):
        self.user_listbox.delete(0, tk.END)
        cursor = self.db.cursor()
        cursor.execute("SELECT id, username, is_admin FROM users")
        for user in cursor.fetchall():
            user_type = "Admin" if user[2] else "User"
            self.user_listbox.insert(tk.END, f"{user[0]}: {user[1]} ({user_type})")
        cursor.close()

    def add_user(self):
        username = simpledialog.askstring("Add User", "Enter username:")
        if username:
            password = simpledialog.askstring("Add User", "Enter password:", show='*')
            if password:
                is_admin = messagebox.askyesno("Add User", "Is this user an admin?")
                cursor = self.db.cursor()
                try:
                    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)",
                                   (username, password, is_admin))
                    self.db.commit()
                    messagebox.showinfo("Success", "User added successfully")
                    self.load_users()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add user: {str(e)}")
                finally:
                    cursor.close()

    def modify_user(self):
        selection = self.user_listbox.curselection()
        if selection:
            user_id = int(self.user_listbox.get(selection[0]).split(':')[0])
            new_username = simpledialog.askstring("Modify User", "Enter new username (or leave blank):")
            new_password = simpledialog.askstring("Modify User", "Enter new password (or leave blank):", show='*')
            is_admin = messagebox.askyesno("Modify User", "Is this user an admin?")

            update_fields = []
            values = []
            if new_username:
                update_fields.append("username = %s")
                values.append(new_username)
            if new_password:
                update_fields.append("password = %s")
                values.append(new_password)
            update_fields.append("is_admin = %s")
            values.append(is_admin)
            values.append(user_id)

            cursor = self.db.cursor()
            try:
                cursor.execute(f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s", tuple(values))
                self.db.commit()
                messagebox.showinfo("Success", "User modified successfully")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to modify user: {str(e)}")
            finally:
                cursor.close()

    def delete_user(self):
        selection = self.user_listbox.curselection()
        if selection:
            user_id = int(self.user_listbox.get(selection[0]).split(':')[0])
            if messagebox.askyesno("Delete User", "Are you sure you want to delete this user?"):
                cursor = self.db.cursor()
                try:
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "User deleted successfully")
                    self.load_users()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
                finally:
                    cursor.close()

    def load_tests(self):
        self.test_listbox.delete(0, tk.END)
        cursor = self.db.cursor()
        cursor.execute("SELECT id, test_name FROM tests")
        for test in cursor.fetchall():
            self.test_listbox.insert(tk.END, f"{test[0]}: {test[1]}")
        cursor.close()

    def add_test(self):
        test_name = simpledialog.askstring("Add Test", "Enter test name:")
        if test_name:
            cursor = self.db.cursor()
            try:
                cursor.execute("INSERT INTO tests (test_name) VALUES (%s)", (test_name,))
                self.db.commit()
                messagebox.showinfo("Success", "Test added successfully")
                self.load_tests()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add test: {str(e)}")
            finally:
                cursor.close()

    def modify_test(self):
        selection = self.test_listbox.curselection()
        if selection:
            test_id = int(self.test_listbox.get(selection[0]).split(':')[0])
            new_test_name = simpledialog.askstring("Modify Test", "Enter new test name:")
            if new_test_name:
                cursor = self.db.cursor()
                try:
                    cursor.execute("UPDATE tests SET test_name = %s WHERE id = %s", (new_test_name, test_id))
                    self.db.commit()
                    messagebox.showinfo("Success", "Test modified successfully")
                    self.load_tests()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to modify test: {str(e)}")
                finally:
                    cursor.close()

    def delete_test(self):
        selection = self.test_listbox.curselection()
        if selection:
            test_id = int(self.test_listbox.get(selection[0]).split(':')[0])
            if messagebox.askyesno("Delete Test", "Are you sure you want to delete this test?"):
                cursor = self.db.cursor()
                try:
                    cursor.execute("DELETE FROM tests WHERE id = %s", (test_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "Test deleted successfully")
                    self.load_tests()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete test: {str(e)}")
                finally:
                    cursor.close()

    def load_patients(self):
        self.patient_listbox.delete(0, tk.END)
        cursor = self.db.cursor()
        cursor.execute("SELECT id, full_name, phone_number FROM patients")
        for patient in cursor.fetchall():
            self.patient_listbox.insert(tk.END, f"{patient[0]}: {patient[1]} ({patient[2]})")
        cursor.close()

    def view_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            patient_id = int(self.patient_listbox.get(selection[0]).split(':')[0])
            cursor = self.db.cursor()
            try:
                cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
                patient = cursor.fetchone()
                if patient:
                    info = f"ID: {patient[0]}\n"
                    info += f"Name: {patient[1]}\n"
                    info += f"Phone: {patient[2]}\n"
                    info += f"Gender: {patient[3]}\n"
                    info += f"DOB: {patient[4]}\n"
                    info += f"Age: {patient[5]}\n"
                    info += f"Address: {patient[6]}\n"
                    info += f"Medical History: {patient[7]}"
                    messagebox.showinfo("Patient Information", info)
                else:
                    messagebox.showinfo("Not Found", "Patient not found")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to view patient: {str(e)}")
            finally:
                cursor.close()

    def delete_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            patient_id = int(self.patient_listbox.get(selection[0]).split(':')[0])
            if messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient and all their records?"):
                cursor = self.db.cursor()
                try:
                    cursor.execute("DELETE FROM patient_tests WHERE patient_id = %s", (patient_id,))
                    cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "Patient and their records deleted successfully")
                    self.load_patients()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
                finally:
                    cursor.close()