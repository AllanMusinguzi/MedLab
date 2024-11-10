import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
import json

class UsersView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db  # Store database connection
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.create_widgets()
        self.setup_styles()
        self.load_data()  
        self._all_items = []

        self._last_sort_col = None
        self._last_sort_reverse = False

       
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Treeview", 
                    rowheight=30, 
                    font=('Ubuntu', 10),
                    foreground='black',
                    background='white'  # Optional: set background color
                    )
        
        style.configure("Treeview.Heading", 
                    font=('Ubuntu', 11, 'bold'),
                    foreground='black',
                    background='white'  # Optional: set background color for headers
                    )
        
    def create_widgets(self):
        # Header with Add User button
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header_frame, text="Users Management", 
                    font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, padx=10)
        
        ctk.CTkButton(header_frame, text="Add New User",
                     command=self.show_add_user_dialog).grid(row=0, column=2, padx=10)
        
        # Search and Filter
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search users...",
                                       textvariable=self.search_var, width=200)
        self.search_entry.pack(side="left", padx=10)
        self.search_var.trace("w", self.filter_users)
        
        self.role_filter = ctk.CTkComboBox(filter_frame, values=["All Roles", "User", "Admin", "SuperAdmin"],
                                         command=self.filter_users)
        self.role_filter.pack(side="left", padx=10)
        
        # Users Table
        self.create_users_table()
        
    def create_users_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Create Treeview with updated columns
        columns = ("ID", "Full Name", "Email", "Phone", "Username", "Address", "Role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        column_widths = {
            "ID": 50,
            "Full Name": 150,
            "Email": 200,
            "Phone": 120,
            "Username": 100,
            "Address": 200,
            "Role": 100
        }
        
        for col, width in column_widths.items():
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=width, minwidth=width)
            
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind("<Double-1>", self.on_user_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)


    def load_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
                
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT user_id, full_name, email, phone_number, username, 
                    address, role FROM users
            """)
            users = cursor.fetchall()
            cursor.close()
            
            # Insert data into treeview
            for user in users:
                self.tree.insert("", "end", values=user)
                
            # Store all items after loading
            self._all_items = self.tree.get_children()
                
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    def show_add_user_dialog(self):
        dialog = AddUserDialog(self, self.db)
        self.wait_window(dialog)
        self.load_data()

    def show_edit_user_dialog(self, user_id):
        dialog = EditUserDialog(self, self.db, user_id)
        self.wait_window(dialog)
        self.load_data()

        
    def filter_users(self, *args):
        search_text = self.search_var.get().lower()
        role_filter = self.role_filter.get()
        
        # Get filtered items
        filtered_items = []
        for values in self._all_items:
            if not values:
                continue
                
            # Convert all values to strings for searching
            string_values = [str(value).lower() for value in values]
            
            # Check if matches search criteria
            matches_search = (
                not search_text or
                any(search_text in value for value in string_values)
            )
            
            # Check if matches role filter
            matches_role = (
                role_filter == "All Roles" or 
                (len(values) > 6 and str(values[6]) == role_filter)
            )
            
            if matches_search and matches_role:
                filtered_items.append(values)
        
        # Apply current sort to filtered items if there is one
        if hasattr(self, '_last_sort_col') and self._last_sort_col is not None:
            col = self._last_sort_col
            try:
                filtered_items.sort(
                    key=lambda x: float(x[col]) if str(x[col]).replace('.', '').isdigit() else str(x[col]).lower(),
                    reverse=self._last_sort_reverse
                )
            except (ValueError, IndexError):
                filtered_items.sort(
                    key=lambda x: str(x[col]).lower(),
                    reverse=self._last_sort_reverse
                )
        
        # Clear and repopulate the tree
        self.tree.delete(*self.tree.get_children())
        for values in filtered_items:
            self.tree.insert('', 'end', values=values)
            
    def sort_treeview(self, col):
        """Sort treeview content when a column header is clicked."""
        try:
            # Toggle sort order if clicking the same column
            if hasattr(self, '_last_sort_col') and self._last_sort_col == col:
                self._last_sort_reverse = not self._last_sort_reverse
            else:
                self._last_sort_reverse = False
            
            self._last_sort_col = col
            
            # Get all current items (this preserves filtering)
            items = []
            for item in self.tree.get_children(""):
                values = self.tree.item(item)['values']
                items.append(values)
            
            # Sort the items
            try:
                items.sort(
                    key=lambda x: float(x[col]) if str(x[col]).replace('.', '').isdigit() else str(x[col]).lower(),
                    reverse=self._last_sort_reverse
                )
            except (ValueError, IndexError):
                items.sort(
                    key=lambda x: str(x[col]).lower(),
                    reverse=self._last_sort_reverse
                )
            
            # Clear and repopulate the tree
            self.tree.delete(*self.tree.get_children())
            for values in items:
                self.tree.insert('', 'end', values=values)
            
            # Update column headers
            for column in self.tree["columns"]:
                if column == col:
                    direction = "▼" if self._last_sort_reverse else "▲"
                    self.tree.heading(column, text=f"{self.tree.heading(column)['text'].split(' ')[0]} {direction}")
                else:
                    self.tree.heading(column, text=self.tree.heading(column)['text'].split(' ')[0])
                    
        except Exception as e:
            messagebox.showerror("Sorting Error", f"Error sorting column: {str(e)}")

    def on_user_double_click(self, event):
        item = self.tree.selection()[0]
        user_id = self.tree.item(item)["values"][0]
        self.show_edit_user_dialog(user_id)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(
                label="Edit User", 
                command=lambda: self.show_edit_user_dialog(
                    self.tree.item(item)["values"][0]
                )
            )
            menu.add_command(
                label="Delete User", 
                command=lambda: self.delete_user(item)
            )
            menu.post(event.x_root, event.y_root)

    def delete_user(self, item):
        user_values = self.tree.item(item)["values"]
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete user {user_values[1]}?"
        ):
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "DELETE FROM users WHERE user_id = %s", 
                    (user_values[0],)
                )
                self.db.commit()
                cursor.close()
                self.tree.delete(item)
                messagebox.showinfo("Success", "User deleted successfully")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                self.db.rollback()

class AddUserDialog(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Add New User")
        self.setup_ui()

    def setup_ui(self):
        # Create fields
        fields = [
            ("Full Name:", "full_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Username:", "username"),
            ("Password:", "password"),
            ("Confirm Password:", "confirm_password"),
            ("Address:", "address")
        ]

        for i, (label_text, field_name) in enumerate(fields):
            ctk.CTkLabel(self, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if field_name in ["password", "confirm_password"]:
                widget = ctk.CTkEntry(self, show="*")
            else:
                widget = ctk.CTkEntry(self)
            widget.grid(row=i, column=1, padx=10, pady=5)
            setattr(self, f"{field_name}_entry", widget)

        # Role selection
        ctk.CTkLabel(self, text="Role:").grid(row=len(fields), column=0, padx=10, pady=5)
        self.role_combo = ctk.CTkComboBox(
            self, 
            values=["User", "Admin", "SuperAdmin"]
        )
        self.role_combo.grid(row=len(fields), column=1, padx=10, pady=5)

        # Preferences
        pref_frame = ctk.CTkFrame(self)
        pref_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        self.notifications_var = ctk.BooleanVar()
        self.newsletter_var = ctk.BooleanVar()
        self.dark_mode_var = ctk.BooleanVar()
        
        ctk.CTkCheckBox(
            pref_frame, 
            text="Notifications", 
            variable=self.notifications_var
        ).pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkCheckBox(
            pref_frame, 
            text="Newsletter", 
            variable=self.newsletter_var
        ).pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkCheckBox(
            pref_frame, 
            text="Dark Mode", 
            variable=self.dark_mode_var
        ).pack(anchor="w", padx=5, pady=2)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Save", 
            command=self.save_user
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=self.destroy
        ).pack(side="left", padx=5)

    def save_user(self):
        # Get values from fields
        data = {
            'full_name': self.full_name_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'username': self.username_entry.get(),
            'password': self.password_entry.get(),
            'confirm_password': self.confirm_password_entry.get(),
            'address': self.address_entry.get(),
            'role': self.role_combo.get()
        }

        # Validate inputs
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Hash password
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), 
            bcrypt.gensalt()
        )

        # Get preferences
        preferences = {
            'notifications': self.notifications_var.get(),
            'newsletter': self.newsletter_var.get(),
            'dark_mode': self.dark_mode_var.get()
        }

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO users (
                    full_name, email, phone_number, username, 
                    password, address, role, preferences
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['full_name'], data['email'], data['phone'],
                data['username'], hashed_password.decode('utf-8'),
                data['address'], data['role'], json.dumps(preferences)
            ))
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "User added successfully")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.db.rollback()

class EditUserDialog(AddUserDialog):
    def __init__(self, parent, db, user_id):
        self.user_id = user_id
        super().__init__(parent, db)
        self.title("Edit User")
        self.load_user_data()

    def load_user_data(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT full_name, email, phone_number, username,
                       address, role, preferences
                FROM users WHERE user_id = %s
            """, (self.user_id,))
            user_data = cursor.fetchone()
            cursor.close()

            if user_data:
                self.full_name_entry.insert(0, user_data[0])
                self.email_entry.insert(0, user_data[1])
                self.phone_entry.insert(0, user_data[2])
                self.username_entry.insert(0, user_data[3])
                self.address_entry.insert(0, user_data[4])
                self.role_combo.set(user_data[5])

                # Load preferences
                preferences = json.loads(user_data[6])
                self.notifications_var.set(preferences.get('notifications', False))
                self.newsletter_var.set(preferences.get('newsletter', False))
                self.dark_mode_var.set(preferences.get('dark_mode', False))

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def save_user(self):
        data = {
            'full_name': self.full_name_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'username': self.username_entry.get(),
            'address': self.address_entry.get(),
            'role': self.role_combo.get()
        }

        # Validate inputs
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Get preferences
        preferences = {
            'notifications': self.notifications_var.get(),
            'newsletter': self.newsletter_var.get(),
            'dark_mode': self.dark_mode_var.get()
        }

        # Check if password is being updated
        password_update = ""
        password_params = []
        if self.password_entry.get() and self.confirm_password_entry.get():
            if self.password_entry.get() != self.confirm_password_entry.get():
                messagebox.showerror("Error", "Passwords do not match.")
                return
            hashed_password = bcrypt.hashpw(
                self.password_entry.get().encode('utf-8'), 
                bcrypt.gensalt()
            )
            password_update = ", password = %s"
            password_params = [hashed_password.decode('utf-8')]

        try:
            cursor = self.db.cursor()
            query = f"""
                UPDATE users 
                SET full_name = %s, 
                    email = %s, 
                    phone_number = %s, 
                    username = %s, 
                    address = %s, 
                    role = %s, 
                    preferences = %s
                    {password_update}
                WHERE user_id = %s
            """
            
            params = [
                data['full_name'],
                data['email'],
                data['phone'],
                data['username'],
                data['address'],
                data['role'],
                json.dumps(preferences)
            ] + password_params + [self.user_id]

            cursor.execute(query, params)
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "User updated successfully")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.db.rollback()