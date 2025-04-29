from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional
import sys

def parse_travel_log_line(line: str) -> Optional[Tuple[date, str, str]]:
    """
    Parse a single travel log line into (date, type, location) or None if invalid.
    Args:
        line: A single line from the travel log.
    Returns:
        Tuple of (date, type, location) or None if parsing fails.
    """
    parts: List[str] = line.split()  # Split on any whitespace (tabs or spaces)
    if len(parts) < 4:
        return None
    date_str: str = parts[1]
    typ: str = parts[2]
    location: str = parts[3]
    try:
        dt: date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (dt, typ, location)
    except Exception:
        return None

def parse_travel_log(travel_log: str) -> List[Tuple[date, str, str]]:
    """
    Parse the travel log into a sorted list of (date, type, location) tuples.
    Args:
        travel_log: The full travel log as a string.
    Returns:
        Sorted list of (date, type, location) tuples.
    """
    lines: List[str] = [line for line in travel_log.strip().split('\n') if line.strip()]
    entries: List[Tuple[date, str, str]] = []
    header_found: bool = False
    for line in lines:
        if not header_found and ("DATE" in line and "TYPE" in line):
            header_found = True
            continue
        entry = parse_travel_log_line(line)
        if entry:
            entries.append(entry)
    entries.sort(key=lambda x: x[0])
    return entries

def build_us_intervals(entries: List[Tuple[date, str, str]], as_of_date: date) -> List[Tuple[date, date]]:
    """
    Build intervals representing time spent in the US from Arrival to Departure.
    Args:
        entries: List of (date, type, location) tuples.
        as_of_date: The reference date for calculation.
    Returns:
        List of (start_date, end_date) intervals in the US.
    """
    filtered_entries: List[Tuple[date, str, str]] = [e for e in entries if e[0] <= as_of_date]
    intervals: List[Tuple[date, date]] = []
    in_us: bool = False
    last_date: Optional[date] = None
    if not filtered_entries:
        return []
    if filtered_entries[-1][0] < as_of_date:
        last_status: str = filtered_entries[-1][1]
        filtered_entries.append((as_of_date, last_status, ""))
    for dt, typ, _ in filtered_entries:
        if typ == "Arrival":
            if not in_us:
                last_date = dt
                in_us = True
        elif typ == "Departure":
            if in_us and last_date:
                intervals.append((last_date, dt))
                in_us = False
                last_date = None
    if in_us and last_date:
        intervals.append((last_date, as_of_date))
    return intervals

def add_window_start_interval(entries: List[Tuple[date, str, str]], intervals: List[Tuple[date, date]], window_start: date) -> List[Tuple[date, date]]:
    """
    If the first event is a Departure and after window_start, assume already in US at window start.
    Args:
        entries: List of (date, type, location) tuples.
        intervals: List of (start_date, end_date) intervals.
        window_start: The start date of the window.
    Returns:
        Possibly modified list of intervals.
    """
    if entries and entries[0][0] > window_start and entries[0][1] == "Departure":
        return [(window_start, entries[0][0])] + intervals
    return intervals

def calculate_overlap_days(intervals: List[Tuple[date, date]], window_start: date, window_end: date) -> int:
    """
    Calculate total days in US within the window from intervals.
    Args:
        intervals: List of (start_date, end_date) intervals.
        window_start: Start of the 12-month window.
        window_end: End of the 12-month window.
    Returns:
        Total number of days in the US in the window.
    """
    total_days: int = 0
    for start, end in intervals:
        overlap_start: date = max(start, window_start)
        overlap_end: date = min(end, window_end)
        if overlap_start < overlap_end:
            days: int = (overlap_end - overlap_start).days
            print(f"[DEBUG] Overlap: {overlap_start} to {overlap_end} = {days} days")
            total_days += days
        else:
            print(f"[DEBUG] No overlap: {start} to {end}")
    print(f"[DEBUG] Total days in US in window: {total_days}")
    return total_days

def print_debug_entries(entries: List[Tuple[date, str, str]]) -> None:
    print("[DEBUG] Parsed entries (up to as_of_date):")
    for e in entries:
        print("  ", e)

def print_debug_intervals(intervals: List[Tuple[date, date]]) -> None:
    print("[DEBUG] Intervals in US:")
    if not intervals:
        print("  [None found]")
    for interval in intervals:
        print(f"  {interval[0]} to {interval[1]}")

def main() -> None:
    print("Paste your travel log (tab-separated, with headers). End input with an empty line:")
    lines: List[str] = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        except EOFError:
            break
    travel_log: str = '\n'.join(lines)
    as_of_date_str: str = input("Enter 'as of' date (YYYY-MM-DD): ").strip()
    try:
        as_of_date: date = datetime.strptime(as_of_date_str, "%Y-%m-%d").date()
    except Exception:
        print("Invalid date format.")
        sys.exit(1)
    window_start: date = as_of_date - timedelta(days=365)
    print(f"\n[DEBUG] Window: {window_start} to {as_of_date}")
    entries: List[Tuple[date, str, str]] = parse_travel_log(travel_log)
    print_debug_entries(entries)
    if not entries:
        print("[DEBUG] No entries found up to as_of_date.")
        print(f"\nDays spent in the US in the 12 months before {as_of_date}: 0")
        input("\nPress Enter to exit.")
        sys.exit(0)
    intervals: List[Tuple[date, date]] = build_us_intervals(entries, as_of_date)
    intervals = add_window_start_interval(entries, intervals, window_start)
    print_debug_intervals(intervals)
    days: int = calculate_overlap_days(intervals, window_start, as_of_date)
    print(f"\nDays spent in the US in the 12 months before {as_of_date}: {days}")
    input("\nPress Enter to exit.")
    sys.exit(0)

if __name__ == "__main__":
    main()

def calculate_days_in_us(entries, as_of_date):
    """Calculate number of days in US in the 12 months before as_of_date."""
    # Only consider entries up to as_of_date
    entries = [e for e in entries if e[0] <= as_of_date]
    window_start = as_of_date - datetime.timedelta(days=365)
    print(f"\n[DEBUG] Window: {window_start} to {as_of_date}")
    print("[DEBUG] Parsed entries (up to as_of_date):")
    for e in entries:
        print("  ", e)
    if not entries:
        print("[DEBUG] No entries found up to as_of_date.")
        return 0
    # Add a virtual entry at as_of_date if needed
    if entries[-1][0] < as_of_date:
        last_status = entries[-1][1]
        entries.append((as_of_date, last_status, ""))
    # Build intervals: in US from Arrival to next Departure
    intervals = []
    in_us = False
    last_date = None
    for date, typ, _ in entries:
        if typ == "Arrival":
            if not in_us:
                last_date = date
                in_us = True
        elif typ == "Departure":
            if in_us and last_date:
                intervals.append((last_date, date))
                in_us = False
                last_date = None
    # If still in US at as_of_date, close interval
    if in_us and last_date:
        intervals.append((last_date, as_of_date))
    # Special case: if the first event is a Departure and window_start < first date, assume you were already in the US
    if entries and entries[0][0] > window_start and entries[0][1] == "Departure":
        intervals = [(window_start, entries[0][0])] + intervals
    print("[DEBUG] Intervals in US:")
    if not intervals:
        print("  [None found]")
    for interval in intervals:
        print(f"  {interval[0]} to {interval[1]}")
    # Calculate overlap with 12 months window
    total_days = 0
    for start, end in intervals:
        overlap_start = max(start, window_start)
        overlap_end = min(end, as_of_date)
        if overlap_start < overlap_end:
            days = (overlap_end - overlap_start).days
            print(f"[DEBUG] Overlap: {overlap_start} to {overlap_end} = {days} days")
            total_days += days
        else:
            print(f"[DEBUG] No overlap: {start} to {end}")
    print(f"[DEBUG] Total days in US in window: {total_days}")
    return total_days

def main():
    print("Paste your travel log (tab-separated, with headers). End input with an empty line:")
    lines = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        except EOFError:
            break
    travel_log = '\n'.join(lines)
    as_of_date_str = input("Enter 'as of' date (YYYY-MM-DD): ").strip()
    try:
        as_of_date = datetime.datetime.strptime(as_of_date_str, "%Y-%m-%d").date()
    except Exception:
        print("Invalid date format.")
        sys.exit(1)
    entries = parse_travel_log(travel_log)
    days = calculate_days_in_us(entries, as_of_date)
    print(f"\nDays spent in the US in the 12 months before {as_of_date}: {days}")

if __name__ == "__main__":
    main()
