# inventory_management.py
import tkinter as tk
from tkinter import ttk

class InventoryManagement(ttk.Frame):
    def __init__(self, master, db, return_callback):
        super().__init__(master)
        self.db = db
        self.return_callback = return_callback
        
        self.setup_ui()
        self.load_inventory()

    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header_frame,
                 text="Inventory Management",
                 font=('Ubuntu', 14, 'bold')).pack(side='left')
        
        ttk.Button(header_frame,
                  text="Back to Dashboard",
                  command=self.return_callback).pack(side='right')

        # Main content
        self.create_inventory_notebook()

    def create_inventory_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Reagents tab
        reagents_frame = ttk.Frame(notebook)
        notebook.add(reagents_frame, text='Reagents')
        self.create_reagents_view(reagents_frame)

        # Equipment tab
        equipment_frame = ttk.Frame(notebook)
        notebook.add(equipment_frame, text='Equipment')
        self.create_equipment_view(equipment_frame)

        # Consumables tab
        consumables_frame = ttk.Frame(notebook)
        notebook.add(consumables_frame, text='Consumables')
        self.create_consumables_view(consumables_frame)

    # ... Additional methods for inventory management ...