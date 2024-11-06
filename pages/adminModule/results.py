import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime

class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = None
        #self.current_user = current_user
        self.create_layout()
        self.bind_events()
        self.create_context_menu()

    def create_layout(self):
        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Status bar
        self.status_bar = ctk.CTkLabel(self, text="No items selected", height=30)
        
        # Create Treeview
        self.results_tree = ttk.Treeview(
            self, 
            columns=("ID", "Patient", "Test", "Result", "Reference", "Units", "Status", "Date"),
            show="headings",
            height=8
        )
        
        # Configure headings
        self.results_tree.heading("ID", text="Result ID")
        self.results_tree.heading("Patient", text="Patient")
        self.results_tree.heading("Test", text="Test")
        self.results_tree.heading("Result", text="Result")
        self.results_tree.heading("Reference", text="Reference Range")
        self.results_tree.heading("Units", text="Units")
        self.results_tree.heading("Status", text="Status")
        self.results_tree.heading("Date", text="Date")
        
        # Configure columns
        self.results_tree.column("ID", width=70)
        self.results_tree.column("Patient", width=150)
        self.results_tree.column("Test", width=150)
        self.results_tree.column("Result", width=100)
        self.results_tree.column("Reference", width=120)
        self.results_tree.column("Units", width=80)
        self.results_tree.column("Status", width=100)
        self.results_tree.column("Date", width=120)
        
        # Configure row tags for styling
        self.results_tree.tag_configure('oddrow', background="#f0f0f0")
        self.results_tree.tag_configure('evenrow', background="white")
        self.results_tree.tag_configure('abnormal', foreground="red")
        self.results_tree.tag_configure('pending', foreground="orange")

        # Layout
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        results_scrollbar_y = ctk.CTkScrollbar(self, orientation="vertical", command=self.results_tree.yview)
        results_scrollbar_x = ctk.CTkScrollbar(self, orientation="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscroll=results_scrollbar_y.set, xscroll=results_scrollbar_x.set)
        results_scrollbar_y.grid(row=0, column=1, sticky="ns")
        results_scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Toolbar
        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=2, column=0, sticky="ew", pady=2.5)
        
        # Buttons
        ctk.CTkButton(toolbar, text="Add", command=self.add_result, width=10).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Modify", command=self.modify_result, width=10).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Delete", command=self.delete_result, width=10).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Verify", command=self.verify_result, width=10).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Print", command=self.print_result, width=10).pack(side="left", padx=2.5)
        
        # Status bar
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.results_tree, tearoff=0)
        self.context_menu.add_command(label="Add Result", command=self.add_result)
        self.context_menu.add_command(label="Modify Selected", command=self.modify_result)
        self.context_menu.add_command(label="Delete Selected", command=self.delete_result)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Verify Result", command=self.verify_result)
        self.context_menu.add_command(label="Print Result", command=self.print_result)

    def bind_events(self):
        self.results_tree.bind('<Delete>', lambda e: self.delete_result())
        self.results_tree.bind('<Control-p>', lambda e: self.print_result())
        self.results_tree.bind('<Control-v>', lambda e: self.verify_result())
        self.results_tree.bind('<Button-3>', self.show_context_menu)
        self.results_tree.bind('<<TreeviewSelect>>', self.update_status_bar)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def update_status_bar(self, event=None):
        selections = len(self.results_tree.selection())
        text = "No items selected" if selections == 0 else f"{selections} item{'s' if selections > 1 else ''} selected"
        self.status_bar.configure(text=text)

    def load_results(self):
        """Load all results from the database and display them in the Treeview."""
        # Clear the current items in the Treeview
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT r.result_id, p.full_name, t.test_name, r.result_value, 
                       r.reference_range, r.units, r.status, r.date_performed
                FROM results r
                JOIN patients p ON r.patient_id = p.patient_id
                JOIN tests t ON r.test_id = t.test_id
                ORDER BY r.date_performed DESC
            """)
            results = cursor.fetchall()
            
            # Insert each result into the Treeview
            for count, result in enumerate(results):
                tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                if result[6] == 'Pending':
                    tags += ('pending',)
                elif self.is_abnormal(result[3], result[4]):
                    tags += ('abnormal',)
                
                self.results_tree.insert("", ctk.END, values=result, tags=tags)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load results: {str(e)}")
        finally:
            cursor.close()

    def add_result(self):
        """Add a new result entry to the database."""
        try:
            cursor = self.db.cursor()
            patient_id = simpledialog.askinteger("Patient ID", "Enter patient ID:")
            test_id = simpledialog.askinteger("Test ID", "Enter test ID:")
            result_value = simpledialog.askstring("Result", "Enter result value:")
            reference_range = simpledialog.askstring("Reference Range", "Enter reference range (e.g., 70-120):")
            units = simpledialog.askstring("Units", "Enter units:")
            status = "Pending"
            
            cursor.execute("""
                INSERT INTO results 
                (patient_id, test_id, result_value, reference_range, units, status, date_performed)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (patient_id, test_id, result_value, reference_range, units, status))
            self.db.commit()
            messagebox.showinfo("Success", "Result added successfully")
            self.load_results()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Database Error", f"Failed to add result: {str(e)}")
        finally:
            cursor.close()

    def modify_result(self):
        """Modify a selected result entry in the database."""
        selected_item = self.results_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a result to modify")
            return
        
        result_id = self.results_tree.item(selected_item[0])['values'][0]
        try:
            cursor = self.db.cursor()
            new_value = simpledialog.askstring("Modify Result", "Enter new result value:")
            new_reference = simpledialog.askstring("Modify Reference", "Enter new reference range:")
            new_units = simpledialog.askstring("Modify Units", "Enter new units:")
            
            cursor.execute("""
                UPDATE results
                SET result_value = %s, reference_range = %s, units = %s, status = 'Modified', date_modified = NOW()
                WHERE result_id = %s
            """, (new_value, new_reference, new_units, result_id))
            self.db.commit()
            messagebox.showinfo("Success", "Result modified successfully")
            self.load_results()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Database Error", f"Failed to modify result: {str(e)}")
        finally:
            cursor.close()

    def delete_result(self):
        """Delete selected result(s) from the database."""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select result(s) to delete")
            return

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_items)} result(s)?"):
            return

        try:
            cursor = self.db.cursor()
            for item in selected_items:
                result_id = self.results_tree.item(item)['values'][0]
                cursor.execute("DELETE FROM results WHERE result_id = %s", (result_id,))
            
            self.db.commit()
            messagebox.showinfo("Success", "Result(s) deleted successfully")
            self.load_results()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Database Error", f"Failed to delete result(s): {str(e)}")
        finally:
            cursor.close()

    def verify_result(self):
        """Verify selected result(s) in the database."""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select result(s) to verify")
            return

        try:
            cursor = self.db.cursor()
            for item in selected_items:
                result_id = self.results_tree.item(item)['values'][0]
                cursor.execute("""
                    UPDATE results 
                    SET status = 'Verified', date_verified = NOW()
                    WHERE result_id = %s
                """, (result_id,))
            
            self.db.commit()
            messagebox.showinfo("Success", "Result(s) verified successfully")
            self.load_results()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Database Error", f"Failed to verify result(s): {str(e)}")
        finally:
            cursor.close()

    def print_result(self):
        """Display selected result(s) details for printing."""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a result to print")
            return

        result_id = self.results_tree.item(selected_items[0])['values'][0]
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT r.*, p.full_name, p.gender, p.age, t.test_name
                FROM results r
                JOIN patients p ON r.patient_id = p.patient_id
                JOIN tests t ON r.test_id = t.test_id
                WHERE r.result_id = %s
            """, (result_id,))
            result = cursor.fetchone()
            
            if result:
                print_message = f"Patient: {result[8]}, Gender: {result[9]}, Age: {result[10]}\n" \
                                f"Test: {result[11]}, Result: {result[3]}, Reference: {result[4]}, Units: {result[5]}\n" \
                                f"Status: {result[6]}, Date Performed: {result[7]}"
                messagebox.showinfo("Print Result", print_message)
            else:
                messagebox.showerror("Error", "Result not found")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to retrieve result: {str(e)}")
        finally:
            cursor.close()