import json
import os
import time
from logic.database import get_parking_lots_main

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Root app directory
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "form.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.json")
EXCEL_FILE = os.path.join(BASE_DIR, "UK Parking.xlsx")  # Excel file at root of app directory

def load_form_data(file_path):
    """Load data from form.json."""
    if not os.path.exists(file_path):
        return None  # File not ready yet
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def save_output_data(data, file_path):
    """Save output data to output.json."""
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def process_parking_data():
    """Process form data and generate output data."""
    # Load form data
    form_data = load_form_data(INPUT_FILE)
    if not form_data:
        print("Waiting for form.json...")
        return False  # form.json is not ready yet

    # Extract data from form
    parking_pass = form_data.get("parkingPass")
    selected_day = form_data.get("selectedDay")
    time_hour = form_data.get("timeHour")
    time_minute = form_data.get("timeMinute")
    is_pm = form_data.get("isPM")

    if not all([parking_pass, selected_day, time_hour, time_minute, is_pm]):
        raise ValueError("Incomplete form data.")

     # Calculate time in 24-hour format
    hour = int(form_data.get("timeHour", 0))
    minute = int(form_data.get("timeMinute", 0))
    time = hour + 12 if is_pm and hour != 12 else hour  # Handle AM/PM conversion

    # Determine if it's a weekend
    weekend_bool = selected_day in ["saturday", "sunday"]

    # Call database logic to get available parking lots
    available_parking_lots = get_parking_lots_main(EXCEL_FILE, time * 100 + minute, weekend_bool, parking_pass)

   

    # Save the result to output.json
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump({"availableParkingLots": available_parking_lots}, f, indent=2)

    return {"status": "success", "availableParkingLots": available_parking_lots}


