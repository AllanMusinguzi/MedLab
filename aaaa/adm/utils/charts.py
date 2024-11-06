# utils/charts.py
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

def create_line_chart(parent, title, data, col):
    frame = ctk.CTkFrame(parent, height=300)
    frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
    
    title_label = ctk.CTkLabel(
        frame, 
        text=title, 
        font=ctk.CTkFont(size=16, weight="bold")
    )
    title_label.pack(pady=10)

    fig, ax = plt.subplots(figsize=(6, 4))
    months, values = zip(*data)
    ax.plot(months, values, marker='o')
    ax.set_xticklabels(months, rotation=45)
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def create_pie_chart(parent, title, data, col):
    frame = ctk