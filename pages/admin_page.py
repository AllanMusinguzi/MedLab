import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as font
import bcrypt

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

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=2)

    def create_admin_profile_frame(self, parent):
        admin_frame = ttk.LabelFrame(parent, text="Admin Profile", padding="10", labelanchor="n")
        admin_frame.columnconfigure(0, weight=1)

        ttk.Label(admin_frame, text=f"Admin Name: {self.username}").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(admin_frame, text=f"User ID: {self.user_id}").grid(row=2, column=0, sticky=tk.W, pady=2)

        ttk.Button(admin_frame, text="Logout", command=self.logout_callback, width=10, style="Custom.TButton").grid(row=0, column=0, sticky=tk.NE, pady=0)

        return admin_frame

    # User Management
    def create_user_management_frame(self, parent):
        user_frame = ttk.LabelFrame(parent, text="User Management", padding="10", labelanchor="n")
        user_frame.columnconfigure(0, weight=1)
        user_frame.rowconfigure(0, weight=1)

        self.user_tree = ttk.Treeview(user_frame, columns=("ID", "Username", "Type"), show="headings", height=8)
        self.user_tree.heading("ID", text="User ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Type", text="User Type")

        self.user_tree.column("ID", width=100)
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Type", width=100)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"), background="#f0f0f0")
        style.configure("Treeview", rowheight=25, font=("Ubuntu", 9), background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#3c3839")])

        self.user_tree.tag_configure('oddrow', background="lightgray")
        self.user_tree.tag_configure('evenrow', background="white")

        self.user_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        user_scrollbar_y = ttk.Scrollbar(user_frame, orient="vertical", command=self.user_tree.yview)
        user_scrollbar_x = ttk.Scrollbar(user_frame, orient="horizontal", command=self.user_tree.xview)
        self.user_tree.configure(yscroll=user_scrollbar_y.set, xscroll=user_scrollbar_x.set)
        user_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        user_scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))

        self.load_users()  

        user_buttons = ttk.Frame(user_frame)
        user_buttons.grid(row=1, column=0, sticky=(tk.E, tk.W), pady=2.5)
        ttk.Button(user_buttons, text="Add", command=self.add_user, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(user_buttons, text="Modify", command=self.modify_user, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(user_buttons, text="Delete", command=self.delete_user, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)

        return user_frame

    def load_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        cursor = self.db.cursor()
        cursor.execute("SELECT role FROM users WHERE username = %s", (self.username,))
        role = cursor.fetchone()

        if role and role[0]:  
            try:
                cursor.execute("SELECT user_id, username, role FROM users")
                count = 0 
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
                role = messagebox.askyesno("Add User", "Is this user an admin?")
                
                # Hash the password with bcrypt
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                cursor = self.db.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username, hashed_password.decode('utf-8'), role)
                    )
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
            user_id = self.user_tree.item(selection)['values'][0]

            new_username = simpledialog.askstring("Modify User", "Enter new username (or leave blank):")
            new_password = simpledialog.askstring("Modify User", "Enter new password (or leave blank):", show='*')
            role = messagebox.askyesno("Modify User", "Is this user an admin?")

            update_fields = []
            values = []

            if new_username:
                update_fields.append("username = %s")
                values.append(new_username)
            if new_password:
                # Hash the new password with bcrypt
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                update_fields.append("password = %s")
                values.append(hashed_password.decode('utf-8'))

            update_fields.append("role = %s")
            values.append(role)
            
            values.append(user_id)

            if update_fields:
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
            else:
                messagebox.showinfo("No Changes", "No fields were modified.")
        else:
            messagebox.showwarning("Selection Required", "Please select a user to modify.")


    def delete_user(self):
        selection = self.user_tree.selection()
        if selection:
            user_id = self.user_tree.item(selection)['values'][0] 

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
        else:
            messagebox.showwarning("Selection Required", "Please select a user to delete.")


    #Test Management
    def create_test_management_frame(self, parent):
        test_frame = ttk.LabelFrame(parent, text="Test Management", padding="10", labelanchor="n")
        test_frame.columnconfigure(0, weight=1)
        test_frame.rowconfigure(0, weight=1)

        # Status bar
        self.status_bar = ttk.Label(test_frame, text="No items selected", relief=tk.SUNKEN, padding=(5, 2))
        
        # Create Treeview
        self.test_tree = ttk.Treeview(test_frame, columns=("ID", "Test Name", "Description"), show="headings", height=8)
        self.test_tree.heading("ID", text="Test ID")
        self.test_tree.heading("Test Name", text="Test Name")
        self.test_tree.heading("Description", text="Description")
        
        self.test_tree.column("ID", width=50)
        self.test_tree.column("Test Name", width=100)
        self.test_tree.column("Description", width=300)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"), background="#f0f0f0")
        style.configure("Treeview", rowheight=25, font=("Ubuntu", 9), background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#3c3839")])

        self.test_tree.tag_configure('oddrow', background="lightgray")
        self.test_tree.tag_configure('evenrow', background="white")

        # Create toolbar with selection buttons
        toolbar = ttk.Frame(test_frame)
        toolbar.grid(row=2, column=0, sticky=(tk.E, tk.W), pady=2.5)
        
        ttk.Button(toolbar, text="Add", command=self.add_test, width=10,
                style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(toolbar, text="Modify", command=self.modify_test, width=10,
                style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(toolbar, text="Select All", command=self.select_all_tests, width=10, 
                style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(toolbar, text="Deselect All", command=self.deselect_all_tests, width=10,
                style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(toolbar, text="Delete", command=self.delete_test, width=10,
                style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)

        # Layout
        self.test_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        test_scrollbar_y = ttk.Scrollbar(test_frame, orient="vertical", command=self.test_tree.yview)
        test_scrollbar_x = ttk.Scrollbar(test_frame, orient="horizontal", command=self.test_tree.xview)
        self.test_tree.configure(yscroll=test_scrollbar_y.set, xscroll=test_scrollbar_x.set)
        test_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        test_scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))
        
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.E, tk.W), pady=(5, 0))

        # Create and bind context menu
        self.create_context_menu()
        
        # Bind events
        self.bind_events()
        
        # Load initial data
        self.load_tests()

        return test_frame

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.test_tree, tearoff=0)
        self.context_menu.add_command(label="Add Test", command=self.add_test)
        self.context_menu.add_command(label="Modify Selected", command=self.modify_test)
        self.context_menu.add_command(label="Delete Selected", command=self.delete_test)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all_tests)
        self.context_menu.add_command(label="Deselect All", command=self.deselect_all_tests)

    def bind_events(self):
        # Bind keyboard shortcuts
        self.test_tree.bind('<Delete>', lambda e: self.delete_test())
        self.test_tree.bind('<Control-a>', lambda e: self.select_all_tests())
        self.test_tree.bind('<Control-A>', lambda e: self.select_all_tests())
        self.test_tree.bind('<Escape>', lambda e: self.deselect_all_tests())
        
        # Bind context menu
        self.test_tree.bind('<Button-3>', self.show_context_menu)
        
        # Bind selection event for status bar update
        self.test_tree.bind('<<TreeviewSelect>>', self.update_status_bar)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def update_status_bar(self, event=None):
        selections = len(self.test_tree.selection())
        if selections == 0:
            self.status_bar.config(text="No items selected")
        elif selections == 1:
            self.status_bar.config(text="1 item selected")
        else:
            self.status_bar.config(text=f"{selections} items selected")

    def select_all_tests(self):
        self.test_tree.selection_set(self.test_tree.get_children())
        self.update_status_bar()

    def deselect_all_tests(self):
        self.test_tree.selection_remove(self.test_tree.get_children())
        self.update_status_bar()

    # Update load_tests to include status bar update
    def load_tests(self):
        for row in self.test_tree.get_children():
            self.test_tree.delete(row)
        
        cursor = self.db.cursor()
        cursor.execute("SELECT test_id, test_name, description FROM tests")
        count = 0 
        for test in cursor.fetchall():
            if count % 2 == 0:
                self.test_tree.insert("", tk.END, values=(test[0], test[1], test[2]), tags=('evenrow',))
            else:
                self.test_tree.insert("", tk.END, values=(test[0], test[1], test[2]), tags=('oddrow',))
            count += 1
        cursor.close()
        self.update_status_bar()

    def add_test(self):
        test_name = simpledialog.askstring("Add Test", "Enter test name:")
        description = simpledialog.askstring("Add Description", "Enter test description:")
        if test_name and description:
            cursor = self.db.cursor()
            try:
                cursor.execute("INSERT INTO tests (test_name, description) VALUES (%s, %s)", (test_name, description,))
                self.db.commit()
                messagebox.showinfo("Success", "Test added successfully")
                self.load_tests()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add test: {str(e)}")
            finally:
                cursor.close()

    def modify_test(self):
        selection = self.test_tree.selection()
        if selection:
            item_values = self.test_tree.item(selection[0])['values']
            test_id = int(item_values[0])

            # Get current values to show in dialog
            cursor = self.db.cursor()
            try:
                cursor.execute("SELECT test_name, description FROM tests WHERE test_id = %s", (test_id,))
                current_test = cursor.fetchone()
                if current_test:
                    current_name, current_description = current_test
                    
                    new_test_name = simpledialog.askstring(
                        "Modify Test", 
                        "Enter new test name:", 
                        initialvalue=current_name
                    )
                    
                    if new_test_name:
                        new_description = simpledialog.askstring(
                            "Modify Description", 
                            "Enter Modified description:", 
                            initialvalue=current_description
                        )
                        
                        cursor.execute(
                            "UPDATE tests SET test_name = %s, description = %s WHERE test_id = %s",
                            (new_test_name, new_description, test_id)
                        )
                        self.db.commit()
                        messagebox.showinfo("Success", "Test modified successfully")
                        self.load_tests()
                        
            except Exception as e:
                self.db.rollback()  # Rollback in case of error
                messagebox.showerror("Error", f"Failed to modify test: {str(e)}")
            finally:
                cursor.close()
        else:
            messagebox.showwarning("Selection Required", "Please select a test to modify.")

    def delete_test(self):
        selections = self.test_tree.selection()
        if not selections:
            messagebox.showwarning("Selection Required", "Please select at least one test to delete.")
            return
            
        # Get all selected test IDs and names
        tests_to_delete = []
        for item in selections:
            values = self.test_tree.item(item)['values']
            tests_to_delete.append((int(values[0]), values[1]))  # (test_id, test_name)
        
        # Confirm deletion with user
        test_names = "\n".join([f"• {name}" for _, name in tests_to_delete])
        if not messagebox.askyesno("Delete Tests", 
            f"Are you sure you want to delete these {len(tests_to_delete)} tests?\n\n{test_names}"):
            return

        cursor = self.db.cursor()
        try:
            # Check for related results
            test_ids = [test_id for test_id, _ in tests_to_delete]
            placeholders = ','.join(['%s'] * len(test_ids))
            
            cursor.execute(f"""
                SELECT test_id, COUNT(*) 
                FROM results 
                WHERE test_id IN ({placeholders})
                GROUP BY test_id
            """, tuple(test_ids))
            
            results_count = cursor.fetchall()
            
            # If any tests have results, show additional warning
            if results_count:
                total_results = sum(count for _, count in results_count)
                if not messagebox.askyesno("Warning",
                    f"These tests have {total_results} total results associated with them.\n"
                    "Deleting these tests will also delete all related results.\n"
                    "Do you want to continue?"):
                    return
            
            # First delete related results
            cursor.execute(f"""
                DELETE FROM results 
                WHERE test_id IN ({placeholders})
            """, tuple(test_ids))
            
            # Then delete the tests
            cursor.execute(f"""
                DELETE FROM tests 
                WHERE test_id IN ({placeholders})
            """, tuple(test_ids))
            
            self.db.commit()
            
            # Show success message with count
            messagebox.showinfo("Success", 
                f"Successfully deleted {len(tests_to_delete)} tests and their related results.")
            
            # Refresh the tree view
            self.load_tests()
            
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", 
                f"Failed to delete tests: {str(e)}\n\nNo changes were made to the database.")
        finally:
            cursor.close()
      
    # Patient Management
    def create_patient_management_frame(self, parent):
        patient_frame = ttk.LabelFrame(parent, text="Patient Management", padding="10", labelanchor="n")
        patient_frame.columnconfigure(0, weight=1)
        patient_frame.rowconfigure(0, weight=1)

        self.patient_tree = ttk.Treeview(patient_frame, columns=("ID", "Name", "Phone", "Gender", "DOB", "Age", "Address", "Medical History"), show="headings", height=8)
        
        self.patient_tree.heading("ID", text="Patient ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Phone", text="Phone")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("DOB", text="DOB")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Address", text="Address")
        self.patient_tree.heading("Medical History", text="Medical History")
        
        self.patient_tree.column("ID", width=80)
        self.patient_tree.column("Name", width=150)
        self.patient_tree.column("Phone", width=100)
        self.patient_tree.column("Gender", width=80)
        self.patient_tree.column("DOB", width=100)
        self.patient_tree.column("Age", width=50)
        self.patient_tree.column("Address", width=200)
        self.patient_tree.column("Medical History", width=250)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"), background="#f0f0f0")
        style.configure("Treeview", rowheight=25, font=("Ubuntu", 9), background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#3c3839")])

        self.patient_tree.tag_configure('oddrow', background="lightgray")
        self.patient_tree.tag_configure('evenrow', background="white")

        self.patient_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        patient_scrollbar_y = ttk.Scrollbar(patient_frame, orient="vertical", command=self.patient_tree.yview)
        patient_scrollbar_x = ttk.Scrollbar(patient_frame, orient="horizontal", command=self.patient_tree.xview)
        self.patient_tree.configure(yscroll=patient_scrollbar_y.set, xscroll=patient_scrollbar_x.set)
        patient_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        patient_scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))
                                                                                                                                                                                                       
        patient_buttons = ttk.Frame(patient_frame)
        patient_buttons.grid(row=2, column=0, sticky=(tk.E, tk.W), pady=2.5)
        ttk.Button(patient_buttons, text="View", command=self.view_patient, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)
        ttk.Button(patient_buttons, text="Delete", command=self.delete_patient, width=10, style="Custom.TButton").pack(side=tk.LEFT, padx=2.5)

        self.load_patients()

        return patient_frame

    def load_patients(self):

        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)
        
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT patient_id, full_name, phone_number, gender, dob, age, address, medical_history 
            FROM patients
        """)
        count = 0  
        for patient in cursor.fetchall():
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
        selection = self.patient_tree.selection()  # Get selected item(s) in Treeview
        if selection:
            # Get the first selected item's patient_id (assuming patient_id is stored in the first column)
            patient_id = int(self.patient_tree.item(selection[0], "values")[0])

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
        else:
            messagebox.showwarning("Selection Required", "Please select a patient to view.")

    def delete_patient(self):
        selection = self.patient_tree.selection()  # Use selection() to get selected item(s)
        if selection:
            patient_id = int(self.patient_tree.item(selection[0], "values")[0])

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
        else:
            messagebox.showwarning("Selection Required", "Please select a patient to delete.")
