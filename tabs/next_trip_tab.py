import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from i94calculator.us_days import (
    parse_travel_log,
    build_us_intervals,
    add_window_start_interval,
    calculate_overlap_days
)

def create_next_trip_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Next Trip")

    trip_log_label = tk.Label(tab, text="Paste your I-94 history (tab-separated, with headers):")
    trip_log_label.pack(anchor="w")

    trip_log_text = scrolledtext.ScrolledText(tab, width=80, height=10)
    trip_log_text.pack(fill=tk.BOTH, expand=True)

    trip_start_label = tk.Label(tab, text="Trip Start Date:")
    trip_start_label.pack(anchor="w", pady=(10,0))

    trip_start_entry = DateEntry(tab, width=20, date_pattern='yyyy-mm-dd')
    trip_start_entry.pack(anchor="w")

    trip_end_label = tk.Label(tab, text="Trip End Date:")
    trip_end_label.pack(anchor="w", pady=(10,0))

    trip_end_entry = DateEntry(tab, width=20, date_pattern='yyyy-mm-dd')
    trip_end_entry.pack(anchor="w")

    def calculate_next_trip_days():
        travel_log = trip_log_text.get("1.0", tk.END).strip()
        trip_start_str = trip_start_entry.get().strip()
        trip_end_str = trip_end_entry.get().strip()
        
        if not travel_log:
            messagebox.showerror("Input Error", "Please paste your I-94 history.")
            return
            
        try:
            trip_start = datetime.strptime(trip_start_str, "%Y-%m-%d").date()
            trip_end = datetime.strptime(trip_end_str, "%Y-%m-%d").date()
            
            if trip_start >= trip_end:
                messagebox.showerror("Input Error", "Trip start date must be before trip end date.")
                return
                
        except Exception:
            messagebox.showerror("Input Error", "Please select valid trip dates.")
            return
            
        # Calculate days spent in the US in the 12 months before the trip end date
        window_start = trip_end - timedelta(days=365)
        entries = parse_travel_log(travel_log)
        if not entries:
            messagebox.showinfo("Result", f"No valid entries found.\nDays in US: 0")
            return
            
        # Add the upcoming trip as an interval
        # Format matches what parse_travel_log returns
        entries.append((trip_start, 'Arrival', 'Next Trip Start'))
        entries.append((trip_end, 'Departure', 'Next Trip End'))
        
        intervals = build_us_intervals(entries, trip_end)
        intervals = add_window_start_interval(entries, intervals, window_start)
        days = calculate_overlap_days(intervals, window_start, trip_end)
        
        # Calculate days remaining before reaching 180
        days_remaining = 180 - days
        
        messagebox.showinfo("Result", 
            f"Days spent in the US in the 12 months before {trip_end}: {days}\n"
            f"Days remaining before reaching 180: {days_remaining if days_remaining > 0 else '0'}")

    calc_next_trip_button = tk.Button(tab, text="Calculate Days for Next Trip", command=calculate_next_trip_days)
    calc_next_trip_button.pack(pady=(10,0))

    return tab
