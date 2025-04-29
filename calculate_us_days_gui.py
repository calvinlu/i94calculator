import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime, date, timedelta
from i94calculator.us_days import (
    parse_travel_log,
    build_us_intervals,
    add_window_start_interval,
    calculate_overlap_days
)

# --- GUI ---
def calculate_days_gui():
    travel_log = travel_log_text.get("1.0", tk.END).strip()
    as_of_date_str = as_of_date_entry.get().strip()
    if not travel_log:
        messagebox.showerror("Input Error", "Please paste your travel log.")
        return
    try:
        as_of_date = datetime.strptime(as_of_date_str, "%Y-%m-%d").date()
    except Exception:
        messagebox.showerror("Input Error", "Please enter a valid 'as of' date (YYYY-MM-DD).")
        return
    window_start = as_of_date - timedelta(days=365)
    entries = parse_travel_log(travel_log)
    if not entries:
        messagebox.showinfo("Result", f"No valid entries found.\nDays in US: 0")
        return
    intervals = build_us_intervals(entries, as_of_date)
    intervals = add_window_start_interval(entries, intervals, window_start)
    days = calculate_overlap_days(intervals, window_start, as_of_date)
    messagebox.showinfo("Result", f"Days spent in the US in the 12 months before {as_of_date}: {days}")

root = tk.Tk()
root.title("US Days Calculator")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- Tab 1: Calculate Days ---
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Calculate Days")

log_label = tk.Label(tab1, text="Paste your travel log (tab-separated, with headers):")
log_label.pack(anchor="w")

travel_log_text = scrolledtext.ScrolledText(tab1, width=80, height=18)
travel_log_text.pack(fill=tk.BOTH, expand=True)

as_of_date_label = tk.Label(tab1, text="Enter 'as of' date (YYYY-MM-DD):")
as_of_date_label.pack(anchor="w", pady=(10,0))

as_of_date_entry = tk.Entry(tab1, width=20)
as_of_date_entry.pack(anchor="w")

calc_button = tk.Button(tab1, text="Calculate Days", command=calculate_days_gui)
calc_button.pack(pady=(10,0))

# --- Tab 2: Next Trip (placeholder) ---
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="Next Trip")

next_trip_label = tk.Label(tab2, text="[Next Trip feature coming soon]")
next_trip_label.pack(padx=20, pady=20)

root.mainloop()
