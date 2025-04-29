import unittest
from datetime import datetime, timedelta
from i94calculator.us_days import parse_travel_log, build_us_intervals, add_window_start_interval, calculate_overlap_days

SAMPLE_DATA = '''Row\tDATE\tTYPE\tLOCATION
1\t2025-04-21\tDeparture\tDMA
2\t2025-04-05\tArrival\tSFR
3\t2025-03-22\tDeparture\tSFR
4\t2025-03-14\tArrival\tVCV
5\t2025-02-17\tDeparture\tSFR
6\t2025-01-25\tArrival\tVCV
7\t2025-01-02\tDeparture\tCHI
8\t2024-12-07\tArrival\tTOR
9\t2024-12-04\tDeparture\tATL
10\t2024-11-02\tArrival\tLOS
11\t2024-10-16\tDeparture\tHHW
12\t2024-10-13\tArrival\tVCV
13\t2024-10-05\tDeparture\tSAC
14\t2024-09-27\tArrival\tTOR
15\t2024-09-14\tDeparture\tATL
16\t2024-07-28\tArrival\tTOR
17\t2024-07-07\tDeparture\tLOS
18\t2024-06-29\tArrival\tTOR
19\t2024-05-12\tDeparture\tDMA
20\t2024-05-05\tArrival\tATL
21\t2024-04-17\tDeparture\tATL
22\t2024-03-28\tArrival\tTOR
23\t2024-02-28\tDeparture\tPHI
24\t2024-02-02\tArrival\tTOR
25\t2024-01-03\tDeparture\tCHI
26\t2023-12-11\tArrival\tDCB'''

class TestNextTripTabLogic(unittest.TestCase):
    def test_days_in_us_last_12_months(self):
        # Test the core calculation for Next Trip tab
        entries = parse_travel_log(SAMPLE_DATA)
        as_of_date = datetime.strptime('2025-06-01', '%Y-%m-%d').date()
        window_start = as_of_date - timedelta(days=365)
        intervals = build_us_intervals(entries, as_of_date)
        intervals = add_window_start_interval(entries, intervals, window_start)
        days = calculate_overlap_days(intervals, window_start, as_of_date)
        self.assertEqual(days, 172)

    def test_empty_log(self):
        entries = parse_travel_log('Row\tDATE\tTYPE\tLOCATION')
        as_of_date = datetime.strptime('2025-06-01', '%Y-%m-%d').date()
        window_start = as_of_date - timedelta(days=365)
        intervals = build_us_intervals(entries, as_of_date)
        intervals = add_window_start_interval(entries, intervals, window_start)
        days = calculate_overlap_days(intervals, window_start, as_of_date)
        self.assertEqual(days, 0)

    def test_invalid_dates(self):
        # Should handle bad dates gracefully (parse_travel_log should skip bad rows)
        bad_data = SAMPLE_DATA + '\n27\tBADDATE\tArrival\tNYC'
        entries = parse_travel_log(bad_data)
        as_of_date = datetime.strptime('2025-06-01', '%Y-%m-%d').date()
        window_start = as_of_date - timedelta(days=365)
        intervals = build_us_intervals(entries, as_of_date)
        intervals = add_window_start_interval(entries, intervals, window_start)
        days = calculate_overlap_days(intervals, window_start, as_of_date)
        self.assertEqual(days, 172)

if __name__ == '__main__':
    unittest.main()
