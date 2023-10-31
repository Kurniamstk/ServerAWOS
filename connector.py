# LIBRARY IMPORT
import mysql.connector

def open_connection():
    conn = mysql.connector.connect(
        host="serverawos.mysql.pythonanywhere-services.com",
        user="serverawos",
        password="rzdempattitiktiga",
        database="serverawos$db_awos"
    )
    return conn