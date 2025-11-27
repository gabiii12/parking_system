from flask import Flask, render_template, request, redirect, url_for, flash,session
import mysql.connector
import base64

app = Flask(__name__)
app.secret_key = "secret123"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="parking_system"
    )
@app.route('/')
def index():
    return render_template('log_in.html')   

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    db = get_db_connection()
    cursor = db.cursor()

    query = "SELECT * FROM accounts WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    db.close()

    if user:
        return redirect(url_for('vehicle'))  
    else:
        flash("Invalid username or password!")
        return redirect(url_for('index'))
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/logs')
def park_logs():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT card_uid, employee_name, vehicle_plate, last_action, time
        FROM parking_logs
        ORDER BY time DESC
    """)
    logs = cursor.fetchall()
    db.close()

    return render_template('logs.html', logs=logs)

@app.route('/vehicle')
def vehicle():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT card_uid, employee_name,vehicle_type, vehicle_plate 
        FROM employee_vehicle
    """)
    logs = cursor.fetchall()

    db.close()

    return render_template("vehicle.html", logs=logs)
@app.route('/acc')
def acc_info():
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    
    cursor.execute("SELECT card_uid FROM parking_logs ORDER BY time DESC LIMIT 1")
    latest_log = cursor.fetchone()
    cursor.close()
    
    processed_logs = []

    if latest_log:
        latest_uid = latest_log[0]
        cr = db.cursor(buffered=True)
        cr.execute(
            "SELECT student_id, student_name, year_level, course, profile_type, img FROM users WHERE tag_id = %s",
            (latest_uid,)
        )
        rows = cr.fetchall()
        cr.close()
        
        for row in rows:
            img_data = row[5]
            img_src = f"data:image/png;base64,{base64.b64encode(img_data).decode('utf-8')}" if img_data else None
            processed_logs.append({
                "student_id": row[0],
                "student_name": row[1],
                "year_level": row[2],
                "course": row[3],
                "profile_type": row[4],
                "img": img_src
            })
    db.close()

    return render_template('acc_info.html', Logs=processed_logs)

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        db = get_db_connection()
        cursor = db.cursor()

        uid = request.form['uid']
        name = request.form['nm']
        vec_t = request.form['vehicle_type']
        vec_p = request.form['vehicle_plate']
        if len(uid) > 8:
                flash("uid must only contains 8 characters!", "uid_error")
                cursor.close()
                db.close()
                return redirect(url_for('reg'))
                
        check_acc = """
            SELECT * FROM employee_vehicle 
            WHERE card_uid = %s OR employee_name = %s OR vehicle_plate = %s
        """
        cursor.execute(check_acc, (uid, name, vec_p))
        existing = cursor.fetchall()
        

        if existing:
            flash("UID, Name, or Plate already exists!", "error")
            
        else:
            cursor.execute("""
                INSERT INTO employee_vehicle (card_uid, employee_name, vehicle_type, vehicle_plate)
                VALUES (%s, %s, %s, %s)
            """, (uid, name, vec_t, vec_p))

            db.commit()
            cursor.close()
            db.close()
            flash("Vehicle registered successfully!", "success")
            return redirect(url_for('reg'))

    return render_template('register.html')







if __name__ == '__main__':
    app.run(debug=True)