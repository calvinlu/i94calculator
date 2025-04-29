from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional

def parse_travel_log_line(line: str) -> Optional[Tuple[date, str, str]]:
    parts: List[str] = line.split()
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
    lines = [line for line in travel_log.strip().split('\n') if line.strip()]
    # Skip header row if present
    if lines and (lines[0].lower().startswith('row') or 'date' in lines[0].lower()):
        lines = lines[1:]
    entries = []
    for line in lines:
        parsed = parse_travel_log_line(line)
        if parsed:
            entries.append(parsed)
    entries.sort(key=lambda x: x[0])
    return entries

def build_us_intervals(entries: List[Tuple[date, str, str]], as_of_date: date) -> List[Tuple[date, date]]:
    filtered_entries = [e for e in entries if e[0] <= as_of_date]
    intervals: List[Tuple[date, date]] = []
    in_us = False
    last_date = None
    if not filtered_entries:
        return []
    if filtered_entries[-1][0] < as_of_date:
        last_status = filtered_entries[-1][1]
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
    return intervals

def add_window_start_interval(entries: List[Tuple[date, str, str]], intervals: List[Tuple[date, date]], window_start: date) -> List[Tuple[date, date]]:
    # If a trip started before the window, but ends inside, adjust the interval
    if not intervals:
        return intervals
    first_interval = intervals[0]
    if first_interval[0] < window_start < first_interval[1]:
        intervals[0] = (window_start, first_interval[1])
    return intervals

def calculate_overlap_days(intervals: List[Tuple[date, date]], window_start: date, window_end: date) -> int:
    total_days = 0
    for start, end in intervals:
        overlap_start = max(start, window_start)
        overlap_end = min(end, window_end)
        if overlap_start < overlap_end:
            days = (overlap_end - overlap_start).days
            total_days += days
    return total_days
