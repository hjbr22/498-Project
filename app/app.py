from flask import Flask, render_template, request, send_file, redirect, jsonify
import json

app = Flask(__name__, static_folder='static')

@app.route("/")
def homePage():
    return render_template("mapHome.html")

@app.route("/data", methods=['POST'])
def get_form_data():
    data = request.get_json()
    print(data)
    if data:
        with open('form.json', 'w') as json_file:
            json.dump(data, json_file, indent=1)
        return jsonify({'status': "success", 'message': 'Data saved successfully'})
    else:
        return jsonify({'status': "error", 'message': 'No data received'})
    
if __name__ == '__main__':
    app.run(debug=True)