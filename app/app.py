from flask import Flask, render_template, request, jsonify
from logic.fetch import process_parking_data
import os
import json

app = Flask(__name__)

# Define the directory to store JSON data
DATA_DIR = os.path.join("data")
os.makedirs(DATA_DIR, exist_ok=True)  # Create the directory if it doesn't exist

@app.route("/")
def home_page():
    return render_template("mapHome.html")

@app.route("/data", methods=['POST'])
def get_form_data():
    data = request.get_json()
    if data:
        # Save the JSON file in the app/data directory
        json_file_path = os.path.join(DATA_DIR, 'form.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return jsonify({'status': 'success', 'message': 'Data saved successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'No data received'})
       
@app.route("/process-data", methods=['GET'])
def process_data():
    """Route to process form.json and generate output.json."""
    try:
        result = process_parking_data()  # Call function from fetch.py
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": str(e)})
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred", "details": str(e)})


if __name__ == '__main__':
    app.run(debug=True)

