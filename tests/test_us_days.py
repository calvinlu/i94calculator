import unittest
from datetime import date
from i94calculator.us_days import (
    parse_travel_log_line,
    parse_travel_log,
    build_us_intervals,
    add_window_start_interval,
    calculate_overlap_days
)

class TestUSDaysCalculator(unittest.TestCase):
    def test_parse_travel_log_line_valid(self):
        line = "1 2024-05-01 Arrival NYC"
        result = parse_travel_log_line(line)
        self.assertEqual(result, (date(2024, 5, 1), "Arrival", "NYC"))

    def test_parse_travel_log_line_invalid(self):
        line = "bad line"
        result = parse_travel_log_line(line)
        self.assertIsNone(result)

    def test_parse_travel_log(self):
        log = "Row DATE TYPE LOCATION\n1 2024-05-01 Arrival NYC\n2 2024-05-10 Departure NYC"
        entries = parse_travel_log(log)
        self.assertEqual(entries, [
            (date(2024, 5, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ])

    def test_build_us_intervals_simple(self):
        entries = [
            (date(2024, 5, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ]
        intervals = build_us_intervals(entries, date(2024, 5, 10))
        self.assertEqual(intervals, [(date(2024, 5, 1), date(2024, 5, 10))])

    def test_add_window_start_interval(self):
        entries = [
            (date(2024, 4, 1), "Arrival", "NYC"),
            (date(2024, 5, 10), "Departure", "NYC")
        ]
        intervals = [(date(2024, 4, 1), date(2024, 5, 10))]
        window_start = date(2024, 5, 1)
        adjusted = add_window_start_interval(entries, intervals, window_start)
        self.assertEqual(adjusted, [(window_start, date(2024, 5, 10))])

    def test_calculate_overlap_days(self):
        intervals = [
            (date(2024, 4, 1), date(2024, 5, 10)),
            (date(2024, 6, 1), date(2024, 6, 15))
        ]
        window_start = date(2024, 5, 1)
        window_end = date(2024, 6, 10)
        days = calculate_overlap_days(intervals, window_start, window_end)
        # Overlap: 2024-05-01 to 2024-05-10 (9 days), 2024-06-01 to 2024-06-10 (9 days)
        self.assertEqual(days, 18)

if __name__ == "__main__":
    unittest.main()
