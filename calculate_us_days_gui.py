import tkinter as tk
from tkinter import ttk
from tabs.calculate_days_tab import create_calculate_days_tab
from tabs.next_trip_tab import create_next_trip_tab

root = tk.Tk()
root.title("US Days Calculator")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add tabs from separate files
create_calculate_days_tab(notebook)
create_next_trip_tab(notebook)

root.mainloop()
