# LIBRARY IMPORT
import mysql.connector

def open_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_awos"
    )
    return conn