from flask import Flask, jsonify
import mysql.connector


def get_murid_data():
    data = None
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="trachel", database="menda_02"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")

        data = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        if connection:
            connection.close()

    return jsonify(data)
