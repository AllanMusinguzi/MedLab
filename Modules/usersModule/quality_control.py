# quality_control.py
import tkinter as tk
from tkinter import ttk

class QualityControl(ttk.Frame):
    def __init__(self, master, db, return_callback):
        super().__init__(master)
        self.db = db
        self.return_callback = return_callback
        
        self.setup_ui()
        self.load_qc_data()

    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header_frame,
                 text="Quality Control",
                 font=('Ubuntu', 14, 'bold')).pack(side='left')
        
        ttk.Button(header_frame,
                  text="Back to Dashboard",
                  command=self.return_callback).pack(side='right')

        # Main content
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # QC Logs tab
        qc_logs_frame = ttk.Frame(notebook)
        notebook.add(qc_logs_frame, text='QC Logs')
        self.create_qc_logs_view(qc_logs_frame)

        # Control Charts tab
        control_charts_frame = ttk.Frame(notebook)
        notebook.add(control_charts_frame, text='Control Charts')
        self.create_control_charts_view(control_charts_frame)

        # Calibration Records tab
        calibration_frame = ttk.Frame(notebook)
        notebook.add(calibration_frame, text='Calibration Records')
        self.create_calibration_view(calibration_frame)

    # ... Additional methods for quality control ...