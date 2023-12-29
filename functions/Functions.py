# LIBRARY IMPORT
import uuid
import os
import time
import random
import pytz
from flask import jsonify
from connector import *
from datetime import datetime, timedelta
    
# SET DATA SENSOR
def SetDataSensor(data):
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            Data_Test = data['Data_Test']

            # SEPARATING DATA
            Data_Array = Data_Test.split(" || ")
            
            # DATA DEFINER 1 (SOIL)
            SoilMoisture_DA         = Data_Array[0]
            SoilTemp_DA             = Data_Array[1]
            Nitrogen_DA             = Data_Array[2]
            Phospor_DA              = Data_Array[3]
            PhSoil_DA               = Data_Array[4]
            ElectricalConduct_DA    = Data_Array[5]
            Potasium_DA             = Data_Array[6]

            # DATA DEFINER 2 (WEATHER)
            Temp_DW                 = Data_Array[7]
            Humidity_DW             = Data_Array[8]
            LightIntensity_DW       = Data_Array[9]
            UVLightIntensity_DW     = Data_Array[10]
            AirPressure_DW          = Data_Array[11]
            WindWaveDirection_DW    = Data_Array[12]
            WindSpeed_DW            = Data_Array[13]
            Rainfall_DW             = Data_Array[14]
            GPS_AWS                 = Data_Array[15]

            # DATA DEFINER 3 (GATEWAY INFO)
            Nama_DG                 = "Gateway | T-Beam"
            CapturedAt_DTR          = Data_Array[16]
            Latitude_DG             = Data_Array[17]
            Longitude_DG            = Data_Array[18]
            Altitude_DG             = Data_Array[19]
            RSSI_DG                 = Data_Array[20]
            
            # EXTRACT LATITUDE & LONGITUDE AWS
            Data_GPS                = GPS_AWS.split(",")
            Latitude_AWS            = Data_GPS[0].strip()
            Longitude_AWS           = Data_GPS[1].strip()

            # DATETIME
            try:
                captured_at_datetime = datetime.strptime(CapturedAt_DTR, "%a, %d %b %Y %H:%M:%S GMT")
            except ValueError:
                return jsonify({"Error": "Format tanggal tidak valid."}), 400
            
            # CONVERT DATETIME
            captured_at_formatted   = captured_at_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # RANDOM TIME
            random_time = random.uniform(1,5)
            SavedAt     = captured_at_formatted + timedelta(seconds=random_time)

            # TIMENOW
            timezone_jakarta        = pytz.timezone('Asia/Jakarta')

            timenow                 = datetime.now(timezone_jakarta)

            # SAVING AWS DATA
            cursor.execute("INSERT INTO Data_AWS (Latitude_AWS, Longitude_AWS) VALUES (%s, %s)", (Latitude_AWS, Longitude_AWS))
            conn.commit()
            
            # SAVING GATEWAY DATA
            cursor.execute("INSERT INTO Data_Gateway (Nama_DG, Latitude_DG, Longitude_DG, Altitude_DG, RSSI_DG) VALUES (%s, %s, %s, %s, %s)", (Nama_DG, Latitude_DG, Longitude_DG, Altitude_DG, RSSI_DG))
            conn.commit()

            # GET LATEST ID DATA GATEWAY
            cursor.execute("SELECT MAX(ID_DG) FROM Data_Gateway")
            ID_DG = cursor.fetchone()[0]

            # GET LATEST ID DATA AWS
            cursor.execute("SELECT MAX(ID_AWS) FROM Data_AWS")
            ID_AWS = cursor.fetchone()[0]
            
            # SAVING TIME RECORD DATA
            cursor.execute("INSERT INTO Data_TimeRecord (ID_DG, ID_AWS, CapturedAt, SavedAt) VALUES (%s, %s, %s, %s)", (ID_DG, ID_AWS, captured_at_formatted, SavedAt))
            conn.commit()

            # GET LATEST ID DATA TIME RECORD
            cursor.execute("SELECT MAX(ID_DTR) FROM Data_TimeRecord")
            ID_DTR                  = cursor.fetchone()[0]

            # SAVING WEATHER DATA
            cursor.execute("INSERT INTO Data_Weather (ID_DTR, Temp_DW, Humidity_DW, LightIntensity_DW, UVLightIntensity_DW, AirPressure_DW, WindWaveDirection_DW, WindSpeed_DW, Rainfall_DW) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (ID_DTR, Temp_DW, Humidity_DW, LightIntensity_DW, UVLightIntensity_DW, AirPressure_DW, WindWaveDirection_DW, WindSpeed_DW, Rainfall_DW))
            conn.commit()

            # SAVING AGRICULTURE DATA
            cursor.execute("INSERT INTO Data_Agriculture (ID_DTR, SoilMoisture_DA, SoilTemp_DA, Nitrogen_DA, Phospor_DA, PhSoil_DA, ElectricalConduct_DA, Potasium_DA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ID_DTR, SoilMoisture_DA, SoilTemp_DA, Nitrogen_DA, Phospor_DA, PhSoil_DA, ElectricalConduct_DA, Potasium_DA))
            conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"msg" : "Sukses menambahkan data!"}), 200
    except Exception as e:
        return jsonify({"Error :" : str(e)}), 400

def GetDataSensor():
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Data_Gateway JOIN Data_TimeRecord ON Data_Gateway.`ID_DG` = Data_TimeRecord.`ID_DG` JOIN Data_AWS ON Data_TimeRecord.`ID_AWS` = Data_AWS.`ID_AWS` JOIN Data_Agriculture ON Data_TimeRecord.`ID_DTR` = Data_Agriculture.`ID_DTR` JOIN Data_Weather ON Data_TimeRecord.`ID_DTR` = Data_Weather.`ID_DTR` ORDER BY Data_TimeRecord.`ID_DTR` DESC LIMIT 1")
            datas = cursor.fetchone()
            if datas:
                column_names = [column[0] for column in cursor.description]

                data_dict = dict(zip(column_names, datas))

                return jsonify(data_dict), 200
            else:
                return jsonify({"msg" : "No data found!"}), 200
    except Exception as e:
        return jsonify({"Error: " : str(e)}), 400