import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class AdminPage(tk.Frame):
    def __init__(self, master, db, user_id, username, password, logout_callback):
        super().__init__(master)
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.logout_callback = logout_callback

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', font=('Ubuntu', 12))

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Admin Profile Frame
        self.admin_frame = self.create_admin_profile_frame(main_frame)
        self.admin_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # User Management Frame
        self.user_frame = self.create_user_management_frame(main_frame)
        self.user_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=(0, 5), pady=10)

        # Test Management Frame
        self.test_frame = self.create_test_management_frame(main_frame)
        self.test_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=(5, 0), pady=10)

        # Patient Management Frame
        self.patient_frame = self.create_patient_management_frame(main_frame)
        self.patient_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=2)

    def create_admin_profile_frame(self, parent):
        admin_frame = ttk.LabelFrame(parent, text="Admin Profile", padding="10")
        ttk.Label(admin_frame, text=f"Admin Name: {self.username}").pack(anchor=tk.W)
        ttk.Label(admin_frame, text="Other Details").pack(anchor=tk.W)
        ttk.Button(admin_frame, text="Logout", command=self.logout_callback).pack(anchor=tk.E, pady=5)
        return admin_frame

    def create_user_management_frame(self, parent):
        user_frame = ttk.LabelFrame(parent, text="User Management", padding="10")
        
        self.user_listbox = tk.Listbox(user_frame)
        self.user_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_users()

        user_buttons = ttk.Frame(user_frame)
        user_buttons.pack(fill=tk.X, pady=5)
        ttk.Button(user_buttons, text="Add User", command=self.add_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(user_buttons, text="Modify User", command=self.modify_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(user_buttons, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)

        return user_frame

    def create_test_management_frame(self, parent):
        test_frame = ttk.LabelFrame(parent, text="Test Management", padding="10")

        self.test_listbox = tk.Listbox(test_frame)
        self.test_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_tests()

        test_buttons = ttk.Frame(test_frame)
        test_buttons.pack(fill=tk.X, pady=5)
        ttk.Button(test_buttons, text="Add Test", command=self.add_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_buttons, text="Modify Test", command=self.modify_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_buttons, text="Delete Test", command=self.delete_test).pack(side=tk.LEFT, padx=5)

        return test_frame

    def create_patient_management_frame(self, parent):
        patient_frame = ttk.LabelFrame(parent, text="Patient Management", padding="10")

        self.patient_listbox = tk.Listbox(patient_frame)
        self.patient_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_patients()

        patient_buttons = ttk.Frame(patient_frame)
        patient_buttons.pack(fill=tk.X, pady=5)
        ttk.Button(patient_buttons, text="View Patient", command=self.view_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(patient_buttons, text="Delete Patient", command=self.delete_patient).pack(side=tk.LEFT, padx=5)

        return patient_frame

    def load_users(self):
        # Clear the listbox
        self.user_listbox.delete(0, tk.END)
        
        # Verify if the current user is an admin
        cursor = self.db.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE username = %s", (self.username,))
        is_admin = cursor.fetchone()

        if is_admin and is_admin[0]:  # Only if the current user is an admin
            try:
                # Load all users (not filtered by username/password)
                cursor.execute("SELECT user_id, username, is_admin FROM users")
                for user in cursor.fetchall():
                    user_type = "Admin" if user[2] else "User"
                    self.user_listbox.insert(tk.END, f"{user[0]}: {user[1]} ({user_type})")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load users: {str(e)}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Error", "You are not authorized to view this information.")

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
                cursor.execute(f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s", tuple(values))
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
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
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
        cursor.execute("SELECT test_id, test_name FROM tests")
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
                    cursor.execute("UPDATE tests SET test_name = %s WHERE test_id = %s", (new_test_name, test_id))
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
                    cursor.execute("DELETE FROM tests WHERE test_id = %s", (test_id,))
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
        cursor.execute("SELECT patient_id, full_name FROM patients")
        for patient in cursor.fetchall():
            self.patient_listbox.insert(tk.END, f"{patient[0]}: {patient[1]}")
        cursor.close()

    def view_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            patient_id = int(self.patient_listbox.get(selection[0]).split(':')[0])
            cursor = self.db.cursor()
            try:
                cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
                patient = cursor.fetchone()
                if patient:
                    info = f"Patient_ID: {patient[0]}\n"
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
            if messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient?"):
                cursor = self.db.cursor()
                try:
                    cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "Patient deleted successfully")
                    self.load_patients()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
                finally:
                    cursor.close()
