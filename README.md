# US Days Calculator (I-94 Travel Log GUI)

A Python GUI application for tracking and calculating the number of days spent in the US based on your I-94 travel history. Designed for travelers who need to monitor their stay for visa, tax, or compliance purposes.

---

## Features

- **Modern GUI** with two main tabs:
  - **Calculate Days**: Calculate how many days you have spent in the US in the last 12 months as of a specific date.
  - **Next Trip**: Plan your next trip by checking how many days you have spent in the US in the 12 months before your next trip's end date.
- Easy date selection with calendar pickers.
- Paste your I-94 travel history directly from the USCIS website, including the header row.
- Tip: For best results, highlight and copy your I-94 history from the bottom up (including the header) before pasting into the app.
- Clear, organized, and modular code structure.

---

## Tab Descriptions

### 1. Calculate Days
- **Purpose:** Find out how many days you have spent in the US in the last 12 months as of a chosen date.
- **How to Use:**
  1. Paste your I-94 travel history (tab-separated, with headers) from the USCIS website into the text area. Make sure to include the header row. (Tip: Highlight and copy from the bottom up for best results.)
  2. Select the 'as of' date using the date picker (defaults to today).
  3. Click **Calculate Days** to see the result.

### 2. Next Trip
- **Purpose:** Plan your next trip by checking your US days usage in the 12 months before your next trip's end date.
- **How to Use:**
  1. Paste your I-94 travel history (tab-separated, with headers) from the USCIS website into the text area. Make sure to include the header row. (Tip: Highlight and copy from the bottom up for best results.)
  2. Select your next trip's start and end dates using the date pickers.
  3. Click **Calculate Days for Next Trip** to see how many days you have spent in the US in the 12 months before your next trip's end date.

---

## How to Run

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Then install dependencies:

```
pip install -r requirements.txt
```

### 2. Start the GUI

```
python calculate_us_days_gui.py
```

### 3. Using the Application
- Prepare your travel log or I-94 history in a tab-separated format (see `sample_data.txt` for an example).
- Paste your data into the appropriate tab and use the date pickers to select dates.
- Click the calculation button to see your result in a popup.

---

## How to Run the Tests

To run unit tests (including for the Next Trip tab logic):

```
python -m unittest discover tests
```

or to run a specific test file:

```
python -m unittest tests/test_next_trip_tab.py
```

---

## Project Structure

```
i94calculator/
│   calculate_us_days_gui.py    # Main GUI entry point
│   requirements.txt            # Python dependencies
│   sample_data.txt             # Example I-94 data
│   README.md                   # This file
│
├── tabs/
│     calculate_days_tab.py     # Tab 1: Calculate Days
│     next_trip_tab.py          # Tab 2: Next Trip
│
├── i94calculator/
│     us_days.py                # Core calculation logic
│     __init__.py
│
└── tests/
      test_next_trip_tab.py     # Unit tests for Next Trip logic
      ...
```

---

## Notes
- All calculations are based on the dates and travel logs you provide. Always double-check your data for accuracy.
- The application is GUI-only; there is no command-line interface.
- For questions or suggestions, feel free to open an issue or contribute!
