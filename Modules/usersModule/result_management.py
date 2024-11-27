# result_management.py
import tkinter as tk
from tkinter import ttk

class ResultManagement(ttk.Frame):
    def __init__(self, master, db, return_callback):
        super().__init__(master)
        self.db = db
        self.return_callback = return_callback
        
        self.setup_ui()
        self.load_pending_results()

    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header_frame,
                 text="Result Management",
                 font=('Ubuntu', 14, 'bold')).pack(side='left')
        
        ttk.Button(header_frame,
                  text="Back to Dashboard",
                  command=self.return_callback).pack(side='right')

        # Main content
        content_frame = ttk.PanedWindow(self, orient='horizontal')
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left pane - Pending Results
        self.create_pending_results_view(content_frame)
        
        # Right pane - Result Entry
        self.create_result_entry_view(content_frame)

    # ... Additional methods for result management ...