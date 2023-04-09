import mysql.connector


def db_connect():
    conn = mysql.connector.connect(
                                    user="root",
                                    password="1234",
                                    host="localhost",
                                    port=3306,
                                    database="user",
                                    )
    db = {'conn': conn, 'cur': conn.cursor(dictionary=True)}
    return db