from datetime import date
import pytest
from i94calculator.us_days import (
    parse_travel_log_line,
    parse_travel_log,
    build_us_intervals,
    add_window_start_interval,
    calculate_overlap_days
)

def test_parse_travel_log_line_valid():
    line = "1 2024-05-01 Arrival NYC"
    result = parse_travel_log_line(line)
    assert result == (date(2024, 5, 1), "Arrival", "NYC")

def test_parse_travel_log_line_invalid():
    line = "bad line"
    result = parse_travel_log_line(line)
    assert result is None

def test_parse_travel_log_line_partial():
    line = "1 2024-05-01 Arrival"
    result = parse_travel_log_line(line)
    assert result is None

def test_parse_travel_log_line_extra_fields():
    line = "1 2024-05-01 Arrival NYC JFK"
    result = parse_travel_log_line(line)
    assert result == (date(2024, 5, 1), "Arrival", "NYC")

def test_parse_travel_log_empty():
    log = ""
    entries = parse_travel_log(log)
    assert entries == []

def test_parse_travel_log_header_only():
    log = "Row DATE TYPE LOCATION"
    entries = parse_travel_log(log)
    assert entries == []

def test_parse_travel_log_multiple_entries():
    log = "Row DATE TYPE LOCATION\n1 2024-05-01 Arrival NYC\n2 2024-05-10 Departure NYC\n3 2024-06-01 Arrival LAX"
    entries = parse_travel_log(log)
    assert entries == [
        (date(2024, 5, 1), "Arrival", "NYC"),
        (date(2024, 5, 10), "Departure", "NYC"),
        (date(2024, 6, 1), "Arrival", "LAX")
    ]

def test_build_us_intervals_simple():
    entries = [
        (date(2024, 5, 1), "Arrival", "NYC"),
        (date(2024, 5, 10), "Departure", "NYC")
    ]
    intervals = build_us_intervals(entries, date(2024, 5, 10))
    assert intervals == [(date(2024, 5, 1), date(2024, 5, 10))]

def test_build_us_intervals_no_entries():
    intervals = build_us_intervals([], date(2024, 5, 10))
    assert intervals == []

def test_build_us_intervals_open_ended():
    entries = [
        (date(2024, 5, 1), "Arrival", "NYC")
    ]
    intervals = build_us_intervals(entries, date(2024, 5, 10))
    assert intervals == []

def test_build_us_intervals_multiple_stays():
    entries = [
        (date(2024, 1, 1), "Arrival", "NYC"),
        (date(2024, 1, 10), "Departure", "NYC"),
        (date(2024, 2, 1), "Arrival", "NYC"),
        (date(2024, 2, 10), "Departure", "NYC"),
    ]
    intervals = build_us_intervals(entries, date(2024, 3, 1))
    assert intervals == [
        (date(2024, 1, 1), date(2024, 1, 10)),
        (date(2024, 2, 1), date(2024, 2, 10))
    ]

def test_add_window_start_interval_adjustment():
    entries = [
        (date(2024, 4, 1), "Arrival", "NYC"),
        (date(2024, 5, 10), "Departure", "NYC")
    ]
    intervals = [(date(2024, 4, 1), date(2024, 5, 10))]
    window_start = date(2024, 5, 1)
    adjusted = add_window_start_interval(entries, intervals, window_start)
    assert adjusted == [(window_start, date(2024, 5, 10))]

def test_add_window_start_interval_no_adjustment():
    intervals = [(date(2024, 5, 2), date(2024, 5, 10))]
    window_start = date(2024, 5, 1)
    adjusted = add_window_start_interval([], intervals, window_start)
    assert adjusted == intervals

def test_calculate_overlap_days():
    intervals = [
        (date(2024, 4, 1), date(2024, 5, 10)),
        (date(2024, 6, 1), date(2024, 6, 15))
    ]
    window_start = date(2024, 5, 1)
    window_end = date(2024, 6, 10)
    days = calculate_overlap_days(intervals, window_start, window_end)
    assert days == 18

def test_calculate_overlap_days_no_overlap_pytest():
    intervals = [
        (date(2024, 1, 1), date(2024, 2, 1)),
        (date(2024, 3, 1), date(2024, 4, 1))
    ]
    window_start = date(2024, 2, 2)
    window_end = date(2024, 2, 28)
    days = calculate_overlap_days(intervals, window_start, window_end)
    assert days == 0

def test_calculate_overlap_days_partial_overlap():
    intervals = [
        (date(2024, 4, 25), date(2024, 5, 5))
    ]
    window_start = date(2024, 5, 1)
    window_end = date(2024, 5, 10)
    days = calculate_overlap_days(intervals, window_start, window_end)
    assert days == 4

def test_calculate_overlap_days_exact_match():
    intervals = [
        (date(2024, 5, 1), date(2024, 5, 10))
    ]
    window_start = date(2024, 5, 1)
    window_end = date(2024, 5, 10)
    days = calculate_overlap_days(intervals, window_start, window_end)
    assert days == 9

def test_calculate_overlap_days_window_inside_interval():
    intervals = [
        (date(2024, 4, 1), date(2024, 6, 1))
    ]
    window_start = date(2024, 5, 1)
    window_end = date(2024, 5, 10)
    days = calculate_overlap_days(intervals, window_start, window_end)
    assert days == 9

def test_calculate_overlap_days_window_outside_all_intervals():
    intervals = [
        (date(2024, 5, 1), date(2024, 5, 10))
    ]
    window_start = date(2024, 6, 1)
    window_end = date(2024, 6, 10)
    days = calculate_overlap_days(intervals, window_start, window_end)
    assert days == 0

def test_calculate_overlap_days_multiple_partial_overlaps():
    intervals = [
        (date(2024, 4, 1), date(2024, 5, 5)),
        (date(2024, 5, 10), date(2024, 6, 1))
    ]
    window_start = date(2024, 5, 1)
    window_end = date(2024, 5, 15)
    days = calculate_overlap_days(intervals, window_start, window_end)
    # 2024-05-01 to 2024-05-05 (4 days), 2024-05-10 to 2024-05-15 (5 days)
    assert days == 9

# To run all tests, use the command:
# pytest tests/test_us_days.py

    def test_parse_travel_log_line_valid():
        line = "1 2024-05-01 Arrival NYC"
        result = parse_travel_log_line(line)
        assert result == (date(2024, 5, 1), "Arrival", "NYC")

    def test_parse_travel_log_line_invalid():
        line = "bad line"
        result = parse_travel_log_line(line)
        assert result is None

    def test_parse_travel_log():
        log = "Row DATE TYPE LOCATION\n1 2024-05-01 Arrival NYC\n2 2024-05-10 Departure NYC"
        entries = parse_travel_log(log)
        assert entries == [
            (date(2024, 5, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ]

    def test_build_us_intervals_simple():
        entries = [
            (date(2024, 5, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ]
        intervals = build_us_intervals(entries, date(2024, 5, 10))
        assert intervals == [(date(2024, 5, 1), date(2024, 5, 10))]

    def test_add_window_start_interval_adjusted():
        entries = [
            (date(2024, 4, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ]
        intervals = [(date(2024, 4, 1), date(2024, 5, 10))]
        window_start = date(2024, 5, 1)
        adjusted = add_window_start_interval(entries, intervals, window_start)
        assert adjusted == [(window_start, date(2024, 5, 10))]


    def test_calculate_overlap_days_no_overlap_class(self):
        intervals = [
            (date(2024, 1, 1), date(2024, 2, 1)),
            (date(2024, 3, 1), date(2024, 4, 1))
        ]
        window_start = date(2024, 2, 2)
        window_end = date(2024, 2, 28)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 0

    # Additional tests

    def test_parse_travel_log_line_partial():
        line = "1 2024-05-01 Arrival"
        result = parse_travel_log_line(line)
        assert result is None

    def test_parse_travel_log_empty():
        log = ""
        entries = parse_travel_log(log)
        assert entries == []

    def test_build_us_intervals_no_entries():
        intervals = build_us_intervals([], date(2024, 5, 10))
        assert intervals == []

    def test_build_us_intervals_open_ended():
        entries = [
            (date(2024, 5, 1), "Arrival", "NYC")
        ]
        intervals = build_us_intervals(entries, date(2024, 5, 10))
        # Should treat as still in US up to as_of_date
        assert intervals == [(date(2024, 5, 1), date(2024, 5, 10))]

    def test_add_window_start_interval_no_adjustment():
        intervals = [(date(2024, 5, 2), date(2024, 5, 10))]
        window_start = date(2024, 5, 1)
        adjusted = add_window_start_interval([], intervals, window_start)
        assert adjusted == intervals

    def test_calculate_overlap_days_partial_overlap():
        intervals = [
            (date(2024, 4, 25), date(2024, 5, 5))
        ]
        window_start = date(2024, 5, 1)
        window_end = date(2024, 5, 10)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 4  # 2024-05-01 to 2024-05-05

    def test_calculate_overlap_days_exact_match():
        intervals = [
            (date(2024, 5, 1), date(2024, 5, 10))
        ]
        window_start = date(2024, 5, 1)
        window_end = date(2024, 5, 10)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 9

    def test_calculate_overlap_days_window_inside_interval():
        intervals = [
            (date(2024, 4, 1), date(2024, 6, 1))
        ]
        window_start = date(2024, 5, 1)
        window_end = date(2024, 5, 10)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 9

    # To run all tests, use the command:
    # pytest tests/test_us_days.py
        assert intervals == [(date(2024, 5, 1), date(2024, 5, 10))]

    def test_add_window_start_interval(self):
        entries = [
            (date(2024, 4, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ]
        intervals = [(date(2024, 4, 1), date(2024, 5, 10))]
        window_start = date(2024, 5, 1)
        adjusted = add_window_start_interval(entries, intervals, window_start)
        assert adjusted == [(window_start, date(2024, 5, 10))]

    def test_calculate_overlap_days(self):
        intervals = [
            (date(2024, 4, 1), date(2024, 5, 10)),
            (date(2024, 6, 1), date(2024, 6, 15))
        ]
        window_start = date(2024, 5, 1)
        window_end = date(2024, 6, 10)
        days = calculate_overlap_days(intervals, window_start, window_end)
        # Overlap: 2024-05-01 to 2024-05-10 (9 days), 2024-06-01 to 2024-06-10 (9 days)
        assert days == 18
    
    def test_calculate_overlap_days_no_overlap(self):
        intervals = [
            (date(2024, 1, 1), date(2024, 2, 1)),
            (date(2024, 3, 1), date(2024, 4, 1))
        ]
        window_start = date(2024, 2, 2)
        window_end = date(2024, 2, 28)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 0

    def test_calculate_overlap_days_head_overlap(self):
        intervals = [
            (date(2024, 1, 1), date(2024, 2, 1)),
            (date(2024, 3, 1), date(2024, 4, 1))
        ]
        window_start = date(2024, 1, 16)
        window_end = date(2024, 2, 15)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 15
        window_start = date(2024, 1, 30)
        window_end = date(2024, 2, 27)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 3
        window_start = date(2024, 1, 31)
        window_end = date(2024, 2, 28)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 2
        window_start = date(2024, 2, 1)
        window_end = date(2024, 2, 29)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 1
        window_start = date(2024, 2, 2)
        window_end = date(2024, 3, 1)
        days = calculate_overlap_days(intervals, window_start, window_end)
        assert days == 1

    


if __name__ == "__main__":
    import pytest
    pytest.main()
