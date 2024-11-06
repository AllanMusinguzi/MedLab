import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PatientsView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_patient_management_frame()

    def create_patient_management_frame(self):
        # Set up grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create main patient frame
        patient_frame = ctk.CTkLabelFrame(self, text="Patient Management", corner_radius=10)
        patient_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        patient_frame.columnconfigure(0, weight=1)
        patient_frame.rowconfigure(0, weight=1)

        # Create Treeview
        self.patient_tree = ctk.CTkTreeview(
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

        # Configure styles
        self.patient_tree.tag_configure('oddrow', background="lightgray")
        self.patient_tree.tag_configure('evenrow', background="white")

        # Add scrollbars
        patient_scrollbar_y = ctk.CTkScrollbar(patient_frame, orientation="vertical", command=self.patient_tree.yview)
        patient_scrollbar_x = ctk.CTkScrollbar(patient_frame, orientation="horizontal", command=self.patient_tree.xview)
        self.patient_tree.configure(yscroll=patient_scrollbar_y.set, xscroll=patient_scrollbar_x.set)

        # Layout
        self.patient_tree.grid(row=0, column=0, sticky="nsew")
        patient_scrollbar_y.grid(row=0, column=1, sticky="ns")
        patient_scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Buttons
        button_frame = ctk.CTkFrame(patient_frame)
        button_frame.grid(row=2, column=0, sticky="ew", pady=2.5)
        
        ctk.CTkButton(button_frame, text="View", command=self.view_patient, width=10).pack(side=tk.LEFT, padx=2.5)
        ctk.CTkButton(button_frame, text="Delete", command=self.delete_patient, width=10).pack(side=tk.LEFT, padx=2.5)

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
