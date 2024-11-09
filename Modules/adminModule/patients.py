import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PatientManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = None 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_patient_management_frame()

    def create_patient_management_frame(self):
        # Create main patient frame
        patient_frame = ctk.CTkFrame(self, corner_radius=10)
        patient_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # Add label separately
        patient_label = tk.Label(patient_frame, text="Patient Management")
        patient_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        patient_frame.columnconfigure(0, weight=1)
        patient_frame.rowconfigure(1, weight=1)  # Changed to 1 to account for label

        # Create custom style for Treeview
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure the Treeview colors
        style.configure("Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0)

        style.configure("Treeview.Heading",
            background="#333333",
            foreground="white",
            borderwidth=1)

        style.map('Treeview',
            background=[('selected', '#347ab7')],
            foreground=[('selected', 'white')])

        # Create Treeview
        self.patient_tree = ttk.Treeview(
            patient_frame, 
            columns=("ID", "Name", "Phone", "Gender", "DOB", "Age", "Address", "Medical History"), 
            show="headings", 
            height=8
        )
        
        # Configure columns
        columns = {
            "ID": 80,
            "Name": 150,
            "Phone": 100,
            "Gender": 80,
            "DOB": 100,
            "Age": 50,
            "Address": 200,
            "Medical History": 250
        }
        
        for col, width in columns.items():
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=width)

        # Configure styles for alternating rows
        self.patient_tree.tag_configure('oddrow', background="#333333")
        self.patient_tree.tag_configure('evenrow', background="#2b2b2b")

        # Add scrollbars (using ttk scrollbars instead of CTkScrollbar)
        patient_scrollbar_y = ttk.Scrollbar(patient_frame, orient="vertical", command=self.patient_tree.yview)
        patient_scrollbar_x = ttk.Scrollbar(patient_frame, orient="horizontal", command=self.patient_tree.xview)
        self.patient_tree.configure(yscrollcommand=patient_scrollbar_y.set, xscrollcommand=patient_scrollbar_x.set)

        # Layout
        self.patient_tree.grid(row=1, column=0, sticky="nsew", padx=(5,0), pady=5)
        patient_scrollbar_y.grid(row=1, column=1, sticky="ns", pady=5)
        patient_scrollbar_x.grid(row=2, column=0, sticky="ew", padx=5)

        # Buttons
        button_frame = ctk.CTkFrame(patient_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5, padx=5)
        
        # Add buttons
        add_button = ctk.CTkButton(button_frame, text="Add", command=self.add_patient, width=100)
        view_button = ctk.CTkButton(button_frame, text="View", command=self.view_patient, width=100)
        edit_button = ctk.CTkButton(button_frame, text="Edit", command=self.edit_patient, width=100)
        delete_button = ctk.CTkButton(button_frame, text="Delete", command=self.delete_patient, width=100)
        
        # Pack buttons with some spacing
        add_button.pack(side=tk.LEFT, padx=5)
        view_button.pack(side=tk.LEFT, padx=5)
        edit_button.pack(side=tk.LEFT, padx=5)
        delete_button.pack(side=tk.LEFT, padx=5)

    def add_patient(self):
        # Create a new window for adding a patient
        add_window = ctk.CTkToplevel(self)
        add_window.title("Add New Patient")
        add_window.geometry("400x500")
        
        # Add form fields
        labels = ["Name:", "Phone:", "Gender:", "DOB:", "Address:", "Medical History:"]
        entries = {}
        
        for i, label in enumerate(labels):
            ctk.CTkLabel(add_window, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            if label == "Gender:":
                entries[label] = ctk.CTkComboBox(add_window, values=["Male", "Female", "Other"])
            elif label == "Medical History:":
                entries[label] = ctk.CTkTextbox(add_window, height=100)
            else:
                entries[label] = ctk.CTkEntry(add_window)
            entries[label].grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        
        def save_patient():
            try:
                # Get values from entries
                name = entries["Name:"].get()
                phone = entries["Phone:"].get()
                gender = entries["Gender:"].get()
                dob = entries["DOB:"].get()
                address = entries["Address:"].get()
                medical_history = entries["Medical History:"].get("1.0", tk.END).strip()
                
                # Calculate age from DOB
                try:
                    dob_date = datetime.strptime(dob, "%Y-%m-%d")
                    age = (datetime.now() - dob_date).days // 365
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                    return
                
                # Insert into database
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO patients (full_name, phone_number, gender, dob, age, address, medical_history)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, phone, gender, dob, age, address, medical_history))
                
                self.db.commit()
                messagebox.showinfo("Success", "Patient added successfully")
                add_window.destroy()
                self.load_patients()
                
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to add patient: {str(e)}")
            finally:
                cursor.close()
        
        # Add save button
        ctk.CTkButton(add_window, text="Save", command=save_patient).grid(row=len(labels), column=0, columnspan=2, pady=20)

    def edit_patient(self):
        selection = self.patient_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a patient to edit.")
            return
            
        patient_id = self.patient_tree.item(selection[0], "values")[0]
        
        # Get current patient data
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()
        cursor.close()
        
        if not patient:
            messagebox.showerror("Error", "Patient not found")
            return
            
        # Create edit window
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit Patient")
        edit_window.geometry("400x500")
        
        # Add form fields with current values
        labels = ["Name:", "Phone:", "Gender:", "DOB:", "Address:", "Medical History:"]
        entries = {}
        
        for i, label in enumerate(labels):
            ctk.CTkLabel(edit_window, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            if label == "Gender:":
                entries[label] = ctk.CTkComboBox(edit_window, values=["Male", "Female", "Other"])
                entries[label].set(patient[3])  # Assuming gender is at index 3
            elif label == "Medical History:":
                entries[label] = ctk.CTkTextbox(edit_window, height=100)
                entries[label].insert("1.0", patient[7])  # Assuming medical history is at index 7
            else:
                entries[label] = ctk.CTkEntry(edit_window)
                # Set values based on patient data
                if label == "Name:":
                    entries[label].insert(0, patient[1])
                elif label == "Phone:":
                    entries[label].insert(0, patient[2])
                elif label == "DOB:":
                    entries[label].insert(0, patient[4])
                elif label == "Address:":
                    entries[label].insert(0, patient[6])
            
            entries[label].grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        
        def update_patient():
            try:
                # Get values from entries
                name = entries["Name:"].get()
                phone = entries["Phone:"].get()
                gender = entries["Gender:"].get()
                dob = entries["DOB:"].get()
                address = entries["Address:"].get()
                medical_history = entries["Medical History:"].get("1.0", tk.END).strip()
                
                # Calculate age from DOB
                try:
                    dob_date = datetime.strptime(dob, "%Y-%m-%d")
                    age = (datetime.now() - dob_date).days // 365
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                    return
                
                # Update database
                cursor = self.db.cursor()
                cursor.execute("""
                    UPDATE patients 
                    SET full_name=%s, phone_number=%s, gender=%s, dob=%s, age=%s, address=%s, medical_history=%s
                    WHERE patient_id=%s
                """, (name, phone, gender, dob, age, address, medical_history, patient_id))
                
                self.db.commit()
                messagebox.showinfo("Success", "Patient updated successfully")
                edit_window.destroy()
                self.load_patients()
                
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
            finally:
                cursor.close()
        
        # Add update button
        ctk.CTkButton(edit_window, text="Update", command=update_patient).grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        # Load initial data
        self.load_patients()

    def load_patients(self):
        # Clear existing items
        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)
        
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT patient_id, full_name, phone_number, gender, dob, age, address, medical_history 
                FROM patients
            """)
            
            for count, patient in enumerate(cursor.fetchall()):
                tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                self.patient_tree.insert("", tk.END, values=patient, tags=(tag,))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load patients: {str(e)}")
        finally:
            cursor.close()

    def view_patient(self):
        selection = self.patient_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a patient to view.")
            return
            
        patient_id = self.patient_tree.item(selection[0], "values")[0]
        cursor = self.db.cursor()
        
        try:
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient = cursor.fetchone()
            
            if patient:
                info = (f"Patient ID: {patient[0]}\n"
                       f"Name: {patient[1]}\n"
                       f"Phone: {patient[2]}\n"
                       f"Gender: {patient[3]}\n"
                       f"DOB: {patient[4]}\n"
                       f"Age: {patient[5]}\n"
                       f"Address: {patient[6]}\n"
                       f"Medical History: {patient[7]}")
                messagebox.showinfo("Patient Information", info)
            else:
                messagebox.showinfo("Not Found", "Patient not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view patient: {str(e)}")
        finally:
            cursor.close()

    def delete_patient(self):
        selection = self.patient_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a patient to delete.")
            return
            
        patient_id = self.patient_tree.item(selection[0], "values")[0]
        
        if not messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient?"):
            return
            
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            self.db.commit()
            messagebox.showinfo("Success", "Patient deleted successfully")
            self.load_patients()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
        finally:
            cursor.close()
