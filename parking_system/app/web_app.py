from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="parking_system"
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT card_uid, employee_name, vehicle_plate, last_action, time
        FROM parking_logs
        ORDER BY time DESC
    """)
    logs = cursor.fetchall()
    db.close()
    return render_template('index.html', logs=logs)

@app.route('/vehicle')
def vehicle():
    db= get_db_connection
    cursor = db.cursor()

    employee = "SELECT card_uid, employee_name, vehicle_plate FROM employee_vehicle"
    cursor.execute(employee)
    logs = cursor.fetchall()
    db.close()
    return render_template("vehicle.html", logs=logs)



if __name__ == '__main__':
    app.run(debug=True)
