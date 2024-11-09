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
  
        if self.current_test_id is not None:
            self.load_parameters(self.current_test_id)

    def bind_events(self):
        # Test tree events
        self.test_tree.bind('<Delete>', lambda e: self.delete_test())
        self.test_tree.bind('<Double-1>', lambda e: self.modify_test())
        
        # Parameter tree events
        self.parameters_tree.bind('<Delete>', lambda e: self.delete_parameter())
        self.parameters_tree.bind('<Double-1>', lambda e: self.modify_parameter())
        self.parameters_tree.bind('<Return>', lambda e: self.enter_results())        

    def create_test_management_frame(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        main_frame = ctk.CTkFrame(self.parent, corner_radius=8)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Tabs
        tab_view = ctk.CTkTabview(main_frame)
        tab_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Test Management Tab
        test_tab = tab_view.add("Tests")
        parameters_tab = tab_view.add("Parameters")
        
        # Configure tabs
        test_tab.grid_columnconfigure(0, weight=1)
        test_tab.grid_rowconfigure(0, weight=1)
        parameters_tab.grid_columnconfigure(0, weight=1)
        parameters_tab.grid_rowconfigure(0, weight=1)

        # Create Test Treeview
        self.test_tree = ttk.Treeview(test_tab, 
            columns=("ID", "Test Name", "Description", "Category"),
            show="headings",
            height=8)
        
        self.test_tree.heading("ID", text="Test ID")
        self.test_tree.heading("Test Name", text="Tests")
        self.test_tree.heading("Description", text="Description")
        self.test_tree.heading("Category", text="Category")

        self.test_tree.column("ID", width=50)
        self.test_tree.column("Test Name", width=150)
        self.test_tree.column("Description", width=250)
        self.test_tree.column("Category", width=100)

        # Create Parameters Treeview
        self.parameters_tree = ttk.Treeview(parameters_tab,
            columns=("ID", "Parameter", "Unit", "Min Range", "Max Range", "Result", "Flag"),
            show="headings",
            height=8)
        
        self.parameters_tree.heading("ID", text="ID")
        self.parameters_tree.heading("Parameter", text="Parameter")
        self.parameters_tree.heading("Unit", text="Unit")
        self.parameters_tree.heading("Min Range", text="Min Range")
        self.parameters_tree.heading("Max Range", text="Max Range")
        self.parameters_tree.heading("Result", text="Result")
        self.parameters_tree.heading("Flag", text="Flag")

        self.parameters_tree.column("ID", width=50)
        self.parameters_tree.column("Parameter", width=150)
        self.parameters_tree.column("Unit", width=70)
        self.parameters_tree.column("Min Range", width=100)
        self.parameters_tree.column("Max Range", width=100)
        self.parameters_tree.column("Result", width=100)
        self.parameters_tree.column("Flag", width=70)

        # Configure styles
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Ubuntu", 13, "bold"))
        style.configure("Treeview", rowheight=30, font=("Ubuntu", 11))
        
        # Configure row tags for both trees
        for tree in [self.test_tree, self.parameters_tree]:
            tree.tag_configure('oddrow', background="#343434")
            tree.tag_configure('evenrow', background="#2b2b2b")
            tree.tag_configure('high', foreground="red")
            tree.tag_configure('low', foreground="blue")
            tree.tag_configure('normal', foreground="green")

        # Test Toolbar
        test_toolbar = ctk.CTkFrame(test_tab)
        test_toolbar.grid(row=1, column=0, sticky="ew", pady=2.5)

        ctk.CTkButton(test_toolbar, text="Add Test", command=self.add_test, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(test_toolbar, text="Modify Test", command=self.modify_test, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(test_toolbar, text="Delete test", command=self.delete_test, width=100).pack(side="left", padx=2.5)

        # Parameters Toolbar
        param_toolbar = ctk.CTkFrame(parameters_tab)
        param_toolbar.grid(row=1, column=0, sticky="ew", pady=2.5)

        ctk.CTkButton(param_toolbar, text="Add Parameter", command=self.add_parameter, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(param_toolbar, text="Edit Parameter", command=self.modify_parameter, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(param_toolbar, text="Delete Parameter", command=self.delete_parameter, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(param_toolbar, text="Enter Results", command=self.enter_results, width=100).pack(side="left", padx=2.5)

        # Layout configuration
        for tab, tree in [(test_tab, self.test_tree), (parameters_tab, self.parameters_tree)]:
            tree.grid(row=0, column=0, sticky="nsew")
            scrollbar_y = ctk.CTkScrollbar(tab, orientation="vertical", command=tree.yview)
            scrollbar_x = ctk.CTkScrollbar(tab, orientation="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            scrollbar_y.grid(row=0, column=1, sticky="ns")
            scrollbar_x.grid(row=2, column=0, sticky="ew")

        # Status bar
        self.status_bar = ctk.CTkLabel(main_frame, text="Ready", anchor="w", height=20)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

        # Bind events
        self.test_tree.bind('<<TreeviewSelect>>', self.on_test_selected)
        self.bind_events()

        self.load_tests()
        return main_frame

    def add_test(self):
        test_name = simpledialog.askstring("Add Test ", "Enter test  name:")
        if test_name:
            category = simpledialog.askstring("Add Category", "Enter test category:")
            description = simpledialog.askstring("Add Description", "Enter test description:")
            
            cursor = self.db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO tests (test_name, description, category) 
                    VALUES (%s, %s, %s)
                """, (test_name, description, category))
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

class TestDialog:
    def __init__(self, parent):
        self.result = None
        
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Add Test ")
        dialog.geometry("400x300")
        
        # Test  Name
        ctk.CTkLabel(dialog, text="Test Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(fill="x", padx=20, pady=5)
        
        # Category
        ctk.CTkLabel(dialog, text="Category:").pack(pady=5)
        category_entry = ctk.CTkEntry(dialog)
        category_entry.pack(fill="x", padx=20, pady=5)
        
        # Description
        ctk.CTkLabel(dialog, text="Description:").pack(pady=5)
        desc_text = ctk.CTkTextbox(dialog, height=100)
        desc_text.pack(fill="both", expand=True, padx=20, pady=5)
        
        def save():
            self.result = {
                'name': name_entry.get(),
                'category': category_entry.get(),
                'description': desc_text.get("1.0", "end-1c")
            }
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="Save", command=save).pack(pady=20)
        
        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)

class ParameterDialog:
    def __init__(self, parent):
        self.result = None
        
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Add Parameter")
        dialog.geometry("400x300")
        
        # Parameter Name
        ctk.CTkLabel(dialog, text="Parameter Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(fill="x", padx=20, pady=5)
        
        # Unit
        ctk.CTkLabel(dialog, text="Unit:").pack(pady=5)
        unit_entry = ctk.CTkEntry(dialog)
        unit_entry.pack(fill="x", padx=20, pady=5)
        
        # Reference Ranges
        range_frame = ctk.CTkFrame(dialog)
        range_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(range_frame, text="Min Range:").pack(side="left", padx=5)
        min_entry = ctk.CTkEntry(range_frame, width=100)
        min_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(range_frame, text="Max Range:").pack(side="left", padx=5)
        max_entry = ctk.CTkEntry(range_frame, width=100)
        max_entry.pack(side="left", padx=5)
        
        def save():
            try:
                min_range = float(min_entry.get())
                max_range = float(max_entry.get())
                
                if min_range >= max_range:
                    messagebox.showerror("Error", "Maximum range must be greater than minimum range")
                    return
                    
                self.result = {
                    'name': name_entry.get(),
                    'unit': unit_entry.get(),
                    'min_range': min_range,
                    'max_range': max_range
                }
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numerical values for ranges")
            
        ctk.CTkButton(dialog, text="Save", command=save).pack(pady=20)
        
        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)

class ModifyParameterDialog(ParameterDialog):
    def __init__(self, parent, current_values):
        super().__init__(parent)
        self.title("Modify Parameter")
        
        # Set current values
        self.name_entry.insert(0, current_values['name'])
        self.unit_entry.insert(0, current_values['unit'])
        self.min_entry.insert(0, str(current_values['min_range']))
        self.max_entry.insert(0, str(current_values['max_range']))

def modify_test(self):
    selection = self.test_tree.selection()
    if not selection:
        messagebox.showwarning("Selection Required", "Please select a test  to modify.")
        return

    item_values = self.test_tree.item(selection[0])['values']
    test_id = int(item_values[0])
    
    cursor = self.db.cursor()
    try:
        cursor.execute("""
            SELECT test_name, description, category 
            FROM tests 
            WHERE test_id = %s
        """, (test_id,))
        current_test = cursor.fetchone()
        
        if current_test:
            dialog = TestDialog(self.parent)
            dialog.name_entry.insert(0, current_test[0])
            dialog.category_entry.insert(0, current_test[2])
            dialog.desc_text.insert("1.0", current_test[1])
            
            if dialog.result:
                cursor.execute("""
                    UPDATE tests 
                    SET test_name = %s, description = %s, category = %s 
                    WHERE test_id = %s
                """, (
                    dialog.result['name'],
                    dialog.result['description'],
                    dialog.result['category'],
                    test_id
                ))
                self.db.commit()
                messagebox.showinfo("Success", "Test modified successfully")
                self.load_tests()
                
    except Exception as e:
        self.db.rollback()
        messagebox.showerror("Error", f"Failed to modify test: {str(e)}")
    finally:
        cursor.close()

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
            current_values = {
                'name': current_param[0],
                'unit': current_param[1],
                'min_range': current_param[2],
                'max_range': current_param[3]
            }
            
            dialog = ModifyParameterDialog(self.parent, current_values)
            if dialog.result:
                cursor.execute("""
                    UPDATE parameters 
                    SET parameter_name = %s, unit = %s, min_range = %s, max_range = %s 
                    WHERE parameter_id = %s
                """, (
                    dialog.result['name'],
                    dialog.result['unit'],
                    dialog.result['min_range'],
                    dialog.result['max_range'],
                    param_id
                ))
                self.db.commit()
                messagebox.showinfo("Success", "Parameter modified successfully")
                self.load_parameters(self.current_test_id)
                
    except Exception as e:
        self.db.rollback()
        messagebox.showerror("Error", f"Failed to modify parameter: {str(e)}")
    finally:
        cursor.close()

def delete_test(self):
    selection = self.test_tree.selection()
    if not selection:
        messagebox.showwarning("Selection Required", "Please select a test to delete.")
        return
        
    test_id = self.test_tree.item(selection[0])['values'][0]
    test_name = self.test_tree.item(selection[0])['values'][1]
    
    if not messagebox.askyesno("Confirm Delete", 
        f"Are you sure you want to delete the test '{test_name}'?\n"
        "This will also delete all associated parameters and results."):
        return
        
    cursor = self.db.cursor()
    try:
        # Delete all parameters associated with this test
        cursor.execute("DELETE FROM parameters WHERE test_id = %s", (test_id,))
        # Delete the test
        cursor.execute("DELETE FROM tests WHERE test_id = %s", (test_id,))
        
        self.db.commit()
        messagebox.showinfo("Success", "Test and associated parameters deleted successfully")
        self.load_tests()
        self.parameters_tree.delete(*self.parameters_tree.get_children())
        self.current_test_id = None
        
    except Exception as e:
        self.db.rollback()
        messagebox.showerror("Error", f"Failed to delete test: {str(e)}")
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

