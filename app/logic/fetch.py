import json
import os
from logic.database import get_parking_coordinate_dict

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Root app directory
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "form.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.json")
EXCEL_FILE = os.path.join(DATA_DIR, "UK_Parking_Coords.xlsx")  # Excel file at root of app directory

def load_form_data(file_path):
    """Load data from form.json."""
    if not os.path.exists(file_path):
        print(f"Debug: form.json not found at {file_path}")
        return None  # File not ready yet
    with open(file_path, 'r') as json_file:
        print("Debug: form.json found. Reading data...")
        return json.load(json_file)

def save_output_data(data, file_path):
    """Save output data to output.json."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    print(f"Debug: output.json saved at {file_path}")

def process_parking_data():
    """Process form data and generate output data."""
    # Load form data
    form_data = load_form_data(INPUT_FILE)
    if not form_data:
        raise FileNotFoundError("form.json is not ready yet")
    
    print("Debug: Loaded form data:", form_data)

    # Extract data from form
    parking_pass = form_data.get("parkingPass")
    selected_day = form_data.get("selectedDay")
    time_hour = form_data.get("timeHour")
    time_minute = form_data.get("timeMinute")
    is_pm = form_data.get("isPM")

    if not all([parking_pass, selected_day, time_hour, time_minute, is_pm is not None]):
        raise ValueError("Incomplete form data.")

    # Calculate time in 24-hour format
    try:
        hour = int(time_hour)
        minute = int(time_minute)
        time = (hour + 12 if is_pm and hour != 12 else hour) % 24  # Handle AM/PM conversion
        time_in_24hr = time * 100 + minute  # Combine hour and minute as HHMM
        print(f"Debug: Calculated time as {time:02}:{minute:02} (24-hour format: {time_in_24hr})")
    except ValueError:
        raise ValueError("Invalid time data provided in form.json.")

    # Determine if it's a weekend
    weekend_bool = selected_day.lower() in ["saturday", "sunday"]
    print(f"Debug: Weekend detected: {weekend_bool}")

    # Call database logic to get available parking lots
    try:
        print(f"Debug: Attempting to access Excel file: {EXCEL_FILE}")
        available_parking_lots = get_parking_coordinate_dict(time_in_24hr, weekend_bool, parking_pass)

        if available_parking_lots:
            print("Debug: Successfully retrieved parking lot data from Excel.")
            print("Debug: Available Parking Lots:", available_parking_lots)
        else:
            print("Debug: No parking lot data found for the given parameters.")
    except FileNotFoundError:
        print(f"Error: Excel file not found at {EXCEL_FILE}. Please ensure the file exists.")
        available_parking_lots = []
    except Exception as e:
        print("Error: An unexpected error occurred while accessing the Excel file:", e)
        available_parking_lots = []

    # Create output data
    output_data = {
        "status": "success",
        "availableParkingLots": available_parking_lots
    }
    
    # Save to output.json
    save_output_data(output_data, OUTPUT_FILE)

    return output_data



