import mysql.connector


try:

    conn = mysql.connector.connect(
        host='localhost',
        user = 'root',
        password='',
        database='oopr'
    )
    cursor = conn.cursor()
    print("DATABASE CONNECTED")
except mysql.connector.error as e:
    print(f"Error: {e}")

while True:
    name = input("Email: ")
    password = input("Password: ")

    query = "SELECT User_Password FROM accounts WHERE (Email = %s OR Username = %s)"
    cursor.execute(query, (name,name,))
    valid = cursor.fetchone()

    if valid:
        Stored_password = valid[0]
        if password == Stored_password:
            print("LOG IN")
        else:
            print("Incorrect Password!")
    else:
        print("Username or Email is not registered!")