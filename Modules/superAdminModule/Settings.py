import customtkinter as ctk
from datetime import datetime
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk, filedialog
from mysql.connector import Error
import csv, os, subprocess, json, psutil, configparser

class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, db=None):
        super().__init__(parent)
        self.db = db
        self.grid(row=0, column=0, sticky="nsew")
        
        # Create notebook-like structure using tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.system_tab = self.tabview.add("System Settings")
        self.audit_tab = self.tabview.add("Audit Logs")
        self.login_tab = self.tabview.add("Login Logs")
        
        self.create_system_settings_tab()
        self.create_audit_log_tab()
        self.create_login_log_tab()

    def create_system_settings_tab(self):
        # System configuration frame
        settings_frame = ctk.CTkFrame(self.system_tab)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Database Management Section
        backup_frame = ctk.CTkFrame(settings_frame)
        backup_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(backup_frame, text="Database Management").pack(pady=5)
        
        db_buttons_frame = ctk.CTkFrame(backup_frame)
        db_buttons_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(db_buttons_frame, text="Backup Database", 
                     command=self.backup_database).pack(side="left", padx=5)
        ctk.CTkButton(db_buttons_frame, text="Restore Database", 
                     command=self.restore_database).pack(side="left", padx=5)
        
        # System Maintenance Section
        maintenance_frame = ctk.CTkFrame(settings_frame)
        maintenance_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(maintenance_frame, text="System Maintenance").pack(pady=5)
        
        maintenance_buttons_frame = ctk.CTkFrame(maintenance_frame)
        maintenance_buttons_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(maintenance_buttons_frame, text="Clear Audit Logs", 
                     command=self.clear_audit_logs).pack(side="left", padx=5)
        ctk.CTkButton(maintenance_buttons_frame, text="System Health Check", 
                     command=self.system_health_check).pack(side="left", padx=5)

    def create_audit_log_tab(self):
        # Create custom treeview-like structure using CTkFrame
        self.audit_frame = ctk.CTkFrame(self.audit_tab)
        self.audit_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Headers
        headers_frame = ctk.CTkFrame(self.audit_frame)
        headers_frame.pack(fill="x", pady=5)
        
        columns = ("Timestamp", "User", "Action", "Details")
        for col in columns:
            ctk.CTkLabel(headers_frame, text=col).pack(side="left", padx=5, expand=True)
        
        # Scrollable frame for logs
        self.audit_scroll = ctk.CTkScrollableFrame(self.audit_frame)
        self.audit_scroll.pack(fill="both", expand=True)
        
        # Controls
        controls_frame = ctk.CTkFrame(self.audit_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(controls_frame, text="Export Logs", 
                     command=self.export_audit_logs).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="Refresh", 
                     command=self.refresh_audit_logs).pack(side="left", padx=5)

    def create_login_log_tab(self):
        # Create scrollable frame for login logs
        self.login_scroll = ctk.CTkScrollableFrame(self.login_tab)
        self.login_scroll.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Headers
        headers_frame = ctk.CTkFrame(self.login_scroll)
        headers_frame.pack(fill="x", pady=5)
        
        columns = ("ID", "Username", "Success", "Role", "Timestamp")
        for col in columns:
            ctk.CTkLabel(headers_frame, text=col).pack(side="left", padx=5, expand=True)
        
        # Content will be populated by refresh_logs
        self.logs_frame = ctk.CTkFrame(self.login_scroll)
        self.logs_frame.pack(fill="both", expand=True)
        
        # Refresh button
        ctk.CTkButton(self.login_tab, text="Refresh Logs", 
                     command=self.refresh_logs).pack(pady=5)

    def refresh_logs(self):
        # Clear existing logs
        for widget in self.logs_frame.winfo_children():
            widget.destroy()
            
        try:
            if self.db:
                cursor = self.db.cursor()
                cursor.execute("""
                    SELECT id, username, success, role, timestamp 
                    FROM login_logs 
                    ORDER BY timestamp DESC
                    LIMIT 1000
                """)
                
                for row in cursor.fetchall():
                    log_entry = ctk.CTkFrame(self.logs_frame)
                    log_entry.pack(fill="x", pady=2)
                    
                    # Format the data
                    success_text = "Yes" if row[2] else "No"
                    timestamp = row[4].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row[4], datetime) else str(row[4])
                    
                    # Create labels for each column
                    ctk.CTkLabel(log_entry, text=str(row[0])).pack(side="left", padx=5, expand=True)
                    ctk.CTkLabel(log_entry, text=row[1]).pack(side="left", padx=5, expand=True)
                    ctk.CTkLabel(log_entry, text=success_text).pack(side="left", padx=5, expand=True)
                    ctk.CTkLabel(log_entry, text=row[3]).pack(side="left", padx=5, expand=True)
                    ctk.CTkLabel(log_entry, text=timestamp).pack(side="left", padx=5, expand=True)
                
                cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load login logs: {str(e)}")

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
        self.load_audit_logs()

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

