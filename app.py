# LIBRARY IMPORT
from flask import Flask, jsonify, request
from flask_cors import CORS
from connector import *

# FUNCTION IMPORT
from functions import Functions

# APP CONFIGURATION
app = Flask(__name__)
CORS(app, origins='*')
app.debug = True

@app.route("/DataSensor", methods=['GET', 'POST'])
def DataSensor():
    if request.method == "GET":
        return Functions.GetDataSensor()
    elif request.method == "POST":
        # CHECK CONTENT TYPE
        if 'application/json' not in request.content_type:
            return jsonify({"status": "Unsupported Media Type. Use 'application/json'"}), 415
        else:
            data = request.get_json()
            if not data:
                return jsonify({"status": "Invalid JSON format in request"}), 400
            return Functions.SetDataSensor(data)

@app.route("/DataSensorFull", methods=['GET'])
def DataSensorFull():
    if request.method == "GET":
        return Functions.GetAllDataSensor()

if __name__ == '__main__':
    app.run()