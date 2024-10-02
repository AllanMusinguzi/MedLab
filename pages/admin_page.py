import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as font

class AdminPage(tk.Frame):
    def __init__(self, master, db, user_id, username, password, phone_number, logout_callback):
        super().__init__(master)
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.logout_callback = logout_callback

        self.custom_font = font.Font(size=10, family='Ubuntu', font='bold')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', font=('Ubuntu', 12))
        self.style.configure('Custom.TButton', font=self.custom_font)  

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
        admin_frame = ttk.LabelFrame(parent, text="Admin Profile", padding="10", labelanchor="n")
        admin_frame.columnconfigure(0, weight=1)

        # Update to ensure proper layout of admin info
        ttk.Label(admin_frame, text=f"Admin Name: {self.username}").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(admin_frame, text=f"User ID: {self.user_id}").grid(row=2, column=0, sticky=tk.W, pady=2)

        # Button with reduced size and custom font style
        ttk.Button(admin_frame, text="Logout", command=self.logout_callback, width=10, style="Custom.TButton").grid(row=0, column=0, sticky=tk.NE, pady=0)

        return admin_frame

    # User Management
    def create_user_management_frame(self, parent):
        user_frame = ttk.LabelFrame(parent, text="User Management", padding="10", labelanchor="n")
        user_frame.columnconfigure(0, weight=1)
        user_frame.rowconfigure(0, weight=1)

        # Create a Treeview widget for displaying users in a table format
        self.user_tree = ttk.Treeview(user_frame, columns=("ID", "Username", "Type"), show="headings", height=8)
        self.user_tree.heading("ID", text="User ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Type", text="User Type")

        # Define column widths
        self.user_tree.column("ID", width=100)
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Type", width=100)

        # Row and column separators (gridlines)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"), background="#f0f0f0")
        style.configure("Treeview", rowheight=25, font=("Ubuntu", 9), background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#3c3839")])

        # Use a tag to add alternating row colors for visibility
        self.user_tree.tag_configure('oddrow', background="lightgray")
        self.user_tree.tag_configure('evenrow', background="white")

        # Pack the Treeview widget
        self.user_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Add scrollbars
        user_scrollbar_y = ttk.Scrollbar(user_frame, orient="vertical", command=self.user_tree.yview)
        user_scrollbar_x = ttk.Scrollbar(user_frame, orient="horizontal", command=self.user_tree.xview)
        self.user_tree.configure(yscroll=user_scrollbar_y.set, xscroll=user_scrollbar_x.set)
        user_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        user_scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))

        self.load_users()  # Load users into the table

        user_buttons = ttk.Frame(user_frame)
        user_buttons.grid(row=1, column=0, sticky=(tk.E, tk.W), pady=2.5)
        ttk.Button(user_buttons, text="Add", command=self.add_user, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(user_buttons, text="Modify", command=self.modify_user, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(user_buttons, text="Delete", command=self.delete_user, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)

        return user_frame

    def load_users(self):
        # Clear the treeview
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        # Verify if the current user is an admin
        cursor = self.db.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE username = %s", (self.username,))
        is_admin = cursor.fetchone()

        if is_admin and is_admin[0]:  
            try:
                # Load all users
                cursor.execute("SELECT user_id, username, is_admin FROM users")
                count = 0  # Counter for alternating color
                for user in cursor.fetchall():
                    user_type = "Admin" if user[2] else "User"
                    tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                    self.user_tree.insert("", tk.END, values=(user[0], user[1], user_type), tags=(tag,))
                    count += 1
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
        selection = self.user_tree.selection()
        if selection:
            # Get the selected user ID from the treeview
            user_id = self.user_tree.item(selection)['values'][0]  # Assuming the first column is user ID

            # Prompt for new username and password
            new_username = simpledialog.askstring("Modify User", "Enter new username (or leave blank):")
            new_password = simpledialog.askstring("Modify User", "Enter new password (or leave blank):", show='*')
            is_admin = messagebox.askyesno("Modify User", "Is this user an admin?")

            # Prepare the update query and parameters
            update_fields = []
            values = []
            if new_username:
                update_fields.append("username = %s")
                values.append(new_username)
            if new_password:
                update_fields.append("password = %s")
                values.append(new_password)

            # Always append is_admin field
            update_fields.append("is_admin = %s")
            values.append(is_admin)

            # Append user_id as the last parameter for the query
            values.append(user_id)

            # Execute the update only if there are fields to update
            if update_fields:
                cursor = self.db.cursor()
                try:
                    cursor.execute(f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s", tuple(values))
                    self.db.commit()
                    messagebox.showinfo("Success", "User modified successfully")
                    self.load_users()  # Reload the users to reflect changes
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to modify user: {str(e)}")
                finally:
                    cursor.close()
            else:
                messagebox.showinfo("No Changes", "No fields were modified.")
        else:
            messagebox.showwarning("Selection Required", "Please select a user to modify.")

    def delete_user(self):
        selection = self.user_tree.selection()
        if selection:
            # Get the selected user ID from the treeview
            user_id = self.user_tree.item(selection)['values'][0]  # Assuming the first column is user ID

            if messagebox.askyesno("Delete User", "Are you sure you want to delete this user?"):
                cursor = self.db.cursor()
                try:
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "User deleted successfully")
                    self.load_users()  # Reload the users to reflect changes
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
                finally:
                    cursor.close()
        else:
            messagebox.showwarning("Selection Required", "Please select a user to delete.")

    # Test Management
    def create_test_management_frame(self, parent):
        test_frame = ttk.LabelFrame(parent, text="Test Management", padding="10", labelanchor="n")
        test_frame.columnconfigure(0, weight=1)
        test_frame.rowconfigure(0, weight=1)

        # Create a Treeview widget for displaying tests in a table format
        self.test_tree = ttk.Treeview(test_frame, columns=("ID", "Test Name"), show="headings", height=8)
        self.test_tree.heading("ID", text="Test ID")
        self.test_tree.heading("Test Name", text="Test Name")
        
        # Define column widths
        self.test_tree.column("ID", width=100)
        self.test_tree.column("Test Name", width=200)
        
        # Add row and column separators (gridlines) with styling
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"), background="#f0f0f0")
        style.configure("Treeview", rowheight=25, font=("Ubuntu", 9), background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#3c3839")])

        # Use a tag to add alternating row colors for visibility
        self.test_tree.tag_configure('oddrow', background="lightgray")
        self.test_tree.tag_configure('evenrow', background="white")

        # Pack the Treeview widget
        self.test_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Add scrollbars
        test_scrollbar_y = ttk.Scrollbar(test_frame, orient="vertical", command=self.test_tree.yview)
        test_scrollbar_x = ttk.Scrollbar(test_frame, orient="horizontal", command=self.test_tree.xview)
        self.test_tree.configure(yscroll=test_scrollbar_y.set, xscroll=test_scrollbar_x.set)
        test_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        test_scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))

        # Add buttons for test management
        test_buttons = ttk.Frame(test_frame)
        test_buttons.grid(row=2, column=0, sticky=(tk.E, tk.W), pady=2.5)
        ttk.Button(test_buttons, text="Add", command=self.add_test, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(test_buttons, text="Modify", command=self.modify_test, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(test_buttons, text="Delete", command=self.delete_test, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)

        # Load tests into the table
        self.load_tests()

        return test_frame

    def load_tests(self):
        # Clear the treeview
        for row in self.test_tree.get_children():
            self.test_tree.delete(row)
        
        # Load all tests from the database
        cursor = self.db.cursor()
        cursor.execute("SELECT test_id, test_name FROM tests")
        count = 0  # Counter to track row for alternating color
        for test in cursor.fetchall():
            if count % 2 == 0:
                self.test_tree.insert("", tk.END, values=(test[0], test[1]), tags=('evenrow',))
            else:
                self.test_tree.insert("", tk.END, values=(test[0], test[1]), tags=('oddrow',))
            count += 1
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
            # Get the selected test ID from the listbox
            test_id = int(self.test_listbox.get(selection[0]).split(':')[0])
            
            # Prompt for the new test name
            new_test_name = simpledialog.askstring("Modify Test", "Enter new test name:")
            
            if new_test_name:
                cursor = self.db.cursor()
                try:
                    # Update the test name in the database
                    cursor.execute("UPDATE tests SET test_name = %s WHERE test_id = %s", (new_test_name, test_id))
                    self.db.commit()
                    messagebox.showinfo("Success", "Test modified successfully")
                    self.load_tests()  # Reload tests to reflect changes
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to modify test: {str(e)}")
                finally:
                    cursor.close()
        else:
            messagebox.showwarning("Selection Required", "Please select a test to modify.")

    def delete_test(self):
        selection = self.test_listbox.curselection()
        if selection:
            # Get the selected test ID from the listbox
            test_id = int(self.test_listbox.get(selection[0]).split(':')[0])
            
            if messagebox.askyesno("Delete Test", "Are you sure you want to delete this test?"):
                cursor = self.db.cursor()
                try:
                    # Delete the test from the database
                    cursor.execute("DELETE FROM tests WHERE test_id = %s", (test_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "Test deleted successfully")
                    self.load_tests()  # Reload tests to reflect changes
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete test: {str(e)}")
                finally:
                    cursor.close()
        else:
            messagebox.showwarning("Selection Required", "Please select a test to delete.")


        
    # Patient Management
    def create_patient_management_frame(self, parent):
        patient_frame = ttk.LabelFrame(parent, text="Patient Management", padding="10", labelanchor="n")
        patient_frame.columnconfigure(0, weight=1)
        patient_frame.rowconfigure(0, weight=1)

        # Create a Treeview widget for displaying patients in a table format with all fields
        self.patient_tree = ttk.Treeview(patient_frame, columns=("ID", "Name", "Phone", "Gender", "DOB", "Age", "Address", "Medical History"), show="headings", height=8)
        
        # Define the headings for all columns
        self.patient_tree.heading("ID", text="Patient ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Phone", text="Phone")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("DOB", text="DOB")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Address", text="Address")
        self.patient_tree.heading("Medical History", text="Medical History")
        
        # Define column widths
        self.patient_tree.column("ID", width=80)
        self.patient_tree.column("Name", width=150)
        self.patient_tree.column("Phone", width=100)
        self.patient_tree.column("Gender", width=80)
        self.patient_tree.column("DOB", width=100)
        self.patient_tree.column("Age", width=50)
        self.patient_tree.column("Address", width=200)
        self.patient_tree.column("Medical History", width=250)
        
        # Add row and column separators (gridlines) with styling
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"), background="#f0f0f0")
        style.configure("Treeview", rowheight=25, font=("Ubuntu", 9), background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#3c3839")])

        # Use a tag to add alternating row colors for visibility
        self.patient_tree.tag_configure('oddrow', background="lightgray")
        self.patient_tree.tag_configure('evenrow', background="white")

        # Pack the Treeview widget
        self.patient_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Add scrollbars
        patient_scrollbar_y = ttk.Scrollbar(patient_frame, orient="vertical", command=self.patient_tree.yview)
        patient_scrollbar_x = ttk.Scrollbar(patient_frame, orient="horizontal", command=self.patient_tree.xview)
        self.patient_tree.configure(yscroll=patient_scrollbar_y.set, xscroll=patient_scrollbar_x.set)
        patient_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        patient_scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))

        # Add buttons for patient management
        patient_buttons = ttk.Frame(patient_frame)
        patient_buttons.grid(row=2, column=0, sticky=(tk.E, tk.W), pady=2.5)
        ttk.Button(patient_buttons, text="View", command=self.view_patient, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(patient_buttons, text="Delete", command=self.delete_patient, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)

        # Load patients into the table
        self.load_patients()

        return patient_frame

    def load_patients(self):
        # Clear the treeview
        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)
        
        # Load all patients from the database
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT patient_id, full_name, phone_number, gender, dob, age, address, medical_history 
            FROM patients
        """)
        count = 0  # Counter to track row for alternating color
        for patient in cursor.fetchall():
            # Insert patient data into the treeview with alternating row colors
            if count % 2 == 0:
                self.patient_tree.insert("", tk.END, values=(
                    patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7]
                ), tags=('evenrow',))
            else:
                self.patient_tree.insert("", tk.END, values=(
                    patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7]
                ), tags=('oddrow',))
            count += 1
        cursor.close()


    def view_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            # Get the selected patient ID from the listbox
            patient_id = int(self.patient_listbox.get(selection[0]).split(':')[0])
            
            cursor = self.db.cursor()
            try:
                # Fetch the patient details from the database
                cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
                patient = cursor.fetchone()
                
                if patient:
                    # Create a detailed information string for the patient
                    info = f"Patient_ID: {patient[0]}\n"
                    info += f"Name: {patient[1]}\n"
                    info += f"Phone: {patient[2]}\n"
                    info += f"Gender: {patient[3]}\n"
                    info += f"DOB: {patient[4]}\n"
                    info += f"Age: {patient[5]}\n"
                    info += f"Address: {patient[6]}\n"
                    info += f"Medical History: {patient[7]}"
                    # Show patient information in a message box
                    messagebox.showinfo("Patient Information", info)
                else:
                    messagebox.showinfo("Not Found", "Patient not found")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to view patient: {str(e)}")
            finally:
                cursor.close()
        else:
            messagebox.showwarning("Selection Required", "Please select a patient to view.")

    def delete_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            # Get the selected patient ID from the listbox
            patient_id = int(self.patient_listbox.get(selection[0]).split(':')[0])
            
            if messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient?"):
                cursor = self.db.cursor()
                try:
                    # Delete the patient from the database
                    cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "Patient deleted successfully")
                    self.load_patients()  # Reload the list of patients
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
                finally:
                    cursor.close()
        else:
            messagebox.showwarning("Selection Required", "Please select a patient to delete.")
