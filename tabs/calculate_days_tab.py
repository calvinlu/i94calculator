import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, date, timedelta
from i94calculator.us_days import (
    parse_travel_log,
    build_us_intervals,
    add_window_start_interval,
    calculate_overlap_days
)

def create_calculate_days_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Calculate Days")

    log_label = tk.Label(tab, text="Paste your travel log (tab-separated, with headers):")
    log_label.pack(anchor="w")

    travel_log_text = scrolledtext.ScrolledText(tab, width=80, height=18)
    travel_log_text.pack(fill=tk.BOTH, expand=True)

    as_of_date_label = tk.Label(tab, text="Enter 'as of' date:")
    as_of_date_label.pack(anchor="w", pady=(10,0))

    as_of_date_entry = DateEntry(tab, width=20, date_pattern='yyyy-mm-dd')
    as_of_date_entry.set_date(date.today())
    as_of_date_entry.pack(anchor="w")

    def calculate_days_gui():
        travel_log = travel_log_text.get("1.0", tk.END).strip()
        as_of_date_str = as_of_date_entry.get().strip()
        if not travel_log:
            messagebox.showerror("Input Error", "Please paste your travel log.")
            return
        try:
            as_of_date = datetime.strptime(as_of_date_str, "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Input Error", "Please select a valid 'as of' date.")
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

    calc_button = tk.Button(tab, text="Calculate Days", command=calculate_days_gui)
    calc_button.pack(pady=(10,0))

    return tab
