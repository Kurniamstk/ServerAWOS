# LIBRARY IMPORT
import uuid
import openpyxl
import os
from flask import jsonify
from connector import *
from datetime import datetime
from pathlib import Path


# DATA FORMATTER
def DataSensorFormat(data):
    data_format = {
        "ID_Test" : data[0],
        "Data_Test": data[1],
        "CreatedAt" : data[2]
    }
    return data_format
    
# UPDATE DATA AWS SENSOR WITH MQTT
def SetDataSensorExcel():
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            current_directory   = Path.cwd()

            file_path           = current_directory / 'functions/data.xlsx'

            # READ DATA FROM EXCEL
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            sheet = workbook.active
            # DATA DEFINER 1 (GATEWAY INFO)
            Nama_DG                 = "Gateway | T-Beam"
            Latitude_DG             = '-6.9816305'
            Longitude_DG            = '107.6223513'

            # SAVE DATA TO TABLE DATA GATEWAY
            cursor.execute("INSERT INTO Data_Gateway (Nama_DG, Latitude_DG, Longitude_DG) VALUES (%s, %s, %s)", (Nama_DG, Latitude_DG, Longitude_DG))
            conn.commit()

            for row in sheet.iter_rows(min_row=2, values_only=True):
                Column1, Column2, time_date, temperature, humidity, air_pressure, light_intensity, rainfall, uv, wind_speed, wind_direction = row

                # GET LATEST ID
                cursor.execute("SELECT MAX(ID_DG) FROM Data_Gateway")

                # DATA DEFINER 2 (TIMESTAMP INFO)
                ID_DG = cursor.fetchone()[0]
                CapturedAt              = time_date
                ReceivedAt              = time_date
                SavedAt                 = datetime.now()

                cursor.execute("INSERT INTO Data_TimeRecord (ID_DG, CapturedAt, ReceivedAt, SavedAt) VALUES (%s, %s, %s, %s)", (ID_DG, CapturedAt, ReceivedAt, SavedAt))
                conn.commit()

                # GET LATEST ID
                cursor.execute("SELECT MAX(ID_DTR) FROM Data_TimeRecord")
                ID_DTR                  = cursor.fetchone()[0]

                # DATA DEFINER 3 (WEATHER DATA INFO)
                Temp_DW                 = temperature
                Humidity_DW             = humidity
                LightIntensity_DW       = light_intensity
                UVLightIntensity_DW     = uv
                AirPressure_DW          = air_pressure
                WindWaveDirection_DW    = wind_direction
                WindSpeed_DW            = wind_speed
                Rainfall_DW             = rainfall

                # SAVE DATA TO TABLE DATA WEATHER
                cursor.execute("INSERT INTO Data_Weather (ID_DTR, Temp_DW, Humidity_DW, LightIntensity_DW, UVLightIntensity_DW, AirPressure_DW, WindWaveDirection_DW, WindSpeed_DW, Rainfall_DW) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (ID_DTR, Temp_DW, Humidity_DW, LightIntensity_DW, UVLightIntensity_DW, AirPressure_DW, WindWaveDirection_DW, WindSpeed_DW, Rainfall_DW))
                conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"msg" : "Sukses menambahkan data!"}), 200
    except Exception as e:
        return jsonify({"Error :" : str(e)}), 400
    
# UPDATE DATA AWS SENSOR WITH MQTT
def SetDataSensor(data):
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            Data_Test = data['Data_Test']

            # SEPARATING DATA
            Data_Array = Data_Test.split(" || ")
            
            # DATA DEFINER 1 (GATEWAY INFO)
            Nama_DG                 = "Gateway | T-Beam"
            Latitude_DG             = Data_Array[15]
            Longitude_DG            = Data_Array[16]

            # SAVE DATA TO TABLE DATA GATEWAY
            cursor.execute("INSERT INTO Data_Gateway (Nama_DG, Latitude_DG, Longitude_DG) VALUES (%s, %s, %s)", (Nama_DG, Latitude_DG, Longitude_DG))
            conn.commit()

            # GET LATEST ID
            cursor.execute("SELECT MAX(ID_DG) FROM Data_Gateway")

            # DATA DEFINER 2 (TIMESTAMP INFO)
            ID_DG = cursor.fetchone()[0]
            CapturedAt              = datetime.now()
            ReceivedAt              = datetime.now()
            SavedAt                 = datetime.now()

            cursor.execute("INSERT INTO Data_TimeRecord (ID_DG, CapturedAt, ReceivedAt, SavedAt) VALUES (%s, %s, %s, %s)", (ID_DG, CapturedAt, ReceivedAt, SavedAt))
            conn.commit()

            # GET LATEST ID
            cursor.execute("SELECT MAX(ID_DTR) FROM Data_TimeRecord")
            ID_DTR                  = cursor.fetchone()[0]

            # DATA DEFINER 3 (WEATHER DATA INFO)
            Temp_DW                 = Data_Array[1]
            Humidity_DW             = Data_Array[2]
            LightIntensity_DW       = Data_Array[3]
            UVLightIntensity_DW     = 0
            AirPressure_DW          = Data_Array[7]
            WindWaveDirection_DW    = Data_Array[0]
            WindSpeed_DW            = Data_Array[11]
            Rainfall_DW             = Data_Array[6]

            # SAVE DATA TO TABLE DATA WEATHER
            cursor.execute("INSERT INTO Data_Weather (ID_DTR, Temp_DW, Humidity_DW, LightIntensity_DW, UVLightIntensity_DW, AirPressure_DW, WindWaveDirection_DW, WindSpeed_DW, Rainfall_DW) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (ID_DTR, Temp_DW, Humidity_DW, LightIntensity_DW, UVLightIntensity_DW, AirPressure_DW, WindWaveDirection_DW, WindSpeed_DW, Rainfall_DW))
            conn.commit()

            # DATA DEFINER 4 (AGRICULTURE DATA INFO)
            SoilMoisture_DA         = 0
            SoilTemp_DA             = 0
            Nitrogen_DA             = Data_Array[5]
            Phospor_DA              = Data_Array[8]
            Calium_DA               = Data_Array[9]
            PhSoil_DA               = Data_Array[4]

            # SAVE DATA TO TABLE DATA AGRICULTURE
            cursor.execute("INSERT INTO Data_Agriculture (ID_DTR, SoilMoisture_DA, SoilTemp_DA, Nitrogen_DA, Phospor_DA, Calium_DA, PhSoil_DA) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ID_DTR, SoilMoisture_DA, SoilTemp_DA, Nitrogen_DA, Phospor_DA, Calium_DA, PhSoil_DA))
            conn.commit()

            # DATA DEFINER 5 (LORA INFO)
            RSSI_DL                 = Data_Array[13]
            Altitude_DL             = Data_Array[12]
            SNR_DL                  = Data_Array[14]
            cursor.execute("INSERT INTO Data_LORA (ID_DG, RSSI_DL, Altitude_DL, SNR_DL) VALUES (%s, %s, %s, %s)", (ID_DG, RSSI_DL, Altitude_DL, SNR_DL))
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
            cursor.execute("SELECT * FROM Data_Test")
            datas = cursor.fetchall()
            if datas:
                formatted_data = []
                for data in datas:
                    data_result = DataSensorFormat(data)
                    formatted_data.append(data_result)
                return jsonify(formatted_data), 200
            else:
                return jsonify({"msg" : "No data found!"}), 200
    except Exception as e:
        return jsonify({"Error: " : str(e)}), 400