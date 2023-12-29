# LIBRARY IMPORT
from flask import Flask, jsonify, request
from connector import *

# FUNCTION IMPORT
from functions import Functions

# APP CONFIGURATION
app = Flask(__name__)
app.debug = True

@app.route("/DataSensor", methods=['GET', 'POST'])
def DataSensor():
    if request.method == "GET":
        return Functions.GetDataSensor()
    elif request.method == "POST":
        # CHECK DATA FORM AVAILABILITY
        if 'multipart/form-data' not in request.content_type:
            return jsonify({"status" : "Missing form-data in request"}), 404
        else:
            data = request.form.to_dict()
            return Functions.SetDataSensor(data)

if __name__ == '__main__':
    app.run()