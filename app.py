# LIBRARY IMPORT
from flask import Flask, jsonify, request
from connector import *
import json
# FUNCTION IMPORT
from functions import Functions

# APP CONFIGURATION
app = Flask(__name__)
app.debug = True

# @app.route('/DataAWSControl', methods=['GET', 'POST'])
# def DataAWSControl():
#     if request.method == "GET":
#         return Functions.GetDataAWS()
#     elif request.method == "POST":
#         # CHECK DATA FORM AVAILABILITY
#         if 'multipart/form-data' not in request.content_type:
#             return jsonify({"status" : "Missing form-data in request"}), 404
#         else:
#             data = request.form.to_dict()
#             return Functions.SetDataAWS(data)

# @app.route('/DataSensorWeatherControl', methods=['GET'])
# def DataSensorWeatherControl(): 
#     if request.method == "GET":
#         return Functions.GetDataSensorWeather()

# @app.route("/DataSensorAgriControl", methods=["GET", "POST"])
# def DataSensorAgriControl():
#     if request.method == "GET":
#         return Functions.GetDataSensorAgri()

@app.route("/DataTest", methods=['GET', 'POST'])
def DataTest():
    if request.method == "GET":
        return Functions.GetDataTest()
    elif request.method == "POST":
        # CHECK DATA FORM AVAILABILITY
        if 'multipart/form-data' not in request.content_type:
            return jsonify({"status" : "Missing form-data in request"}), 404
        else:
            data = request.form.to_dict()
            return Functions.SetDataTest(data)
        
if __name__ == '__main__':
    app.run()