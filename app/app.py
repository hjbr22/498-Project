from flask import Flask, render_template, request, send_file, redirect, jsonify



app = Flask(__name__, static_folder='static')

@app.route("/")
def homePage():
    return render_template("base.html")

@app.route("/get_employees", methods=['POST'])
def get_employees():
    return

@app.route("/get_students", methods=['POST'])
def add_employee():
    return