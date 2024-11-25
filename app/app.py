from flask import Flask, render_template, request, jsonify
from logic.fetch import process_parking_data
import os
import json

app = Flask(__name__)

# Define the directory to store JSON data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/")
def home_page():
    return render_template("mapHome.html")

@app.route("/parking-data", methods=['POST', 'GET'])
def parking_data():
    """Handle POST to save form.json and GET to process data."""
    if request.method == 'POST':
        data = request.get_json()
        if data:
            # Save the JSON file in the data directory
            json_file_path = os.path.join(DATA_DIR, 'form.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=2)
            return jsonify({'status': 'success', 'message': 'Data saved successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400

    if request.method == 'GET':
        try:
            # Process data using fetch.py function
            result = process_parking_data()
            return jsonify(result)
        except FileNotFoundError as e:
            # Handle case where form.json is not ready yet
            return jsonify({"status": "error", "message": str(e)}), 404
        except ValueError as e:
            # Handle incomplete form data
            return jsonify({"status": "error", "message": str(e)}), 400
        except Exception as e:
            # Handle other exceptions
            return jsonify({"status": "error", "message": "An unexpected error occurred", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

