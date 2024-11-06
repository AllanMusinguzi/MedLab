import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime

class TestsView:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.test_tree = None
        self.status_bar = None
        self.context_menu = None

    def create_test_management_frame(self):
        ctk.set_appearance_mode("System")  # "Dark", "Light" or "System"
        ctk.set_default_color_theme("blue")  # Available themes: "blue", "green", "dark-blue"

        test_frame = ctk.CTkFrame(self.parent, corner_radius=8)
        test_frame.grid_columnconfigure(0, weight=1)
        test_frame.grid_rowconfigure(0, weight=1)

        # Status bar
        self.status_bar = ctk.CTkLabel(test_frame, text="No items selected", anchor="w", height=20)

        # Create Treeview
        self.test_tree = ctk.CTkTreeview(test_frame, columns=("ID", "Test Name", "Description"), show="headings", height=8)
        self.test_tree.heading("ID", text="Test ID")
        self.test_tree.heading("Test Name", text="Test Name")
        self.test_tree.heading("Description", text="Description")

        self.test_tree.column("ID", width=50)
        self.test_tree.column("Test Name", width=100)
        self.test_tree.column("Description", width=300)

        # Configure styles for Treeview
        style = ctk.CTkStyle()
        style.configure("Treeview.Heading", font=("Ubuntu", 10, "bold"))
        style.configure("Treeview", rowheight=30, font=("Ubuntu", 9), background="#2b2b2b", foreground="#e0e0e0")
        self.test_tree.tag_configure('oddrow', background="#343434")
        self.test_tree.tag_configure('evenrow', background="#2b2b2b")

        # Create toolbar with buttons
        toolbar = ctk.CTkFrame(test_frame)
        toolbar.grid(row=2, column=0, sticky="ew", pady=2.5)

        ctk.CTkButton(toolbar, text="Add", command=self.add_test, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Modify", command=self.modify_test, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Select All", command=self.select_all_tests, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Deselect All", command=self.deselect_all_tests, width=100).pack(side="left", padx=2.5)
        ctk.CTkButton(toolbar, text="Delete", command=self.delete_test, width=100).pack(side="left", padx=2.5)

        # Layout configuration
        self.test_tree.grid(row=0, column=0, sticky="nsew")
        
        test_scrollbar_y = ctk.CTkScrollbar(test_frame, orientation="vertical", command=self.test_tree.yview)
        test_scrollbar_x = ctk.CTkScrollbar(test_frame, orientation="horizontal", command=self.test_tree.xview)
        self.test_tree.configure(yscrollcommand=test_scrollbar_y.set, xscrollcommand=test_scrollbar_x.set)
        
        test_scrollbar_y.grid(row=0, column=1, sticky="ns")
        test_scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 0))

        self.create_context_menu()
        self.bind_events()
        self.load_tests()

        return test_frame

    def create_context_menu(self):
        self.context_menu = ctk.CTkMenu(self.test_tree)
        self.context_menu.add_command(label="Add Test", command=self.add_test)
        self.context_menu.add_command(label="Modify Selected", command=self.modify_test)
        self.context_menu.add_command(label="Delete Selected", command=self.delete_test)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all_tests)
        self.context_menu.add_command(label="Deselect All", command=self.deselect_all_tests)

    def bind_events(self):
        self.test_tree.bind('<Delete>', lambda e: self.delete_test())
        self.test_tree.bind('<Control-a>', lambda e: self.select_all_tests())
        self.test_tree.bind('<Control-A>', lambda e: self.select_all_tests())
        self.test_tree.bind('<Escape>', lambda e: self.deselect_all_tests())
        self.test_tree.bind('<Button-3>', self.show_context_menu)
        self.test_tree.bind('<<TreeviewSelect>>', self.update_status_bar)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def update_status_bar(self, event=None):
        selections = len(self.test_tree.selection())
        self.status_bar.configure(text=f"{selections} item{'s' if selections != 1 else ''} selected")

    def select_all_tests(self):
        self.test_tree.selection_set(self.test_tree.get_children())
        self.update_status_bar()

    def deselect_all_tests(self):
        self.test_tree.selection_remove(self.test_tree.get_children())
        self.update_status_bar()

    def load_tests(self):
        for row in self.test_tree.get_children():
            self.test_tree.delete(row)
        
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT test_id, test_name, description FROM tests")
            for count, test in enumerate(cursor.fetchall()):
                tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                self.test_tree.insert("", "end", values=test, tags=(tag,))
            self.update_status_bar()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tests: {str(e)}")
        finally:
            cursor.close()

    def add_test(self):
        test_name = simpledialog.askstring("Add Test", "Enter test name:")
        if test_name:
            description = simpledialog.askstring("Add Description", "Enter test description:")
            if description:
                cursor = self.db.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO tests (test_name, description) VALUES (%s, %s)", 
                        (test_name, description)
                    )
                    self.db.commit()
                    messagebox.showinfo("Success", "Test added successfully")
                    self.load_tests()
                except Exception as e:
                    self.db.rollback()
                    messagebox.showerror("Error", f"Failed to add test: {str(e)}")
                finally:
                    cursor.close()

    def modify_test(self):
        selection = self.test_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a test to modify.")
            return

        item_values = self.test_tree.item(selection[0])['values']
        test_id = int(item_values[0])
        
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
                        "Enter modified description:", 
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
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to modify test: {str(e)}")
        finally:
            cursor.close()

    def delete_test(self):
        selections = self.test_tree.selection()
        if not selections:
            messagebox.showwarning("Selection Required", "Please select at least one test to delete.")
            return
            
        tests_to_delete = [(int(self.test_tree.item(item)['values'][0]), 
                           self.test_tree.item(item)['values'][1]) 
                          for item in selections]
        
        test_names = "\n".join([f"• {name}" for _, name in tests_to_delete])
        if not messagebox.askyesno("Delete Tests", 
            f"Are you sure you want to delete these {len(tests_to_delete)} tests?\n\n{test_names}"):
            return

        cursor = self.db.cursor()
        try:
            test_ids = [test_id for test_id, _ in tests_to_delete]
            placeholders = ','.join(['%s'] * len(test_ids))
            
            # Check for related results
            cursor.execute(f"""
                SELECT test_id, COUNT(*) 
                FROM results 
                WHERE test_id IN ({placeholders})
                GROUP BY test_id
            """, tuple(test_ids))
            
            results_count = cursor.fetchall()
            
            if results_count:
                total_results = sum(count for _, count in results_count)
                if not messagebox.askyesno("Warning",
                    f"These tests have {total_results} total results associated with them.\n"
                    "Deleting these tests will also delete all related results.\n"
                    "Do you want to continue?"):
                    return
            
            # Delete related results first
            cursor.execute(f"DELETE FROM results WHERE test_id IN ({placeholders})", tuple(test_ids))
            # Then delete the tests
            cursor.execute(f"DELETE FROM tests WHERE test_id IN ({placeholders})", tuple(test_ids))
            
            self.db.commit()
            messagebox.showinfo("Success", 
                f"Successfully deleted {len(tests_to_delete)} tests and their related results.")
            self.load_tests()
            
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", 
                f"Failed to delete tests: {str(e)}\n\nNo changes were made to the database.")
        finally:
            cursor.close()
