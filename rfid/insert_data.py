import mysql.connector
import serial
import os
import time
from database import db

password = os.getenv('MYSQL_PASS')

class attendance:
    def __init__(self):
        self.db = db()
        self.cursor = self.db.cursor

    def insert_data(self,tag_id,student_id,student_name):
        try:
            qr = "SELECT status_log FROM ATTENDANCE WHERE tag_id = %s ORDER BY log_time DESC LIMIT 1"
            self.cursor.execute(qr,(tag_id,))
            last = self.cursor.fetchone()
            if last and last[0] == 'IN':
                new_status = 'OUT'
            else:
                new_status = 'IN'

            query = """INSERT INTO attendance (tag_id, student_id, student_name,status_log)
                        VALUES(%s,%s,%s,%s)
            """
            self.cursor.execute(query,(tag_id,student_id,student_name,new_status))
            self.db.conn.commit()
            print("SUCCESSFULY STORED")
        except mysql.connector.Error as e:
            print(F"Error: {e}")

    def main(self):
        self.insert_data()

if __name__ == "__main__":
    att=attendance()
    att.main()
