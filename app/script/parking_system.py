from database import db
import serial
import time
import mysql.connector

port = 'COM4'
baud = 9600
class Parking:
    def __init__(self):
        self.db = db()       
        self.db.conn.autocommit = True           
        # ARDUINO CONNECTION
        try:
            self.arduino = serial.Serial(port,baud,timeout=1)
            time.sleep(2)
            print("ARDUINO SUCCESSFULLY CONNECTED!")
        except Exception as e:
            print(f"Error: {e}")

    def insert_data(self):
        if self.status == True:
            try:
                cursor = self.db.conn.cursor()
                get_data = "SELECT employee_name, vehicle_plate FROM employee_vehicle WHERE card_uid = %s"
                cursor.execute(get_data,(self.tag_id,))
                emp_inf = cursor.fetchone()
                if emp_inf:
                    employee_name, vehicle_plate = emp_inf


                last_action = "SELECT  last_action FROM parking_logs WHERE card_uid = %s ORDER BY id DESC LIMIT 1"""
                cursor.execute(last_action,(self.tag_id,))
                la = cursor.fetchone()

                if la and la[0] == "ENTRY":
                    new_status = "EXIT"
                else:
                    new_status = "ENTRY"

                if employee_name == 'admin':
                    print("ADMIN")
                else:

                    insert_data = """INSERT INTO parking_logs (card_uid, employee_name, vehicle_plate, last_action)
                                VALUES(%s,%s,%s,%s)
                    """
                    cursor.execute(insert_data,(self.tag_id,employee_name,vehicle_plate,new_status))
                    self.db.conn.commit()
                    print("INSERTED!")
            except mysql.connector.Error as e:
                print(f"Error {e}")
        else:
            print("NO DATA!")

    def check_id(self):
        cursor = self.db.conn.cursor()
        query = "SELECT employee_name from employee_vehicle WHERE card_uid = %s"
        cursor.execute(query,(self.tag_id,))
        Check_id = cursor.fetchone()
        cursor.close()

        
        if Check_id:
            self.status = True
            student_name = Check_id[0]
            print("Access Granted")
            self.arduino.write("Access Granted\n".encode())
            self.arduino.write(f"{student_name}\n".encode())
        else:
            self.status = False
            print("Access Denied")
            self.arduino.write("Access Denied\n".encode())
            self.arduino.write("ID UNRECOGNIZED\n".encode())

    def read_from_arduino(self):
        if self.arduino:
            line = self.arduino.readline().decode('utf-8').strip()
            if line:
                print(f"UID: {line}")
                self.tag_id = line
                self.check_id()
                self.insert_data()

        
    def run(self):
        while True:
            self.read_from_arduino()

if __name__ == "__main__":
    parking = Parking()
    parking.run()
