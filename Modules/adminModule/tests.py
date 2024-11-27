import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime

class TestManagement:
    def __init__(self, parent):
        self.parent = parent
        self.db = None
        self.test_tree = None
        self.parameters_tree = None
        self.status_bar = None
        self.current_test_id = None
        self.test_stats = {}
        
        if self.current_test_id is not None:
            self.load_parameters(self.current_test_id)

    def create_test_management_frame(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        main_frame = ctk.CTkFrame(self.parent, corner_radius=8)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Create top stats cards
        self.create_stats_cards(main_frame)

        # Create main tab view
        tab_view = ctk.CTkTabview(main_frame)
        tab_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create tabs
        test_tab = tab_view.add("Tests")
        parameters_tab = tab_view.add("Parameters")
        results_tab = tab_view.add("Results")
        reports_tab = tab_view.add("Reports")
        
        # Configure tabs
        for tab in [test_tab, parameters_tab, results_tab, reports_tab]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        # Set up each tab's content
        self.setup_test_tab(test_tab)
        self.setup_parameters_tab(parameters_tab)
        self.setup_results_tab(results_tab)
        self.setup_reports_tab(reports_tab)

        # Status bar
        self.status_bar = ctk.CTkLabel(main_frame, text="Ready", anchor="w", height=20)
        self.status_bar.grid(row=2, column=0, sticky="ew", pady=(5, 0))

        self.bind_events()
        self.load_tests()
        return main_frame

    def create_stats_cards(self, parent):
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Create stat cards
        self.create_stat_card(stats_frame, 0, "Total Tests", "0", "tests")
        self.create_stat_card(stats_frame, 1, "Parameters", "0", "active")
        self.create_stat_card(stats_frame, 2, "Completed", "0", "completed")
        self.create_stat_card(stats_frame, 3, "Pending", "0", "pending")

    def create_stat_card(self, parent, col, title, value, key):
        card = ctk.CTkFrame(parent, corner_radius=6)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(card, text=title, font=("Ubuntu", 12)).pack(pady=(10,0))
        value_label = ctk.CTkLabel(card, text=value, font=("Ubuntu", 20, "bold"))
        value_label.pack(pady=(5,10))
        self.test_stats[key] = value_label

    def setup_test_tab(self, parent):
        # Create Test Treeview with scrollbars
        tree_frame = ctk.CTkFrame(parent)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.test_tree = ttk.Treeview(tree_frame, 
            columns=("ID", "Test Name", "Description", "Category", "Status", "Last Updated"),
            show="headings",
            height=8)
        
        # Configure columns
        columns = {
            "ID": 50,
            "Test Name": 150,
            "Description": 250,
            "Category": 100,
            "Status": 100,
            "Last Updated": 150
        }
        
        for col, width in columns.items():
            self.test_tree.heading(col, text=col)
            self.test_tree.column(col, width=width)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.test_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.test_tree.xview)
        self.test_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Layout
        self.test_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Toolbar
        toolbar = self.create_toolbar(parent, [
            ("Add Test", self.add_test),
            ("Modify Test", self.modify_test),
            ("Delete Test", self.delete_test),
            ("Export Tests", self.export_tests)
        ])
        toolbar.grid(row=1, column=0, sticky="ew", pady=5)

    def setup_parameters_tab(self, parent):
        # Create Parameters Treeview with scrollbars
        tree_frame = ctk.CTkFrame(parent)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.parameters_tree = ttk.Treeview(tree_frame,
            columns=("ID", "Parameter", "Unit", "Min Range", "Max Range", "Result", "Flag", "Last Updated"),
            show="headings",
            height=8)
        
        # Configure columns
        columns = {
            "ID": 50,
            "Parameter": 150,
            "Unit": 70,
            "Min Range": 100,
            "Max Range": 100,
            "Result": 100,
            "Flag": 70,
            "Last Updated": 150
        }
        
        for col, width in columns.items():
            self.parameters_tree.heading(col, text=col)
            self.parameters_tree.column(col, width=width)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.parameters_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.parameters_tree.xview)
        self.parameters_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Layout
        self.parameters_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Toolbar
        toolbar = self.create_toolbar(parent, [
            ("Add Parameter", self.add_parameter),
            ("Edit Parameter", self.modify_parameter),
            ("Delete Parameter", self.delete_parameter),
            ("Enter Results", self.enter_results),
            ("Export Parameters", self.export_parameters)
        ])
        toolbar.grid(row=1, column=0, sticky="ew", pady=5)

    def setup_results_tab(self, parent):
        # Create a frame for filters
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Date Range:").pack(side="left", padx=5)
        self.date_from = ctk.CTkEntry(filter_frame, width=100)
        self.date_from.pack(side="left", padx=5)
        ctk.CTkLabel(filter_frame, text="to").pack(side="left", padx=5)
        self.date_to = ctk.CTkEntry(filter_frame, width=100)
        self.date_to.pack(side="left", padx=5)
        
        ctk.CTkButton(filter_frame, text="Apply Filters", 
                     command=self.apply_result_filters).pack(side="left", padx=5)
        
        # Create results tree
        self.results_tree = ttk.Treeview(parent,
            columns=("Date", "Test", "Parameter", "Result", "Status", "Flagged"),
            show="headings",
            height=8)
        
        columns = {
            "Date": 100,
            "Test": 150,
            "Parameter": 150,
            "Result": 100,
            "Status": 100,
            "Flagged": 100
        }
        
        for col, width in columns.items():
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=width)
            
        self.results_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def setup_reports_tab(self, parent):
        # Create buttons for different report types
        report_frame = ctk.CTkFrame(parent)
        report_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        reports = [
            ("Daily Summary Report", self.generate_daily_report),
            ("Monthly Statistics", self.generate_monthly_report),
            ("Parameter Trends", self.generate_trend_report),
            ("Custom Report", self.generate_custom_report)
        ]
        
        for i, (text, command) in enumerate(reports):
            ctk.CTkButton(report_frame, text=text, 
                         command=command).grid(row=i, column=0, pady=5, padx=5, sticky="ew")

    def create_toolbar(self, parent, buttons):
        toolbar = ctk.CTkFrame(parent)
        for text, command in buttons:
            ctk.CTkButton(toolbar, text=text, command=command, 
                         width=100).pack(side="left", padx=2.5)
        return toolbar

    # New utility methods
    def export_tests(self):
        messagebox.showinfo("Export", "Test export functionality will be implemented here")
        
    def export_parameters(self):
        messagebox.showinfo("Export", "Parameter export functionality will be implemented here")
        
    def apply_result_filters(self):
        messagebox.showinfo("Filters", "Filter functionality will be implemented here")
        
    def generate_daily_report(self):
        messagebox.showinfo("Report", "Daily report generation will be implemented here")
        
    def generate_monthly_report(self):
        messagebox.showinfo("Report", "Monthly report generation will be implemented here")
        
    def generate_trend_report(self):
        messagebox.showinfo("Report", "Trend report generation will be implemented here")
        
    def generate_custom_report(self):
        messagebox.showinfo("Report", "Custom report generation will be implemented here")

    #test management methods
    def add_test(self):
        test_name = simpledialog.askstring("Add Test ", "Enter test  name:")
        if test_name:
            category = simpledialog.askstring("Add Category", "Enter test category:")
            description = simpledialog.askstring("Add Description", "Enter test description:")
            
            cursor = self.db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO tests (test_name, category, description) 
                    VALUES (%s, %s, %s)
                """, (test_name, category, description))
                self.db.commit()
                self.load_tests()
                messagebox.showinfo("Success", "Test  added successfully")
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to add test : {str(e)}")
            finally:
                cursor.close()

    def modify_test(self):
        selection = self.test_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a test  to modify.")
            return

        item_values = self.test_tree.item(selection[0])['values']
        test_id = int(item_values[0])
        
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT test_name, description, category FROM tests WHERE test_id = %s", (test_id,))
            current_test = cursor.fetchone()
            
            if current_test:
                new_name = simpledialog.askstring("Modify Test ", 
                    "Enter new test  name:", initialvalue=current_test[0])
                if new_name:
                    new_category = simpledialog.askstring("Modify Category", 
                        "Enter new category:", initialvalue=current_test[2])
                    new_description = simpledialog.askstring("Modify Description", 
                        "Enter new description:", initialvalue=current_test[1])
                    
                    cursor.execute("""
                        UPDATE tests 
                        SET test_name = %s, description = %s, category = %s 
                        WHERE test_id = %s
                    """, (new_name, new_description, new_category, test_id))
                    
                    self.db.commit()
                    messagebox.showinfo("Success", "Test  modified successfully")
                    self.load_tests()
                    
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to modify test : {str(e)}")
        finally:
            cursor.close()

    def delete_test(self):
        selection = self.test_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a test  to delete.")
            return
            
        test_id = self.test_tree.item(selection[0])['values'][0]
        test_name = self.test_tree.item(selection[0])['values'][1]
        
        if not messagebox.askyesno("Confirm Delete", 
            f"Are you sure you want to delete the test  '{test_name}'?\n"
            "This will also delete all associated parameters and results."):
            return
            
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM parameters WHERE test_id = %s", (test_id,))
            cursor.execute("DELETE FROM tests WHERE test_id = %s", (test_id,))
            
            self.db.commit()
            messagebox.showinfo("Success", "Test  and associated parameters deleted successfully")
            self.load_tests()
            self.parameters_tree.delete(*self.parameters_tree.get_children())
            self.current_test_id = None
            
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to delete test : {str(e)}")
        finally:
            cursor.close()

    #parameter management methods
    def load_parameters(self, test_id):
        """Load parameters for the selected test and display in the tree view."""
        if test_id is None:
            return  # No test selected, so no parameters to load

        # Clear the current list of parameters
        for row in self.parameters_tree.get_children():
            self.parameters_tree.delete(row)

        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT parameter_id, parameter_name, unit, min_range, max_range 
                FROM parameters 
                WHERE test_id = %s
            """, (test_id,))
            
            # Fetch and insert each parameter into the tree view
            for param in cursor.fetchall():
                self.parameters_tree.insert("", "end", values=param)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load parameters: {str(e)}")
        finally:
            cursor.close()

    def add_parameter(self):
        if not self.current_test_id:
            messagebox.showwarning("Warning", "Please select a test first")
            return

        param_name = simpledialog.askstring("Add Parameter", "Enter parameter name:")
        if param_name:
            unit = simpledialog.askstring("Add Unit", "Enter unit of measurement:")
            try:
                min_range = float(simpledialog.askstring("Add Min Range", "Enter minimum range:"))
                max_range = float(simpledialog.askstring("Add Max Range", "Enter maximum range:"))
                
                cursor = self.db.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO parameters 
                        (test_id, parameter_name, unit, min_range, max_range) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (self.current_test_id, param_name, unit, min_range, max_range))
                    
                    self.db.commit()
                    self.load_parameters(self.current_test_id) 
                    messagebox.showinfo("Success", "Parameter added successfully")
                    
                except Exception as e:
                    self.db.rollback()
                    messagebox.showerror("Error", f"Failed to add parameter: {str(e)}")
                finally:
                    cursor.close()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numerical values for ranges")

    def modify_parameter(self):
        selection = self.parameters_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a parameter to modify.")
            return

        item_values = self.parameters_tree.item(selection[0])['values']
        param_id = int(item_values[0])
        
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT parameter_name, unit, min_range, max_range 
                FROM parameters 
                WHERE parameter_id = %s
            """, (param_id,))
            current_param = cursor.fetchone()
            
            if current_param:
                new_name = simpledialog.askstring("Modify Parameter", 
                    "Enter new parameter name:", initialvalue=current_param[0])
                if new_name:
                    new_unit = simpledialog.askstring("Modify Unit", 
                        "Enter new unit:", initialvalue=current_param[1])
                    try:
                        new_min = float(simpledialog.askstring("Modify Min Range", 
                            "Enter new minimum range:", initialvalue=str(current_param[2])))
                        new_max = float(simpledialog.askstring("Modify Max Range", 
                            "Enter new maximum range:", initialvalue=str(current_param[3])))
                        
                        cursor.execute("""
                            UPDATE parameters 
                            SET parameter_name = %s, unit = %s, min_range = %s, max_range = %s 
                            WHERE parameter_id = %s
                        """, (new_name, new_unit, new_min, new_max, param_id))
                        
                        self.db.commit()
                        messagebox.showinfo("Success", "Parameter modified successfully")
                        self.load_parameters(self.current_test_id) 
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numerical values for ranges")
                    
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to modify parameter: {str(e)}")
        finally:
            cursor.close()

    def delete_parameter(self):
        selection = self.parameters_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a parameter to delete.")
            return
            
        param_id = self.parameters_tree.item(selection[0])['values'][0]
        param_name = self.parameters_tree.item(selection[0])['values'][1]
        
        if not messagebox.askyesno("Confirm Delete", 
            f"Are you sure you want to delete the parameter '{param_name}'?"):
            return
            
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM parameters WHERE parameter_id = %s", (param_id,))
            self.db.commit()
            messagebox.showinfo("Success", "Parameter deleted successfully")
            self.load_parameters(self.current_test_id)
            
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to delete parameter: {str(e)}")
        finally:
            cursor.close()

    def enter_results(self):
        selection = self.parameters_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a parameter")
            return

        param_id = self.parameters_tree.item(selection[0])['values'][0]
        result = simpledialog.askfloat("Enter Result", "Enter the result value:")
        
        if result is not None:
            cursor = self.db.cursor()
            try:
                # Get parameter ranges
                cursor.execute("""
                    SELECT min_range, max_range 
                    FROM parameters 
                    WHERE parameter_id = %s
                """, (param_id,))
                ranges = cursor.fetchone()
                
                if ranges:
                    min_range, max_range = ranges
                    # Determine flag
                    flag = 'N'  # Normal
                    if result < min_range:
                        flag = 'L'  # Low
                    elif result > max_range:
                        flag = 'H'  # High

                    # Update result and flag
                    cursor.execute("""
                        UPDATE parameters 
                        SET result = %s, flag = %s 
                        WHERE parameter_id = %s
                    """, (result, flag, param_id))
                    
                    self.db.commit()
                    self.load_parameters(self.current_test_id)
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to save result: {str(e)}")
            finally:
                cursor.close()

    def on_test_selected(self, event):
        selection = self.test_tree.selection()
        if selection:
            test_id = self.test_tree.item(selection[0])['values'][0]
            self.current_test_id = test_id
            self.load_parameters(test_id)

    def load_parameters(self, test_id):
        for item in self.parameters_tree.get_children():
            self.parameters_tree.delete(item)
            
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT parameter_id, parameter_name, unit, min_range, max_range, result, flag
                FROM parameters 
                WHERE test_id = %s
            """, (test_id,))
            
            for i, param in enumerate(cursor.fetchall()):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                if param[6]:  # If flag exists
                    if param[6] == 'H':
                        tag = ('high',)
                    elif param[6] == 'L':
                        tag = ('low',)
                    elif param[6] == 'N':
                        tag = ('normal',)
                        
                self.parameters_tree.insert("", "end", values=param, tags=tag)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load parameters: {str(e)}")
        finally:
            cursor.close()

    def load_tests(self):
        for item in self.test_tree.get_children():
            self.test_tree.delete(item)
            
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT test_id, test_name, description, category FROM tests")
            for i, test in enumerate(cursor.fetchall()):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.test_tree.insert("", "end", values=test, tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tests: {str(e)}")
        finally:
            cursor.close()

    def update_stats(self):
        """Update the statistics cards with current data"""
        if self.db:
            cursor = self.db.cursor()
            try:
                # Get total tests
                cursor.execute("SELECT COUNT(*) FROM tests")
                total_tests = cursor.fetchone()[0]
                self.test_stats["tests"].configure(text=str(total_tests))
                
                # Get total parameters
                cursor.execute("SELECT COUNT(*) FROM parameters")
                total_params = cursor.fetchone()[0]
                self.test_stats["active"].configure(text=str(total_params))
                
                # Get completed and pending counts
                cursor.execute("SELECT COUNT(*) FROM parameters WHERE result IS NOT NULL")
                completed = cursor.fetchone()[0]
                self.test_stats["completed"].configure(text=str(completed))
                
                cursor.execute("SELECT COUNT(*) FROM parameters WHERE result IS NULL")
                pending = cursor.fetchone()[0]
                self.test_stats["pending"].configure(text=str(pending))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update statistics: {str(e)}")
            finally:
                cursor.close()

    def bind_events(self):
        # Test tree events
        self.test_tree.bind('<Delete>', lambda e: self.delete_test())
        self.test_tree.bind('<Double-1>', lambda e: self.modify_test())
        self.test_tree.bind('<<TreeviewSelect>>', self.on_test_selected)
        
        # Parameter tree events
        self.parameters_tree.bind('<Delete>', lambda e: self.delete_parameter())
        self.parameters_tree.bind('<Double-1>', lambda e: self.modify_parameter())
        self.parameters_tree.bind('<Return>', lambda e: self.enter_results())