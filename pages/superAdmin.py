# pages/superadmin_page.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from mysql.connector import Error
import bcrypt, csv, os, subprocess, json, psutil, configparser
from datetime import datetime

class SuperAdminPage(ttk.Frame):
    def __init__(self, master, db, user_id, username, password, phone_number, logout_callback):
        super().__init__(master)
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.logout_callback = logout_callback

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text=f"Super Administrator Dashboard - {self.username}", 
                font=('Helvetica', 16, 'bold')).pack(side="left")
        
        ttk.Button(header_frame, text="Logout", command=self.logout_callback).pack(side="right")

        # Notebook for different management sections
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # User Management Tab
        self.user_frame = self.create_user_management_tab()
        self.notebook.add(self.user_frame, text="User Management")

        # System Settings Tab
        self.settings_frame = self.create_system_settings_tab()
        self.notebook.add(self.settings_frame, text="System Settings")

        # Audit Log Tab
        self.audit_frame = self.create_audit_log_tab()
        self.notebook.add(self.audit_frame, text="Audit Logs")

        # Login Logs Tab
        self.login_frame = self.create_login_log_tab()
        self.notebook.add(self.login_frame, text="Login Logs")

        self.refresh_logs()  

    def create_user_management_tab(self):
        user_frame = ttk.Frame(self.notebook)

        # User management controls
        controls_frame = ttk.Frame(user_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)

        # User list
        columns = ("ID", "Username", "Role", "Phone", "Status")
        self.user_tree = ttk.Treeview(user_frame, columns=columns, show="headings")
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=100)

        self.user_tree.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Button(controls_frame, text="Add New User", command=self.show_add_user).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Modify Selected", command=self.modify_user).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Delete Selected", command=self.delete_user).pack(side="left", padx=5)  
        
        return user_frame

    def create_system_settings_tab(self):
        settings_frame = ttk.Frame(self.notebook)

        # System configuration controls
        settings_container = ttk.LabelFrame(settings_frame, text="System Configuration")
        settings_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Database backup controls
        backup_frame = ttk.LabelFrame(settings_container, text="Database Management")
        backup_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(backup_frame, text="Backup Database", command=self.backup_database).pack(side="left", padx=5, pady=5)
        ttk.Button(backup_frame, text="Restore Database", command=self.restore_database).pack(side="left", padx=5, pady=5)

        # System maintenance controls
        maintenance_frame = ttk.LabelFrame(settings_container, text="System Maintenance")
        maintenance_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(maintenance_frame, text="Clear Audit Logs", command=self.clear_audit_logs).pack(side="left", padx=5, pady=5)
        ttk.Button(maintenance_frame, text="System Health Check", command=self.system_health_check).pack(side="left", padx=5, pady=5)

        return settings_frame

    def create_audit_log_tab(self):
        audit_frame = ttk.Frame(self.notebook)

        # Audit log viewer
        columns = ("Timestamp", "User", "Action", "Details")
        self.audit_tree = ttk.Treeview(audit_frame, columns=columns, show="headings")
        
        for col in columns:
            self.audit_tree.heading(col, text=col)
            self.audit_tree.column(col, width=150)

        self.audit_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Controls
        controls_frame = ttk.Frame(audit_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(controls_frame, text="Export Logs", command=self.export_audit_logs).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_audit_logs).pack(side="left", padx=5)

        return audit_frame

    def create_login_log_tab(self):
        login_frame = ttk.Frame(self.notebook)

        # Create Treeview for login logs
        columns = ("ID", "Username", "Success", "Role", "Timestamp")
        self.tree = ttk.Treeview(login_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(login_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return login_frame

    def refresh_logs(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT id, username, success, role, timestamp 
                FROM login_logs 
                ORDER BY timestamp DESC
                LIMIT 1000
            """)
            
            # Insert new data
            for row in cursor.fetchall():
                # Convert boolean to Yes/No for better readability
                success_text = "Yes" if row[2] else "No"
                # Format timestamp
                timestamp = row[4].strftime("%Y-%m-%d %H:%M:%S")
                
                self.tree.insert("", tk.END, values=(
                    row[0],         # ID
                    row[1],         # Username
                    success_text,   # Success
                    row[3],         # Role
                    timestamp       # Timestamp
                ))
            
            cursor.close()
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load login logs: {str(e)}")

    def load_data(self):
        self.load_users()
        self.load_audit_logs()

    def load_users(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT user_id, username, role, phone_number, is_active 
                FROM users 
                ORDER BY user_id
            """)
            
            # Clear existing items
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)
                
            # Insert new data
            for user in cursor.fetchall():
                self.user_tree.insert("", "end", values=user)
                
            cursor.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading users: {str(e)}")

    def load_audit_logs(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT timestamp, username, action, details 
                FROM audit_log 
                JOIN users ON audit_log.user_id = users.user_id 
                ORDER BY timestamp DESC 
                LIMIT 1000
            """)
            
            # Clear existing items
            for item in self.audit_tree.get_children():
                self.audit_tree.delete(item)
                
            # Insert new data
            for log in cursor.fetchall():
                self.audit_tree.insert("", "end", values=log)
                
            cursor.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading audit logs: {str(e)}")

    def clear_audit_logs(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all audit logs?"):
            try:
                cursor = self.db.cursor()
                cursor.execute("TRUNCATE TABLE audit_log")
                self.db.commit()
                cursor.close()
                
                self.log_action("Cleared all audit logs")
                self.load_audit_logs()
                messagebox.showinfo("Success", "Audit logs cleared successfully!")
            except Error as e:
                messagebox.showerror("Error", f"Failed to clear audit logs: {str(e)}")

    def system_health_check(self):
        try:
            cursor = self.db.cursor()
            
            # Check database connection
            db_status = "OK" if self.db.is_connected() else "Failed"
            
            # Check database size
            cursor.execute("""
                SELECT table_schema, 
                       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                GROUP BY table_schema
            """)
            db_size = cursor.fetchone()[1]
            
            # Check user statistics
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 'active'")
            active_users = cursor.fetchone()[0]
            
            # System metrics
            system_metrics = {
                "Database Connection": db_status,
                "Database Size (MB)": db_size,
                "Total Users": total_users,
                "Active Users": active_users,
                "Memory Usage (MB)": round(self.get_memory_usage() / 1024 / 1024, 2),
                "Disk Space Available (GB)": round(self.get_disk_space() / 1024 / 1024 / 1024, 2)
            }
            
            # Display results
            health_window = tk.Toplevel(self)
            health_window.title("System Health Check Results")
            health_window.geometry("400x300")
            
            ttk.Label(health_window, text="System Health Report", 
                     font=('Helvetica', 12, 'bold')).pack(pady=10)
            
            for metric, value in system_metrics.items():
                ttk.Label(health_window, 
                         text=f"{metric}: {value}").pack(pady=5)
            
            cursor.close()
            self.log_action("Performed system health check")
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to perform health check: {str(e)}")

    def get_memory_usage(self):
        """Get current process memory usage"""

        process = psutil.Process(os.getpid())
        return process.memory_info().rss

    def get_disk_space(self):
        """Get available disk space"""
        return psutil.disk_usage('.').free


    def load_db_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return {
            'host': config['DATABASE']['host'],
            'user': config['DATABASE']['user'],
            'password': config['DATABASE']['password'],
            'database': config['DATABASE']['database']
        }
    

    def backup_database(self):
        try:
            # Load database credentials from config file
            config = self.load_db_config()

            # Create backup directory if it doesn't exist
            if not os.path.exists('backups'):
                os.makedirs('backups')

            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"backups/backup_{timestamp}.sql"
            
            # Construct mysqldump command
            cmd = [
                'mysqldump',
                f"--host={config['host']}",
                f"--user={config['user']}",
                f"--password={config['password']}",
                config['database']
            ]
            
            # Execute backup
            with open(backup_file, 'w') as outfile:
                subprocess.run(cmd, stdout=outfile, check=True)
            
            self.log_action(f"Created database backup: {backup_file}")
            messagebox.showinfo("Success", f"Database backup created successfully!\nLocation: {backup_file}")
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def restore_database(self):
        try:
            backup_file = filedialog.askopenfilename(
                initialdir="backups",
                title="Select Backup File",
                filetypes=(("SQL files", "*.sql"), ("All files", "*.*"))
            )
            
            if not backup_file:
                return
            
            if messagebox.askyesno("Confirm Restore", 
                                 "This will overwrite the current database. Continue?"):
                # Get database configuration
                config = {
                    'host': self.db.server_host,
                    'user': self.db.user,
                    'password': self.db.get_password(),
                    'database': self.db.database
                }
                
                # Construct mysql command
                cmd = [
                    'mysql',
                    f"--host={config['host']}",
                    f"--user={config['user']}",
                    f"--password={config['password']}",
                    config['database']
                ]
                
                # Execute restore
                with open(backup_file, 'r') as infile:
                    subprocess.run(cmd, stdin=infile, check=True)
                
                self.log_action(f"Restored database from backup: {backup_file}")
                messagebox.showinfo("Success", "Database restored successfully!")
                
                # Reload data
                self.load_data()
                
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Restore Error", f"Failed to restore backup: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def export_audit_logs(self):
        try:
            # Get save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Audit Logs"
            )
            
            if not filename:
                return
            
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT timestamp, username, action, details 
                FROM audit_log 
                JOIN users ON audit_log.user_id = users.id 
                ORDER BY timestamp DESC
            """)
            
            # Write to CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(["Timestamp", "Username", "Action", "Details"])
                # Write data
                writer.writerows(cursor.fetchall())
            
            cursor.close()
            self.log_action(f"Exported audit logs to: {filename}")
            messagebox.showinfo("Success", "Audit logs exported successfully!")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error exporting logs: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_audit_logs(self):
        self.load_audit_logs()

    def log_action(self, action_details):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO audit_log (user_id, action, details, timestamp)
                VALUES (%s, %s, %s, NOW())
            """, (self.user_id, "SUPERADMIN_ACTION", action_details))
            self.db.commit()
            cursor.close()
        except Error as e:
            print(f"Error logging action: {str(e)}")


    def show_add_user(self):
        add_user_window = tk.Toplevel(self)
        add_user_window.title("Add New User")

        # Create entry fields for each required attribute
        tk.Label(add_user_window, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        full_name_entry = tk.Entry(add_user_window)
        full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        email_entry = tk.Entry(add_user_window)
        email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(add_user_window)
        phone_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Username:").grid(row=3, column=0, padx=5, pady=5)
        username_entry = tk.Entry(add_user_window)
        username_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Password:").grid(row=4, column=0, padx=5, pady=5)
        password_entry = tk.Entry(add_user_window, show="*")
        password_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Confirm Password:").grid(row=5, column=0, padx=5, pady=5)
        confirm_password_entry = tk.Entry(add_user_window, show="*")
        confirm_password_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Address:").grid(row=6, column=0, padx=5, pady=5)
        address_entry = tk.Entry(add_user_window)
        address_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(add_user_window, text="Role:").grid(row=7, column=0, padx=5, pady=5)
        role_entry = ttk.Combobox(add_user_window, values=["User", "Admin", "SuperAdmin"])
        role_entry.grid(row=7, column=1, padx=5, pady=5)

        # Checkbox for preferences
        preferences_frame = tk.LabelFrame(add_user_window, text="Preferences")
        preferences_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        notifications_var = tk.BooleanVar()
        tk.Checkbutton(preferences_frame, text="Notifications", variable=notifications_var).pack(anchor="w")

        newsletter_var = tk.BooleanVar()
        tk.Checkbutton(preferences_frame, text="Newsletter", variable=newsletter_var).pack(anchor="w")

        dark_mode_var = tk.BooleanVar()
        tk.Checkbutton(preferences_frame, text="Dark Mode", variable=dark_mode_var).pack(anchor="w")

        def add_user_to_db():
            full_name = full_name_entry.get()
            email = email_entry.get()
            phone_number = phone_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            address = address_entry.get()
            role = role_entry.get()
            
            # Preferences
            preferences = {
                'notifications': notifications_var.get(),
                'newsletter': newsletter_var.get(),
                'dark_mode': dark_mode_var.get()
            }

            # Validate inputs
            if not all([full_name, email, phone_number, username, password, confirm_password, address]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO users (full_name, email, phone_number, username, password, 
                                    profile_picture, address, role, preferences) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (full_name, email, phone_number, username, hashed_password.decode('utf-8'), 
                    None, address, role, json.dumps(preferences)))
                self.db.commit()
                cursor.close()
                messagebox.showinfo("Success", "User added successfully.")
                add_user_window.destroy()
                self.load_data()  # Reloads the user data to reflect the new entry
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                self.db.rollback()

            tk.Button(add_user_window, text="Add User", command=add_user_to_db).grid(row=4, columnspan=2, pady=10)

                

    def modify_user(self):
        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showerror("Error", "Please select a user to modify.")
            return

        modify_user_window = tk.Toplevel(self)
        modify_user_window.title("Modify User")

        # Retrieve existing data
        user_id, full_name, email, phone_number, username, address, role = selected_user

        # Create entry fields pre-filled with the selected user details
        tk.Label(modify_user_window, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        full_name_entry = tk.Entry(modify_user_window)
        full_name_entry.insert(0, full_name)
        full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(modify_user_window, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        email_entry = tk.Entry(modify_user_window)
        email_entry.insert(0, email)
        email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(modify_user_window, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(modify_user_window)
        phone_entry.insert(0, phone_number)
        phone_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(modify_user_window, text="Address:").grid(row=3, column=0, padx=5, pady=5)
        address_entry = tk.Entry(modify_user_window)
        address_entry.insert(0, address)
        address_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(modify_user_window, text="Role:").grid(row=4, column=0, padx=5, pady=5)
        role_entry = ttk.Combobox(modify_user_window, values=["User", "Admin", "SuperAdmin"])
        role_entry.set(role)
        role_entry.grid(row=4, column=1, padx=5, pady=5)

        def save_changes():
            updated_data = {
                'full_name': full_name_entry.get(),
                'email': email_entry.get(),
                'phone_number': phone_entry.get(),
                'address': address_entry.get(),
                'role': role_entry.get()
            }

            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    UPDATE users SET full_name = %s, email = %s, phone_number = %s, 
                                    address = %s, role = %s WHERE user_id = %s
                """, (updated_data['full_name'], updated_data['email'], updated_data['phone_number'], 
                    updated_data['address'], updated_data['role'], user_id))
                self.db.commit()
                messagebox.showinfo("Success", "User modified successfully.")
                modify_user_window.destroy()
                self.load_data()  # Reload the user data to reflect updates
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                self.db.rollback()

        tk.Button(modify_user_window, text="Save Changes", command=save_changes).grid(row=5, columnspan=2, pady=10)



    def delete_user(self):
        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showerror("Error", "Please select a user to delete.")
            return

        user_id = selected_user[0]  # Assuming the first item is user_id
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?")
        if response:
            try:
                cursor = self.db.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                self.db.commit()
                messagebox.showinfo("Success", "User deleted successfully.")
                self.load_data()  # Reload the user data to reflect deletions
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                self.db.rollback()


    def get_selected_user(self):
        selected_item = self.user_table.selection()
        if not selected_item:
            return None
        user_data = self.user_table.item(selected_item, "values")
        return user_data  # Adjust this based on the values returned by `user_table`