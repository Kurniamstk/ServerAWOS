# LIBRARY IMPORT
from flask import jsonify
from connector import *
import uuid
import datetime

# # DATA FORMATTER
# def DataAWSFormat(data):
#     data_format = {
#         "ID_AWS"        : data[0],
#         "Nama_AWS"      : data[1],
#         "Latitude_AWS"  : data[2],
#         "Longitude_AWS" : data[3]
#     }
#     return data_format

# def DataSensorWeatherFormat(data):
#     data_format = {
#         "ID_AWOS_Weather"   : data[0],
#         "Temp_Weather"      : data[1],
#         "Humidity_Weather"  : data[2],
#         "LightInten_Weather": data[3],
#         "AirPress_Weather"  : data[4],
#         "WindWave_Weather"  : data[5],
#         "Rainfall_Weather"  : data[6],
#         "Thunder_Weather"   : data[7],
#         "UpdatedAt"         : data[8],
#         "CreatedAt"         : data[9]
#     }
#     return data_format

# def DataSensorAgriFormat(data):
#     data_format = {
#         "ID_AWOS_Agri"      : data[0],
#         "SoilMoisture_Agri" : data[1],
#         "SoilTemp_Agri"     : data[2],
#         "Nitrogen_Agri"     : data[3],
#         "Phospor_Agri"      : data[4],
#         "Calium_Agri"       : data[5],
#         "PHSoil_Agri"       : data[6],
#         "UpdatedAt"         : data[7],
#         "CreatedAt"         : data[8]
#     }
#     return data_format

def DataTestFormat(data):
    data_format = {
        "ID_Test" : data[0],
        "Data_Test": data[1],
        "CreatedAt" : data[2]
    }
    return data_format

# # GET DATA 
# def GetDataAWS():
#     try:
#         conn = open_connection()
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT * FROM data_aws")
#             datas = cursor.fetchall()
#             if datas:
#                 formatted_data = []
#                 for data in datas:
#                     data_result = DataAWSFormat(data)
#                     formatted_data.append(data_result)
#                 return jsonify(formatted_data), 200
#             else:
#                 return jsonify({"msg" : "No data found!"}), 200
#     except Exception as e:
#         return jsonify({"Error: " : str(e)}), 400
    

# def GetDataSensorWeather():
#     try:
#         conn = open_connection()
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT * FROM data_AWOSSky")
#             datas = cursor.fetchall()
#             if datas:
#                 formatted_data = []
#                 for data in datas:
#                     data_result = DataSensorWeatherFormat(data)
#                     formatted_data.append(data_result)
#                 return jsonify(formatted_data), 200
#             else:
#                 return jsonify({"msg" : "No data found!"}), 200
#     except Exception as e:
#         return jsonify({"Error: " : str(e)}), 400

# def GetDataSensorAgri():
#     try:
#         conn = open_connection()
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT * FROM data_AWOSAgriculture")
#             datas = cursor.fetchall()
#             if datas:
#                 formatted_data = []
#                 for data in datas:
#                     data_result = DataSensorAgriFormat(data)
#                     formatted_data.append(data_result)
#                 return jsonify(formatted_data), 200
#             else:
#                 return jsonify({"msg" : "No data found!"}), 200
#     except Exception as e:
#         return jsonify({"Error: " : str(e)}), 400
    

# # SET DATA
# def SetDataAWS(data):
#     try:
#         conn = open_connection()
#         with conn.cursor() as cursor:
#             # GET DATA REQUEST
#             ID_AWS          = str(uuid.uuid4())
#             Nama_AWS        = data['Nama_AWS']
#             Latitude_AWS    = data['Latitude_AWS']
#             Longitude_AWS   = data['Longitude_AWS']

#             # INSERTING DATA 
#             cursor.execute("INSERT INTO data_aws (ID_AWS, Nama_AWS, Latitude, Longitude) VALUES (%s, %s, %s, %s)", (ID_AWS, Nama_AWS, Latitude_AWS, Longitude_AWS))

#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"msg" : "Sukses menambahkan data!"}), 200
#     except Exception as e:
#         return jsonify({"Error: " : str(e)}), 400
    
# UPDATE DATA AWS SENSOR WITH MQTT
def SetDataTest(message):
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            ID_Test = str(uuid.uuid4())
            Data_Test = str(message)
            # INSERTING DATA
            cursor.execute("INSERT INTO data_test (ID_Test, Data_Test) VALUES (%s, %s)", (ID_Test, Data_Test))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"msg" : "Sukses menambahkan data!"}), 200
    except Exception as e:
        return jsonify({"Error :" : str(e)}), 400


def GetDataTest():
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM data_test")
            datas = cursor.fetchall()
            if datas:
                formatted_data = []
                for data in datas:
                    data_result = DataTestFormat(data)
                    formatted_data.append(data_result)
                return jsonify(formatted_data), 200
            else:
                return jsonify({"msg" : "No data found!"}), 200
    except Exception as e:
        return jsonify({"Error: " : str(e)}), 400
    