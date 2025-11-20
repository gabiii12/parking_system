import mysql.connector
import os

class db:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                database='rfid_db',
                password=''  
            )
            self.cursor = self.conn.cursor()
            print("DATABASE SUCCESSFULLY CONNECTED")
        except mysql.connector.Error as e:
            print(f"Error {e}")

if __name__ == "__main__":
    db = db()
